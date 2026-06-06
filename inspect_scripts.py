# Let's write a python script to inspect the script section of the original HTML file.
# We will search for all <script> tag starts and endings to find where the main javascript starts,
# so we can insert the payment logic safely inside the first script block.
with open('GolCerto2026_FINAL6_original.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = list(re.finditer(r'<script.*?>', content))
print(f"Found {len(matches)} script blocks.")
for idx, m in enumerate(matches):
    start = m.start()
    end_tag = content.find('</script>', start)
    print(f"Script block {idx}: starts at index {start}, length {end_tag - start}")
    # Print a snippet of the start of the script block
    snippet = content[start:start+200].encode('ascii', errors='replace').decode('ascii')
    print(f"  Snippet: {snippet} ...")
