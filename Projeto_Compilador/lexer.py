import ply.lex as lex
import re

class PascalLexer:
    def __init__(self):
        self.lexer = None

    tokens = (
        'PROGRAM', 'VAR', 'BEGIN', 'END', 'FUNCTION', 'FORWARD', 'EXTERNAL',
        'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FOR', 'TO', 'DOWNTO',
        'IDENTIFIER', 'DIGSEQ', 'REALNUMBER', 'CHARACTER_STRING', 'NIL',
        'TREAL', 'TINTEGER', 'TBOOLEAN', 'TSTRING', 'TCHAR',
        'ASSIGNMENT', 'COLON', 'SEMICOLON', 'DOT', 'COMMA', 'DOTDOT',
        'PLUS', 'MINUS', 'STAR', 'SLASH', 'DIV', 'MOD', 'AND', 'OR', 'NOT',
        'EQUAL', 'NOTEQUAL', 'LT', 'GT', 'LE', 'GE', 'IN',
        'LPAREN', 'RPAREN', 'LBRAC', 'RBRAC', 'STARSTAR', 'UPARROW', 'COMMENT', 'ARRAY',
        'OF'
    )

    def t_PROGRAM(self, t):
        r'program'
        return t

    def t_VAR(self, t):
        r'var'
        return t

    def t_BEGIN(self, t):
        r'begin'
        return t

    def t_END(self, t):
        r'end'
        return t

    def t_FUNCTION(self, t):
        r'function'
        return t

    def t_FORWARD(self, t):
        r'forward'
        return t

    def t_EXTERNAL(self, t):
        r'external'
        return t

    def t_IF(self, t):
        r'if'
        return t

    def t_THEN(self, t):
        r'then'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_WHILE(self, t):
        r'while'
        return t
    
    def t_DOWNTO(self, t):
        r'downto'
        return t

    def t_DO(self, t):
        r'do'
        return t

    def t_FOR(self, t):
        r'for'
        return t

    def t_TO(self, t):
        r'to'
        return t

    def t_TREAL(self, t):
        r'real'
        return t

    def t_TINTEGER(self, t):
        r'integer'
        return t

    def t_TBOOLEAN(self, t):
        r'boolean'
        return t

    def t_TSTRING(self, t):
        r'string'
        return t

    def t_TCHAR(self, t):
        r'char'
        return t

    def t_DIV(self, t):
        r'div'
        return t

    def t_MOD(self, t):
        r'mod'
        return t

    def t_AND(self, t):
        r'and'
        return t

    def t_OR(self, t):
        r'or'
        return t

    def t_NOT(self, t):
        r'not'
        return t

    def t_NIL(self, t):
        r'nil'
        return t

    def t_IN(self, t):
        r'in'
        return t

    def t_ARRAY(self, t):
        r'array'
        return t

    def t_OF(self, t):
        r'of'
        return t

    t_ASSIGNMENT = r':='
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_DOT = r'\.'
    t_COMMA = r','
    t_DOTDOT = r'\.\.'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_SLASH = r'/'
    t_STARSTAR = r'\*\*'
    t_UPARROW = r'\^'
    t_EQUAL = r'='
    t_NOTEQUAL = r'<>'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRAC = r'\['
    t_RBRAC = r'\]'

    def t_REALNUMBER(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_DIGSEQ(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_COMMENT(self, t):
        r'\{[^}]*\}|\(\*[^*]*\*\)'
        pass

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    def t_CHARACTER_STRING(self, t):
        r"'([^']|'')*'"
        t.value = t.value[1:-1]
        return t

    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, reflags=re.IGNORECASE, **kwargs)
        return self.lexer
