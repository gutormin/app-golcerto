with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'.{0,50}API\s*=\s*.{0,100}', content)
for m in matches:
    print(m)
