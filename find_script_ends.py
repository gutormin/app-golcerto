with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '<script>' in line:
        print(f"Script starts on line: {idx+1}")
    if '</script>' in line:
        print(f"Script ends on line: {idx+1}")
