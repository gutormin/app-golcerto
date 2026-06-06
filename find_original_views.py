import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's search the log for the first view_file tool output where StartLine is 1 and EndLine is 800 (or not specified) or similar,
# or let's search for "Total Bytes: 1503693" to find the last complete view of the file.
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if '1503693' in line:
            try:
                data = json.loads(line)
                print(f"FOUND 1503693 at Index {idx}, Step {data.get('step_index')}, len: {len(data.get('content', ''))}")
            except:
                pass
