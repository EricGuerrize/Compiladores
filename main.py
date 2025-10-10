from lexico import lexer
from parser import init_parser

with open("exemplo.mj", "r") as f:
    codigo = f.read()

tokens = lexer(codigo)
print("Tokens gerados:")
for t in tokens:
    print(t)

print("\nAnálise sintática iniciada : ")
init_parser(tokens)