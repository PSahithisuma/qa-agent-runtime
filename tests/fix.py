# fix conftest files
with open('conftest.py', 'w', encoding='utf-8') as f:
    f.write('import sys\nimport os\nsys.path.insert(0, os.path.abspath("."))\n')

with open('tests/conftest.py', 'w', encoding='utf-8') as f:
    f.write('')

with open('src/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

with open('src/sandbox/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

with open('src/runner/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

with open('tests/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

print('All fixed!')