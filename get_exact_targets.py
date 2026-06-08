with open('GolCerto2026_FINAL6_original.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read().replace('\r\n', '\n')

prefixes = {
    'score_vars': "const hw = pred ? pred.home_win_prob : '–';",
    'match_card_render_start': "const top3HTML = top.length ? `",
    'header_actions': '<div class="header-actions">'
}

for name, prefix in prefixes.items():
    pos = content.find(prefix)
    if pos != -1:
        print(f"=== {name} EXACT CONTENT ===")
        print(content[pos:pos+500])
        print("="*40)
    else:
        print(f"Prefix not found for {name}")
