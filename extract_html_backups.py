import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        # We want to see all write_to_file calls to GolCerto2026_FINAL6 (2).html
        if 'GolCerto2026_FINAL6' in line and 'write_to_file' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                for tc in data.get('tool_calls', []):
                    args = tc.get('args', {})
                    dest = args.get('TargetFile', '')
                    if 'GolCerto2026_FINAL6' in dest and tc.get('name') == 'write_to_file':
                        content = args.get('CodeContent', '')
                        print(f"Line {idx}, Step {step}, content len: {len(content)}")
                        # Write it to a file
                        out_path = f"backup_step_{step}.html"
                        with open(out_path, 'w', encoding='utf-8') as out_f:
                            out_f.write(content)
                        print(f"Saved to {out_path}")
            except Exception as e:
                print("Err:", e)
