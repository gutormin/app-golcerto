import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's inspect step 1351. Index 1344 is the PLANNER_RESPONSE.
# The tool output might be at Index 1345 or 1346 or 1347. Let's list indexes 1340 to 1355.
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 1340 <= idx <= 1360 or 1385 <= idx <= 1405:
            try:
                data = json.loads(line)
                print(f"Index {idx}, Step {data.get('step_index')}, Source {data.get('source')}, Type {data.get('type')}, content len {len(data.get('content', '') or '')}")
            except Exception as e:
                print("Err:", e)
