import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's inspect step 1351 or 1391 which are very recent views of the HTML file.
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if '1391' in line or '1393' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index')
                # Let's print out some information about the step
                print(f"Index {idx}, Step {step}, Type {data.get('type')}, Source {data.get('source')}")
                if 'content' in data:
                    print(f"Content length: {len(data['content'])}")
            except:
                pass
