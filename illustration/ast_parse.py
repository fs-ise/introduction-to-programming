import ast
from pathlib import Path

source = Path("example.py").read_text(encoding="utf-8")
tree = ast.parse(source)

print(ast.unparse(tree))