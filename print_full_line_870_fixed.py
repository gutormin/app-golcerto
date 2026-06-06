import json

with open('full_line_870_code.py', 'r', encoding='utf-8') as f:
    content = f.read().strip()

# If it is wrapped in double quotes as a JSON string, let's load it
if content.startswith('"') and content.endswith('"'):
    try:
        decoded = json.loads(content)
    except Exception as e:
        # Try wrapping it in brackets or object to see if it's a valid JSON fragment
        try:
            decoded = json.loads(f"[{content}]")[0]
        except Exception as e2:
            print("Failed loading as JSON:", e, e2)
            decoded = eval(content) # Fallback to eval since it is a python string literal in json
else:
    decoded = content

with open('full_line_870_code_fixed.py', 'w', encoding='utf-8') as out:
    out.write(decoded)

print("Decoded version written to full_line_870_code_fixed.py")
