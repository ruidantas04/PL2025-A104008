from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, List, Optional, TypeVar, override

T = TypeVar("T", bound="Translator")


class Translator(ABC, Generic[T]):
    @abstractmethod
    def visit_program(self, program: Program) -> T:
        pass

    @abstractmethod
    def visit_block(self, block: Block) -> T:
        pass

    @abstractmethod
    def visit_function_declaration(self, function_declaration: FunctionDeclaration) -> T:
        pass

    @abstractmethod
    def visit_variable_declaration(self, variable_declaration: VariableDeclaration) -> T:
        pass
    
    @abstractmethod
    def visit_procedure_call(self, procedure_call: ProcedureCall) -> T:
        pass

    @abstractmethod
    def visit_compound_statement(self, compound_statement: CompoundStatement) -> T:
        pass

    @abstractmethod
    def visit_assignment_statement(self, assignment_statement: AssignmentStatement) -> T:
        pass

    @abstractmethod
    def visit_if_statement(self, if_statement: IfStatement) -> T:
        pass

    @abstractmethod
    def visit_while_statement(self, while_statement: WhileStatement) -> T:
        pass

    @abstractmethod
    def visit_for_statement(self, for_statement: ForStatement) -> T:
        pass

    @abstractmethod
    def visit_variable_access(self, variable_access: VariableAccess) -> T:
        pass

    @abstractmethod
    def visit_binary_expression(self, binary_expression: BinaryExpression) -> T:
        pass

    @abstractmethod
    def visit_signed_expression(self, signed_expression: SignedExpression) -> T:
        pass

    @abstractmethod
    def visit_exponentiation(self, exponentiation: Exponentiation) -> T:
        pass

    @abstractmethod
    def visit_not_expression(self, not_expression: NotExpression) -> T:
        pass

    @abstractmethod
    def visit_constant(self, constant: Constant) -> T:
        pass

    @abstractmethod
    def visit_set_constructor(self, set_constructor: SetConstructor) -> T:
        pass

    @abstractmethod
    def visit_pointer_dereference(self, pointer_dereference: PointerDereference) -> T:
        pass

    @abstractmethod
    def visit_indexed_variable(self, indexed_variable: IndexedVariable) -> T:
        pass

    @abstractmethod
    def visit_field_designator(self, field_designator: FieldDesignator) -> T:
        pass

    @abstractmethod
    def visit_array_type(self, array_type: ArrayType) -> T:
        pass

    @abstractmethod
    def visit_ast(self, ast: AbstractSyntaxTree) -> T:
        pass

    @abstractmethod
    def translate(self, ast: AbstractSyntaxTree) -> T:
        pass


class TranslationError(Exception):
    pass

