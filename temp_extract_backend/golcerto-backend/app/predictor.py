"""Motor preditivo do GolCerto 2026.

Usa modelo de Poisson bivariado (Dixon-Coles) calibrado com odds de mercado
para calcular probabilidades de resultado e os placares mais prováveis.
"""
import math
import numpy as np
from scipy.stats import poisson
from typing import Any
from dataclasses import dataclass


@dataclass
class MatchPrediction:
    """Resultado completo de uma predição."""
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    home_goals_expected: float
    away_goals_expected: float
    top_scores: list[dict]          # 3 placares mais prováveis
    confidence: float               # 0-100
    model_details: dict             # detalhes internos do modelo


# Força histórica base dos times — modelo MULTIPLICATIVO (padrão Dixon-Coles)
#
#   mu_home = attack_home × defense_away × HOME_ADVANTAGE
#   mu_away = attack_away × defense_home
#
#   attack  > 1.0 → time marca acima da média mundial
#   defense < 1.0 → time concede abaixo da média (boa defesa)
#   defense > 1.0 → time concede acima da média (defesa fraca)
# Ataque e defesa em escala de gols esperados por partida
# Serão ajustados dinamicamente com dados reais da API
BASE_TEAM_STRENGTH: dict[str, dict[str, float]] = {
    "Brazil":       {"attack": 1.55, "defense": 0.72},
    "France":       {"attack": 1.50, "defense": 0.76},
    "Argentina":    {"attack": 1.45, "defense": 0.80},
    "England":      {"attack": 1.40, "defense": 0.82},
    "Germany":      {"attack": 1.38, "defense": 0.85},
    "Spain":        {"attack": 1.35, "defense": 0.80},
    "Portugal":     {"attack": 1.30, "defense": 0.88},
    "Netherlands":  {"attack": 1.28, "defense": 0.86},
    "Belgium":      {"attack": 1.22, "defense": 0.92},
    "Croatia":      {"attack": 1.18, "defense": 0.90},
    "Denmark":      {"attack": 1.15, "defense": 0.88},
    "Switzerland":  {"attack": 1.12, "defense": 0.90},
    "Uruguay":      {"attack": 1.15, "defense": 0.94},
    "Colombia":     {"attack": 1.12, "defense": 0.96},
    "Serbia":       {"attack": 1.10, "defense": 0.98},
    "Japan":        {"attack": 1.05, "defense": 1.00},
    "Morocco":      {"attack": 1.02, "defense": 0.96},
    "USA":          {"attack": 1.08, "defense": 1.02},
    "Mexico":       {"attack": 0.95, "defense": 1.10},
    "South Korea":  {"attack": 0.98, "defense": 1.08},
    "Senegal":      {"attack": 0.95, "defense": 1.02},
    "Poland":       {"attack": 1.00, "defense": 1.05},
    "Australia":    {"attack": 0.88, "defense": 1.12},
    "Ecuador":      {"attack": 0.90, "defense": 1.10},
    "Canada":       {"attack": 0.92, "defense": 1.12},
    "Wales":        {"attack": 0.92, "defense": 1.04},
    "Ghana":        {"attack": 0.85, "defense": 1.18},
    "Cameroon":     {"attack": 0.82, "defense": 1.20},
    "Tunisia":      {"attack": 0.82, "defense": 1.15},
    "Iran":         {"attack": 0.75, "defense": 1.12},
    "Saudi Arabia": {"attack": 0.78, "defense": 1.18},
    "Qatar":        {"attack": 0.65, "defense": 1.30},
}

# Vantagem de jogar em campo neutro (Copa do Mundo)
HOME_ADVANTAGE = 1.06


def _get_team_strength(team_name: str, recent_matches: list[dict] | None = None) -> dict[str, float]:
    """Retorna força ajustada do time.

    Se houver partidas recentes, ajusta os coeficientes base com a
    performance das últimas 5 partidas (weighted — mais recentes valem mais).

    Args:
        team_name: Nome do time conforme football-data.org.
        recent_matches: Lista de partidas recentes do time (opcional).

    Returns:
        Dict com 'attack' e 'defense' ajustados.
    """
    base = BASE_TEAM_STRENGTH.get(team_name, {"attack": 1.10, "defense": 1.10}).copy()

    if not recent_matches:
        return base

    # Usar até 5 partidas, com pesos decrescentes (mais recente = maior peso)
    matches = recent_matches[:5]
    weights = [0.35, 0.25, 0.20, 0.12, 0.08]

    scored_list, conceded_list = [], []

    for i, match in enumerate(matches):
        score = match.get("score", {}).get("fullTime", {})
        home_id = match.get("homeTeam", {}).get("id")
        is_home = match.get("homeTeam", {}).get("name") == team_name

        goals_scored = score.get("home" if is_home else "away") or 0
        goals_conceded = score.get("away" if is_home else "home") or 0

        w = weights[i] if i < len(weights) else 0.05
        scored_list.append((goals_scored, w))
        conceded_list.append((goals_conceded, w))

    if scored_list:
        avg_scored = sum(g * w for g, w in scored_list) / sum(w for _, w in scored_list)
        avg_conceded = sum(g * w for g, w in conceded_list) / sum(w for _, w in conceded_list)

        # Blend: 60% dados reais + 40% base histórica
        base["attack"] = 0.6 * max(avg_scored, 0.3) + 0.4 * base["attack"]
        base["defense"] = 0.6 * max(avg_conceded, 0.3) + 0.4 * base["defense"]

    return base


