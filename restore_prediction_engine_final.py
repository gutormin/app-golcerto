import re

# Read fixed matches from the fixed python matches file we generated
with open('copa_matches_and_groups_fixed.py', 'r', encoding='utf-8') as f:
    matches_and_groups_content = f.read()

# Let's extract GROUPS and COPA_MATCHES definitions from it
groups_match = re.search(r'GROUPS\s*=\s*\{.*?\}', matches_and_groups_content, re.DOTALL)
copa_matches_match = re.search(r'COPA_MATCHES\s*=\s*\[.*?\]', matches_and_groups_content, re.DOTALL)

groups_def = groups_match.group(0)
copa_matches_def = copa_matches_match.group(0)

# We will define the full team ratings, Portuguese names, and real last results
# exactly as they were in the original prediction_engine.py (which we viewed fully in step 6)
team_ratings_def = """TEAM_RATINGS = {
    'Brazil':          {'att': 1.85, 'def': 0.80, 'fifa': 1800},
    'France':          {'att': 1.80, 'def': 0.82, 'fifa': 1790},
    'Argentina':       {'att': 1.75, 'def': 0.85, 'fifa': 1780},
    'England':         {'att': 1.70, 'def': 0.88, 'fifa': 1760},
    'Portugal':        {'att': 1.65, 'def': 0.90, 'fifa': 1740},
    'Spain':           {'att': 1.60, 'def': 0.92, 'fifa': 1730},
    'Germany':         {'att': 1.55, 'def': 0.95, 'fifa': 1710},
    'Netherlands':     {'att': 1.50, 'def': 0.96, 'fifa': 1700},
    'Belgium':         {'att': 1.48, 'def': 0.98, 'fifa': 1680},
    'Croatia':         {'att': 1.42, 'def': 1.00, 'fifa': 1650},
    'Uruguay':         {'att': 1.45, 'def': 0.98, 'fifa': 1660},
    'Colombia':        {'att': 1.40, 'def': 1.00, 'fifa': 1640},
    'Japan':           {'att': 1.35, 'def': 1.02, 'fifa': 1620},
    'Morocco':         {'att': 1.30, 'def': 0.98, 'fifa': 1610},
    'USA':             {'att': 1.32, 'def': 1.05, 'fifa': 1600},
    'South Korea':     {'att': 1.25, 'def': 1.08, 'fifa': 1560},
    'Switzerland':     {'att': 1.22, 'def': 1.06, 'fifa': 1570},
    'Denmark':         {'att': 1.24, 'def': 1.07, 'fifa': 1565},
    'Serbia':          {'att': 1.28, 'def': 1.12, 'fifa': 1540},
    'Sweden':          {'att': 1.26, 'def': 1.09, 'fifa': 1550},
    'Ecuador':         {'att': 1.22, 'def': 1.08, 'fifa': 1530},
    'Senegal':         {'att': 1.20, 'def': 1.06, 'fifa': 1545},
    'Iran':            {'att': 1.18, 'def': 1.08, 'fifa': 1520},
    'Norway':          {'att': 1.30, 'def': 1.15, 'fifa': 1510},
    'Turkey':          {'att': 1.22, 'def': 1.12, 'fifa': 1500},
    'Saudi Arabia':    {'att': 1.12, 'def': 1.20, 'fifa': 1450},
    'Qatar':           {'att': 1.00, 'def': 1.30, 'fifa': 1350},
    'Canada':          {'att': 1.18, 'def': 1.22, 'fifa': 1460},
    'Bosnia':          {'att': 1.10, 'def': 1.24, 'fifa': 1420},
    'Australia':       {'att': 1.15, 'def': 1.18, 'fifa': 1480},
    'Haiti':           {'att': 0.95, 'def': 1.35, 'fifa': 1300},
    'Scotland':        {'att': 1.14, 'def': 1.20, 'fifa': 1470},
    'Cape Verde':      {'att': 1.05, 'def': 1.25, 'fifa': 1380},
    'Iraq':            {'att': 1.02, 'def': 1.28, 'fifa': 1360},
    'Algeria':         {'att': 1.16, 'def': 1.20, 'fifa': 1465},
    'Austria':         {'att': 1.20, 'def': 1.16, 'fifa': 1490},
    'Jordan':          {'att': 0.98, 'def': 1.32, 'fifa': 1340},
    'Congo DR':        {'att': 1.06, 'def': 1.26, 'fifa': 1390},
    'Uzbekistan':      {'att': 1.08, 'def': 1.24, 'fifa': 1400},
    'Ghana':           {'att': 1.10, 'def': 1.22, 'fifa': 1430},
    'Panama':          {'att': 1.08, 'def': 1.25, 'fifa': 1410},
    'Czech Republic':  {'att': 1.18, 'def': 1.18, 'fifa': 1485},
    'Paraguay':        {'att': 1.06, 'def': 1.18, 'fifa': 1440},
    'South Africa':    {'att': 1.10, 'def': 1.22, 'fifa': 1410},
    'Curacao':         {'att': 0.95, 'def': 1.32, 'fifa': 1320},
    'Ivory Coast':     {'att': 1.18, 'def': 1.20, 'fifa': 1475},
    'Tunisia':         {'att': 1.08, 'def': 1.22, 'fifa': 1445},
    'Egypt':           {'att': 1.16, 'def': 1.18, 'fifa': 1480},
    'New Zealand':     {'att': 0.94, 'def': 1.34, 'fifa': 1310},
    'Mexico':          {'att': 1.24, 'def': 1.06, 'fifa': 1615}
}"""

