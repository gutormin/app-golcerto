import re

# Read the extracted JS matches
with open('extracted_copa_matches_js.py', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Let's clean it up to make it a valid python list definition
# We want to add quotes to keys: home, away, group, date, time, venue, oh, od, oa
lines = js_content.split('\n')
python_matches = []

for line in lines:
    line = line.strip()
    if not line or line.startswith('//') or line.startswith('const') or line.startswith('];'):
        continue
    # Extract values using regex
    # Format: {home:'Mexico',      away:'South Africa',   group:'A', date:'11/06', time:'16:00', venue:'Azteca · Cidade do México',    oh:1.90, od:3.40, oa:3.80},
    # Let's match each key-value pair.
    # home can be single quoted or double quoted
    # oh can be float
    match_data = {}
    
    # We can use regex to extract key-values
    # For strings: key:'value' or key:"value"
    # For numbers: key:value
    pairs = re.findall(r'(\w+)\s*:\s*(?:\'([^\']*)\'|"([^"]*)"|([0-9.]+))', line)
    for pair in pairs:
        key = pair[0]
        val = pair[1] or pair[2] or pair[3]
        # if float, convert
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

# Print how many matches we found
print(f"Parsed {len(python_matches)} matches!")

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

# Format to print GROUPS and COPA_MATCHES as Python code
output = []
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

with open('copa_matches_and_groups.py', 'w', encoding='utf-8') as out:
    out.write('\n'.join(output))

print("Successfully generated copa_matches_and_groups.py")
