import json
import re

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

# Let's write a script that reads transcript.jsonl from start to end, maintaining a virtual copy of the HTML file
# by simulating/applying each replace_file_content or multi_replace_file_content tool call that was executed successfully!
# Wait! This is perfect! Let's do this.
# But wait, what was the initial content of the file?
# Since the file existed in the workspace at the very beginning of the run (Step 0) and had a size of 865816 bytes (Step 3: LIST_DIRECTORY),
# and the first tool call to edit the HTML file was Step 55, let's look at Step 55.
# Step 55 was: Tool replace_file_content, Start 11, End 412, Target len: 2072, Replacement len: 2072.
# Let's inspect the target content and replacement content of Step 55!
# If the target content of Step 55 matches something, that target content must have been in the original file.
# But wait, did we ever have a full copy of the original file in any view_file?
# Step 15 viewed lines 1 to 800. Step 17 viewed lines 800 to 1206.
# 1 to 800 and 800 to 1206 covers the ENTIRE file from line 1 to 1206!
# Since the original file had 1206 lines, we have 100% of the original file's lines in the view_file calls of Step 15 and Step 17!
# Let's verify this!
# Step 15 has lines 1-800. Step 17 has lines 800-1206.
# Let's extract these lines and combine them to reconstruct the original HTML file EXACTLY!
# Once we reconstruct the original file, we can then apply all subsequent successful edits to it sequentially!
# This is incredibly powerful and 100% accurate!

# Let's first extract the exact line contents from step 15 (Index 15) and step 17 (Index 17).
original_lines = {}

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx in [15, 17]:
            data = json.loads(line)
            content = data.get('content', '')
            for l in content.splitlines():
                m = re.match(r'^(\d+): (.*)$', l)
                if m:
                    ln = int(m.group(1))
                    val = m.group(2)
                    original_lines[ln] = val

print(f"Extracted {len(original_lines)} original lines.")
missing_orig = [i for i in range(1, 1207) if i not in original_lines]
print("Missing original lines:", missing_orig)

# Let's write the original file
with open('original_reconstructed.html', 'w', encoding='utf-8') as out:
    for i in range(1, 1207):
        out.write(original_lines.get(i, '') + '\n')
print("Wrote original_reconstructed.html")