portuguese_team_names_def = """PORTUGUESE_TEAM_NAMES = {
    'Brazil': 'Seleção Brasileira de futebol',
    'Mexico': 'Seleção Mexicana de futebol',
    'Argentina': 'Seleção Argentina de futebol',
    'Germany': 'Seleção Alemã de futebol',
    'England': 'Seleção da Inglaterra de futebol',
    'Portugal': 'Seleção de Portugal de futebol',
    'France': 'Seleção da França de futebol',
    'Spain': 'Seleção da Espanha de futebol',
    'Netherlands': 'Seleção da Holanda de futebol',
    'Belgium': 'Seleção da Bélgica de futebol',
    'Croatia': 'Seleção da Croácia de futebol',
    'Uruguay': 'Seleção do Uruguai de futebol',
    'Colombia': 'Seleção da Colômbia de futebol',
    'Japan': 'Seleção do Japão de futebol',
    'Morocco': 'Seleção de Marrocos de futebol',
    'USA': 'Seleção dos Estados Unidos de futebol',
    'South Korea': 'Seleção da Coreia do Sul de futebol',
    'Serbia': 'Seleção da Sérvia de futebol',
    'Denmark': 'Seleção da Dinamarca de futebol',
    'Switzerland': 'Seleção da Suíça de futebol',
    'South Africa': 'Seleção da África do Sul de futebol',
    'Qatar': 'Seleção do Catar de futebol',
    'Canada': 'Seleção do Canadá de futebol',
    'Bosnia': 'Seleção da Bósnia de futebol',
    'Australia': 'Seleção da Austrália de futebol',
    'Turkey': 'Seleção da Turquia de futebol',
    'Haiti': 'Seleção do Haiti de futebol',
    'Scotland': 'Seleção da Escócia de futebol',
    'Ivory Coast': 'Seleção da Costa do Marfim de futebol',
    'Ecuador': 'Seleção do Equador de futebol',
    'Curacao': 'Seleção de Curaçao de futebol',
    'Sweden': 'Seleção da Suíça de futebol',  # wait, Switzerland is also Suica, but Sweden is Selecao da Suecia de futebol
    'Sweden': 'Seleção da Suécia de futebol',
    'Tunisia': 'Seleção da Tunísia de futebol',
    'Egypt': 'Seleção do Egito de futebol',
    'Iran': 'Seleção do Irã de futebol',
    'New Zealand': 'Seleção da Nova Zelândia de futebol',
    'Saudi Arabia': 'Seleção da Arábia Saudita de futebol',
    'Cape Verde': 'Seleção de Cabo Verde de futebol',
    'Senegal': 'Seleção do Senegal de futebol',
    'Iraq': 'Seleção do Iraque de futebol',
    'Norway': 'Seleção da Noruega de futebol',
    'Algeria': 'Seleção da Argélia de futebol',
    'Austria': 'Seleção da Áustria de futebol',
    'Jordan': 'Seleção da Jordânia de futebol',
    'Congo DR': 'Seleção da República Democrática do Congo de futebol',
    'Uzbekistan': 'Seleção do Uzbequistão de futebol',
    'Ghana': 'Seleção de Gana de futebol',
    'Panama': 'Seleção do Panamá de futebol',
    'Czech Republic': 'Seleção da República Tcheca de futebol',
    'Paraguay': 'Seleção do Paraguai de futebol'
}"""

