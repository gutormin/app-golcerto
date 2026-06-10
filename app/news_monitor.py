"""Monitor de notícias e variações de odds para o GolCerto 2026.

Verifica periodicamente:
- Notícias importantes de seleções (lesões, escalações, suspensões)
- Variações de odds que mudem o palpite da IA
Armazena alertas em memória e expõe via endpoint /alerts
"""
import asyncio
import httpx
import time
import re
import html
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any
from app import prediction_engine

# ─── ESTADO GLOBAL ────────────────────────────────────────────────────────────
_alerts: list[dict] = []          # alertas gerados
_last_predictions: dict = {}      # palpites anteriores por jogo
_last_odds: dict = {}             # odds anteriores por jogo
_running = False
_last_recap_time = 0.0

# ─── ODDS ATUAIS (simuladas com variação realista) ────────────────────────────
BASE_ODDS = {
    "Brazil x Mexico":       {"home": 1.72, "draw": 3.80, "away": 5.20},
    "Argentina x Germany":   {"home": 2.10, "draw": 3.30, "away": 3.20},
    "France x Spain":        {"home": 2.20, "draw": 3.40, "away": 3.10},
    "England x Portugal":    {"home": 2.40, "draw": 3.25, "away": 2.80},
    "Netherlands x Belgium": {"home": 2.15, "draw": 3.35, "away": 3.30},
    "Japan x Morocco":       {"home": 2.60, "draw": 3.20, "away": 2.70},
    "USA x Mexico":          {"home": 2.30, "draw": 3.30, "away": 2.95},
    "Uruguay x Colombia":    {"home": 2.25, "draw": 3.20, "away": 3.10},
}

# Notícias relevantes de seleções (em produção: buscar de RSS/news API)
NEWS_SOURCES = [
    {
        "url": "https://newsdata.io/api/1/news?apikey=&q=copa+2026+lesao+escalacao&language=pt&category=sports",
        "active": False  # desativado até ter API key
    }
]

# Palavras-chave que indicam notícia importante
KEYWORDS_HIGH = ["lesão", "lesao", "lesionado", "suspenso", "suspensão", "fora da copa",
                  "convocado", "Neymar", "Mbappé", "Messi", "Haaland", "Vinicius"]
KEYWORDS_MEDIUM = ["treinamento", "escalação", "titular", "reserva", "recuperação", "volta"]

import os

# ─── TELEGRAM BOT BOT INTEGRATION ─────────────────────────────────────────────
async def send_telegram_alert_async(title: str, body: str, match: str, priority: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    
    # Format message with markdown (Telegram support)
    # Emojis based on priority
    emoji = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
    msg = (
        f"🏆 *GolCerto 2026 — Alerta VIP* 🏆\n\n"
        f"{emoji} *{title}*\n"
        f"{body}\n\n"
    )
    if match:
        msg += f"⚽ *Jogo/Seleção:* {match}\n"
    msg += f"⚡ *Prioridade:* {priority.upper()}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json={
                "chat_id": chat_id,
                "text": msg,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            })
            if resp.status_code != 200:
                print(f"[Telegram] Failed to send message: {resp.text}")
    except Exception as e:
        print(f"[Telegram] Error sending message: {e}")

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _add_alert(alert_type: str, title: str, body: str, match: str = "", priority: str = "medium"):
    """Adiciona um alerta na fila (máx 50)."""
    global _alerts
    alert = {
        "id": int(time.time() * 1000),
        "type": alert_type,       # "news" | "odds_change" | "prediction_change"
        "title": title,
        "body": body,
        "match": match,
        "priority": priority,     # "high" | "medium" | "low"
        "timestamp": _now_iso(),
        "read": False,
    }
    _alerts.insert(0, alert)
    try:
        print(f"[ALERTA] {priority.upper()} | {title}")
    except UnicodeEncodeError:
        print(f"[ALERTA] {priority.upper()} | {title.encode('ascii', errors='replace').decode('ascii')}")
        
    # Trigger Telegram broadcast asynchronously
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            loop.create_task(send_telegram_alert_async(title, body, match, priority))
    except RuntimeError:
        # No running loop (e.g. during script usage), run synchronously
        pass

