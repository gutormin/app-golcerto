with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total content length: {len(content)}")
import re
for m in re.finditer(r'script', content, re.IGNORECASE):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print(f"Word 'script' found at index {m.start()}:")
    print(content[start:end].strip())
    print("-" * 50)
    if m.start() > 10000:  # limit output
        break
