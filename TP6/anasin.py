from analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado:", simb)

# Lê o próximo símbolo do lexer
def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

# Regra para reconhecer fatores (números)
def rec_Fator():
    global prox_simb
    if prox_simb.type == 'NUM':
        valor = int(prox_simb.value)
        rec_term('NUM')
        return valor
    else:
        parserError(prox_simb)
        return 0

# Regra para reconhecer termos (multiplicações primeiro)
def rec_Termo():
    global prox_simb
    valor = rec_Fator()
    while prox_simb and prox_simb.type == 'MULT':  # Verifique se prox_simb não é None
        rec_term('MULT')
        valor *= rec_Fator()
    return valor


# Regra para reconhecer expressões completas (+ e - depois de *)
def rec_Expressao():
    global prox_simb
    valor = rec_Termo()
    while prox_simb and prox_simb.type in ['PLUS', 'MINUS']:  # Verifique se prox_simb não é None
        if prox_simb.type == 'PLUS':
            rec_term('PLUS')
            valor += rec_Termo()
        elif prox_simb.type == 'MINUS':
            rec_term('MINUS')
            valor -= rec_Termo()
    return valor


# Função principal que inicia o parser
def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    resultado = rec_Expressao()
    print("Resultado:", resultado)
    return resultado