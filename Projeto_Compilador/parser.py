import ply.yacc as yacc
import syntax as ast


class PascalParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens 
        self.parser = yacc.yacc(module=self)
        self.error_count = 0

    def parse(self, code):
        self.error_count = 0
        result = self.parser.parse(code, lexer=self.lexer.lexer)
        return ast.AbstractSyntaxTree(result)

    def p_program(self, p):
        '''program : program_heading SEMICOLON block DOT'''
        p[0] = ast.Program(p[1], p[3])

    def p_program_heading(self, p):
        '''program_heading : PROGRAM identifier
                          | PROGRAM identifier LPAREN identifier_list RPAREN'''
        if len(p) == 3:
            p[0] = ('program_heading', p[2])
        else:
            p[0] = ('program_heading_with_params', p[2], p[4])

    def p_identifier_list(self, p):
        '''identifier_list : identifier_list COMMA identifier
                          | identifier'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_block(self, p):
        '''block : function_declaration_part variable_declaration_part statement_part'''
        p[0] = ast.Block(p[1], p[2], p[3])

    def p_function_declaration_part(self, p):
        '''function_declaration_part : function_declaration_list SEMICOLON
                                    | empty'''
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[0] = None

    def p_function_declaration_list(self, p):
        '''function_declaration_list : function_declaration_list SEMICOLON function_declaration
                                    | function_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_function_declaration(self, p):
        '''function_declaration : function_heading SEMICOLON directive
                                | function_identification SEMICOLON function_block
                                | function_heading SEMICOLON function_block'''
        if len(p) == 4 and isinstance(p[3], tuple) and p[3][0] == 'directive':
            p[0] = ast.FunctionDeclaration(p[1], p[3])
        else:
            local_vars = p[3].variables if isinstance(p[3], ast.Block) else None
            body = p[3] if isinstance(p[3], ast.Block) else p[3]
            p[0] = ast.FunctionDeclaration(p[1], body, local_vars)

    def p_directive(self, p):
        '''directive : FORWARD
                    | EXTERNAL'''
        p[0] = ('directive', p[1])

    def p_function_heading(self, p):
        '''function_heading : FUNCTION identifier COLON type_denoter
                           | FUNCTION identifier formal_parameter_list COLON type_denoter'''
        if len(p) == 5 and p[3] == ':':
            p[0] = ('function_heading', p[2], p[4])
        else:
            p[0] = ('function_heading_with_params', p[2], p[3], p[5])

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : LPAREN formal_parameter_section_list RPAREN'''
        p[0] = ('formal_parameter_list', p[2])

    def p_formal_parameter_section_list(self, p):
        '''formal_parameter_section_list : formal_parameter_section_list SEMICOLON formal_parameter_section
                                        | formal_parameter_section'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_formal_parameter_section(self, p):
        '''formal_parameter_section : value_parameter_specification
                                   | variable_parameter_specification
                                   | functional_parameter_specification'''
        p[0] = ('formal_parameter_section', p[1])

    def p_value_parameter_specification(self, p):
        '''value_parameter_specification : identifier_list COLON type_denoter'''
        p[0] = ('value_parameter', p[1], p[3])

    def p_variable_parameter_specification(self, p):
        '''variable_parameter_specification : VAR identifier_list COLON type_denoter'''
        p[0] = ('variable_parameter', p[2], p[4])

    def p_functional_parameter_specification(self, p):
        '''functional_parameter_specification : function_heading'''
        p[0] = ('functional_parameter', p[1])

    def p_function_identification(self, p):
        '''function_identification : FUNCTION identifier'''
        p[0] = ('function_identification', p[2])

    def p_function_block(self, p):
        '''function_block : block'''
        p[0] = p[1]

    def p_variable_declaration_part(self, p):
        '''variable_declaration_part : VAR variable_declaration_list SEMICOLON
                                    | empty'''
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = None

    def p_variable_declaration_list(self, p):
        '''variable_declaration_list : variable_declaration_list SEMICOLON variable_declaration
                                    | variable_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_variable_declaration(self, p):
        '''variable_declaration : identifier_list COLON type_denoter'''
        p[0] = ast.VariableDeclaration(p[1], p[3])

    def p_statement_part(self, p):
        '''statement_part : compound_statement'''
        p[0] = p[1]

    def p_compound_statement(self, p):
        '''compound_statement : BEGIN statement_sequence END'''
        p[0] = ast.CompoundStatement(p[2])

    def p_statement_sequence(self, p):
        '''statement_sequence : statement_sequence SEMICOLON statement
                             | statement
                             | error'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] != 'error' else []
        else:
            p[0] = p[1] + [p[3]] if p[3] != 'error' else p[1]

    def p_statement(self, p):
        '''statement : open_statement
                    | closed_statement'''
        p[0] = p[1]

    def p_open_statement(self, p):
        '''open_statement : open_if_statement
                        | open_while_statement
                        | open_for_statement'''
        p[0] = p[1]

    def p_closed_statement(self, p):
        '''closed_statement : assignment_statement
                            | compound_statement
                            | closed_if_statement
                            | closed_while_statement
                            | closed_for_statement
                            | procedure_statement
                            | empty'''
        p[0] = p[1] if p[1] is not None else ast.CompoundStatement([])

    def p_open_while_statement(self, p):
        '''open_while_statement : WHILE boolean_expression DO open_statement'''
        p[0] = ast.WhileStatement(p[2], p[4])

    def p_closed_while_statement(self, p):
        '''closed_while_statement : WHILE boolean_expression DO closed_statement'''
        p[0] = ast.WhileStatement(p[2], p[4])

    def p_open_for_statement(self, p):
        '''open_for_statement : FOR control_variable ASSIGNMENT initial_value direction final_value DO open_statement'''
        p[0] = ast.ForStatement(p[2], p[4], p[5], p[6], p[8])

    def p_closed_for_statement(self, p):
        '''closed_for_statement : FOR control_variable ASSIGNMENT initial_value direction final_value DO closed_statement'''
        p[0] = ast.ForStatement(p[2], p[4], p[5], p[6], p[8])

    def p_open_if_statement(self, p):
        '''open_if_statement : IF boolean_expression THEN statement
                            | IF boolean_expression THEN closed_statement ELSE open_statement'''
        if len(p) == 5:
            p[0] = ast.IfStatement(p[2], p[4])
        else:
            p[0] = ast.IfStatement(p[2], p[4], p[6])

    def p_closed_if_statement(self, p):
        '''closed_if_statement : IF boolean_expression THEN closed_statement ELSE closed_statement'''
        p[0] = ast.IfStatement(p[2], p[4], p[6])

    def p_assignment_statement(self, p):
        '''assignment_statement : variable_access ASSIGNMENT expression'''
        p[0] = ast.AssignmentStatement(p[1], p[3])
    
    def p_procedure_statement(self, p):
        '''procedure_statement : identifier params
                            | identifier'''
        if len(p) == 3:
            p[0] = ast.ProcedureCall(p[1], p[2])
        else:
            p[0] = ast.ProcedureCall(p[1], None)

    def p_variable_access(self, p):
        '''variable_access : identifier
                          | indexed_variable
                          | field_designator
                          | variable_access UPARROW'''
        if len(p) == 2:
            if isinstance(p[1], tuple) and p[1][0] == 'identifier':
                p[0] = ast.VariableAccess(p[1])
            else:
                p[0] = p[1]
        else:
            p[0] = ast.PointerDereference(p[1])

    def p_indexed_variable(self, p):
        '''indexed_variable : variable_access LBRAC index_expression_list RBRAC'''
        p[0] = ast.IndexedVariable(p[1], p[3])

    def p_index_expression_list(self, p):
        '''index_expression_list : index_expression_list COMMA index_expression
                                | index_expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_index_expression(self, p):
        '''index_expression : expression'''
        p[0] = p[1]

    def p_field_designator(self, p):
        '''field_designator : variable_access DOT identifier'''
        p[0] = ast.FieldDesignator(p[1], p[3])

    def p_params(self, p):
        '''params : LPAREN actual_parameter_list RPAREN'''
        p[0] = ('params', p[2])

    def p_actual_parameter_list(self, p):
        '''actual_parameter_list : actual_parameter_list COMMA actual_parameter
                                | actual_parameter'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_actual_parameter(self, p):
        '''actual_parameter : expression
                          | expression COLON expression
                          | expression COLON expression COLON expression'''
        if len(p) == 2:
            p[0] = ('actual_parameter', p[1])
        elif len(p) == 4:
            p[0] = ('actual_parameter_range', p[1], p[3])
        else:
            p[0] = ('actual_parameter_multirange', p[1], p[3], p[5])

    def p_control_variable(self, p):
        '''control_variable : identifier'''
        p[0] = p[1]

    def p_initial_value(self, p):
        '''initial_value : expression'''
        p[0] = p[1]

    def p_direction(self, p):
        '''direction : TO
                    | DOWNTO'''
        p[0] = ('direction', p[1])

    def p_final_value(self, p):
        '''final_value : expression'''
        p[0] = p[1]

    def p_boolean_expression(self, p):
        '''boolean_expression : expression'''
        p[0] = p[1]

    def p_expression(self, p):
        '''expression : simple_expression
                    | simple_expression relop simple_expression
                    | error'''
        if len(p) == 2:
            p[0] = p[1] if p[1] != 'error' else None
        else:
            p[0] = ast.BinaryExpression(p[2], p[1], p[3])

    def p_simple_expression(self, p):
        '''simple_expression : term
                           | simple_expression addop term'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.BinaryExpression(p[2], p[1], p[3])

    def p_term(self, p):
        '''term : factor
               | term mulop factor'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.BinaryExpression(p[2], p[1], p[3])

    def p_factor(self, p):
        '''factor : sign factor
                 | exponentiation'''
        if len(p) == 3:
            p[0] = ast.SignedExpression(p[1], p[2])
        else:
            p[0] = p[1]

    def p_exponentiation(self, p):
        '''exponentiation : primary
                        | primary STARSTAR exponentiation'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.Exponentiation(p[1], p[3])

    def p_primary(self, p):
        '''primary : variable_access
                  | unsigned_constant
                  | function_designator
                  | set_constructor
                  | LPAREN expression RPAREN
                  | NOT primary'''
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = ast.NotExpression(p[2])

    def p_unsigned_constant(self, p):
        '''unsigned_constant : unsigned_number
                           | CHARACTER_STRING
                           | NIL'''
        p[0] = ast.Constant(('constant', p[1]))

    def p_unsigned_number(self, p):
        '''unsigned_number : unsigned_integer
                          | unsigned_real'''
        p[0] = p[1]

    def p_unsigned_integer(self, p):
        '''unsigned_integer : DIGSEQ'''
        p[0] = ('integer', p[1])

    def p_unsigned_real(self, p):
        '''unsigned_real : REALNUMBER'''
        p[0] = ('real', p[1])

    def p_function_designator(self, p):
        '''function_designator : identifier params'''
        p[0] = ast.FunctionCall(p[1], p[2])

    def p_set_constructor(self, p):
        '''set_constructor : LBRAC member_designator_list RBRAC
                          | LBRAC RBRAC'''
        if len(p) == 4:
            p[0] = ast.SetConstructor(p[2])
        else:
            p[0] = ast.SetConstructor(None)

    def p_member_designator_list(self, p):
        '''member_designator_list : member_designator_list COMMA member_designator
                                 | member_designator'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_member_designator(self, p):
        '''member_designator : member_designator DOTDOT expression
                            | expression'''
        if len(p) == 2:
            p[0] = ('set_member', p[1])
        else:
            p[0] = ('set_range', p[1], p[3])

    def p_sign(self, p):
        '''sign : PLUS
                | MINUS'''
        p[0] = ('sign', p[1])

    def p_addop(self, p):
        '''addop : PLUS
                | MINUS
                | OR'''
        p[0] = ('addop', p[1])

    def p_mulop(self, p):
        '''mulop : STAR
                | SLASH
                | DIV
                | MOD
                | AND'''
        p[0] = ('mulop', p[1])

    def p_relop(self, p):
        '''relop : EQUAL
                | NOTEQUAL
                | LT
                | GT
                | LE
                | GE
                | IN'''
        p[0] = ('relop', p[1])

    def p_type_denoter(self, p):
        '''type_denoter : TREAL
                       | TINTEGER
                       | TBOOLEAN
                       | TSTRING
                       | TCHAR
                       | array_type'''
        p[0] = ('type', p[1])
    
    def p_array_type(self, p):
        '''array_type : ARRAY LBRAC index_range RBRAC OF type_denoter'''
        p[0] = ast.ArrayType(p[3], p[6])
    
    def p_index_range(self, p):
        '''index_range : simple_expression DOTDOT simple_expression'''
        p[0] = ('index_range', p[1], p[3])

    def p_identifier(self, p):
        '''identifier : IDENTIFIER'''
        p[0] = ('identifier', p[1])

    def p_empty(self, p):
        '''empty :'''
        p[0] = None

    def p_error(self, p):
        self.error_count += 1
        if p:
            print(f"Syntax error at line {p.lineno}, token {p.type} ('{p.value}')")
        else:
            print("Syntax error at EOF")