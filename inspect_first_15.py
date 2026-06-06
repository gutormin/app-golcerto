import json
import re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's search the log for ANY step containing the user input where the file was initially modified or uploaded.
# But wait, did the user provide the file GolCerto2026_FINAL6 (2).html as an upload/attachment, or in their workspace?
# If the file was in the workspace at the very beginning of the run (Step 0), then we wouldn't see a write_to_file for it in the transcript.
# Let's search the log for the word "GolCerto2026_FINAL6 (2).html" and see if there are messages/transcripts before Step 15.
# Let's write a script to look at the first few lines of transcript.jsonl.
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx < 15:
            try:
                data = json.loads(line)
                print(f"Index {idx}, Step {data.get('step_index')}, Type {data.get('type')}, Source {data.get('source')}")
                if 'content' in data:
                    print(data['content'][:500])
                    print("==================\n")
            except Exception as e:
                print("Err:", e)
