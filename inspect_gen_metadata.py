import sqlite3

db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Let's count how many items exist in table `gen_metadata` and see what is in there.
cursor.execute("SELECT COUNT(*) FROM gen_metadata;")
print("gen_metadata count:", cursor.fetchone()[0])

cursor.execute("SELECT idx, size FROM gen_metadata LIMIT 20;")
print("gen_metadata idx, size:")
for row in cursor.fetchall():
    print(row)
    
# Let's select one row and print the first 200 bytes of the data
cursor.execute("SELECT idx, data FROM gen_metadata WHERE size > 1000 LIMIT 1;")
res = cursor.fetchone()
if res:
    idx, data = res
    print(f"gen_metadata idx {idx} data len: {len(data)}")
    # check if zlib compresses or what
    print(data[:200])
conn.close()
