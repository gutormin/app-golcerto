with open('GolCerto2026_FINAL6 (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find('// Premium / VIP subscription simulator logic')
if pos != -1:
    print("Insertion context:")
    print(content[max(0, pos-400):min(len(content), pos+800)])
else:
    print("Could not find the comment in HTML!")
