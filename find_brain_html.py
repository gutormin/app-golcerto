import os

# Let's list files in the appDataDir brain directories to see if any conversation has an artifact folder or something.
# The artifacts are saved under C:\Users\Gustavo\.gemini\antigravity\brain\<conversation-id>
# Let's check if there are other files in the brain/<conv-id> directories recursively.
for root, dirs, files in os.walk(r'C:\Users\Gustavo\.gemini\antigravity\brain'):
    for f in files:
        if 'GolCerto' in f or f.endswith('.html'):
            full = os.path.join(root, f)
            print(f"Found html/golcerto in brain: {full}, size {os.path.getsize(full)}")
