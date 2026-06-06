with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "REAL_LAST_RESULTS" or "last_results" or "Congo DR" or "Cape Verde" or "Belgium" inside script tags
import re
matches = re.findall(r'<script>.*?</script>', content, re.DOTALL)
print(f"Found {len(matches)} script tags.")
for idx, m in enumerate(matches):
    for word in ['Congo DR', 'Cape Verde', 'Belgium', 'REAL_LAST_RESULTS']:
        if word in m:
            print(f"Script tag {idx} contains '{word}'!")
            # print context around the word
            pos = m.find(word)
            print(m[max(0, pos-200):min(len(m), pos+300)])
            print("-" * 50)
