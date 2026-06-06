import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 841 < idx < 885:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                tool_calls = data.get('tool_calls', [])
                tools_str = ", ".join([tc.get('name', '') for tc in tool_calls])
                print(f"Line {idx}, Step {step}, Source {data.get('source')}, Type {data.get('type')}, Tools: {tools_str}")
            except Exception as e:
                pass
