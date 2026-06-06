import json
import re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's search the log for ALL replace_file_content or multi_replace_file_content calls to GolCerto2026_FINAL6
# We want to extract each chunk and print it.
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'GolCerto2026_FINAL6' in line and ('replace_file_content' in line or 'multi_replace_file_content' in line):
            try:
                data = json.loads(line)
                step = data.get('step_index')
                for tc in data.get('tool_calls', []):
                    args = tc.get('args', {})
                    if 'GolCerto2026_FINAL6' in args.get('TargetFile', ''):
                        if 'ReplacementContent' in args:
                            print(f"Step {step}, Tool {tc.get('name')}, Start {args.get('StartLine')}, End {args.get('EndLine')}, Target len: {len(args.get('TargetContent', ''))}, Replacement len: {len(args.get('ReplacementContent', ''))}")
                        elif 'ReplacementChunks' in args:
                            print(f"Step {step}, Tool {tc.get('name')}, chunks count: {len(args.get('ReplacementChunks', []))}")
                            for chunk in args.get('ReplacementChunks', []):
                                print(f"  Chunk: Start {chunk.get('StartLine')}, End {chunk.get('EndLine')}, Target len: {len(chunk.get('TargetContent', ''))}, Replacement len: {len(chunk.get('ReplacementContent', ''))}")
            except:
                pass
