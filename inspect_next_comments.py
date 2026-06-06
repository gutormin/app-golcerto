import re

with open('GolCerto2026_FINAL6_original.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's locate the PROFILE page
start_tag = '<!-- PAGE: PROFILE -->'
start_idx = content.find(start_tag)
if start_idx == -1:
    print("Cannot find PROFILE page")
    exit()

# Let's search for the NEXT HTML comments after start_idx.
# HTML comment pattern is <!-- ... -->
comments = []
for m in re.finditer(r'<!--(.*?)-->', content[start_idx:start_idx+10000]):
    comments.append((m.group(0), start_idx + m.start(), start_idx + m.end()))

print("Comments found within 10000 chars of PROFILE start:")
for c, s, e in comments:
    print(f"  {c} at index {s}-{e}")
