import sqlite3
import json

db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Let's check which tables contain the actual tool call output (content) or conversation history messages.
# trajectory_metadata_blob? Let's check trajectory_metadata_blob.
cursor.execute("SELECT id, data FROM trajectory_metadata_blob;")
for row in cursor.fetchall():
    print("trajectory_metadata_blob ID:", row[0], "data len:", len(row[1]))
    # Print start of data
    val = row[1]
    if len(val) > 200:
        val = val[:200]
    print(val)
conn.close()
