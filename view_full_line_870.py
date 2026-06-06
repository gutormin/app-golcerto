import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'
line_to_view = 870

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx == line_to_view:
            try:
                data = json.loads(line)
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    args = tc.get('args', {})
                    code = args.get('CodeContent', '')
                    with open('full_line_870_code.py', 'w', encoding='utf-8') as out:
                        out.write(code)
                    print("Successfully wrote full code of line 870 to full_line_870_code.py")
            except Exception as e:
                print("Error:", e)
            break
