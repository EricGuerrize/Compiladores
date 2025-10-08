from lexico import lexer
from parser import init_parser

with open("teste-aritmetica.mj", "r") as f:
    codigo = f.read()

tokens = lexer(codigo)
print("Tokens gerados:")
for t in tokens:
    print(t)

print("\nIniciando análise sintática...")
init_parser(tokens)