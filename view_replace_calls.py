import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'
lines_to_view = [856, 860, 870]

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx in lines_to_view:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    print(f"--- Line {idx}, Step {step}, Tool {tc.get('name')} ---")
                    args = tc.get('args', {})
                    for k, v in args.items():
                        if k in ['ReplacementContent', 'CodeContent']:
                            print(f"{k}:")
                            print(v)
            except Exception as e:
                print("Error on line", idx, ":", e)
