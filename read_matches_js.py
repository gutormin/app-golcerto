with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- SECTION 1 (550-600) ---")
for i in range(549, min(600, len(lines))):
    print(f"{i+1}: {lines[i].encode('ascii', errors='replace').decode('ascii').strip()}")

print("\n--- SECTION 2 (860-920) ---")
for i in range(859, min(920, len(lines))):
    print(f"{i+1}: {lines[i].encode('ascii', errors='replace').decode('ascii').strip()}")
