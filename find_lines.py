with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'loadStats()' in line:
            print(f"{idx}: {line.strip()}")
