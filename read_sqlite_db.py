import json
import sqlite3
import os

# Let's inspect the SQLite database files for our conversation or previous conversations!
# The databases are stored in C:\Users\Gustavo\.gemini\antigravity\conversations\
# Let's look for "GolCerto2026_FINAL6 (2).html" content or tool calls inside the databases.
# Specifically, bd24e051-143e-4678-bb61-92d1d310912f.db is the database for the current conversation.
# sqlite3 databases store the messages, tool calls, and states. Let's see if we can query them!

db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Let's see what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)
        
        # Let's query one of the tables
        for table in tables:
            tname = table[0]
            cursor.execute(f"PRAGMA table_info({tname});")
            info = cursor.fetchall()
            print(f"Table {tname} columns:", [i[1] for i in info])
            
            # Let's count rows
            cursor.execute(f"SELECT COUNT(*) FROM {tname};")
            count = cursor.fetchone()[0]
            print(f"Table {tname} row count: {count}")
    except Exception as e:
        print("Err:", e)
    finally:
        conn.close()
else:
    print("Database not found.")
