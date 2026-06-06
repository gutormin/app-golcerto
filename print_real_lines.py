with open('full_line_870_code_real.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines[:100]):
    print(f"{idx+1}: {line}", end='')
