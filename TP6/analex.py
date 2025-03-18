import ply.lex as lex

# Lista de tokens reconhecidos
tokens = ['NUM', 'PLUS', 'MINUS', 'MULT']

# Expressões regulares para os tokens
t_PLUS  = r'\+'
t_MINUS = r'-'
t_MULT  = r'\*'

# Regras para identificar números inteiros
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)  # Converte para inteiro
    return t

# Ignorar espaços em branco
t_ignore = ' \t'

# Tratamento de erro
def t_error(t):
    print("Caractere ilegal:", t.value[0])
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()
    