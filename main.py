from lexico import lexer
from parser import init_parser

with open("exemplo.mj", "r") as f:
    codigo = f.read()

tokens = lexer(codigo)
print("Tokens:")
for t in tokens:
    print(t)

print("\nAnalise sintatica:")
init_parser(tokens)