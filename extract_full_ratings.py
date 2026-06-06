import json, re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

import json, re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'TEAM_RATINGS' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if 'TEAM_RATINGS' in content and 'Brazil' in content:
                    print(f"Candidate step {data.get('step_index')}")
                    # Clean line numbers
                    clean_lines = []
                    for l in content.split('\n'):
                        clean_lines.append(re.sub(r'^\d+:\s*', '', l))
                    clean_content = '\n'.join(clean_lines)
                    
                    start = clean_content.find('TEAM_RATINGS = {')
                    if start != -1:
                        brace_count = 0
                        end = -1
                        for i in range(start, len(clean_content)):
                            if clean_content[i] == '{':
                                brace_count += 1
                            elif clean_content[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    end = i
                                    break
                        if end != -1:
                            print(f"Success! Extracted from line {idx}, step {data.get('step_index')}")
                            with open('extracted_ratings.py', 'w', encoding='utf-8') as out:
                                out.write(clean_content[start:end+1])
                            break
            except Exception as e:
                pass
