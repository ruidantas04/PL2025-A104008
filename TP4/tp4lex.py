import ply.lex as lex

# Lista de tokens
tokens = (
    'KW_SELECT', 'KW_WHERE', 'KW_LIMIT', 'KW_A',
    'ID', 'PREFIX', 'DPONTOS', 'SUFIXO', 'STRING', 'NUM',
    'PA', 'PF', 'PONTO', 'OP'
)

def t_KW_SELECT(t):
    r'select'
    return t

def t_KW_WHERE(t):
    r'where'
    return t

def t_KW_LIMIT(t):
    r'LIMIT'
    return t
def t_SUFIXO(t):
    r'(?<=:)[a-zA-Z_]\w*'
    return t
def t_KW_A(t):
    r' a '
    return t

def t_ID(t):
    r'\?[a-zA-Z_]\w*'
    return t

def t_PREFIX(t):
    r'[a-zA-Z_]\w*(?=:)'
    return t

def t_DPONTOS(t):
    r':'
    return t



def t_STRING(t):
    r'"[^"\r\n]*"(?:@[a-zA-Z]+)?'
    return t

def t_NUM(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

def t_PA(t):
    r'\{'
    return t

def t_PF(t):
    r'\}'
    return t

def t_PONTO(t):
    r'\.'
    return t

def t_OP(t):
    r'[=><!]'
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1
    
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

code = '''
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
'''

lexer.input(code)
while (token := lexer.token()):
    print(token)