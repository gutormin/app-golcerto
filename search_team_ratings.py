import json, re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'TEAM_RATINGS' in line and 'Brazil' in line and 'att' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if 'TEAM_RATINGS' in content:
                    print(f"Found match on line {idx}, step_index {data.get('step_index')}")
                    # Let's clean the line numbers from content
                    # The lines look like '12: TEAM_RATINGS = {'
                    clean_lines = []
                    for line in content.split('\\n'):
                        # Remove prefix like '12: '
                        clean_line = re.sub(r'^\\d+:\\s*', '', line)
                        clean_lines.append(clean_line)
                    clean_content = '\\n'.join(clean_lines)
                    
                    start = clean_content.find('TEAM_RATINGS = {')
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
                    if start != -1 and end != -1:
                        ratings = clean_content[start:end+1]
                        print("Extracted TEAM_RATINGS!")
                        with open('extracted_ratings.py', 'w', encoding='utf-8') as out:
                            out.write(ratings)
                        break
            except Exception as e:
                print("Error parsing line:", e)
