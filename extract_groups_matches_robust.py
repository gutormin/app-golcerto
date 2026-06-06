import json, re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's read all lines and find where COPA_MATCHES is present
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'COPA_MATCHES' in line and 'Mexico' in line and 'South Africa' in line:
            try:
                data = json.loads(line)
                content = data.get('content', '') or str(data.get('tool_calls', ''))
                # Let's search for GROUPS inside the content
                # The content might have newline characters escaped as \\n or \n
                content_unescaped = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'")
                
                # Check if both GROUPS and COPA_MATCHES are in unescaped content
                if 'GROUPS = {' in content_unescaped and 'COPA_MATCHES = [' in content_unescaped:
                    print(f"Found on line {idx}, step_index {data.get('step_index')}")
                    start_groups = content_unescaped.find('GROUPS = {')
                    start_matches = content_unescaped.find('COPA_MATCHES = [')
                    
                    # Count brackets to find the end of COPA_MATCHES list
                    bracket_count = 0
                    end_matches = -1
                    for i in range(start_matches, len(content_unescaped)):
                        if content_unescaped[i] == '[':
                            bracket_count += 1
                        elif content_unescaped[i] == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                end_matches = i
                                break
                    if end_matches != -1:
                        print("SUCCESSFULLY EXTRACTED!")
                        with open('extracted_groups_matches.py', 'w', encoding='utf-8') as out:
                            out.write(content_unescaped[start_groups:end_matches+1])
                        break
            except Exception as e:
                print("Err:", e)
