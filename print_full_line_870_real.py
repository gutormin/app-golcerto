import json

with open('full_line_870_code.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's decode JSON string correctly:
try:
    # If the file is literally a JSON string, let's load it
    decoded = json.loads(content)
except Exception as e:
    # If it fails, maybe it has surrounding quotes and is double escaped
    if content.startswith('"') and content.endswith('"'):
        # Parse it as a raw string literal or use json.loads
        try:
            decoded = json.loads(content)
        except Exception as e2:
            import ast
            decoded = ast.literal_eval(content)
    else:
        decoded = content

# If it is still containing literal '\n', let's evaluate or replace them
if isinstance(decoded, str):
    # If the string contains literal '\n' as backslash-n, replace it
    # But wait, python's ast.literal_eval or json.loads should have handled it.
    # Let's print out if it contains literal '\n'
    if '\\n' in decoded:
        decoded = decoded.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')

with open('full_line_870_code_real.py', 'w', encoding='utf-8') as out:
    out.write(decoded)

print("Decoded version written to full_line_870_code_real.py")
