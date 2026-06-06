import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'COPA_MATCHES' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                # Let's inspect the entire dict recursively for any string containing COPA_MATCHES
                def find_string_with_matches(obj):
                    if isinstance(obj, str):
                        if 'COPA_MATCHES =' in obj or 'COPA_MATCHES =' in obj.replace(' ', ''):
                            return obj
                    elif isinstance(obj, dict):
                        for k, v in obj.items():
                            res = find_string_with_matches(v)
                            if res:
                                return res
                    elif isinstance(obj, list):
                        for item in obj:
                            res = find_string_with_matches(item)
                            if res:
                                return res
                    return None
                
                content = find_string_with_matches(data)
                if content:
                    print(f"Found on line {idx}, step {step}, content length {len(content)}")
                    if 'GROUPS =' in content:
                        print("Found GROUPS too!")
                        # Write to extracted_groups_matches.py
                        with open('extracted_groups_matches.py', 'w', encoding='utf-8') as out:
                            out.write(content)
                        print("Successfully wrote extracted_groups_matches.py")
                        break
            except Exception as e:
                print(f"Error parsing line {idx}: {e}")
