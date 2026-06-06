import json
import re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's collect ALL view_file tool output fragments for GolCerto2026_FINAL6 (2).html
# and reconstruct the lines. We want to see what is missing.
# Let's print out the exact line numbers we have and check if we have any overlapping or mismatched content.
# Also, let's write out the reconstructed file as best as we can, leaving "MISSING" markers for missing lines.
lines_dict = {}

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'view_file' in line or 'VIEW_FILE' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if not content or 'Total Lines:' not in content:
                    continue
                # Parse lines
                for l in content.splitlines():
                    m = re.match(r'^(\d+): (.*)$', l)
                    if m:
                        ln = int(m.group(1))
                        val = m.group(2)
                        lines_dict[ln] = val
            except:
                pass

if not lines_dict:
    print("No lines found!")
    exit()

max_ln = max(lines_dict.keys())
print(f"Max line number: {max_ln}")

# Write reconstructed file
with open('reconstructed_temp.html', 'w', encoding='utf-8') as out:
    for i in range(1, max_ln + 1):
        if i in lines_dict:
            out.write(lines_dict[i] + '\n')
        else:
            out.write(f"<!-- MISSING LINE {i} -->\n")

print("Wrote reconstructed_temp.html")
