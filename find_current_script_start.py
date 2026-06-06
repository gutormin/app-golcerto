with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '<script' in line:
        print(f"Script tag at line {idx+1}: {line.strip()}")
    if 'renderProfile' in line or 'function render' in line:
        print(f"Render function at line {idx+1}: {line.strip()}")
