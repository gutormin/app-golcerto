import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's write a python script to apply the logged edits sequentially to GolCerto2026_FINAL6_original.html.
# Note that in multi_replace_file_content, sometimes ReplacementChunks might be stored as a serialized JSON string
# or is a list. Let's handle both!
edits = []

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 'GolCerto2026_FINAL6' in line and ('replace_file_content' in line or 'multi_replace_file_content' in line):
            try:
                data = json.loads(line)
                step = data.get('step_index')
                for tc in data.get('tool_calls', []):
                    args = tc.get('args', {})
                    if 'GolCerto2026_FINAL6' in args.get('TargetFile', ''):
                        edits.append({
                            'step': step,
                            'name': tc.get('name'),
                            'args': args
                        })
            except Exception as e:
                pass

with open('apply_logged_edits.py', 'w', encoding='utf-8') as out:
    out.write("# Auto-generated script to apply logged edits sequentially\n")
    out.write("import json\n\n")
    out.write("html_path = 'GolCerto2026_FINAL6_original.html'\n")
    out.write("with open(html_path, 'r', encoding='utf-8') as f:\n")
    out.write("    content = f.read()\n\n")
    
    for edit in edits:
        step = edit['step']
        name = edit['name']
        args = edit['args']
        
        out.write(f"# --- STEP {step}: {name} ---\n")
        if name == 'replace_file_content':
            target = args.get('TargetContent', '')
            replacement = args.get('ReplacementContent', '')
            out.write(f"target_{step} = {repr(target)}\n")
            out.write(f"replacement_{step} = {repr(replacement)}\n")
            out.write(f"if target_{step} in content:\n")
            out.write(f"    content = content.replace(target_{step}, replacement_{step}, 1)\n")
            out.write(f"    print('Applied step {step} replace_file_content')\n")
            out.write(f"else:\n")
            out.write(f"    print('WARNING: target_{step} not found for step {step}!')\n\n")
        elif name == 'multi_replace_file_content':
            chunks = args.get('ReplacementChunks', [])
            if isinstance(chunks, str):
                try:
                    chunks = json.loads(chunks)
                except:
                    pass
            out.write(f"# Multi-replace with {len(chunks)} chunks\n")
            for c_idx, chunk in enumerate(chunks):
                if isinstance(chunk, str):
                    continue
                target = chunk.get('TargetContent', '')
                replacement = chunk.get('ReplacementContent', '')
                out.write(f"target_{step}_{c_idx} = {repr(target)}\n")
                out.write(f"replacement_{step}_{c_idx} = {repr(replacement)}\n")
                out.write(f"if target_{step}_{c_idx} in content:\n")
                out.write(f"    content = content.replace(target_{step}_{c_idx}, replacement_{step}_{c_idx}, 1)\n")
                out.write(f"    print('  Applied chunk {c_idx}')\n")
                out.write(f"else:\n")
                out.write(f"    print('  WARNING: chunk {c_idx} target not found!')\n")
            out.write("\n")
            
    out.write("with open('GolCerto2026_FINAL6_reconstructed.html', 'w', encoding='utf-8') as f:\n")
    out.write("    f.write(content)\n")
    out.write("print('Reconstruction complete! Created GolCerto2026_FINAL6_reconstructed.html')\n")

print("Created apply_logged_edits.py")
