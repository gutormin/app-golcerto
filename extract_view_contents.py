import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's search for lines containing 'replace_file_content' or 'multi_replace_file_content'
# on 'GolCerto2026_FINAL6 (2).html' and extract their targets and replacements.
# Let's reconstruct the file step-by-step from the start of the logs!
# But wait, we can also see if there's any file view tool call that viewed the whole file.
# Yes, Step 15 viewed lines 1 to 800, Step 17 viewed lines 800 to 1206.
# Let's check how many lines the file originally had. 
# Step 17 shows EndLine 1206.
# Let's write a script to build a version of the HTML from the view_file tool output or by applying the replacements.
# Let's extract all view_file contents of the HTML from the logs!
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'view_file' in line and 'GolCerto2026_FINAL6' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index')
                # A view_file response comes from the SYSTEM or the output of the tool.
                # In transcript.jsonl, a tool output step has type "TOOL_OUTPUT" or similar, or the next line contains the system response.
                print(f"Step {step} had view_file call")
            except:
                pass
