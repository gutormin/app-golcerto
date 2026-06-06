import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'GolCerto2026_FINAL6' in line:
            if 'USER_INPUT' in line or 'USER_EXPLICIT' in line:
                continue
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    name = tc.get('name', '')
                    args = tc.get('args', {})
                    dest = args.get('TargetFile', '')
                    if 'GolCerto2026_FINAL6' in dest:
                        print(f"Line {idx}, Step {step}, Tool {name}, Dest {dest}")
            except Exception as e:
                pass
