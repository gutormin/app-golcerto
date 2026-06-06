import json
import os

# Let's search Conversation 84117c73-21d3-4d22-935c-ed7d032fea89 or fad9d7f4-adb0-48e2-9088-083ecd252cea for "GolCerto2026_FINAL6 (2).html" writes.
convs = ['84117c73-21d3-4d22-935c-ed7d032fea89', 'fad9d7f4-adb0-48e2-9088-083ecd252cea']

for c in convs:
    log_path = f'C:\\Users\\Gustavo\\.gemini\\antigravity\\brain\\{c}\\.system_generated\\logs\\transcript.jsonl'
    if not os.path.exists(log_path):
        continue
    print(f"\nChecking {c}...")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f):
            if 'GolCerto2026_FINAL6' in line and 'write_to_file' in line:
                try:
                    data = json.loads(line)
                    step = data.get('step_index')
                    for tc in data.get('tool_calls', []):
                        args = tc.get('args', {})
                        if 'GolCerto2026_FINAL6' in args.get('TargetFile', ''):
                            print(f"  Line {idx}, Step {step}, content len: {len(args.get('CodeContent', ''))}")
                except Exception as e:
                    pass
