import sys
import os

# Add backend to path
sys.path.append(r'C:\Users\Gustavo\.gemini\antigravity\scratch\gol certo\golcerto-backend-update (1)\golcerto-update')

# Let's import prediction_engine
try:
    from app import prediction_engine
    # Since GROUPS and COPA_MATCHES might be missing in prediction_engine, let's see if we get an error
    print("GROUPS in prediction_engine:", hasattr(prediction_engine, 'GROUPS'))
    print("COPA_MATCHES in prediction_engine:", hasattr(prediction_engine, 'COPA_MATCHES'))
    
    # Run prediction
    res = prediction_engine.predict_match('Brazil', 'Morocco')
    print("Brazil last results:", res['last_results']['home'])
    print("Morocco last results:", res['last_results']['away'])
except Exception as e:
    print("Error:", e)
