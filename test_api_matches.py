import httpx
import json

try:
    r = httpx.get('http://localhost:8002/matches', timeout=15.0)
    data = r.json()
    matches = data.get('matches', [])
    print(f"Total matches returned: {len(matches)}")
    # Find Brazil vs Morocco match (should be in Group C, id 31 or index 30)
    for m in matches:
        if m['home'] == 'Brazil' and m['away'] == 'Morocco':
            print("\nBrazil vs Morocco Match prediction:")
            print(json.dumps(m['prediction']['last_results'], indent=2))
            break
except Exception as e:
    print("API Error:", e)