class Expression(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def evaluate(self, translator: Translator):
        pass

class Statement(Expression):
    pass 

class Program(Expression):
    def __init__(self, heading: tuple, block: 'Block'):
        super().__init__()
        self.heading = heading
        self.block = block

    @override
    def __repr__(self):
        return f"Program(heading={self.heading}, block={self.block})"

    @override
    def __eq__(self, other):
        return isinstance(other, Program) and self.heading == other.heading and self.block == other.block

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_program(self)


class Block(Expression):
    def __init__(self, functions: Optional[List['FunctionDeclaration']], variables: Optional[List['VariableDeclaration']], statements: 'CompoundStatement'):
        super().__init__()
        self.functions = functions
        self.variables = variables
        self.statements = statements

    @override
    def __repr__(self):
        return f"Block(functions={self.functions}, variables={self.variables}, statements={self.statements})"

    @override
    def __eq__(self, other):
        return isinstance(other, Block) and self.functions == other.functions and self.variables == other.variables and self.statements == other.statements

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_block(self)


class FunctionDeclaration(Expression):
    def __init__(self, heading: tuple, body: 'Block' | tuple, local_variables: Optional[List['VariableDeclaration']] = None):
        super().__init__()
        self.heading = heading
        self.body = body
        self.local_variables = local_variables or []

    def __repr__(self):
        return f"FunctionDeclaration(heading={self.heading}, local_variables={self.local_variables}, body={self.body})"

    def __eq__(self, other):
        return isinstance(other, FunctionDeclaration) and self.heading == other.heading and self.local_variables == other.local_variables and self.body == other.body

    def evaluate(self, translator: Translator):
        return translator.visit_function_declaration(self)


class VariableDeclaration(Expression):
    def __init__(self, identifiers: List[tuple], type_denoter: tuple):
        super().__init__()
        self.identifiers = identifiers
        self.type_denoter = type_denoter

    @override
    def __repr__(self):
        return f"VariableDeclaration(identifiers={self.identifiers}, type={self.type_denoter})"

    @override
    def __eq__(self, other):
        return isinstance(other, VariableDeclaration) and self.identifiers == other.identifiers and self.type_denoter == other.type_denoter

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_variable_declaration(self)

class ProcedureCall:
    def __init__(self, identifier, args):
        super().__init__()
        self.identifier = identifier 
        self.args = args             

    @override
    def __repr__(self):
        args_str = f", args={self.args}" if self.args is not None else ""
        return f"ProcedureCall({self.identifier[1]}{args_str})"
    
    def evaluate(self, translator: Translator):
        return translator.visit_procedure_call(self)

class CompoundStatement(Expression):
    def __init__(self, statements: List['Statement']):
        super().__init__()
        self.statements = statements or []

    @override
    def __repr__(self):
        if self.statements:
            return f"CompoundStatement(statements={self.statements})"
        return ""

    @override
    def __eq__(self, other):
        return isinstance(other, CompoundStatement) and self.statements == other.statements

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_compound_statement(self)

class AssignmentStatement(Statement):
    def __init__(self, variable: 'VariableAccess', expression: Expression):
        super().__init__()
        self.variable = variable
        self.expression = expression

    @override
    def __repr__(self):
        return f"AssignmentStatement(variable={self.variable}, expression={self.expression})"

    @override
    def __eq__(self, other):
        return isinstance(other, AssignmentStatement) and self.variable == other.variable and self.expression == other.expression

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_assignment_statement(self)


class IfStatement(Statement):
    def __init__(self, condition: Expression, then_stmt: Statement, else_stmt: Optional[Statement] = None):
        super().__init__()
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    @override
    def __repr__(self):
        return f"IfStatement(condition={self.condition}, then={self.then_stmt}, else={self.else_stmt})"

    @override
    def __eq__(self, other):
        return isinstance(other, IfStatement) and self.condition == other.condition and self.then_stmt == other.then_stmt and self.else_stmt == other.else_stmt

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_if_statement(self)


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement):
        super().__init__()
        self.condition = condition
        self.body = body

    @override
    def __repr__(self):
        return f"WhileStatement(condition={self.condition}, body={self.body})"

    @override
    def __eq__(self, other):
        return isinstance(other, WhileStatement) and self.condition == other.condition and self.body == other.body

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_while_statement(self)


class ForStatement(Statement):
    def __init__(self, control_var: tuple, initial_value: Expression, direction: tuple, final_value: Expression, body: Statement):
        super().__init__()
        self.control_var = control_var
        self.initial_value = initial_value
        self.direction = direction
        self.final_value = final_value
        self.body = body

    @override
    def __repr__(self):
        return f"ForStatement(control_var={self.control_var}, initial={self.initial_value}, direction={self.direction}, final={self.final_value}, body={self.body})"

    @override
    def __eq__(self, other):
        return isinstance(other, ForStatement) and self.control_var == other.control_var and self.initial_value == other.initial_value and self.direction == other.direction and self.final_value == other.final_value and self.body == other.body

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_for_statement(self)


class VariableAccess(Expression):
    def __init__(self, identifier: tuple):
        super().__init__()
        self.identifier = identifier

    @override
    def __repr__(self):
        return f"VariableAccess(identifier={self.identifier})"

    @override
    def __eq__(self, other):
        return isinstance(other, VariableAccess) and self.identifier == other.identifier

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_variable_access(self)


class FunctionCall(Expression):
    def __init__(self, identifier: tuple, params: tuple):
        super().__init__()
        self.identifier = identifier
        self.params = params

    @override
    def __repr__(self):
        return f"FunctionCall(identifier={self.identifier}, params={self.params})"

    @override
    def __eq__(self, other):
        return isinstance(other, FunctionCall) and self.identifier == other.identifier and self.params == other.params

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_function_call(self)

