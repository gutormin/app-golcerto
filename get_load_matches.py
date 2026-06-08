with open('GolCerto2026_FINAL6_original.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read().replace('\r\n', '\n')

import re
pos = content.find('async function loadMatches()')
if pos != -1:
    with open('load_matches_def.txt', 'w', encoding='utf-8') as out:
        out.write(content[pos:pos+2500])
    print("Definition written to load_matches_def.txt")
else:
    print("loadMatches not found")
