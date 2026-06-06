with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'handleSubscribe', content)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print(content[start:end])
    print("-" * 50)
