# Complete Pascal Grammar

program -> program_heading semicolon block DOT

program_heading -> PROGRAM identifier 
                 | PROGRAM identifier LPAREN identifier_list RPAREN

identifier_list -> identifier_list comma identifier 
                 | identifier

block -> procedure_and_function_declaration_part variable_declaration_part statement_part

procedure_and_function_declaration_part -> proc_or_func_declaration_list semicolon 
                                         | ε

proc_or_func_declaration_list -> proc_or_func_declaration_list semicolon proc_or_func_declaration 
                               | proc_or_func_declaration

proc_or_func_declaration -> procedure_declaration 
                          | function_declaration

procedure_declaration -> procedure_heading semicolon directive 
                       | procedure_heading semicolon procedure_block

procedure_heading -> procedure_identification 
                   | procedure_identification formal_parameter_list

directive -> FORWARD 
           | EXTERNAL

formal_parameter_list -> LPAREN formal_parameter_section_list RPAREN

formal_parameter_section_list -> formal_parameter_section_list semicolon formal_parameter_section 
                               | formal_parameter_section

formal_parameter_section -> value_parameter_specification 
                          | variable_parameter_specification 
                          | procedural_parameter_specification 
                          | functional_parameter_specification

value_parameter_specification -> identifier_list COLON type_denoter
variable_parameter_specification -> VAR identifier_list COLON type_denoter
procedural_parameter_specification -> procedure_heading
functional_parameter_specification -> function_heading

procedure_identification -> PROCEDURE identifier
procedure_block -> block

function_declaration -> function_heading semicolon directive 
                      | function_identification semicolon function_block 
                      | function_heading semicolon function_block

function_heading -> FUNCTION identifier COLON type_denoter
                   | FUNCTION identifier formal_parameter_list COLON type_denoter

function_identification -> FUNCTION identifier
function_block -> block

variable_declaration_part -> VAR variable_declaration_list semicolon 
                           | ε

variable_declaration_list -> variable_declaration_list semicolon variable_declaration 
                           | variable_declaration

variable_declaration -> identifier_list COLON type_denoter

statement_part -> compound_statement

compound_statement -> BEGIN statement_sequence END

statement_sequence -> statement_sequence semicolon statement 
                    | statement 
                    | error 

statement -> open_statement 
            | closed_statement

open_statement -> open_if_statement 
              | open_while_statement 
              | open_for_statement

closed_statement ->  assignment_statement 
                     | compound_statement 
                     | closed_if_statement 
                     | closed_while_statement 
                     | closed_for_statement
                     | procedure_statement 
                     | ε

open_while_statement -> WHILE boolean_expression DO open_statement
closed_while_statement -> WHILE boolean_expression DO closed_statement

open_for_statement -> FOR control_variable ASSIGNMENT initial_value direction final_value DO open_statement
closed_for_statement -> FOR control_variable ASSIGNMENT initial_value direction final_value DO closed_statement

open_if_statement -> IF boolean_expression THEN statement 
                   | IF boolean_expression THEN closed_statement ELSE open_statement
closed_if_statement -> IF boolean_expression THEN closed_statement ELSE closed_statement

assignment_statement -> variable_access ASSIGNMENT expression

variable_access -> identifier 
                 | indexed_variable 
                 | field_designator 
                 | variable_access UPARROW

indexed_variable -> variable_access LBRAC index_expression_list RBRAC
index_expression_list -> index_expression_list comma index_expression 
                       | index_expression
index_expression -> expression

field_designator -> variable_access DOT identifier

procedure_statement -> identifier params 
                     | identifier
                     
params -> LPAREN actual_parameter_list RPAREN
actual_parameter_list -> actual_parameter_list comma actual_parameter 
                       | actual_parameter

actual_parameter -> expression 
                 | expression COLON expression 
                 | expression COLON expression COLON expression

control_variable -> identifier

initial_value -> expression

direction -> TO 
            | DOWNTO

final_value -> expression

boolean_expression -> expression

expression -> simple_expression 
            | simple_expression relop simple_expression 
            | error

simple_expression -> term 
                   | simple_expression addop term

term -> factor 
       | term mulop factor

factor -> sign factor 
         | exponentiation

exponentiation -> primary 
                | primary STARSTAR exponentiation

primary -> variable_access 
         | unsigned_constant 
         | function_designator 
         | set_constructor 
         | LPAREN expression RPAREN 
         | NOT primary

unsigned_constant -> unsigned_number 
                   | CHARACTER_STRING 
                   | NIL

unsigned_number -> unsigned_integer 
                 | unsigned_real

unsigned_integer -> DIGSEQ

unsigned_real -> REALNUMBER

function_designator -> identifier params

set_constructor -> LBRAC member_designator_list RBRAC 
                 | LBRAC RBRAC

member_designator_list -> member_designator_list comma member_designator 
                        | member_designator

member_designator -> member_designator DOTDOT expression 
                   | expression

addop -> PLUS 
       | MINUS 
       | OR

mulop -> STAR 
       | SLASH 
       | DIV 
       | MOD 
       | AND

relop -> EQUAL 
       | NOTEQUAL 
       | LT 
       | GT 
       | LE 
       | GE 
       | IN

type_denoter -> TREAL
              | TINTEGER
              | TBOOLEAN
              | TSTRING
              | TCHAR
              | ARRAY LBRAC index_range RBRAC OF type_denoter

index_range -> simple_expression DOTDOT simple_expression

identifier -> IDENTIFIER

semicolon -> SEMICOLON

comma -> COMMA
