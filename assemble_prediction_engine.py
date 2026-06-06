import re

# Let's read the JS matches file
with open('extracted_copa_matches_js.py', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace Levi\'s with Levi s to avoid single quote parsing issues
js_content_clean = js_content.replace("Levi\\'s", "Levi s").replace("Levi's", "Levi s")

# Replace single quotes with double quotes for easy parsing
# But let's be careful: only replace quotes that are not inside strings.
# A simpler way: we know it is a list of dicts.
# Let's parse each line using a regex that extracts values specifically.
lines = js_content_clean.split('\n')
python_matches = []

for line in lines:
    line = line.strip()
    if not line or line.startswith('//') or line.startswith('const') or line.startswith('];'):
        continue
    
    # Extract values. Examples:
    # {home:'Mexico',      away:'South Africa',   group:'A', date:'11/06', time:'16:00', venue:'Azteca · Cidade do México',    oh:1.90, od:3.40, oa:3.80},
    # Let's find home, away, group, date, time, venue, oh, od, oa
    home_match = re.search(r"home\s*:\s*['\"]([^'\"]+)['\"]", line)
    away_match = re.search(r"away\s*:\s*['\"]([^'\"]+)['\"]", line)
    group_match = re.search(r"group\s*:\s*['\"]([^'\"]+)['\"]", line)
    date_match = re.search(r"date\s*:\s*['\"]([^'\"]+)['\"]", line)
    time_match = re.search(r"time\s*:\s*['\"]([^'\"]+)['\"]", line)
    venue_match = re.search(r"venue\s*:\s*['\"]([^'\"]+)['\"]", line)
    
    oh_match = re.search(r"oh\s*:\s*([0-9.]+)", line)
    od_match = re.search(r"od\s*:\s*([0-9.]+)", line)
    oa_match = re.search(r"oa\s*:\s*([0-9.]+)", line)
    
    if home_match and away_match:
        m = {
            'home': home_match.group(1),
            'away': away_match.group(1),
            'group': group_match.group(1) if group_match else '',
            'date': date_match.group(1) if date_match else '',
            'time': time_match.group(1) if time_match else '',
            'venue': venue_match.group(1) if venue_match else '',
            'oh': float(oh_match.group(1)) if oh_match else 1.0,
            'od': float(od_match.group(1)) if od_match else 1.0,
            'oa': float(oa_match.group(1)) if oa_match else 1.0
        }
        python_matches.append(m)

print(f"Parsed {len(python_matches)} matches successfully!")

# Construct GROUPS dict
groups = {}
for m in python_matches:
    g = m.get('group')
    h = m.get('home')
    a = m.get('away')
    if g not in groups:
        groups[g] = []
    if h not in groups[g]:
        groups[g].append(h)
    if a not in groups[g]:
        groups[g].append(a)

# Now, let's load the current content of golcerto-backend-update (1)/golcerto-update/app/prediction_engine.py
with open(r'golcerto-backend-update (1)/golcerto-update/app/prediction_engine.py', 'r', encoding='utf-8') as f:
    orig_code = f.read()

# Let's write the new prediction_engine.py.
# We will construct it carefully with all the correct structures.
new_code = []

# 1. Imports
new_code.append("""import math
import random
import hashlib
import re
import urllib.parse
import xml.etree.ElementTree as ET
import httpx
import asyncio
from typing import Dict, List, Tuple, Any
""")

# 2. TEAM_RATINGS (we keep the original TEAM_RATINGS)
# Let's extract TEAM_RATINGS from orig_code
ratings_match = re.search(r'TEAM_RATINGS\s*=\s*\{.*?\n\}', orig_code, re.DOTALL)
if ratings_match:
    new_code.append(ratings_match.group(0))
else:
    raise Exception("Could not find TEAM_RATINGS in original code!")

new_code.append("\nDEFAULT_TEAM = {'att': 1.00, 'def': 1.20, 'fifa': 1300}\n")

# 3. GROUPS and COPA_MATCHES
new_code.append("# Group composition for World Cup 2026")
new_code.append("GROUPS = {")
for g in sorted(groups.keys()):
    new_code.append(f"    '{g}': {groups[g]},")
new_code.append("}\n")

new_code.append("# Full list of 72 group stage matches")
new_code.append("COPA_MATCHES = [")
for m in python_matches:
    new_code.append(f"    {repr(m)},")
new_code.append("]\n")

# 4. PORTUGUESE_TEAM_NAMES and REAL_NEWS_CACHE
names_match = re.search(r'PORTUGUESE_TEAM_NAMES\s*=\s*\{.*?\n\}', orig_code, re.DOTALL)
if names_match:
    new_code.append(names_match.group(0))
else:
    raise Exception("Could not find PORTUGUESE_TEAM_NAMES in original code!")

new_code.append("\nREAL_NEWS_CACHE = {}\n")

# 5. REAL_LAST_RESULTS
results_match = re.search(r'REAL_LAST_RESULTS\s*=\s*\{.*?\n\}', orig_code, re.DOTALL)
if results_match:
    new_code.append(results_match.group(0))
else:
    raise Exception("Could not find REAL_LAST_RESULTS in original code!")

# 6. Helper functions: get_deterministic_hash, get_team_rating, poisson_prob, calculate_lambdas, dixon_coles_adjustment
new_code.append("""
def get_deterministic_hash(team_name: str, seed: int) -> int:
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
""")

# 7. Scraper functions: get_mock_last_results, get_mock_news, update_all_news_cache_loop
new_code.append("""
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
""")

# 8. Remaining logic from original file (get_match_summary, predict_match, Monte Carlo functions)
# Let's find get_match_summary onwards in the original code
summary_idx = orig_code.find('def get_match_summary')
if summary_idx != -1:
    new_code.append(orig_code[summary_idx:])
else:
    raise Exception("Could not find get_match_summary onwards in original code!")

# Save to the actual backend file!
output_path = r'golcerto-backend-update (1)/golcerto-update/app/prediction_engine.py'
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(new_code))

print("Successfully assembled and updated prediction_engine.py!")