def _dixon_coles_correction(home_goals: int, away_goals: int, mu_h: float, mu_a: float, rho: float = -0.13) -> float:
    """Fator de correção Dixon-Coles para placares baixos (0-0, 1-0, 0-1, 1-1).

    Placares baixos são sub/superestimados pelo Poisson simples.
    rho negativo indica correlação negativa entre gols dos times.

    Args:
        home_goals, away_goals: Placar da partida.
        mu_h, mu_a: Médias esperadas de gols.
        rho: Parâmetro de correlação (tipicamente -0.1 a -0.2).

    Returns:
        Fator multiplicativo para a probabilidade Poisson.
    """
    if home_goals == 0 and away_goals == 0:
        return 1 - mu_h * mu_a * rho
    elif home_goals == 0 and away_goals == 1:
        return 1 + mu_h * rho
    elif home_goals == 1 and away_goals == 0:
        return 1 + mu_a * rho
    elif home_goals == 1 and away_goals == 1:
        return 1 - rho
    return 1.0


def _calibrate_with_odds(
    model_probs: tuple[float, float, float],
    odds_home: float | None,
    odds_draw: float | None,
    odds_away: float | None,
) -> tuple[float, float, float]:
    """Calibra probabilidades do modelo com odds de mercado.

    As odds de mercado contêm informação valiosa (lesões, clima, etc.).
    Fazemos um blend: 70% modelo + 30% mercado.

    Args:
        model_probs: (P_home_win, P_draw, P_away_win) do modelo Poisson.
        odds_home, odds_draw, odds_away: Odds decimais das casas de aposta.

    Returns:
        Tupla de probabilidades calibradas e normalizadas.
    """
    p_model = np.array(model_probs)

    if odds_home and odds_draw and odds_away:
        # Converter odds para probabilidades implícitas (remover margem)
        raw = np.array([1 / odds_home, 1 / odds_draw, 1 / odds_away])
        p_market = raw / raw.sum()  # normalizar removendo overround

        # Blend ponderado
        p_final = 0.70 * p_model + 0.30 * p_market
    else:
        p_final = p_model

    # Garantir que soma = 1
    p_final = np.clip(p_final, 0.01, 0.99)
    p_final /= p_final.sum()

    return float(p_final[0]), float(p_final[1]), float(p_final[2])


def _compute_confidence(
    p_win: float,
    home_strength: dict,
    away_strength: dict,
    recent_home: list | None,
    recent_away: list | None,
    has_odds: bool,
) -> float:
    """Calcula o índice de confiança do modelo (0-100).

    Fatores: dominância das probabilidades, dados disponíveis,
    qualidade das partidas recentes e presença de odds.

    Returns:
        Confiança entre 0 e 100.
    """
    # Base: quão dominante é o resultado mais provável
    max_prob = max(p_win)
    confidence = 40 + (max_prob - 0.33) * 120  # 40-100 range

    # Bônus por dados reais disponíveis
    if recent_home and len(recent_home) >= 3:
        confidence += 8
    if recent_away and len(recent_away) >= 3:
        confidence += 8
    if has_odds:
        confidence += 6

    return round(min(max(confidence, 35), 97), 1)


