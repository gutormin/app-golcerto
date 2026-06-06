import os

# Let's list directories under C:\Users\Gustavo\.gemini\antigravity
print("List of C:\\Users\\Gustavo\\.gemini\\antigravity:")
try:
    print(os.listdir(r'C:\Users\Gustavo\.gemini\antigravity'))
except Exception as e:
    print(e)

print("\nList of C:\\Users\\Gustavo\\.gemini\\antigravity\\scratch:")
try:
    print(os.listdir(r'C:\Users\Gustavo\.gemini\antigravity\scratch'))
except Exception as e:
    print(e)
