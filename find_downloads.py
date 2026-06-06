import os

# Let's search C:\Users\Gustavo\Downloads for "GolCerto" or "FINAL6".
# The user might have downloaded the HTML file originally from Chrome!
print("Searching Downloads...")
downloads_dir = r'C:\Users\Gustavo\Downloads'
if os.path.exists(downloads_dir):
    for root, dirs, files in os.walk(downloads_dir):
        for f in files:
            if 'GolCerto' in f or 'FINAL6' in f:
                full = os.path.join(root, f)
                print(f"Downloads file: {full}, size {os.path.getsize(full)}")
