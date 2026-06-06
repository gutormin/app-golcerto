import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'prediction_engine.py' in line and ('write_to_file' in line or 'replace_file_content' in line):
            try:
                data = json.loads(line)
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    args = tc.get('args', {})
                    # Let's check CodeContent or ReplacementContent
                    content = args.get('CodeContent', '') or args.get('ReplacementContent', '')
                    if 'TEAM_RATINGS = {' in content:
                        print(f"Found TEAM_RATINGS in tool call at line {idx}, step {data.get('step_index')}")
                        start = content.find('TEAM_RATINGS = {')
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
                        if end != -1:
                            print("Successfully extracted full TEAM_RATINGS from tool call arguments!")
                            with open('extracted_ratings.py', 'w', encoding='utf-8') as out:
                                out.write(content[start:end+1])
                            break
            except Exception as e:
                print("Err:", e)