real_last_results_def = """REAL_LAST_RESULTS = {
    'Brazil': [
        {'res': 'V', 'score': '6-2', 'opp': 'Panama', 'loc': 'C'},
        {'res': 'V', 'score': '2-0', 'opp': 'Senegal', 'loc': 'C'},
        {'res': 'E', 'score': '1-1', 'opp': 'Tunisia', 'loc': 'F'}
    ],
    'Morocco': [
        {'res': 'V', 'score': '4-0', 'opp': 'Madagascar', 'loc': 'C'},
        {'res': 'V', 'score': '7-0', 'opp': 'Lesotho', 'loc': 'C'},
        {'res': 'V', 'score': '5-1', 'opp': 'Gabon', 'loc': 'F'}
    ],
    'Mexico': [
        {'res': 'E', 'score': '1-1', 'opp': 'Belgium', 'loc': 'F'},
        {'res': 'E', 'score': '0-0', 'opp': 'Portugal', 'loc': 'F'},
        {'res': 'V', 'score': '4-0', 'opp': 'Iceland', 'loc': 'C'}
    ],
    'South Africa': [
        {'res': 'V', 'score': '3-0', 'opp': 'Congo DR', 'loc': 'C'},
        {'res': 'E', 'score': '1-1', 'opp': 'Congo DR', 'loc': 'F'},
        {'res': 'V', 'score': '5-0', 'opp': 'Congo', 'loc': 'C'}
    ],
    'Argentina': [
        {'res': 'V', 'score': '3-0', 'opp': 'Chile', 'loc': 'C'},
        {'res': 'D', 'score': '1-2', 'opp': 'Colombia', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Peru', 'loc': 'C'}
    ],
    'France': [
        {'res': 'V', 'score': '2-0', 'opp': 'Belgium', 'loc': 'C'},
        {'res': 'V', 'score': '4-1', 'opp': 'Israel', 'loc': 'F'},
        {'res': 'V', 'score': '2-1', 'opp': 'Italy', 'loc': 'F'}
    ],
    'Germany': [
        {'res': 'E', 'score': '2-2', 'opp': 'Netherlands', 'loc': 'F'},
        {'res': 'V', 'score': '2-1', 'opp': 'Bosnia', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Netherlands', 'loc': 'C'}
    ],
    'Spain': [
        {'res': 'V', 'score': '4-1', 'opp': 'Switzerland', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Denmark', 'loc': 'C'},
        {'res': 'V', 'score': '3-2', 'opp': 'Switzerland', 'loc': 'C'}
    ],
    'Portugal': [
        {'res': 'V', 'score': '2-1', 'opp': 'Croatia', 'loc': 'C'},
        {'res': 'V', 'score': '3-1', 'opp': 'Poland', 'loc': 'F'},
        {'res': 'V', 'score': '5-1', 'opp': 'Poland', 'loc': 'C'}
    ],
    'Uruguay': [
        {'res': 'V', 'score': '3-2', 'opp': 'Colombia', 'loc': 'C'},
        {'res': 'E', 'score': '1-1', 'opp': 'Brazil', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Peru', 'loc': 'C'}
    ],
    'Colombia': [
        {'res': 'V', 'score': '2-1', 'opp': 'Argentina', 'loc': 'C'},
        {'res': 'V', 'score': '1-0', 'opp': 'Paraguay', 'loc': 'F'},
        {'res': 'D', 'score': '2-3', 'opp': 'Uruguay', 'loc': 'F'}
    ],
    'USA': [
        {'res': 'V', 'score': '1-0', 'opp': 'Panama', 'loc': 'C'},
        {'res': 'V', 'score': '2-1', 'opp': 'Costa Rica', 'loc': 'F'},
        {'res': 'V', 'score': '4-2', 'opp': 'Jamaica', 'loc': 'C'}
    ],
    'Canada': [
        {'res': 'E', 'score': '0-0', 'opp': 'France', 'loc': 'F'},
        {'res': 'V', 'score': '2-1', 'opp': 'USA', 'loc': 'F'},
        {'res': 'V', 'score': '3-0', 'opp': 'Panama', 'loc': 'C'}
    ],
    'England': [
        {'res': 'V', 'score': '2-0', 'opp': 'Finland', 'loc': 'F'},
        {'res': 'V', 'score': '3-1', 'opp': 'Finland', 'loc': 'C'},
        {'res': 'D', 'score': '1-2', 'opp': 'Greece', 'loc': 'C'}
    ],
    'Croatia': [
        {'res': 'D', 'score': '1-2', 'opp': 'Portugal', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Poland', 'loc': 'C'},
        {'res': 'V', 'score': '3-0', 'opp': 'Scotland', 'loc': 'C'}
    ],
    'Netherlands': [
        {'res': 'V', 'score': '5-2', 'opp': 'Bosnia', 'loc': 'C'},
        {'res': 'E', 'score': '2-2', 'opp': 'Germany', 'loc': 'C'},
        {'res': 'D', 'score': '0-1', 'opp': 'Germany', 'loc': 'F'}
    ],
    'Belgium': [
        {'res': 'V', 'score': '3-1', 'opp': 'Israel', 'loc': 'C'},
        {'res': 'D', 'score': '0-2', 'opp': 'France', 'loc': 'F'},
        {'res': 'D', 'score': '1-2', 'opp': 'France', 'loc': 'C'}
    ],
    'Japan': [
        {'res': 'V', 'score': '7-0', 'opp': 'China', 'loc': 'C'},
        {'res': 'V', 'score': '5-0', 'opp': 'Bahrain', 'loc': 'F'},
        {'res': 'V', 'score': '2-0', 'opp': 'Saudi Arabia', 'loc': 'F'}
    ],
    'South Korea': [
        {'res': 'E', 'score': '0-0', 'opp': 'Palestine', 'loc': 'C'},
        {'res': 'V', 'score': '3-1', 'opp': 'Oman', 'loc': 'F'},
        {'res': 'V', 'score': '2-0', 'opp': 'Jordan', 'loc': 'F'}
    ],
    'Ecuador': [
        {'res': 'D', 'score': '0-1', 'opp': 'Brazil', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Peru', 'loc': 'C'},
        {'res': 'E', 'score': '0-0', 'opp': 'Uruguay', 'loc': 'F'}
    ],
    'Chile': [
        {'res': 'D', 'score': '0-3', 'opp': 'Argentina', 'loc': 'F'},
        {'res': 'D', 'score': '1-2', 'opp': 'Bolivia', 'loc': 'C'},
        {'res': 'D', 'score': '1-2', 'opp': 'Brazil', 'loc': 'C'}
    ],
    'Senegal': [
        {'res': 'V', 'score': '1-0', 'opp': 'Burundi', 'loc': 'F'},
        {'res': 'E', 'score': '1-1', 'opp': 'Burkina Faso', 'loc': 'C'},
        {'res': 'V', 'score': '4-0', 'opp': 'Malawi', 'loc': 'C'}
    ],
    'Egypt': [
        {'res': 'V', 'score': '3-0', 'opp': 'Cape Verde', 'loc': 'C'},
        {'res': 'V', 'score': '4-0', 'opp': 'Botswana', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Mauritania', 'loc': 'C'}
    ],
    'Saudi Arabia': [
        {'res': 'E', 'score': '1-1', 'opp': 'Indonesia', 'loc': 'C'},
        {'res': 'V', 'score': '2-1', 'opp': 'China', 'loc': 'F'},
        {'res': 'D', 'score': '0-2', 'opp': 'Japan', 'loc': 'C'}
    ]
}"""

