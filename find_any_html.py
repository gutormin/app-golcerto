import os

# Let's search C:\Users\Gustavo\Downloads or C:\Users\Gustavo\.gemini\antigravity\scratch\ recursively for any HTML files that might have been the original file or a copy!
for root, dirs, files in os.walk(r'C:\Users\Gustavo\.gemini\antigravity\scratch'):
    for f in files:
        if 'GolCerto' in f or f.endswith('.html'):
            full = os.path.join(root, f)
            print(f"Found: {full}, size: {os.path.getsize(full)}")
