import ast
from pathlib import Path

source = Path(__file__).with_name("example.py").read_text(encoding="utf-8")
tree = ast.parse(source)

print(ast.unparse(tree))
