import ast

engine_path = r'C:\Users\Gustavo\.gemini\antigravity\scratch\gol certo\golcerto-backend-update (1)\golcerto-update\app\prediction_engine.py'

with open(engine_path, 'r', encoding='utf-8') as f:
    tree = ast.parse(f.read())

functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
print("Functions in prediction_engine.py:", functions)

globals_vars = []
for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                globals_vars.append(target.id)
print("Globals in prediction_engine.py:", globals_vars)
