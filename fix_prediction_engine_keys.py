# Load current prediction_engine.py
file_path = r'golcerto-backend-update (1)/golcerto-update/app/prediction_engine.py'

with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace keys in REAL_LAST_RESULTS and get_mock_last_results
# 'res' -> 'status'
# 'opp' -> 'opponent'
# 'loc' -> 'where'
# 'C' -> 'Home'
# 'F' -> 'Away'

# Let's do search-and-replace carefully
code = code.replace("'res':", "'status':")
code = code.replace("'opp':", "'opponent':")
code = code.replace("'loc':", "'where':")
code = code.replace("'loc':", "'where':") # just in case
code = code.replace("'loc'", "'where'")
code = code.replace("'opp'", "'opponent'")
code = code.replace("'res'", "'status'")

# Also fix the values 'C' -> 'Home' and 'F' -> 'Away' in REAL_LAST_RESULTS
# Note that we only want to replace them inside the REAL_LAST_RESULTS dictionary definition.
# Let's target the exact string patterns:
code = code.replace("'loc': 'C'", "'where': 'Home'")
code = code.replace("'loc': 'F'", "'where': 'Away'")
code = code.replace("'where': 'C'", "'where': 'Home'")
code = code.replace("'where': 'F'", "'where': 'Away'")

# Fix get_mock_last_results function body:
# original:
#         results.append({
#             'status': res,
#             'score': score,
#             'opponent': opp,
#             'where': 'C' if h % 2 == 0 else 'F'
#         })
# replaced to use 'Home' and 'Away':
code = code.replace("'where': 'C' if h % 2 == 0 else 'F'", "'where': 'Home' if h % 2 == 0 else 'Away'")

with open(file_path, 'w', encoding='utf-8') as out:
    out.write(code)

print("Successfully updated keys in prediction_engine.py")
