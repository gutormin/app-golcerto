import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'
line_to_extract = 27

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx == line_to_extract:
            try:
                data = json.loads(line)
                with open('extracted_log_line.txt', 'w', encoding='utf-8') as out:
                    out.write(json.dumps(data, indent=2))
                print(f"Successfully wrote line {line_to_extract} to extracted_log_line.txt")
            except Exception as e:
                print("Error:", e)
            break
