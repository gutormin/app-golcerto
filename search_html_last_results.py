with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'last_results', content)
for m in matches:
    start = max(0, m.start() - 150)
    end = min(len(content), m.end() + 250)
    print(content[start:end])
    print("="*60)
