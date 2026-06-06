import json
import re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's write a script to extract all view_file calls for 'GolCerto2026_FINAL6 (2).html'
# and print out the range of lines they cover. Let's see which steps actually returned the views.
# We will inspect steps that have source = 'SYSTEM' or type = 'VIEW_FILE' or type = 'TOOL_OUTPUT'
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'GolCerto2026_FINAL6' in line and ('view_file' in line or 'VIEW_FILE' in line):
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                # Let's print the line index, step index, type, source, and if there is a StartLine / EndLine in tool_calls
                tc_info = ""
                for tc in data.get('tool_calls', []):
                    args = tc.get('args', {})
                    tc_info += f" range: {args.get('StartLine')}-{args.get('EndLine')}"
                
                content_snippet = ""
                content = data.get('content', '')
                if content:
                    lines = content.splitlines()
                    content_snippet = f" lines in content: {len(lines)}"
                    # check if it contains line numbers
                    lns = [int(re.match(r'^(\d+):', l).group(1)) for l in lines if re.match(r'^(\d+):', l)]
                    if lns:
                        content_snippet += f" (range {min(lns)}-{max(lns)})"
                
                print(f"Line {idx}, Step {step}, Type {data.get('type')}, Source {data.get('source')}{tc_info}{content_snippet}")
            except Exception as e:
                pass
