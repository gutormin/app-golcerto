import re
import json

with open('extracted_copa_matches_js.py', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace escaped quotes inside venue names
js_content_clean = js_content.replace("\\'", "''").replace("'", '"')

# Now let's parse using regex
# We want to match: key: "value" or key: value
lines = js_content_clean.split('\n')
python_matches = []

for line in lines:
    line = line.strip()
    if not line or line.startswith('//') or line.startswith('const') or line.startswith('];'):
        continue
    
    match_data = {}
    # Find all matches of key : "value" or key : float
    pairs = re.findall(r'(\w+)\s*:\s*(?:"([^"]*)"|([0-9.]+))', line)
    for pair in pairs:
        key = pair[0]
        val = pair[1] or pair[2]
        
        # Restore double single-quotes to single quote
        if isinstance(val, str):
            val = val.replace("''", "'")
            
        try:
            if '.' in val:
                val = float(val)
            else:
                val = int(val)
        except ValueError:
            pass
        match_data[key] = val
        
    if match_data:
        python_matches.append(match_data)

print(f"Parsed {len(python_matches)} matches successfully!")

# Construct GROUPS dict
groups = {}
for m in python_matches:
    g = m.get('group')
    h = m.get('home')
    a = m.get('away')
    if g not in groups:
        groups[g] = []
    if h not in groups[g]:
        groups[g].append(h)
    if a not in groups[g]:
        groups[g].append(a)

# Generate output python code
output = []
output.append("import math")
output.append("import random")
output.append("import hashlib")
output.append("import re")
output.append("import urllib.parse")
output.append("import xml.etree.ElementTree as ET")
output.append("import httpx")
output.append("import asyncio")
output.append("from typing import Dict, List, Tuple, Any\n")

output.append("# Group composition for World Cup 2026")
output.append("GROUPS = {")
for g in sorted(groups.keys()):
    output.append(f"    '{g}': {groups[g]},")
output.append("}\n")

output.append("# Full list of 72 group stage matches")
output.append("COPA_MATCHES = [")
for m in python_matches:
    output.append(f"    {repr(m)},")
output.append("]")

with open('copa_matches_and_groups_fixed.py', 'w', encoding='utf-8') as out:
    out.write('\n'.join(output))

print("Successfully wrote copa_matches_and_groups_fixed.py")
