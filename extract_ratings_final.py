import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx == 62:
            data = json.loads(line)
            for tc in data.get('tool_calls', []):
                args = tc.get('args', {})
                content = args.get('CodeContent', '')
                print("Content length:", len(content))
                start = content.find('TEAM_RATINGS = {')
                print("Start index:", start)
                if start != -1:
                    brace_count = 0
                    end = -1
                    for i in range(start, len(content)):
                        if content[i] == '{':
                            brace_count += 1
                        elif content[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end = i
                                break
                    print("End index:", end)
                    if end != -1:
                        print("SUCCESS!")
                        with open('extracted_ratings.py', 'w', encoding='utf-8') as out:
                            out.write(content[start:end+1])
