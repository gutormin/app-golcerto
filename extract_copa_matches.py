import json, re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'COPA_MATCHES' in line and 'Mexico' in line and 'South Africa' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if 'COPA_MATCHES = [' in content:
                    print(f"Candidate found at line {idx}, step {data.get('step_index')}, content length {len(content)}")
                    # Clean line numbers
                    clean_lines = []
                    for l in content.split('\n'):
                        clean_lines.append(re.sub(r'^\d+:\s*', '', l))
                    clean_content = '\n'.join(clean_lines)
                    
                    # Find GROUPS and COPA_MATCHES
                    start_groups = clean_content.find('GROUPS = {')
                    start_matches = clean_content.find('COPA_MATCHES = [')
                    
                    if start_groups != -1 and start_matches != -1:
                        # Find the end of COPA_MATCHES (closing bracket)
                        # Since COPA_MATCHES is a list of dicts, we count brackets
                        bracket_count = 0
                        end_matches = -1
                        for i in range(start_matches, len(clean_content)):
                            if clean_content[i] == '[':
                                bracket_count += 1
                            elif clean_content[i] == ']':
                                bracket_count -= 1
                                if bracket_count == 0:
                                    end_matches = i
                                    break
                                    
                        if end_matches != -1:
                            print("SUCCESS! Found both GROUPS and COPA_MATCHES!")
                            with open('extracted_groups_matches.py', 'w', encoding='utf-8') as out:
                                out.write(clean_content[start_groups:end_matches+1])
                            break
            except Exception as e:
                pass
