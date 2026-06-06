import sqlite3
import zlib
import re

# Let's inspect step 16 payload further.
db_path = r'C:\Users\Gustavo\.gemini\antigravity\conversations\bd24e051-143e-4678-bb61-92d1d310912f.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT idx, step_payload FROM steps WHERE idx = 16;")
idx, payload = cursor.fetchone()

print("Payload total size:", len(payload))
# Let's print out all ascii sequences of length >= 10 in the payload
strings = re.findall(b'[a-zA-Z0-9_/\\.\\-\\:\\(\\)\\{\\}\\"\\\'\\,\\=\\[\\] ]{10,}', payload)
print("ASCII Strings in payload:")
for s in strings[:30]:
    print(" ", s.decode('ascii', errors='ignore'))
    
# Let's check if there is any zlib compressed block in the payload.
# zlib compressed data usually starts with 0x78 and then 0x01, 0x5e, 0x9c, 0xda, etc.
for i in range(len(payload)):
    if payload[i] == 0x78:
        if i + 1 < len(payload) and payload[i+1] in [0x01, 0x5e, 0x9c, 0xda]:
            # Try to decompress
            try:
                dec = zlib.decompress(payload[i:])
                print(f"Success decompressing from offset {i}, size: {len(dec)}")
                print(dec[:500].decode('utf-8', errors='ignore'))
                break
            except Exception as e:
                pass
conn.close()
