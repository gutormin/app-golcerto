import re

with open('GolCerto2026_FINAL6_original.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's locate the PROFILE page
start_tag = '<!-- PAGE: PROFILE -->'
start_idx = content.find(start_tag)
if start_idx == -1:
    print("Cannot find PROFILE page")
    exit()

# Let's search for the next page or section marker:
# <div class="bottom-nav"> is typically at the end of the body, let's see.
# Let's search for the first occurrence of '<script>' or 'class="bottom-nav"' after start_idx.
script_idx = content.find('<script>', start_idx)
print("Index of next <script> after PROFILE:", script_idx)

# Let's print out the text between start_idx and script_idx by writing to a file (to avoid console unicode error)
with open('profile_page_original_raw.html', 'w', encoding='utf-8') as f:
    f.write(content[start_idx:script_idx])
print("Wrote profile_page_original_raw.html")
