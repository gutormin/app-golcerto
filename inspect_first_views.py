import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's list all indices where view_file on the HTML was performed before step 1330 (which was when the check-point started).
# Or let's just find the very first view of the file in the conversation!
# At the beginning of the conversation: Step 15 viewed lines 1 to 800, Step 17 viewed lines 800 to 1206.
# Let's check the content of Step 15 (Index 14 or 15) and Step 17 (Index 16 or 17).
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx in [14, 15, 16, 17, 18, 19]:
            try:
                data = json.loads(line)
                print(f"Index {idx}, Step {data.get('step_index')}, Type {data.get('type')}, Content len {len(data.get('content', '') or '')}")
                if 'content' in data:
                    print(data['content'][:200])
                    print("...")
            except:
                pass