def _simulate_odds_variation(match_key: str, odds: dict) -> dict:
    """Simula variação realista de odds (±5%) para demonstração.
    Em produção: buscar odds reais de API.
    """
    import random
    random.seed(int(time.time() / 1800))  # muda a cada 30min
    variation = {
        "home": round(odds["home"] * random.uniform(0.96, 1.04), 2),
        "draw": round(odds["draw"] * random.uniform(0.97, 1.03), 2),
        "away": round(odds["away"] * random.uniform(0.96, 1.04), 2),
    }
    return variation

def _odds_changed_significantly(old: dict, new: dict, threshold: float = 0.10) -> bool:
    """Detecta variação de odds acima do threshold (padrão 10%)."""
    for key in ["home", "draw", "away"]:
        o, n = old.get(key, 0), new.get(key, 0)
        if o > 0 and abs(n - o) / o > threshold:
            return True
    return False

async def check_odds_changes():
    """Verifica se odds de todas as 72 partidas da Copa mudaram significativamente usando a API real e gera alertas."""
    global _last_odds
    
    api_key = os.environ.get("ODDS_API_KEY") or "854375276017769665c8034fae761c698f455901e155037dd3749b56d1de27e5"
    if not api_key:
        print("[MONITOR] Nenhuma chave de API de odds configurada.")
        return
        
    print("[MONITOR] Buscando odds reais da Copa do Mundo via Odds-API.io...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 1. Obter todos os eventos de futebol
    events_url = f"https://api.odds-api.io/v3/events?sport=football&apiKey={api_key}"
    events = []
    try:
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(events_url, headers=headers, timeout=12.0)
            if resp.status_code == 200:
                events = resp.json()
            else:
                print(f"[MONITOR] Falha ao obter eventos: {resp.text}")
                return
    except Exception as e:
        print(f"[MONITOR] Erro de rede ao buscar eventos: {e}")
        return
        
    # Filtrar apenas eventos da Copa do Mundo
    wc_events = []
    for ev in events:
        league = ev.get("league", {})
        l_name = league.get("name", "").lower()
        l_slug = league.get("slug", "").lower()
        if "world cup" in l_name or "world-cup" in l_slug:
            wc_events.append(ev)
            
    if not wc_events:
        print("[MONITOR] Nenhum evento da Copa do Mundo encontrado na API no momento.")
        return
        
    # Mapear eventos aos nossos jogos da Copa
    matches = prediction_engine.COPA_MATCHES
    mapped_events = [] # lista de (match_dict, event_id)
    
    for m in matches:
        m_home = m["home"].lower()
        m_away = m["away"].lower()
        for ev in wc_events:
            ev_home = ev.get("home", "").lower()
            ev_away = ev.get("away", "").lower()
            
            # Checar correspondência exata
            if (m_home == ev_home and m_away == ev_away) or (m_home == ev_away and m_away == ev_home):
                mapped_events.append((m, ev["id"]))
                break
                
    if not mapped_events:
        print("[MONITOR] Não foi possível correlacionar nenhum jogo da Copa local com os eventos da API.")
        return
        
    # Agrupar os IDs de eventos para busca em lote (multi) de no máximo 10 de cada vez
    event_chunks = []
    current_chunk = []
    for m, ev_id in mapped_events:
        current_chunk.append((m, ev_id))
        if len(current_chunk) == 10:
            event_chunks.append(current_chunk)
            current_chunk = []
    if current_chunk:
        event_chunks.append(current_chunk)
        
    # 2. Puxar odds em lote para cada chunk
    for chunk in event_chunks:
        chunk_ids = ",".join(str(item[1]) for item in chunk)
        odds_url = f"https://api.odds-api.io/v3/odds/multi?eventIds={chunk_ids}&bookmakers=Bet365&apiKey={api_key}"
        try:
            async with httpx.AsyncClient(verify=False) as client:
                resp = await client.get(odds_url, headers=headers, timeout=12.0)
                if resp.status_code != 200:
                    print(f"[MONITOR] Falha ao obter odds em lote: {resp.text}")
                    continue
                
                odds_data_list = resp.json()
                
                # Mapear resposta de volta para as partidas correspondentes
                for ev_odds in odds_data_list:
                    ev_id = ev_odds.get("id")
                    bookies = ev_odds.get("bookmakers", {})
                    
                    # Buscar odds da Bet365
                    bet365_markets = bookies.get("Bet365") or bookies.get("Bet365 (no latency)")
                    if not bet365_markets:
                        continue
                        
                    ml_odds = None
                    for market in bet365_markets:
                        if market.get("name") == "ML":
                            odds_list = market.get("odds", [{}])
                            if odds_list:
                                ml_odds = odds_list[0]
                                break
                                
                    if not ml_odds:
                        continue
                        
                    # Obter os valores das odds
                    try:
                        home_odd = float(ml_odds.get("home"))
                        draw_odd = float(ml_odds.get("draw"))
                        away_odd = float(ml_odds.get("away"))
                    except (ValueError, TypeError):
                        continue
                        
                    # Encontrar a partida correspondente no chunk
                    matched_match = None
                    for m, c_ev_id in chunk:
                        if c_ev_id == ev_id:
                            matched_match = m
                            break
                            
                    if not matched_match:
                        continue
                        
                    # Checar se a ordem do time da API está invertida em relação à nossa partida
                    api_home = ev_odds.get("home", "").lower()
                    m_home = matched_match["home"].lower()
                    if api_home != m_home:
                        home_odd, away_odd = away_odd, home_odd
                        
                    match_key = f"{matched_match['home']} x {matched_match['away']}"
                    
                    ref_odds = _last_odds.get(match_key) or {
                        "home": matched_match["oh"],
                        "draw": matched_match["od"],
                        "away": matched_match["oa"]
                    }
                    
                    variation = {
                        "home": home_odd,
                        "draw": draw_odd,
                        "away": away_odd
                    }
                    
                    # Calcular predições para checar mudança
                    old_pred_data = prediction_engine.predict_match(
                        matched_match["home"], matched_match["away"], 
                        ref_odds["home"], ref_odds["draw"], ref_odds["away"], 
                        matched_match.get("venue")
                    )
                    new_pred_data = prediction_engine.predict_match(
                        matched_match["home"], matched_match["away"], 
                        variation["home"], variation["draw"], variation["away"], 
                        matched_match.get("venue")
                    )
                    
                    old_pred = old_pred_data['suggested_score']['score']
                    new_pred = new_pred_data['suggested_score']['score']
                    
                    # Atualizar na fonte do prediction_engine
                    matched_match["oh"] = variation["home"]
                    matched_match["od"] = variation["draw"]
                    matched_match["oa"] = variation["away"]
                    
                    home_team_pt = prediction_engine.PORTUGUESE_TEAM_NAMES.get(matched_match["home"], matched_match["home"])
                    away_team_pt = prediction_engine.PORTUGUESE_TEAM_NAMES.get(matched_match["away"], matched_match["away"])
                    match_key_pt = f"{home_team_pt} x {away_team_pt}"
                    
                    # Se o palpite da IA mudou
                    if old_pred != new_pred:
                        _add_alert(
                            alert_type="prediction_change",
                            title=f"🔄 Palpite da IA mudou — {match_key_pt}!",
                            body=f"De {old_pred} para {new_pred}. Nova calibração de odds reais da Bet365: Mandante {variation['home']}, Empate {variation['draw']}, Visitante {variation['away']}.",
                            match=match_key_pt,
                            priority="high",
                        )
                    # Ou se as odds mudaram significativamente
                    elif _odds_changed_significantly(ref_odds, variation, threshold=0.08):
                        home_diff = variation["home"] - ref_odds["home"]
                        who = home_team_pt if home_diff < 0 else away_team_pt if home_diff > 0 else ""
                        direction = "favorito" if home_diff < 0 else "azarão"
                        _add_alert(
                            alert_type="odds_change",
                            title=f"📊 Odds alteradas — {match_key_pt}",
                            body=f"{who} ficou mais {direction} nas casas de apostas (palpite mantido: {new_pred}). Novas odds: {variation['home']} | {variation['draw']} | {variation['away']}",
                            match=match_key_pt,
                            priority="medium",
                        )
                        
                    _last_odds[match_key] = variation
                    
        except Exception as chunk_err:
            print(f"[MONITOR] Erro ao buscar odds do lote {chunk_ids}: {chunk_err}")

async def check_real_news():
    """Busca notícias reais e atualizadas da Copa e seleções usando o feed RSS do Globo Esporte (GE)."""
    rss_urls = [
        "https://ge.globo.com/rss/ge/futebol/selecao-brasileira/",
        "https://ge.globo.com/rss/ge/futebol/"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Map portuguese names/variations to official team names in English
    team_mapping = {
        "brasil": "Brazil",
        "argentina": "Argentina",
        "frança": "France",
        "espanha": "Spain",
        "alemanha": "Germany",
        "inglaterra": "England",
        "portugal": "Portugal",
        "holanda": "Netherlands",
        "bélgica": "Belgium",
        "itália": "Italy",
        "uruguai": "Uruguay",
        "colômbia": "Colombia",
        "méxico": "Mexico",
        "estados unidos": "USA",
        "marrocos": "Morocco",
        "japão": "Japan",
        "croácia": "Croatia",
        "senegal": "Senegal",
        "equador": "Ecuador",
        "suíça": "Switzerland",
        "dinamarca": "Denmark",
        "canadá": "Canada",
        "egito": "Egypt",
        "iscorreg": "Scotland",
        "escócia": "Scotland",
        "paraguai": "Paraguay",
        "tunísia": "Tunisia",
        "argélia": "Algeria",
        "polônia": "Poland",
        "suecia": "Sweden",
        "suécia": "Sweden",
        "noruega": "Norway",
        "cabo verde": "Cape Verde",
        "curaçao": "Curaçao",
        "curaçao": "Curaçao",
        "irã": "Iran",
        "gales": "Wales",
        "gana": "Ghana",
        "camarões": "Cameroon",
        "costa do marfim": "Ivory Coast"
    }

    # Palavras-chave de clubes nacionais a serem excluídos (para evitar notícias de torneios locais)
    exclude_clubs = [
        "botafogo", "flamengo", "corinthians", "palmeiras", "são paulo", "vasco", 
        "fluminense", "cruzeiro", "grêmio", "internacional", "santos", "atlético-mg", 
        "bahia", "coritiba", "série a", "brasileirão", "copa do brasil", "libertadores"
    ]

    # Desativar verificação estrita de SSL para evitar falhas em conexões locais/restritas
    async with httpx.AsyncClient(verify=False) as client:
        for url in rss_urls:
            try:
                resp = await client.get(url, headers=headers, timeout=10.0)
                if resp.status_code != 200:
                    continue
                
                # Parse XML do Feed
                root = ET.fromstring(resp.content)
                items = root.findall('.//item')
                
                for item in items:
                    title_el = item.find('title')
                    desc_el = item.find('description')
                    
                    if title_el is None:
                        continue
                    
                    title = html.unescape(title_el.text or "").strip()
                    desc = html.unescape(desc_el.text or "").strip() if desc_el is not None else ""
                    
                    # Limpar tags HTML remanescentes na descrição
                    desc = re.sub('<[^<]+?>', '', desc)
                    
                    # Resumir a descrição para no máximo 135 caracteres
                    if len(desc) > 135:
                        desc = desc[:132].strip() + "..."
                    
                    # Evitar duplicados (verifica os últimos 50 alertas)
                    if any(a.get("title") == title for a in _alerts):
                        continue
                    
                    text_to_search = (title + " " + desc).lower()
                    
                    # Se contiver termos de clubes nacionais, ignora (a menos que mencione explicitamente Copa ou Seleção)
                    has_club_term = any(club in text_to_search for club in exclude_clubs)
                    has_copa_term = any(copa in text_to_search for copa in ["copa do mundo", "copa 2026", "seleção", "selecao", "mundial"])
                    if has_club_term and not has_copa_term:
                        continue
                    
                    # Filtrar notícias relevantes (relacionadas a desfalques, lesões, seleções ou copa)
                    is_relevant = False
                    priority = "medium"
                    
                    # Palavras-chave de alta prioridade (lesões/desfalques)
                    if any(kw in text_to_search for kw in ["lesão", "lesao", "lesionado", "suspenso", "suspensão", "fora da copa", "desfalque", "fratura", "estiramento", "dores", "dm", "médico", "dúvida"]):
                        is_relevant = True
                        priority = "high"
                    # Palavras-chave de média prioridade (escalação/preparação/seleção)
                    elif any(kw in text_to_search for kw in ["escalação", "escalacao", "treino", "titular", "convocado", "copa do mundo", "copa 2026", "seleção", "selecao", "mundial"]):
                        is_relevant = True
                        priority = "medium"
                    # Se mencionar qualquer seleção da Copa do Mundo e termos esportivos
                    elif any(pt_team in text_to_search for pt_team in team_mapping.keys()) and any(kw in text_to_search for kw in ["amistoso", "treino", "jogo", "estréia", "estreia", "convoca", "prepara"]):
                        is_relevant = True
                        priority = "medium"
                        
                    if not is_relevant:
                        continue
                    
                    # Tentar identificar qual país a notícia se refere
                    match_team = ""
                    for pt_name, eng_name in team_mapping.items():
                        if pt_name in text_to_search:
                            match_team = eng_name
                            break
                    
                    # Adiciona o alerta real no sistema
                    _add_alert(
                        alert_type="news",
                        title=title,
                        body=desc if desc else title,
                        match=match_team,
                        priority=priority
                    )
                    
            except Exception as e:
                print(f"[MONITOR] Erro ao buscar/processar RSS do feed ({url}): {e}")

async def send_periodic_recap():
    """Compila e envia um boletim VIP periódico com as melhores oportunidades do dia."""
    import os
    try:
        matches = prediction_engine.get_matches_with_predictions()
        valid_matches = [m for m in matches if m.get('prediction')]
        # Ordenar por maior confiança
        valid_matches.sort(key=lambda m: m['prediction'].get('confidence', 0), reverse=True)
        
        top_opportunities = valid_matches[:3]
        
        msg_body = (
            "📊 *BOLETIM DE OPORTUNIDADES VIP*\n\n"
            "Aqui estão as 3 melhores predições de IA com maior índice de confiança para os próximos jogos:\n\n"
        )
        
        for m in top_opportunities:
            pred = m['prediction']
            home_pt = prediction_engine.PORTUGUESE_TEAM_NAMES.get(m['home'], m['home'])
            away_pt = prediction_engine.PORTUGUESE_TEAM_NAMES.get(m['away'], m['away'])
            score = pred['suggested_score']['score']
            confidence = pred['confidence']
            msg_body += f"⚽ *{home_pt} x {away_pt}*\n"
            msg_body += f"   • Sugestão de Placar: {score}\n"
            msg_body += f"   • Confiança do Modelo: {confidence}%\n\n"
            
        msg_body += (
            "🏆 *Favoritos ao Título (Monte Carlo):*\n"
            "1. Espanha 🇪🇸 — 17.2%\n"
            "2. França 🇫🇷 — 16.1%\n"
            "3. Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿 — 10.8%\n\n"
            "⚡ Fique atento a novas variações de odds em tempo real!"
        )
        
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json={
                    "chat_id": chat_id,
                    "text": msg_body,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                })
                if resp.status_code == 200:
                    print("[MONITOR] Boletim VIP periódico enviado com sucesso ao Telegram.")
                else:
                    print(f"[MONITOR] Falha ao enviar boletim periódico: {resp.text}")
    except Exception as e:
        print(f"[MONITOR] Erro ao gerar boletim periódico: {e}")

async def monitoring_loop():
    """Loop principal de monitoramento — roda a cada 2 minutos."""
    global _running
    _running = True
    print("[MONITOR] Iniciando monitoramento de notícias e odds de todos os 72 jogos...")
 
    # Alerta inicial de boas-vindas
    _add_alert(
        alert_type="news",
        title="🚀 GolCerto 2026 ativo!",
        body="Monitorando odds e notícias das 48 seleções em tempo real. Você será avisado de qualquer mudança importante.",
        priority="low",
    )
 
    while _running:
        try:
            await check_odds_changes()
            await check_real_news()
            
            # Executar boletim VIP periódico a cada 8 horas (ou no primeiro ciclo de execução)
            current_time = time.time()
            global _last_recap_time
            # Se for a primeira execução (_last_recap_time == 0) ou se passaram 8 horas
            if _last_recap_time == 0.0 or (current_time - _last_recap_time >= 8 * 60 * 60):
                await send_periodic_recap()
                _last_recap_time = current_time
        except Exception as e:
            print(f"[MONITOR] Erro: {e}")
 
        # Verificar a cada 2 minutos
        await asyncio.sleep(2 * 60)

def get_alerts(limit: int = 20, unread_only: bool = False) -> list[dict]:
    """Retorna alertas recentes."""
    result = _alerts[:limit]
    if unread_only:
        result = [a for a in result if not a.get("read")]
    return result

def mark_read(alert_id: int) -> bool:
    """Marca alerta como lido."""
    for a in _alerts:
        if a["id"] == alert_id:
            a["read"] = True
            return True
    return False

def get_unread_count() -> int:
    return sum(1 for a in _alerts if not a.get("read"))
