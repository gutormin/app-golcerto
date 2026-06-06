import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        try:
            data = json.loads(line)
            step = data.get('step_index')
            if step == 63 or idx == 63:
                print(f"FOUND Step 63 or Line 63 at line {idx}, step_index {step}")
                with open(f'step_63_raw_{idx}.json', 'w', encoding='utf-8') as out:
                    out.write(json.dumps(data, indent=2))
                print(f"Wrote step_63_raw_{idx}.json")
        except Exception as e:
            pass
