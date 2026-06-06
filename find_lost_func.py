import json

log_path = r'C:\Users\Gustavo\.gemini\antigravity\brain\bd24e051-143e-4678-bb61-92d1d310912f\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx < 1000 and 'update_all_news_cache_loop' in line and 'def ' in line:
            try:
                data = json.loads(line)
                step = data.get('step_index', idx)
                
                # Let's find any content that contains the implementation of the function
                def find_impl(obj):
                    if isinstance(obj, str):
                        if 'def update_all_news_cache_loop' in obj:
                            return obj
                    elif isinstance(obj, dict):
                        for k, v in obj.items():
                            res = find_impl(v)
                            if res:
                                return res
                    elif isinstance(obj, list):
                        for item in obj:
                            res = find_impl(item)
                            if res:
                                return res
                    return None
                
                impl = find_impl(data)
                if impl:
                    print(f"FOUND IMPLEMENTATION ON LINE {idx}, STEP {step}:")
                    print(impl[:1500])
                    print("===================================\n")
            except Exception as e:
                pass
