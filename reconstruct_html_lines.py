import json
import re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

lines_dict = {}

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'view_file' in line or 'VIEW_FILE' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if not content:
                    continue
                # Parse lines
                for l in content.splitlines():
                    # Look for line numbers
                    m = re.match(r'^(\d+): (.*)$', l)
                    if m:
                        ln = int(m.group(1))
                        val = m.group(2)
                        lines_dict[ln] = val
            except Exception as e:
                pass

print(f"Collected {len(lines_dict)} unique lines from VIEW_FILE steps.")
if lines_dict:
    max_ln = max(lines_dict.keys())
    print(f"Max line number: {max_ln}")
    missing = []
    current_missing_start = None
    for i in range(1, max_ln + 1):
        if i not in lines_dict:
            if current_missing_start is None:
                current_missing_start = i
        else:
            if current_missing_start is not None:
                missing.append((current_missing_start, i - 1))
                current_missing_start = None
    if current_missing_start is not None:
        missing.append((current_missing_start, max_ln))
    print("Missing line ranges:", missing)
