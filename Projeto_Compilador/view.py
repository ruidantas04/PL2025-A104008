from typing import List, Optional
from syntax import *

class ASTPrinter(Translator[str]):
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size
        self.current_indent = 0

    def _indent(self):
        self.current_indent += self.indent_size

    def _dedent(self):
        self.current_indent -= self.indent_size

    def _make_indent(self) -> str:
        return " " * self.current_indent

    def visit_program(self, program: Program) -> str:
        heading = f"{self._make_indent()}Program:\n"
        self._indent()
        heading += f"{self._make_indent()}Heading: {program.heading}\n"
        heading += f"{self._make_indent()}Block:\n"
        self._indent()
        heading += program.block.evaluate(self)
        self._dedent()
        self._dedent()
        return heading

    def visit_block(self, block: Block) -> str:
        result = ""
        
        if block.functions:
            result += f"{self._make_indent()}Functions:\n"
            self._indent()
            for func in block.functions:
                result += func.evaluate(self)
            self._dedent()
        
        if block.variables:
            result += f"{self._make_indent()}Variables:\n"
            self._indent()
            for var in block.variables:
                result += var.evaluate(self)
            self._dedent()
        
        result += f"{self._make_indent()}Statements:\n"
        self._indent()
        result += block.statements.evaluate(self)
        self._dedent()
        
        return result

    def visit_function_declaration(self, func_decl: FunctionDeclaration) -> str:
        result = f"{self._make_indent()}FunctionDeclaration:\n"
        self._indent()
        result += f"{self._make_indent()}Heading: {func_decl.heading}\n"
        result += f"{self._make_indent()}Body:\n"
        self._indent()
        if isinstance(func_decl.body, Block):
            result += func_decl.body.evaluate(self)
        else:
            result += f"{self._make_indent()}{func_decl.body}\n"
        self._dedent()
        self._dedent()
        return result

    def visit_variable_declaration(self, var_decl: VariableDeclaration) -> str:
        result = f"{self._make_indent()}VariableDeclaration:\n"
        self._indent()
        result += f"{self._make_indent()}Identifiers: {var_decl.identifiers}\n"
        result += f"{self._make_indent()}Type:\n"
        self._indent()
        if isinstance(var_decl.type_denoter, ArrayType):
            result += var_decl.type_denoter.evaluate(self)
        elif isinstance(var_decl.type_denoter, tuple) and var_decl.type_denoter[0] == 'type':
            result += f"{self._make_indent()}{var_decl.type_denoter[1]}\n"
        else:
            result += f"{self._make_indent()}{var_decl.type_denoter}\n"
        self._dedent()
        self._dedent()
        return result

    def visit_compound_statement(self, compound_stmt: CompoundStatement) -> str:
        if not compound_stmt.statements:
            return ""
            
        result = f"{self._make_indent()}CompoundStatement:\n"
        self._indent()
        for stmt in compound_stmt.statements:
            result += stmt.evaluate(self)
        self._dedent()
        return result

    def visit_assignment_statement(self, assign_stmt: AssignmentStatement) -> str:
        result = f"{self._make_indent()}AssignmentStatement:\n"
        self._indent()
        result += f"{self._make_indent()}Variable:\n"
        self._indent()
        result += assign_stmt.variable.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Expression:\n"
        self._indent()
        result += assign_stmt.expression.evaluate(self)
        self._dedent()
        self._dedent()
        return result

    def visit_if_statement(self, if_stmt: IfStatement) -> str:
        result = f"{self._make_indent()}IfStatement:\n"
        self._indent()
        result += f"{self._make_indent()}Condition:\n"
        self._indent()
        result += if_stmt.condition.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Then:\n"
        self._indent()
        result += if_stmt.then_stmt.evaluate(self)
        self._dedent()
        if if_stmt.else_stmt:
            result += f"{self._make_indent()}Else:\n"
            self._indent()
            result += if_stmt.else_stmt.evaluate(self)
            self._dedent()
        self._dedent()
        return result

    def visit_while_statement(self, while_stmt: WhileStatement) -> str:
        result = f"{self._make_indent()}WhileStatement:\n"
        self._indent()
        result += f"{self._make_indent()}Condition:\n"
        self._indent()
        result += while_stmt.condition.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Body:\n"
        self._indent()
        result += while_stmt.body.evaluate(self)
        self._dedent()
        self._dedent()
        return result

    def visit_for_statement(self, for_stmt: ForStatement) -> str:
        result = f"{self._make_indent()}ForStatement:\n"
        self._indent()
        result += f"{self._make_indent()}ControlVar: {for_stmt.control_var}\n"
        result += f"{self._make_indent()}InitialValue:\n"
        self._indent()
        result += for_stmt.initial_value.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Direction: {for_stmt.direction}\n"
        result += f"{self._make_indent()}FinalValue:\n"
        self._indent()
        result += for_stmt.final_value.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Body:\n"
        self._indent()
        result += for_stmt.body.evaluate(self)
        self._dedent()
        self._dedent()
        return result

    def visit_variable_access(self, var_access: VariableAccess) -> str:
        return f"{self._make_indent()}VariableAccess: {var_access.identifier}\n"

    def visit_function_call(self, func_call: FunctionCall) -> str:
        result = f"{self._make_indent()}FunctionCall:\n"
        self._indent()
        result += f"{self._make_indent()}Function: {func_call.identifier}\n"
        if func_call.params:
            result += f"{self._make_indent()}Params:\n"
            self._indent()
            if isinstance(func_call.params, tuple) and func_call.params[0] == 'params':
                for param in func_call.params[1]:
                    if isinstance(param, Expression):
                        result += param.evaluate(self)
                    else:
                        result += f"{self._make_indent()}{param}\n"
            else:
                result += f"{self._make_indent()}{func_call.params}\n"
            self._dedent()
        self._dedent()
        return result

    def visit_procedure_call(self, proc_call: ProcedureCall) -> str:
        result = f"{self._make_indent()}ProcedureCall: {proc_call.identifier[1]}\n"
        if proc_call.args is not None:
            self._indent()
            result += f"{self._make_indent()}Arguments:\n"
            self._indent()
            if isinstance(proc_call.args, tuple) and proc_call.args[0] == 'params':
                for arg in proc_call.args[1]:
                    if isinstance(arg, Expression):
                        result += arg.evaluate(self)
                    else:
                        result += f"{self._make_indent()}{arg}\n"
            else:
                result += f"{self._make_indent()}{proc_call.args}\n"
            self._dedent()
            self._dedent()
        return result

    def visit_binary_expression(self, bin_expr: BinaryExpression) -> str:
        result = f"{self._make_indent()}BinaryExpression ({bin_expr.operator[1]}):\n"
        self._indent()
        result += f"{self._make_indent()}Left:\n"
        self._indent()
        result += bin_expr.left.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Right:\n"
        self._indent()
        result += bin_expr.right.evaluate(self)
        self._dedent()
        self._dedent()
        return result

    def visit_signed_expression(self, signed_expr: SignedExpression) -> str:
        result = f"{self._make_indent()}SignedExpression ({signed_expr.sign[1]}):\n"
        self._indent()
        result += signed_expr.expression.evaluate(self)
        self._dedent()
        return result

    def visit_exponentiation(self, exponentiation: Exponentiation) -> str:
        result = f"{self._make_indent()}Exponentiation:\n"
        self._indent()
        result += f"{self._make_indent()}Base:\n"
        self._indent()
        result += exponentiation.base.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Exponent:\n"
        self._indent()
        result += exponentiation.exponent.evaluate(self)
        self._dedent()
        self._dedent()
        return result

    def visit_not_expression(self, not_expr: NotExpression) -> str:
        result = f"{self._make_indent()}NotExpression:\n"
        self._indent()
        result += not_expr.expression.evaluate(self)
        self._dedent()
        return result

    def visit_constant(self, constant: Constant) -> str:
        return f"{self._make_indent()}Constant: {constant.value}\n"

    def visit_set_constructor(self, set_constr: SetConstructor) -> str:
        result = f"{self._make_indent()}SetConstructor:\n"
        if set_constr.members:
            self._indent()
            for member in set_constr.members:
                if isinstance(member, tuple):
                    result += f"{self._make_indent()}{member}\n"
                else:
                    result += member.evaluate(self)
            self._dedent()
        return result

    def visit_pointer_dereference(self, ptr_deref: PointerDereference) -> str:
        result = f"{self._make_indent()}PointerDereference:\n"
        self._indent()
        result += ptr_deref.variable.evaluate(self)
        self._dedent()
        return result

    def visit_indexed_variable(self, indexed_var: IndexedVariable) -> str:
        result = f"{self._make_indent()}IndexedVariable:\n"
        self._indent()
        result += f"{self._make_indent()}Variable:\n"
        self._indent()
        result += indexed_var.variable.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Indices:\n"
        self._indent()
        if isinstance(indexed_var.indices, list):
            for idx in indexed_var.indices:
                if isinstance(idx, Expression):
                    result += idx.evaluate(self)
                else:
                    result += f"{self._make_indent()}{idx}\n"
        else:
            result += f"{self._make_indent()}{indexed_var.indices}\n"
        self._dedent()
        self._dedent()
        return result

    def visit_field_designator(self, field_des: FieldDesignator) -> str:
        result = f"{self._make_indent()}FieldDesignator:\n"
        self._indent()
        result += f"{self._make_indent()}Variable:\n"
        self._indent()
        result += field_des.variable.evaluate(self)
        self._dedent()
        result += f"{self._make_indent()}Field: {field_des.field}\n"
        self._dedent()
        return result
    
    def visit_array_type(self, array_type: ArrayType) -> str:
        result = f"{self._make_indent()}ArrayType:\n"
        self._indent()
        result += f"{self._make_indent()}Index Range:\n"
        self._indent()
        if isinstance(array_type.index_range, tuple) and array_type.index_range[0] == 'index_range':
            result += f"{self._make_indent()}From: {array_type.index_range[1]}\n"
            result += f"{self._make_indent()}To: {array_type.index_range[2]}\n"
        else:
            result += f"{self._make_indent()}{array_type.index_range}\n"
        self._dedent()
        result += f"{self._make_indent()}Element Type:\n"
        self._indent()
        if isinstance(array_type.element_type, tuple) and array_type.element_type[0] == 'type':
            result += f"{self._make_indent()}{array_type.element_type[1]}\n"
        else:
            result += array_type.element_type.evaluate(self)
        self._dedent()
        self._dedent()
        return result

    def visit_ast(self, ast: AbstractSyntaxTree) -> str:
        return ast.program.evaluate(self)

    def translate(self, ast: AbstractSyntaxTree) -> str:
        return self.visit_ast(ast)


def print_ast(ast: AbstractSyntaxTree, indent_size: int = 2):
    printer = ASTPrinter(indent_size)
    print(printer.translate(ast))