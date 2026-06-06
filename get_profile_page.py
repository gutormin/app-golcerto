with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'<div[^>]+class="page"[^>]*id="page-profile"', content)
for m in matches:
    start = m.start()
    # find matching closing div
    div_count = 0
    end = -1
    for i in range(start, len(content)):
        if content[i:i+4] == '<div':
            div_count += 1
        elif content[i:i+5] == '</div':
            div_count -= 1
            if div_count == 0:
                end = i + 6
                break
    if end != -1:
        with open('profile_page_content.html', 'w', encoding='utf-8') as out:
            out.write(content[start:end])
        print("Wrote profile_page_content.html")