class BinaryExpression(Expression):
    def __init__(self, operator: tuple, left: Expression, right: Expression):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right

    @override
    def __repr__(self):
        return f"BinaryExpression(operator={self.operator}, left={self.left}, right={self.right})"

    @override
    def __eq__(self, other):
        return isinstance(other, BinaryExpression) and self.operator == other.operator and self.left == other.left and self.right == other.right

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_binary_expression(self)


class SignedExpression(Expression):
    def __init__(self, sign: tuple, expression: Expression):
        super().__init__()
        self.sign = sign
        self.expression = expression

    @override
    def __repr__(self):
        return f"SignedExpression(sign={self.sign}, expression={self.expression})"

    @override
    def __eq__(self, other):
        return isinstance(other, SignedExpression) and self.sign == other.sign and self.expression == other.expression

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_signed_expression(self)


class Exponentiation(Expression):
    def __init__(self, base: Expression, exponent: Expression):
        super().__init__()
        self.base = base
        self.exponent = exponent

    @override
    def __repr__(self):
        return f"Exponentiation(base={self.base}, exponent={self.exponent})"

    @override
    def __eq__(self, other):
        return isinstance(other, Exponentiation) and self.base == other.base and self.exponent == other.exponent

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_exponentiation(self)


class NotExpression(Expression):
    def __init__(self, expression: Expression):
        super().__init__()
        self.expression = expression

    @override
    def __repr__(self):
        return f"NotExpression(expression={self.expression})"

    @override
    def __eq__(self, other):
        return isinstance(other, NotExpression) and self.expression == other.expression

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_not_expression(self)


class Constant(Expression):
    def __init__(self, value: tuple):
        super().__init__()
        self.value = value

    @override
    def __repr__(self):
        return f"Constant(value={self.value})"

    @override
    def __eq__(self, other):
        return isinstance(other, Constant) and self.value == other.value

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_constant(self)


class SetConstructor(Expression):
    def __init__(self, members: Optional[List[tuple]]):
        super().__init__()
        self.members = members

    @override
    def __repr__(self):
        return f"SetConstructor(members={self.members})"

    @override
    def __eq__(self, other):
        return isinstance(other, SetConstructor) and self.members == other.members

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_set_constructor(self)


class PointerDereference(Expression):
    def __init__(self, variable: 'VariableAccess'):
        super().__init__()
        self.variable = variable

    @override
    def __repr__(self):
        return f"PointerDereference(variable={self.variable})"

    @override
    def __eq__(self, other):
        return isinstance(other, PointerDereference) and self.variable == other.variable

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_pointer_dereference(self)


class IndexedVariable(Expression):
    def __init__(self, variable: 'VariableAccess', indices: List[Expression]):
        super().__init__()
        self.variable = variable
        self.indices = indices

    @override
    def __repr__(self):
        return f"IndexedVariable(variable={self.variable}, indices={self.indices})"

    @override
    def __eq__(self, other):
        return isinstance(other, IndexedVariable) and self.variable == other.variable and self.indices == other.indices

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_indexed_variable(self)


class FieldDesignator(Expression):
    def __init__(self, variable: 'VariableAccess', field: tuple):
        super().__init__()
        self.variable = variable
        self.field = field

    @override
    def __repr__(self):
        return f"FieldDesignator(variable={self.variable}, field={self.field})"

    @override
    def __eq__(self, other):
        return isinstance(other, FieldDesignator) and self.variable == other.variable and self.field == other.field

    @override
    def evaluate(self, translator: Translator):
        return translator.visit_field_designator(self)

class ArrayType:
    def __init__(self, index_range, element_type):
        self.index_range = index_range  
        self.element_type = element_type  

    @override  
    def __repr__(self):
        return f"Array[{self.index_range[1]}..{self.index_range[2]}] of {self.element_type}"
    
    @override
    def evaluate(self, translator: Translator):
        return translator.visit_array_type(self)


class AbstractSyntaxTree:
    def __init__(self, program: Program):
        self.program = program

    @override
    def __repr__(self):
        return f"AST(program={self.program})"

    @override
    def __eq__(self, other):
        return isinstance(other, AbstractSyntaxTree) and self.program == other.program

    def evaluate(self, translator: Translator):
        return translator.visit_ast(self)