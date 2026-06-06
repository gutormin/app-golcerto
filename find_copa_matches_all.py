import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'COPA_MATCHES' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                # search recursively
                def find_strings(obj):
                    res = []
                    if isinstance(obj, str):
                        if 'COPA_MATCHES' in obj:
                            res.append(obj)
                    elif isinstance(obj, dict):
                        for k, v in obj.items():
                            res.extend(find_strings(v))
                    elif isinstance(obj, list):
                        for item in obj:
                            res.extend(find_strings(item))
                    return res
                
                found_strings = find_strings(data)
                for s in found_strings:
                    if len(s) > 1000:
                        print(f"Line {idx}, Step {step}, Length {len(s)}: {s[:150]}...")
            except Exception as e:
                pass
