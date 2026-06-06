# Let's print the last few lines of profile_page_original_raw.html safely by replacing any unicode characters.
with open('profile_page_original_raw.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in profile_page_original_raw.html: {len(lines)}")
for idx, line in enumerate(lines[-20:]):
    safe_line = line.strip().encode('ascii', errors='replace').decode('ascii')
    print(f"{len(lines) - 20 + idx + 1}: {safe_line}")
