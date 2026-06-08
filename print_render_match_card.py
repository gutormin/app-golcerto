import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/Gustavo/.gemini/antigravity/scratch/gol certo/GolCerto2026_FINAL6 (2).html", "r", encoding="utf-8") as f:
    lines = f.readlines()

found = False
for idx, line in enumerate(lines):
    if "function renderMatchCard" in line:
        found = True
        start_line = idx + 1
        break

if found:
    print(f"Found renderMatchCard starting at line {start_line}")
    # Print 200 lines from start_line
    for i in range(start_line - 1, start_line + 250):
        if i < len(lines):
            print(f"{i+1}: {lines[i]}", end="")
else:
    print("Not found")
