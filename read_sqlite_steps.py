import json
import sqlite3
import os

# Let's inspect the `steps` table in the SQLite database to see if it contains full tool calls and responses,
# specifically view_file calls or write_to_file calls.
# Let's look for rows in the `steps` table that contain 'view_file' or 'GolCerto2026_FINAL6'
# column 'step_payload' or 'render_info' or 'metadata'.

db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT idx, step_type, step_payload FROM steps WHERE step_payload LIKE '%GolCerto2026_FINAL6%' AND step_type = 'VIEW_FILE' LIMIT 10;")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} matching steps in DB.")
    for row in rows:
        idx, step_type, payload = row
        print(f"Step {idx}: Type={step_type}, Payload len={len(payload)}")
        # Let's parse the JSON payload
        try:
            p_data = json.loads(payload)
            print("Payload keys:", p_data.keys())
            # Let's check where the content or output is stored.
            # Usually, payload has "result" or "response" or "output"
            if 'output' in p_data:
                print("Output length:", len(p_data['output']))
                # print a snippet of output
                print(p_data['output'][:500])
        except Exception as e:
            print("JSON parse error:", e)
        print("="*40)
except Exception as e:
    print(e)
finally:
    conn.close()
