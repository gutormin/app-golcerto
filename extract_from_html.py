import re

html_path = r'C:\Users\Gustavo\.gemini\antigravity\scratch\gol certo\GolCerto2026_FINAL6 (2).html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find const COPA_MATCHES = [ ... ]
match = re.search(r'const\s+COPA_MATCHES\s*=\s*\[(.*?)\];', content, re.DOTALL)
if match:
    copa_matches_str = match.group(0)
    print("Found COPA_MATCHES in HTML!")
    with open('extracted_copa_matches_js.py', 'w', encoding='utf-8') as out:
        out.write(copa_matches_str)
else:
    print("COPA_MATCHES not found in HTML!")

# Let's search for GROUPS in HTML as well
groups_match = re.search(r'const\s+GROUPS\s*=\s*\{.*?\};', content, re.DOTALL)
if groups_match:
    groups_str = groups_match.group(0)
    print("Found GROUPS in HTML!")
    with open('extracted_groups_js.py', 'w', encoding='utf-8') as out:
        out.write(groups_str)
else:
    # Let's find any object mapping group letters
    groups_match2 = re.search(r'groups\s*=\s*\{.*?\}', content, re.IGNORECASE | re.DOTALL)
    if groups_match2:
        print("Found groups object variant in HTML!")
        print(groups_match2.group(0)[:200])
