"""GolCerto 2026 API — com sistema de alertas em tempo real e IA preditiva."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import asyncio
import os
from app import news_monitor
from app import prediction_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicia o monitoramento quando a API sobe."""
    # Run a fast Monte Carlo simulation at startup to populate cache
    prediction_engine.get_cached_rankings()
    # Fetch real news on startup and run background loop
    asyncio.create_task(prediction_engine.update_all_news_cache_loop())
    task = asyncio.create_task(news_monitor.monitoring_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="GolCerto 2026 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROOT ENDPOINT ────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    """Retorna a Landing Page do aplicativo."""
    file_name = "landing.html"
    if os.path.exists(file_name):
        return FileResponse(file_name)
    scratch_path = os.path.join("C:\\Users\\Gustavo\\.gemini\\antigravity\\scratch\\gol certo", file_name)
    if os.path.exists(scratch_path):
        return FileResponse(scratch_path)
    return {
        "status": "ok",
        "service": "GolCerto 2026 API",
        "monitoring": news_monitor._running,
        "alerts_count": len(news_monitor._alerts)
    }

@app.get("/player.jpg")
async def get_player():
    """Retorna a imagem do jogador de fundo."""
    file_name = "player.jpg"
    if os.path.exists(file_name):
        return FileResponse(file_name)
    scratch_path = os.path.join("C:\\Users\\Gustavo\\.gemini\antigravity\\scratch\\gol certo", file_name)
    if os.path.exists(scratch_path):
        return FileResponse(scratch_path)
    raise HTTPException(status_code=404, detail="Imagem player.jpg não encontrada.")

# ─── APP ENDPOINT ─────────────────────────────────────────────────────────────
@app.get("/app")
async def get_app():
    """Retorna o aplicativo frontend (HTML)."""
    file_name = "GolCerto2026_FINAL6 (2).html"
    # Procurar no Cwd
    if os.path.exists(file_name):
        return FileResponse(file_name)
    # Procurar um nível acima
    parent_path = os.path.join("..", file_name)
    if os.path.exists(parent_path):
        return FileResponse(parent_path)
    # Procurar dois níveis acima
    grandparent_path = os.path.join("..", "..", file_name)
    if os.path.exists(grandparent_path):
        return FileResponse(grandparent_path)
    # Procurar no diretório específico de scratch
    scratch_path = os.path.join("C:\\Users\\Gustavo\\.gemini\\antigravity\\scratch\\gol certo", file_name)
    if os.path.exists(scratch_path):
        return FileResponse(scratch_path)
    raise HTTPException(status_code=404, detail="Arquivo HTML do aplicativo não encontrado.")


@app.get("/logo.jpg")
async def get_logo():
    """Retorna o logotipo (logo.jpg)."""
    file_name = "logo.jpg"
    # Procurar no Cwd
    if os.path.exists(file_name):
        return FileResponse(file_name)
    # Procurar um nível acima
    parent_path = os.path.join("..", file_name)
    if os.path.exists(parent_path):
        return FileResponse(parent_path)
    # Procurar dois níveis acima
    grandparent_path = os.path.join("..", "..", file_name)
    if os.path.exists(grandparent_path):
        return FileResponse(grandparent_path)
    # Procurar no diretório específico de scratch
    scratch_path = os.path.join("C:\\Users\\Gustavo\\.gemini\\antigravity\\scratch\\gol certo", file_name)
    if os.path.exists(scratch_path):
        return FileResponse(scratch_path)
    raise HTTPException(status_code=404, detail="Logotipo não encontrado.")


# ─── ENDPOINTS DE ALERTAS ─────────────────────────────────────────────────────

@app.get("/alerts")
async def get_alerts(
    limit: int = Query(default=20, le=50),
    unread_only: bool = Query(default=False),
):
    """Retorna alertas recentes (notícias + mudanças de odds/palpite)."""
    alerts = news_monitor.get_alerts(limit=limit, unread_only=unread_only)
    return {
        "alerts": alerts,
        "unread_count": news_monitor.get_unread_count(),
        "total": len(alerts),
    }

@app.post("/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: int):
    """Marca um alerta como lido."""
    ok = news_monitor.mark_read(alert_id)
    return {"success": ok}

@app.get("/alerts/unread-count")
async def unread_count():
    """Contagem rápida de alertas não lidos."""
    return {"count": news_monitor.get_unread_count()}

# ─── ENDPOINTS DE PREDIÇÃO E SIMULAÇÃO ───────────────────────────────────────

@app.get("/predict")
async def get_prediction(
    home: str = Query(..., description="Nome da seleção mandante (em inglês)"),
    away: str = Query(..., description="Nome da seleção visitante (em inglês)"),
    odds_home: float = Query(None, description="Odds para vitória do mandante"),
    odds_draw: float = Query(None, description="Odds para empate"),
    odds_away: float = Query(None, description="Odds para vitória do visitante"),
):
    """Retorna predição detalhada para uma partida com Dixon-Coles/Poisson."""
    try:
        pred = prediction_engine.predict_match(home, away, odds_home, odds_draw, odds_away)
        return pred
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no cálculo de predição: {str(e)}")

@app.get("/champion-odds")
async def get_champion_odds():
    """Retorna o ranking de probabilidades de título via Monte Carlo."""
    try:
        rankings = prediction_engine.get_cached_rankings()
        return {
            "rankings": rankings,
            "count": len(rankings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na simulação Monte Carlo: {str(e)}")

@app.get("/team-ratings")
async def get_team_ratings():
    """Retorna os ratings de ataque, defesa e pontuação FIFA de todas as seleções."""
    try:
        ratings = prediction_engine.TEAM_RATINGS
        return {"ratings": ratings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter ratings: {str(e)}")

# ─── ENDPOINTS DE PARTIDAS ───────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "monitoring": news_monitor._running,
        "alerts_count": len(news_monitor._alerts),
    }

@app.get("/matches")
async def get_matches():
    """Retorna a lista completa de 72 partidas da Copa 2026 com predições pré-calculadas."""
    try:
        matches = prediction_engine.get_matches_with_predictions()
        return {"matches": matches, "count": len(matches)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter partidas: {str(e)}")
