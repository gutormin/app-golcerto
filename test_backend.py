import sys
sys.path.append("golcerto-backend-update (1)/golcerto-update")

from app import prediction_engine
from collections import Counter

matches = prediction_engine.get_matches_with_predictions()

scores = []
for m in matches:
    scores.append(m['prediction']['suggested_score']['score'])

print("--- NEW MODEL DISTRIBUTION ---")
counts = Counter(scores)
for score, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"Placar {score}: {count} jogos")
