import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'GolCerto2026_FINAL6' in line and 'view_file' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    name = tc.get('name', '')
                    args = tc.get('args', {})
                    dest = args.get('AbsolutePath', '')
                    if 'GolCerto2026_FINAL6' in dest:
                        print(f"Line {idx}, Step {step}, Tool {name}, Dest {dest}, StartLine {args.get('StartLine')}, EndLine {args.get('EndLine')}")
            except Exception as e:
                pass
