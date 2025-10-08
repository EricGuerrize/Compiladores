import re

#linguagem mini java
KEYWORDS = {
    "public", "class", "static", "void", "main", "String",
    "double", "if", "else", "while", "System.out.println", "lerDouble", "System.out.println"
}

# identificacao regex para cada tipo de token
token_specs = [
    ('NUM',      r'\d+\.\d+'),                          # reais
    ('ID',       r'[a-zA-Z_][a-zA-Z_0-9]*'),            # identificadores
    ('OP',       r'==|!=|>=|<=|[+\-*/<>]'),             # operadores
    ('SYMBOL',   r'[(){}\[\];,=\.]'),                     # símbolos + ponto (sem ponto deu erro)
    ('NEWLINE',  r'\n'),                                # quebra de linha
    ('SKIP',     r'[ \t]+'),                            # espaços e tabs
    ('MISMATCH', r'.'),                                 # qualquer outro caractere nao add
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
get_token = re.compile(tok_regex).match

def lexer(code):
    pos = 0
    tokens = []
    line = 1

    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f"Erro léxico na linha {line}")
        
        typ = match.lastgroup
        val = match.group(typ)

        if typ == 'NUM':
            tokens.append(('NUM', val))
        elif typ == 'ID':
            if val in KEYWORDS:
                tokens.append(('KW', val))
            else:
                tokens.append(('ID', val))
        elif typ == 'OP':
            tokens.append(('OP', val))
        elif typ == 'SYMBOL':
            tokens.append(('SYMBOL', val))
        elif typ == 'NEWLINE':
            line += 1
        elif typ == 'SKIP':
            pass
        elif typ == 'MISMATCH':
            raise SyntaxError(f"Caractere inválido '{val}' na linha {line}")
        
        pos = match.end()
    
    return tokens