def predict_match(
    home_team: str,
    away_team: str,
    odds_home: float | None = None,
    odds_draw: float | None = None,
    odds_away: float | None = None,
    recent_home: list[dict] | None = None,
    recent_away: list[dict] | None = None,
    max_goals: int = 7,
) -> MatchPrediction:
    """Gera predição completa para uma partida usando modelo Poisson + Dixon-Coles.

    Args:
        home_team: Nome do time mandante.
        away_team: Nome do time visitante.
        odds_home: Odd decimal para vitória do mandante (usado internamente).
        odds_draw: Odd decimal para empate (usado internamente).
        odds_away: Odd decimal para vitória do visitante (usado internamente).
        recent_home: Partidas recentes do mandante (da API).
        recent_away: Partidas recentes do visitante (da API).
        max_goals: Máximo de gols por time considerado no modelo.

    Returns:
        MatchPrediction com todos os dados da predição.
    """
    # 1. Força dos times (ajustada com dados reais se disponíveis)
    str_h = _get_team_strength(home_team, recent_home)
    str_a = _get_team_strength(away_team, recent_away)

    # 2. Gols esperados (lambda Poisson)
    # mu = ataque_mandante / defesa_visitante * fator_de_campo
    # Modelo multiplicativo Dixon-Coles: attack × defense_oponente
    # defense < 1.0 = boa defesa; defense > 1.0 = defesa fraca
    mu_home = str_h["attack"] * str_a["defense"] * HOME_ADVANTAGE
    mu_away = str_a["attack"] * str_h["defense"]

    mu_home = max(mu_home, 0.2)
    mu_away = max(mu_away, 0.2)

    # 3. Matriz de probabilidades de placares (Dixon-Coles)
    score_matrix: dict[tuple[int, int], float] = {}
    p_home_win = p_draw = p_away_win = 0.0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p_h = poisson.pmf(h, mu_home)
            p_a = poisson.pmf(a, mu_away)
            dc = _dixon_coles_correction(h, a, mu_home, mu_away)
            prob = p_h * p_a * dc
            score_matrix[(h, a)] = prob

            if h > a:
                p_home_win += prob
            elif h == a:
                p_draw += prob
            else:
                p_away_win += prob

    # Normalizar (porque cortamos em max_goals)
    total = p_home_win + p_draw + p_away_win
    p_home_win /= total
    p_draw /= total
    p_away_win /= total

    # 4. Calibrar com odds de mercado (usadas APENAS no cálculo)
    p_home_win, p_draw, p_away_win = _calibrate_with_odds(
        (p_home_win, p_draw, p_away_win),
        odds_home, odds_draw, odds_away,
    )

    # 5. Top 3 placares mais prováveis
    sorted_scores = sorted(score_matrix.items(), key=lambda x: x[1], reverse=True)
    top3 = [
        {
            "home": h,
            "away": a,
            "score": f"{h} × {a}",
            "probability": round(prob * 100, 1),
            "rank": i + 1,
        }
        for i, ((h, a), prob) in enumerate(sorted_scores[:3])
    ]

    # 6. Confiança
    confidence = _compute_confidence(
        (p_home_win, p_draw, p_away_win),
        str_h, str_a, recent_home, recent_away,
        bool(odds_home and odds_draw and odds_away),
    )

    return MatchPrediction(
        home_win_prob=round(p_home_win * 100, 1),
        draw_prob=round(p_draw * 100, 1),
        away_win_prob=round(p_away_win * 100, 1),
        home_goals_expected=round(mu_home, 2),
        away_goals_expected=round(mu_away, 2),
        top_scores=top3,
        confidence=confidence,
        model_details={
            "home_attack": str_h["attack"],
            "home_defense": str_h["defense"],
            "away_attack": str_a["attack"],
            "away_defense": str_a["defense"],
            "mu_home": round(mu_home, 3),
            "mu_away": round(mu_away, 3),
            "odds_used": bool(odds_home),
            "recent_matches_home": len(recent_home or []),
            "recent_matches_away": len(recent_away or []),
        },
    )


def predict_champion(teams: list[str]) -> list[dict[str, Any]]:
    """Calcula probabilidade de cada time ser campeão via simulação Monte Carlo.

    Simula 50.000 torneios completos usando o modelo Poisson para cada partida.
    Retorna ranking com probabilidades de título.

    Args:
        teams: Lista de nomes dos times participantes.

    Returns:
        Lista ordenada de dicts com 'team', 'probability', 'rank'.
    """
    n_simulations = 50_000
    champion_count: dict[str, int] = {t: 0 for t in teams}

    for _ in range(n_simulations):
        remaining = list(teams)
        np.random.shuffle(remaining)

        # Simula mata-mata (pares de times)
        while len(remaining) > 1:
            next_round = []
            for i in range(0, len(remaining), 2):
                if i + 1 >= len(remaining):
                    next_round.append(remaining[i])
                    continue

                team_a = remaining[i]
                team_b = remaining[i + 1]
                pred = predict_match(team_a, team_b)

                # Sortear vencedor pela probabilidade do modelo
                rand = np.random.random()
                if rand < pred.home_win_prob / 100:
                    next_round.append(team_a)
                elif rand < (pred.home_win_prob + pred.draw_prob) / 100:
                    # Empate → pênaltis (50/50)
                    next_round.append(team_a if np.random.random() < 0.5 else team_b)
                else:
                    next_round.append(team_b)

            remaining = next_round

        if remaining:
            champion_count[remaining[0]] += 1

    results = [
        {
            "team": team,
            "probability": round(count / n_simulations * 100, 1),
            "rank": 0,
        }
        for team, count in champion_count.items()
    ]
    results.sort(key=lambda x: x["probability"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results
