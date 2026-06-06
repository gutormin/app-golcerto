import hashlib

TEAM_RATINGS = {
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
}

def get_deterministic_hash(team_name: str, seed: int) -> int:
    val = f"{team_name}_{seed}"
    return int(hashlib.md5(val.encode('utf-8')).hexdigest(), 16)

for team in ['brazil', 'morocco']:
    h1 = get_deterministic_hash(team, 1)
    h2 = get_deterministic_hash(team, 2)
    h3 = get_deterministic_hash(team, 3)

    opponents = [t for t in TEAM_RATINGS.keys() if t != team]

    print(f"\n--- {team} ---")
    print("Opponent 1:", opponents[h1 % len(opponents)])
    print("Opponent 2:", opponents[h2 % len(opponents)])
    print("Opponent 3:", opponents[h3 % len(opponents)])
