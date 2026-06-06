"with open('golcerto-backend-update (1)/golcerto-update/app/prediction_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the complete REAL_LAST_RESULTS database
real_last_results_def = """REAL_LAST_RESULTS = {
    'Brazil': [
        {'res': 'V', 'score': '6-2', 'opp': 'Panama', 'loc': 'C'},
        {'res': 'V', 'score': '2-0', 'opp': 'Senegal', 'loc': 'C'},
        {'res': 'E', 'score': '1-1', 'opp': 'Tunisia', 'loc': 'F'}
    ],
    'Morocco': [
        {'res': 'V', 'score': '4-0', 'opp': 'Madagascar', 'loc': 'C'},
        {'res': 'V', 'score': '7-0', 'opp': 'Lesotho', 'loc': 'C'},
        {'res': 'V', 'score': '5-1', 'opp': 'Gabon', 'loc': 'F'}
    ],
    'Mexico': [
        {'res': 'E', 'score': '1-1', 'opp': 'Belgium', 'loc': 'F'},
        {'res': 'E', 'score': '0-0', 'opp': 'Portugal', 'loc': 'F'},
        {'res': 'V', 'score': '4-0', 'opp': 'Iceland', 'loc': 'C'}
    ],
    'South Africa': [
        {'res': 'V', 'score': '3-0', 'opp': 'Congo DR', 'loc': 'C'},
        {'res': 'E', 'score': '1-1', 'opp': 'Congo DR', 'loc': 'F'},
        {'res': 'V', 'score': '5-0', 'opp': 'Congo', 'loc': 'C'}
    ],
    'Argentina': [
        {'res': 'V', 'score': '3-0', 'opp': 'Chile', 'loc': 'C'},
        {'res': 'D', 'score': '1-2', 'opp': 'Colombia', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Peru', 'loc': 'C'}
    ],
    'France': [
        {'res': 'V', 'score': '2-0', 'opp': 'Belgium', 'loc': 'C'},
        {'res': 'V', 'score': '4-1', 'opp': 'Israel', 'loc': 'F'},
        {'res': 'V', 'score': '2-1', 'opp': 'Italy', 'loc': 'F'}
    ],
    'Germany': [
        {'res': 'E', 'score': '2-2', 'opp': 'Netherlands', 'loc': 'F'},
        {'res': 'V', 'score': '2-1', 'opp': 'Bosnia', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Netherlands', 'loc': 'C'}
    ],
    'Spain': [
        {'res': 'V', 'score': '4-1', 'opp': 'Switzerland', 'loc': 'F'},
        {'res': 'V', 'score': '1-0', 'opp': 'Denmark', 'loc': 'C'},
        {'res': 'V'
<truncated 5752 bytes>