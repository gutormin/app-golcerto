with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'async\s+function\s+loadMatches', content)
for m in matches:
    start = m.start()
    # find ending brace of loadMatches
    brace_count = 0
    end = -1
    for i in range(start, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i
                break
    if end != -1:
        with open('load_matches_impl.js', 'w', encoding='utf-8') as out:
            out.write(content[start:end+1])
        print("Wrote load_matches_impl.js")
