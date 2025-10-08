symbol_table = {}   
next_address = 0       
codigo_gerado = []  # Lista com as instruções do código objeto
rotulo_counter = 0
def novo_rotulo():
    global rotulo_counter
    r = rotulo_counter
    rotulo_counter += 1
    return r

tokens = []
pos = 0

def init_parser(toks):
    global tokens, pos
    tokens = toks
    pos = 0
    prog()
    if pos < len(tokens):
        token = tokens[pos]
        raise SyntaxError(f"Token inesperado após fim do programa: {token}")
    print("Tabela de símbolos (variáveis declaradas):")
    for var, addr in symbol_table.items():
        print(f"  {var} -> endereço {addr}")
    print("\u2713 Análise sintática finalizada com sucesso.")
    print("Código objeto gerado:")
    for instr in codigo_gerado:
        print(instr)
    with open("codigo-gerado.txt", "w") as f:
        for instr in codigo_gerado:
            f.write(instr + "\n")
    print("Código objeto salvo em 'codigo-gerado.txt'")

def match(expected_type, expected_value=None):
    global pos
    if pos >= len(tokens):
        raise SyntaxError("Fim inesperado do código.")

    token_type, token_value = tokens[pos]

    if token_type != expected_type:
        raise SyntaxError(f"Esperado tipo {expected_type}, mas encontrou {token_type} '{token_value}'")

    if expected_value and token_value != expected_value:
        raise SyntaxError(f"Esperado '{expected_value}', mas encontrou '{token_value}'")

    pos += 1

def lookahead_is(expected_type, expected_value=None):
    if pos >= len(tokens):
        return False
    ttype, tval = tokens[pos]
    if ttype != expected_type:
        return False
    if expected_value and tval != expected_value:
        return False
    return True

# ======= GRAMÁTICA =======

def prog():
    match('KW', 'public')
    match('KW', 'class')
    match('ID')
    match('SYMBOL', '{')
    match('KW', 'public')
    match('KW', 'static')
    match('KW', 'void')
    match('KW', 'main')
    match('SYMBOL', '(')
    match('KW', 'String')
    match('SYMBOL', '[')
    match('SYMBOL', ']')
    match('ID')
    match('SYMBOL', ')')
    match('SYMBOL', '{')
    cmds()
    match('SYMBOL', '}')
    match('SYMBOL', '}')

def cmds():
    if lookahead_is('SYMBOL', '}'):
        return

    if lookahead_is('KW', 'double'):
        var_decl()
        match('SYMBOL', ';')
        cmds()
        return

    if lookahead_is('ID'):
        assignment_or_cmd()
        match('SYMBOL', ';')
        cmds()
        return

    if lookahead_is('KW', 'if'):
        cmd_if()
        cmds()
        return

    if lookahead_is('KW', 'while'):
        cmd_while()
        cmds()
        return

    return

def var_decl():
    match('KW', 'double')
    vars_list()

def vars_list():
    global next_address

    match('ID')
    var_name = tokens[pos - 1][1]

    if var_name in symbol_table:
        raise Exception(f"Variável '{var_name}' já declarada.")

    symbol_table[var_name] = next_address
    next_address += 1

    if lookahead_is('SYMBOL', ','):
        match('SYMBOL', ',')
        vars_list()

def assignment_or_cmd():
    if lookahead_is('ID') and tokens[pos][1] == 'System':
        # System.out.println(...)
        match('ID', 'System')
        match('SYMBOL', '.')
        match('ID', 'out')
        match('SYMBOL', '.')
        match('ID', 'println')
        match('SYMBOL', '(')
        expr_result = expr()
        codigo_gerado.extend(expr_result)
        codigo_gerado.append("IMPR")
        match('SYMBOL', ')')
    else:
        match('ID')
        var_name = tokens[pos - 1][1]

        if var_name not in symbol_table:
            raise Exception(f"Variável '{var_name}' usada sem declaração.")

        match('SYMBOL', '=')
        expr_result = expr()
        codigo_gerado.extend(expr_result)  # expr_result contém instruções como LEIT ou CRVL
        codigo_gerado.append(f"ARMZ {symbol_table[var_name]}")

def expr():
    # EXPRESSAO -> id | NUM | lerDouble() | (expr)
    if lookahead_is('ID'):
        match('ID')
        var_name = tokens[pos - 1][1]
        if var_name not in symbol_table:
            raise Exception(f"Variável '{var_name}' usada sem declaração.")
        return [f"CRVL {symbol_table[var_name]}"]
    elif lookahead_is('NUM'):
        match('NUM')
        valor = tokens[pos - 1][1]
        return [f"CRCT {valor}"]
    elif lookahead_is('KW', 'lerDouble'):
        match('KW', 'lerDouble')
        match('SYMBOL', '(')
        match('SYMBOL', ')')
        return ["LEIT"]
    elif lookahead_is('SYMBOL', '('):
        match('SYMBOL', '(')
        resultado = expr()
        match('SYMBOL', ')')
        return resultado
    else:
        raise SyntaxError("Expressão inválida")

def cmd_if():
    match('KW', 'if')
    match('SYMBOL', '(')
    expr1 = expr()
    match('OP')
    expr2 = expr()
    match('SYMBOL', ')')

    rot_else = novo_rotulo()
    rot_end = novo_rotulo()

    codigo_gerado.extend(expr1)
    codigo_gerado.extend(expr2)
    codigo_gerado.append("CPMA")
    codigo_gerado.append(f"DSVF R{rot_else}")

    match('SYMBOL', '{')
    cmds()
    match('SYMBOL', '}')

    if lookahead_is('KW', 'else'):
        codigo_gerado.append(f"DSVI R{rot_end}")
        codigo_gerado.append(f"R{rot_else}:")
        match('KW', 'else')
        match('SYMBOL', '{')
        cmds()
        match('SYMBOL', '}')
        codigo_gerado.append(f"R{rot_end}:")
    else:
        codigo_gerado.append(f"R{rot_else}:")

def cmd_while():
    match('KW', 'while')
    match('SYMBOL', '(')
    rot_inicio = novo_rotulo()
    rot_fim = novo_rotulo()
    codigo_gerado.append(f"R{rot_inicio}:")
    expr1 = expr()
    match('OP')
    expr2 = expr()
    codigo_gerado.extend(expr1)
    codigo_gerado.extend(expr2)
    codigo_gerado.append("CPMA")
    codigo_gerado.append(f"DSVF R{rot_fim}")
    match('SYMBOL', ')')
    match('SYMBOL', '{')
    cmds()
    match('SYMBOL', '}')
    codigo_gerado.append(f"DSVI R{rot_inicio}")
    codigo_gerado.append(f"R{rot_fim}:")