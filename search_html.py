with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for Congo DR or Cape Verde or Belgium in HTML
for word in ['Congo DR', 'Cape Verde', 'Morocco', 'last_results', 'lastResults', 'historico']:
    count = content.count(word)
    print(f"Occurrence of '{word}': {count}")
    if count > 0 and len(word) > 5:
        # print first match context
        idx = content.find(word)
        print(f"Context of '{word}': {content[max(0, idx-100):min(len(content), idx+200)]}")
        print("-" * 50)
