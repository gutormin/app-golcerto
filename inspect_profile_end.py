# Let's inspect profile_page_original_raw.html content around line 43 to find where the page-profile ends.
# Since it is a small file, let's view its content. Wait, we can write a python script to search for the ending
# pattern of page-profile div.
# In profile_page_original_raw.html, let's look for how it ends or if it has another sub-cta or page-profile content.
with open('profile_page_original_raw.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in profile_page_original_raw.html: {len(lines)}")
for idx, line in enumerate(lines[-20:]):
    print(f"{len(lines) - 20 + idx + 1}: {line.strip()}")
