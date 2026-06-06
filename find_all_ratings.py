import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'TEAM_RATINGS' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                tool_calls = data.get('tool_calls', [])
                args_len = 0
                for tc in tool_calls:
                    args_len = max(args_len, len(tc.get('args', {}).get('CodeContent', '') or tc.get('args', {}).get('ReplacementContent', '')))
                print(f"Line {idx}, step_index {data.get('step_index')}, type {data.get('type')}, content len {len(content)}, args len {args_len}")
            except Exception as e:
                pass
