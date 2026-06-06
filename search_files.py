import os

root_dir = r'C:\Users\Gustavo\.gemini\antigravity\scratch\gol certo'
target = 'update_all_news_cache'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.py') or filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if target in content:
                        print(f"Found '{target}' in file: {filepath}")
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