# Assemble all code without f-string to avoid curly brace escaping issues
final_code = "import math\nimport random\nimport hashlib\nimport re\nimport urllib.parse\nimport xml.etree.ElementTree as ET\nimport httpx\nimport asyncio\nfrom typing import Dict, List, Tuple, Any\n\n"
final_code += team_ratings_def + "\n\n"
final_code += "DEFAULT_TEAM = {'att': 1.00, 'def': 1.20, 'fifa': 1300}\n\n"
final_code += groups_def + "\n\n"
final_code += copa_matches_def + "\n\n"
final_code += portuguese_team_names_def + "\n\n"
final_code += "REAL_NEWS_CACHE = {}\n\n"
final_code += real_last_results_def + "\n\n"

final_code += """def get_deterministic_hash(team_name: str, seed: int) -> int:
    val = f"{team_name}_{seed}"
    return int(hashlib.md5(val.encode('utf-8')).hexdigest(), 16)

def get_team_rating(team: str) -> Dict[str, float]:
    return TEAM_RATINGS.get(team, DEFAULT_TEAM)

def poisson_prob(k: int, lamb: float) -> float:
    \"\"\"Calculates Poisson probability for k events with expected value lamb.\"\"\"
    if lamb <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.pow(lamb, k) * math.exp(-lamb)) / math.factorial(k)

def calculate_lambdas(home: str, away: str, odds_home: float = None, odds_draw: float = None, odds_away: float = None, venue: str = None) -> Tuple[float, float]:
    \"\"\"
    Calculates expected goals (lambdas) for home and away.
    Calibrates using a 70% model and 30% market odds approach.
    \"\"\"
    home_rating = get_team_rating(home)
    away_rating = get_team_rating(away)
    
    # Apply host country advantage (15% boost to attack of host teams)
    home_att_mult = 1.15 if home in ['Mexico', 'USA', 'Canada'] else 1.0
    
    # Model lambdas based on attack/defense parameters
    base_mu = 1.35
    lambda_home_model = base_mu * (home_rating['att'] * home_att_mult) * away_rating['def']
    lambda_away_model = base_mu * away_rating['att'] * home_rating['def']
    
    # Incorporate market odds if provided
    if odds_home and odds_draw and odds_away:
        p_home = 1.0 / odds_home
        p_draw = 1.0 / odds_draw
        p_away = 1.0 / odds_away
        total_p = p_home + p_draw + p_away
        
        p_home /= total_p
        p_draw /= total_p
        p_away /= total_p
        
        implied_total_goals = 2.65
        lambda_home_market = implied_total_goals * (p_home + 0.5 * p_draw)
        lambda_away_market = implied_total_goals * (p_away + 0.5 * p_draw)
        
        lambda_home = 0.7 * lambda_home_model + 0.3 * lambda_home_market
        lambda_away = 0.7 * lambda_away_model + 0.3 * lambda_away_market
    else:
        lambda_home = lambda_home_model
        lambda_away = lambda_away_model
        
    return lambda_home, lambda_away

def dixon_coles_adjustment(x: int, y: int, lambda_home: float, lambda_away: float, rho: float = -0.05) -> float:
    if x == 0 and y == 0:
        return 1.0 - lambda_home * lambda_away * rho
    elif x == 1 and y == 0:
        return 1.0 + lambda_away * rho
    elif x == 0 and y == 1:
        return 1.0 + lambda_home * rho
    elif x == 1 and y == 1:
        return 1.0 - rho
    return 1.0

def get_mock_last_results(team: str) -> List[Dict[str, Any]]:
    # Use real results database if available
    if team in REAL_LAST_RESULTS:
        return REAL_LAST_RESULTS[team]
        
    # Fallback to deterministic mock results
    h1 = get_deterministic_hash(team, 1)
    h2 = get_deterministic_hash(team, 2)
    h3 = get_deterministic_hash(team, 3)
    
    fifa = TEAM_RATINGS.get(team, DEFAULT_TEAM)['fifa']
    opponents = [t for t in TEAM_RATINGS.keys() if t != team]
    
    results = []
    for i, h in enumerate([h1, h2, h3]):
        opp = opponents[h % len(opponents)]
        fifa_opp = TEAM_RATINGS.get(opp, DEFAULT_TEAM)['fifa']
        
        diff = fifa - fifa_opp
        if diff > 150:
            res = 'V'
            score = f"{2 + (h % 2)}-{h % 2}"
        elif diff < -150:
            res = 'D'
            score = f"{h % 2}-{2 + (h % 2)}"
        else:
            res = 'E'
            score = f"{h % 2}-{h % 2}"
            
        results.append({
            'res': res,
            'score': score,
            'opp': opp,
            'loc': 'C' if h % 2 == 0 else 'F'
        })
    return results

def get_mock_news(team: str) -> List[Dict[str, str]]:
    # Use real-time news cache if available
    if team in REAL_NEWS_CACHE and len(REAL_NEWS_CACHE[team]) >= 2:
        return REAL_NEWS_CACHE[team]

    h1 = get_deterministic_hash(team, 10)
    h2 = get_deterministic_hash(team, 20)
    
    injury_players = {
        'Brazil': 'Neymar Jr.', 'Argentina': 'Lionel Messi', 'France': 'Kylian Mbappé',
        'England': 'Harry Kane', 'Portugal': 'Cristiano Ronaldo', 'Spain': 'Rodri',
        'Germany': 'Jamal Musiala', 'Netherlands': 'Virgil van Dijk', 'Belgium': 'Kevin De Bruyne',
        'Uruguay': 'Federico Valverde', 'Colombia': 'Luis Díaz'
    }
    p1 = injury_players.get(team, 'O meio-campista titular')
    
    news_templates = [
        {"title": f"Dúvida médica: {p1} realiza exames físicos na coxa esquerda.", "type": "warning"},
        {"title": "Treino técnico-tático foca na saída de bola sob pressão adversária.", "type": "info"},
        {"title": "Clima favorável: delegação expressa confiança total na coletiva.", "type": "success"},
        {"title": "Mudança tática: técnico estuda fechar o meio-campo no próximo duelo.", "type": "info"},
        {"title": "Suspensão temporária: zagueiro treina em separado após dores leves.", "type": "warning"},
    ]
    
    idx1 = h1 % len(news_templates)
    idx2 = h2 % len(news_templates)
    if idx1 == idx2:
        idx2 = (idx2 + 1) % len(news_templates)
        
    return [news_templates[idx1], news_templates[idx2]]

async def update_all_news_cache_loop():
    while True:
        try:
            print("[NEWS] Updating news cache for all teams...")
            for team in TEAM_RATINGS.keys():
                try:
                    q = PORTUGUESE_TEAM_NAMES.get(team, f"Seleção de {team} de futebol")
                    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
                    async with httpx.AsyncClient() as client:
                        r = await client.get(url, timeout=10.0)
                        if r.status_code == 200:
                            root = ET.fromstring(r.content)
                            items = root.findall('.//item')
                            team_news = []
                            for item in items[:2]:
                                title = item.find('title').text
                                title_clean = re.sub(r'\\s+-\\s+[^-\\n]+$', '', title)
                                
                                title_lower = title_clean.lower()
                                if any(kw in title_lower for kw in ['lesão', 'lesionado', 'suspenso', 'suspensão', 'fora', 'desfalque']):
                                    ntype = 'warning'
                                elif any(kw in title_lower for kw in ['treino', 'titular', 'escalação', 'volta', 'escalado']):
                                    ntype = 'info'
                                else:
                                    ntype = 'success'
                                    
                                team_news.append({'title': title_clean, 'type': ntype})
                            if team_news:
                                REAL_NEWS_CACHE[team] = team_news
                except Exception as team_err:
                    pass
                await asyncio.sleep(0.1)
            print("[NEWS] News cache update complete!")
        except Exception as e:
            print(f"[NEWS] Error in loop: {e}")
        await asyncio.sleep(30 * 60)

def get_match_summary(home: str, away: str, venue: str, lh: float, la: float, fav: str) -> str:
    h_rating = get_team_rating(home)
    a_rating = get_team_rating(away)
    
    is_host = home in ['Mexico', 'USA', 'Canada']
    venue_name = venue.split(' · ')[0] if venue else "Estádio"
    
    summary = f"O confronto entre {home} e {away} promete movimentar a rodada. "
    
    if is_host:
        summary += f"Jogando sob seus domínios no {venue_name}, {home} conta com forte apoio local e vantagem de país-sede (+15% xG). "
    
    if fav == "home":
        summary += f"A IA aponta {home} como favorita para vencer, sustentada por {lh:.2f} gols esperados (xG) contra {la:.2f} do adversário. "
    elif fav == "away":
        summary += f"Mesmo como visitante, {away} detém o favoritismo estatístico, com {la:.2f} xG projetados contra {lh:.2f} do {home}. "
    else:
        summary += f"O equilíbrio impera nas projeções estatísticas (xG de {lh:.2f} vs {la:.2f}), com alta chance de empate técnico. "
        
    if h_rating['att'] > a_rating['att']:
        summary += f"O diferencial pode ser o ataque mais agressivo de {home}."
    else:
        summary += f"A defesa de {home} precisará conter o volume ofensivo de {away}."
        
    return summary

def predict_match(home: str, away: str, odds_home: float = None, odds_draw: float = None, odds_away: float = None, venue: str = None) -> Dict[str, Any]:
    \"\"\"
    Computes score probability distribution using Dixon-Coles adjusted Bivariate Poisson.
    Returns: win/draw/loss probabilities, top 3 scores, confidence, expected goals,
    suggested_score (with alternative rule), summary, news, last_results.
    \"\"\"
    lambda_home, lambda_away = calculate_lambdas(home, away, odds_home, odds_draw, odds_away, venue)
    
    prob_grid = {}
    p_home_win = 0.0
    p_draw = 0.0
    p_away_win = 0.0
    
    for x in range(7):
        for y in range(7):
            p_x = poisson_prob(x, lambda_home)
            p_y = poisson_prob(y, lambda_away)
            independent_p = p_x * p_y
            adjustment = dixon_coles_adjustment(x, y, lambda_home, lambda_away)
            prob = independent_p * adjustment
            
            prob_grid[(x, y)] = prob
            
            if x > y:
                p_home_win += prob
            elif x == y:
                p_draw += prob
            else:
                p_away_win += prob
                
    total_grid_p = sum(prob_grid.values())
    if total_grid_p > 0:
        p_home_win = (p_home_win / total_grid_p) * 100
        p_draw = (p_draw / total_grid_p) * 100
        p_away_win = (p_away_win / total_grid_p) * 100
        for k in prob_grid:
            prob_grid[k] = (prob_grid[k] / total_grid_p) * 100
            
    score_list = []
    for (x, y), prob in prob_grid.items():
        score_list.append({
            'score': f"{x}–{y}",
            'home': x,
            'away': y,
            'probability': round(prob, 1)
        })
    score_list.sort(key=lambda item: item['probability'], reverse=True)
    top_scores = score_list[:3]
    
    # Determine favored outcome
    if abs(p_home_win - p_away_win) < 6.0:
        fav_outcome = "draw"
    elif p_home_win > p_draw and p_home_win > p_away_win:
        fav_outcome = "home"
    elif p_away_win > p_draw and p_away_win > p_home_win:
        fav_outcome = "away"
    else:
        fav_outcome = "draw"
        
    # Determine tactical style
    h_rating = get_team_rating(home)
    a_rating = get_team_rating(away)
    score_potency = h_rating['att'] + a_rating['att'] - 0.5 * (h_rating['def'] + a_rating['def'])
    
    match_hash = get_deterministic_hash(home + "_" + away, 99)
    hash_bias = (match_hash % 100) / 100.0 - 0.5
    final_trend = score_potency + hash_bias
    
    if final_trend > 1.9:
        style = "ABERTO"
    elif final_trend < 1.3:
        style = "TRUNCADO"
    else:
        style = "EQUILIBRADO"
        
    # Suggested score rule
    best_score_tuple = (1, 1)
    best_score_val = -1.0
    for (x, y), prob in prob_grid.items():
        is_match = False
        if fav_outcome == "home" and x > y:
            is_match = True
        elif fav_outcome == "away" and x < y:
            is_match = True
        elif fav_outcome == "draw" and x == y:
            is_match = True
            
        if is_match:
            dist = abs(x - lambda_home) + abs(y - lambda_away)
            score_val = prob / (1.0 + 0.4 * dist)
            
            # Apply weights based on tactical style
            weight = 1.0
            if style == "ABERTO":
                if x + y >= 3:
                    weight = 1.6
                else:
                    weight = 0.4
            elif style == "TRUNCADO":
                if x + y <= 2:
                    weight = 1.6
                if x > 0 and y > 0:
                    weight *= 0.4
            else:
                pass
                
            final_val = score_val * weight
            if final_val > best_score_val:
                best_score_val = final_val
                best_score_tuple = (x, y)
                
    suggested_score = {
        'home': best_score_tuple[0],
        'away': best_score_tuple[1],
        'score': f"{best_score_tuple[0]}–{best_score_tuple[1]}"
    }
    
    model_confidence = min(max(int(top_scores[0]['probability'] * 2.5 + abs(p_home_win - p_away_win) * 0.4), 45), 95)
    
    summary = get_match_summary(home, away, venue, lambda_home, lambda_away, fav_outcome)
    news = {
        'home': get_mock_news(home),
        'away': get_mock_news(away)
    }
    last_results = {
        'home': get_mock_last_results(home),
        'away': get_mock_last_results(away)
    }
    
    return {
        'home_win_prob': round(p_home_win),
        'draw_prob': round(p_draw),
        'away_win_prob': round(p_away_win),
        'home_goals_expected': round(lambda_home, 2),
        'away_goals_expected': round(lambda_away, 2),
        'top_scores': top_scores,
        'suggested_score': suggested_score,
        'confidence': model_confidence,
        'summary': summary,
        'news': news,
        'last_results': last_results
    }

# --- MONTE CARLO SIMULATOR ---

def simulate_match_score(home: str, away: str) -> Tuple[int, int]:
    \"\"\"Simulates a match score based on Poisson expected values.\"\"\"
    lambda_home, lambda_away = calculate_lambdas(home, away)
    goals_home = 0
    goals_away = 0
    
    r_home = random.random()
    cumulative = 0.0
    for i in range(10):
        cumulative += poisson_prob(i, lambda_home)
        if r_home < cumulative:
            goals_home = i
            break
            
    r_away = random.random()
    cumulative = 0.0
    for i in range(10):
        cumulative += poisson_prob(i, lambda_away)
        if r_away < cumulative:
            goals_away = i
            break
            
    return goals_home, goals_away

def simulate_group_stage(group_teams: List[str]) -> List[Tuple[str, int, int, int]]:
    \"\"\"
    Simulates the group stage for a list of 4 teams.
    Returns sorted list: (team, points, goal_difference, goals_scored)
    \"\"\"
    stats = {team: {'pts': 0, 'gf': 0, 'ga': 0} for team in group_teams}
    
    for i in range(len(group_teams)):
        for j in range(i + 1, len(group_teams)):
            t1, t2 = group_teams[i], group_teams[j]
            g1, g2 = simulate_match_score(t1, t2)
            
            stats[t1]['gf'] += g1
            stats[t1]['ga'] += g2
            stats[t2]['gf'] += g2
            stats[t2]['ga'] += g1
            
            if g1 > g2:
                stats[t1]['pts'] += 3
            elif g1 < g2:
                stats[t2]['pts'] += 3
            else:
                stats[t1]['pts'] += 1
                stats[t2]['pts'] += 1
                
    results = []
    for team, data in stats.items():
        gd = data['gf'] - data['ga']
        results.append((team, data['pts'], gd, data['gf']))
        
    results.sort(key=lambda item: (item[1], item[2], item[3]), reverse=True)
    return results

def simulate_single_tournament() -> str:
    \"\"\"Simulates the entire World Cup 2026. Returns champion's name.\"\"\"
    group_results = {}
    for g_id, teams in GROUPS.items():
        group_results[g_id] = simulate_group_stage(teams)
        
    qualifiers = []
    third_placed = []
    
    for g_id, results in group_results.items():
        qualifiers.append(results[0][0])
        qualifiers.append(results[1][0])
        third_placed.append((results[2][0], results[2][1], results[2][2], results[2][3]))
        
    third_placed.sort(key=lambda item: (item[1], item[2], item[3]), reverse=True)
    for i in range(8):
        qualifiers.append(third_placed[i][0])
        
    random.shuffle(qualifiers)
    
    current_round = qualifiers
    while len(current_round) > 1:
        next_round = []
        for i in range(0, len(current_round), 2):
            t1 = current_round[i]
            t2 = current_round[i+1]
            g1, g2 = simulate_match_score(t1, t2)
            
            if g1 > g2:
                next_round.append(t1)
            elif g1 < g2:
                next_round.append(t2)
            else:
                rate1 = get_team_rating(t1)['fifa']
                rate2 = get_team_rating(t2)['fifa']
                prob1 = rate1 / (rate1 + rate2)
                if random.random() < prob1:
                    next_round.append(t1)
                else:
                    next_round.append(t2)
        current_round = next_round
        
    return current_round[0]

_cached_rankings = []

def run_monte_carlo(iterations: int = 5000) -> List[Dict[str, Any]]:
    \"\"\"Runs Monte Carlo simulation and returns sorted title odds.\"\"\"
    global _cached_rankings
    
    champion_counts = {team: 0 for team in TEAM_RATINGS}
    for _ in range(iterations):
        winner = simulate_single_tournament()
        if winner in champion_counts:
            champion_counts[winner] += 1
            
    rankings = []
    for team, count in champion_counts.items():
        prob = (count / iterations) * 100
        rankings.append({
            'team': team,
            'probability': round(prob, 1)
        })
        
    rankings.sort(key=lambda item: item['probability'], reverse=True)
    for idx, item in enumerate(rankings):
        item['rank'] = idx + 1
        
    _cached_rankings = rankings
    return rankings

def get_cached_rankings() -> List[Dict[str, Any]]:
    \"\"\"Returns cached rankings or runs a fast simulation if cache is empty.\"\"\"
    global _cached_rankings
    if not _cached_rankings:
        run_monte_carlo(1000)
    return _cached_rankings

def get_matches_with_predictions() -> List[Dict[str, Any]]:
    \"\"\"Returns all 72 matches with pre-calculated predictions.\"\"\"
    results = []
    for idx, m in enumerate(COPA_MATCHES):
        pred = predict_match(m['home'], m['away'], m['oh'], m['od'], m['oa'], m['venue'])
        results.append({
            'id': idx + 1,
            'group': m['group'],
            'home': m['home'],
            'away': m['away'],
            'date': m['date'],
            'time': m['time'],
            'venue': m['venue'],
            'oh': m['oh'],
            'od': m['od'],
            'oa': m['oa'],
            'status': 'SCHEDULED',
            'score': {'home': None, 'away': None},
            'prediction': pred
        })
    return results
"""


# Write it directly to the backend file!
with open(r'golcerto-backend-update (1)/golcerto-update/app/prediction_engine.py', 'w', encoding='utf-8') as out:
    out.write(final_code)

print("Restored successfully!")
