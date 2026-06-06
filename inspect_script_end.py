# Let's write a python script to inspect the bottom section of the original HTML file to find the closing </script> tag
# and some surrounding lines.
with open('GolCerto2026_FINAL6_original.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for the last occurrence of '</script>'
last_script_end = content.rfind('</script>')
print(f"Last </script> starts at index {last_script_end}")

# Let's print the 200 characters before and 200 characters after last_script_end
before = content[max(0, last_script_end-300):last_script_end].encode('ascii', errors='replace').decode('ascii')
after = content[last_script_end:min(len(content), last_script_end+300)].encode('ascii', errors='replace').decode('ascii')

print("--- BEFORE ---")
print(before)
print("--- AFTER ---")
print(after)
