import sqlite3
import json

db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT idx, step_type FROM steps LIMIT 20;")
    print("First 20 steps:")
    for row in cursor.fetchall():
        print(row)
        
    cursor.execute("SELECT idx, step_type FROM steps WHERE idx IN (15, 16, 17, 18, 19, 20);")
    print("Steps 15-20:")
    for row in cursor.fetchall():
        print(row)
        
    # Let's inspect step 16 payload or output
    cursor.execute("SELECT idx, step_payload FROM steps WHERE idx = 16;")
    res = cursor.fetchone()
    if res:
        idx, payload = res
        print(f"Step 16 Payload size: {len(payload)}")
        # Let's print the first 500 chars of payload
        print(payload[:500])
except Exception as e:
    print(e)
finally:
    conn.close()
