import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 800 < idx < 950 and ('REAL_NEWS_CACHE' in line or 'update_all_news_cache' in line):
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                def find_strings(obj):
                    if isinstance(obj, str):
                        if 'REAL_NEWS_CACHE' in obj or 'update_all_news_cache' in obj:
                            return obj
                    elif isinstance(obj, dict):
                        for k, v in obj.items():
                            res = find_strings(v)
                            if res:
                                return res
                    elif isinstance(obj, list):
                        for item in obj:
                            res = find_strings(item)
                            if res:
                                return res
                    return None
                
                impl = find_strings(data)
                if impl and len(impl) > 100:
                    print(f"FOUND ON LINE {idx}, STEP {step}:")
                    print(impl[:1500])
                    print("===================================\n")
            except Exception as e:
                pass
