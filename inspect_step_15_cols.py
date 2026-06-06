import sqlite3
import json

db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Let's query step 15
cursor.execute("SELECT idx, step_payload FROM steps WHERE idx = 15;")
res = cursor.fetchone()
if res:
    idx, payload = res
    print(f"Step 15 Payload size: {len(payload)}")
    try:
        # Protobuf is not JSON, but let's see if there is any readable text or if we can query step_type = 15
        # Wait, the column is idx and step_type. Let's see what values step_type can take.
        # In PRAGMA table_info, it's INTEGER.
        # Let's select all columns for idx = 15
        cursor.execute("SELECT * FROM steps WHERE idx = 15;")
        row = cursor.fetchone()
        print("Columns:")
        # Column names: ['idx', 'step_type', 'status', 'has_subtrajectory', 'metadata', 'error_details', 'permissions', 'task_details', 'render_info', 'step_payload', 'step_format']
        for col_val, col_name in zip(row, ['idx', 'step_type', 'status', 'has_subtrajectory', 'metadata', 'error_details', 'permissions', 'task_details', 'render_info', 'step_payload', 'step_format']):
            val_str = str(col_val)
            if len(val_str) > 300:
                val_str = val_str[:300] + "..."
            print(f" {col_name}: {val_str}")
    except Exception as e:
        print(e)
conn.close()
