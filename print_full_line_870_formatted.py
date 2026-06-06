with open('full_line_870_code.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's clean the string (it is double-json-encoded or similar)
import json
try:
    decoded = json.loads(content)
except:
    # If it is raw, maybe just print it
    decoded = content

with open('full_line_870_code_formatted.py', 'w', encoding='utf-8') as out:
    out.write(decoded)

print("Formatted version written to full_line_870_code_formatted.py")
