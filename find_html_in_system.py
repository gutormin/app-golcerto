import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's find tool response steps. In transcript.jsonl, a tool call's output is usually in a step of type 'TOOL_OUTPUT' or 'SYSTEM_MESSAGE' or is the next step with 'source':'SYSTEM'.
# Let's find any step whose source is 'SYSTEM' and occurs immediately after a view_file tool call of GolCerto2026_FINAL6 (2).html
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        try:
            data = json.loads(line)
            step = data.get('step_index')
            # Look for system/tool output steps containing HTML content
            if data.get('source') == 'SYSTEM' and ('<!DOCTYPE html>' in line or '<html' in line or 'Partidas' in line):
                print(f"Index {idx}, Step {step}, content length: {len(data.get('content', ''))}")
        except:
            pass
