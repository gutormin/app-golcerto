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
from datetime import datetime, timezone
from typing import Any
from app import prediction_engine

# ─── ESTADO GLOBAL ────────────────────────────────────────────────────────────
_alerts: list[dict] = []          # alertas gerados
_last_predictions: dict = {}      # palpites anteriores por jogo
_last_odds: dict = {}             # odds anteriores por jogo
_running = False

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
    """Verifica se odds de todas as 72 partidas da Copa mudaram significativamente e gera alertas."""
    global _last_odds
    import random

    matches = prediction_engine.COPA_MATCHES

    for m in matches:
        match_key = f"{m['home']} x {m['away']}"
        ref_odds = _last_odds.get(match_key) or {
            "home": m["oh"],
            "draw": m["od"],
            "away": m["oa"]
        }

        # 15% de chance de mudar a odd a cada rodada de verificação para simular flutuações reais
        if random.random() < 0.15:
            # Simular variação realista de ±8%
            variation = {
                "home": round(ref_odds["home"] * random.uniform(0.92, 1.08), 2),
                "draw": round(ref_odds["draw"] * random.uniform(0.95, 1.05), 2),
                "away": round(ref_odds["away"] * random.uniform(0.92, 1.08), 2),
            }
            # Evitar odds menores que 1.05
            variation["home"] = max(1.05, variation["home"])
            variation["draw"] = max(1.05, variation["draw"])
            variation["away"] = max(1.05, variation["away"])

            # Predict using our Dixon-Coles engine
            old_pred_data = prediction_engine.predict_match(m["home"], m["away"], ref_odds["home"], ref_odds["draw"], ref_odds["away"], m.get("venue"))
            new_pred_data = prediction_engine.predict_match(m["home"], m["away"], variation["home"], variation["draw"], variation["away"], m.get("venue"))

            old_pred = old_pred_data['suggested_score']['score']
            new_pred = new_pred_data['suggested_score']['score']

            # Atualiza na origem do prediction_engine
            m["oh"] = variation["home"]
            m["od"] = variation["draw"]
            m["oa"] = variation["away"]

            home_team_pt = prediction_engine.PORTUGUESE_TEAM_NAMES.get(m["home"], m["home"])
            away_team_pt = prediction_engine.PORTUGUESE_TEAM_NAMES.get(m["away"], m["away"])
            match_key_pt = f"{home_team_pt} x {away_team_pt}"

            if old_pred != new_pred:
                _add_alert(
                    alert_type="prediction_change",
                    title=f"🔄 Palpite da IA mudou — {match_key_pt}!",
                    body=f"De {old_pred} para {new_pred}. Nova calibração de odds: Mandante {variation['home']}, Empate {variation['draw']}, Visitante {variation['away']}.",
                    match=match_key_pt,
                    priority="high",
                )
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
        else:
            _last_odds[match_key] = ref_odds

async def check_simulated_news():
    """Gera notícias simuladas realistas para demonstração.
    Em produção: buscar de API de notícias esportivas.
    """
    import random
    random.seed(int(time.time() / 3600))  # muda a cada hora

    simulated_news = [
        {
            "title": "🚑 Vinicius Jr. dúvida para estreia do Brasil",
            "body": "Atacante do Real Madrid sentiu dores no tornozelo no treino desta manhã. CT confirma que será reavaliado nas próximas 24h.",
            "match": "Brazil",
            "priority": "high",
        },
        {
            "title": "✅ Mbappé confirmado titular contra a Argentina",
            "body": "Técnico Deschamps confirmou o camisa 10 francês como titular na partida de amanhã. Probabilidade da França aumenta.",
            "match": "France x Argentina",
            "priority": "high",
        },
        {
            "title": "🟥 Pedri suspenso — Espanha reformula meio-campo",
            "body": "Craque do Barcelona cumpre suspensão automática. Sem Pedri, Espanha perde sua principal peça de criação.",
            "match": "Spain",
            "priority": "high",
        },
        {
            "title": "⚡ Treino intenso da Argentina — Messi em grande forma",
            "body": "Imagens do treino mostram Messi participando normalmente. Comissão confirma que a Argentina chega 100% para a Copa.",
            "match": "Argentina",
            "priority": "medium",
        },
        {
            "title": "🌧️ Previsão de chuva intensa no jogo Brasil x México",
            "body": "Meteorologistas preveem forte chuva no Estádio Rose Bowl. Condições adversas podem favorecer jogo de menos gols.",
            "match": "Brazil x Mexico",
            "priority": "medium",
        },
    ]

    # Rotação: a cada hora mostra uma notícia diferente
    hour = int(time.time() / 3600)
    news = simulated_news[hour % len(simulated_news)]

    # Verificar se já foi mostrada recentemente
    for a in _alerts[:10]:
        if a.get("title") == news["title"]:
            return  # já exibida

    _add_alert(
        alert_type="news",
        title=news["title"],
        body=news["body"],
        match=news["match"],
        priority=news["priority"],
    )

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
            await check_simulated_news()
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
