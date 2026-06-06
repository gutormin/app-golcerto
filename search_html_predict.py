with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "function predict" or "predictMatch" or "poisson" in the HTML
for word in ['predict', 'Poisson', 'Dixon', 'calculate', 'hash', 'mock']:
    count = content.count(word)
    print(f"Occurrence of '{word}': {count}")
    if count > 0 and len(word) > 4:
        idx = content.find(word)
        print(f"Context of '{word}': {content[max(0, idx-50):min(len(content), idx+150)]}")
        print("-" * 50)
