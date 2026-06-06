with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'id="page-profile"' in line:
        print(f"Starts on line: {idx+1}")
    if '<!-- VALUE PROPOSITION / FAQ -->' in line:
        print(f"FAQ starts on line: {idx+1}")
    if 'id="page-stats"' in line or 'page-alerts' in line:
        print(f"Next page starts on line: {idx+1}")
