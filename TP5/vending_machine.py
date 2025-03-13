import ply.lex as lex
import json

# Lista de tokens
tokens = (
    'LISTAR', 'MOEDA', 'SELECIONAR', 'SAIR', 'ADICIONAR',
    'NUMERO', 'CENTIMOS', 'EUROS', 'CODIGO',)

t_ignore = ' \t\r'

# Definição dos tokens
def t_LISTAR(t): r'LISTAR'; return t

def t_MOEDA(t): r'MOEDA'; return t

def t_SELECIONAR(t): r'SELECIONAR'; return t

def t_ADICIONAR(t): r'ADICIONAR'; return t

def t_SAIR(t): r'SAIR'; return t

def t_EUROS(t):
    r'\b\d+e\b'
    t.value = int(t.value[:-1]) * 100
    return t

def t_CENTIMOS(t):
    r'\b\d+c\b'
    t.value = int(t.value[:-1])
    return t

def t_CODIGO(t):
    r'[A-Z][0-9]{2}'
    t.value = t.value.strip()
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f'Caractere ilegal: {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

# Variáveis globais
saldo = 0
stock = []

def carregar_stock():
    global stock
    try:
        with open('stock.json', 'r') as file:
            stock = json.load(file)
    except FileNotFoundError:
        stock = []

def salvar_stock():
    with open('stock.json', 'w') as file:
        json.dump(stock, file, indent=4)

def devolver_troco(saldo):
    moedas = [50, 20, 10, 5, 2, 1]
    troco = []
    for moeda in moedas:
        count = saldo // moeda
        saldo -= count * moeda
        if count > 0:
            troco.append((count, moeda))
    return troco

def processar_comando(tokens):
    global saldo

    if tokens[0] == 'LISTAR':
        print("maq:")
        print("cod  | nome         | quantidade | preço")
        print("--------------------------------------")
        for produto in stock:
            print(f"{produto['cod']}  {produto['nome']:<12} {produto['quant']:<10} {produto['preco']:.2f}e")

    elif tokens[0] == 'MOEDA':
        saldo += sum(tokens[1:])
        print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")

    elif tokens[0] == 'SELECIONAR':
        codigo = tokens[1]
        produto = next((p for p in stock if p['cod'] == codigo), None)

        if produto:
            if saldo >= produto['preco'] * 100:
                if produto['quant'] > 0:
                    produto['quant'] -= 1
                    saldo -= int(produto['preco'] * 100)
                    print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
                    print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
                else:
                    print(f"maq: Produto {produto['nome']} fora de estoque.")
            else:
                print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c; Pedido = {int(produto['preco'] * 100)}c")
        else:
            print(f"maq: Produto com código {codigo} não encontrado.")

    elif tokens[0] == 'ADICIONAR':
        codigo, nome, quant, preco = tokens[1], tokens[2], tokens[3], tokens[4]
        produto = next((p for p in stock if p['cod'] == codigo), None)

        if produto:
            produto['quant'] += quant
        else:
            stock.append({"cod": codigo, "nome": nome, "quant": quant, "preco": preco})
        print(f"maq: Produto {nome} adicionado/atualizado.")
        salvar_stock()

    elif tokens[0] == 'SAIR':
        troco = devolver_troco(saldo)
        print("maq: Pode retirar o troco:", end=" ")
        print(", ".join([f"{c}x {m}c" for c, m in troco]))
        print("maq: Até à próxima")
        salvar_stock()
        exit()

def processar_entrada(entrada):
    lexer.input(entrada)
    tokens_processados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_processados.append(tok.value if tok.type in ['EUROS', 'CENTIMOS', 'NUMERO', 'CODIGO'] else tok.type)
    return tokens_processados

if __name__ == "__main__":
    print("maq: 2024-03-08, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    carregar_stock()
    while True:
        try:
            entrada = input('>> ')
        except EOFError:
            break
        if not entrada:
            continue
        tokens_processados = processar_entrada(entrada)
        processar_comando(tokens_processados)