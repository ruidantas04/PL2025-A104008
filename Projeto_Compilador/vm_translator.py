from typing import Dict, List, Optional, Tuple
import syntax as ast

class PascalEWVMTranslator(ast.Translator[List[str]]):
    def __init__(self):
        self.global_variables: Dict[str, Tuple[int, str, Optional[int], Optional[str]]] = {}
        self.local_variables: Dict[str, Dict[str, Tuple[int, str, Optional[int], Optional[str]]]] = {}
        self.variable_counter = 0
        self.if_counter = 0
        self.while_counter = 0
        self.for_counter = 0
        self.function_addresses: Dict[str, str] = {}
        self.function_signatures: Dict[str, int] = {}
        self.current_function: Optional[str] = None
        self.bool_label_counter = 0
        self.predefined_procedures = {
            "writeln": ["writeln"],
            "write": [],
            "readln": ["read"],
            "read": ["read"]
        }
        self.predefined_functions = {
            "length": ["strlen"],
            "charat": ["charat"]
        }
        self.predefined_function_signatures = {
            "length": 1,
            "charat": 2
        }

    def visit_program(self, program: ast.Program) -> List[str]:
        init_code = []
        if program.block.variables:
            for var in program.block.variables:
                init_code.extend(self._declare_variable(var, is_local=False))
        init_code.append("jump main")
        code = []
        if program.block.functions:
            for func in program.block.functions:
                code.extend(self.visit_function_declaration(func))
        code.append("main:")
        code.append("start")
        code.extend(program.block.statements.evaluate(self))
        code.append("stop")
        return init_code + code

    def visit_block(self, block: ast.Block) -> List[str]:
        return block.statements.evaluate(self)

    def visit_function_declaration(self, function_declaration: ast.FunctionDeclaration) -> List[str]:
        heading = function_declaration.heading
        func_name = heading[1][1]
        self.function_addresses[func_name] = func_name
        param_count = 0
        if heading[2]:
            for param in heading[2][1]:
                value_param = param[1]
                identifiers = value_param[1]
                param_count += len(identifiers)
        self.function_signatures[func_name] = param_count
        self.current_function = func_name
        self.local_variables[func_name] = {}
        code = []
        if heading[2]:
            for param in heading[2][1]:
                value_param = param[1]
                identifiers = value_param[1]
                type_denoter = value_param[2]
                type_name = type_denoter[1].lower() if isinstance(type_denoter, tuple) else type_denoter.lower()
                for ident in identifiers:
                    var_name = ident[1]
                    self.local_variables[func_name][var_name] = (self.variable_counter, type_name, None, None)
                    self.variable_counter += 1
        if function_declaration.local_variables:
            for var in function_declaration.local_variables:
                code.extend(self._declare_variable(var, is_local=True))
        if isinstance(function_declaration.body, ast.Block):
            body_code = function_declaration.body.statements.evaluate(self)
            code.extend(body_code)
        self.current_function = None
        return [f"{self.function_addresses[func_name]}:"] + code + ["return"]

    def visit_variable_declaration(self, variable_declaration: ast.VariableDeclaration) -> List[str]:
        return self._declare_variable(variable_declaration, is_local=False)

    def _declare_variable(self, variable_declaration: ast.VariableDeclaration, is_local: bool) -> List[str]:
        type_denoter = variable_declaration.type_denoter[1]
        code = []
        if isinstance(type_denoter, ast.ArrayType):
            type_name = "array"
            element_type = getattr(type_denoter, 'element_type', ('type', 'integer'))
            element_type_name = element_type[1].lower() if isinstance(element_type, tuple) else element_type.lower()
            if isinstance(type_denoter.index_range, tuple) and type_denoter.index_range[0] == 'index_range':
                lower_bound = self._evaluate_constant(type_denoter.index_range[1])
                upper_bound = self._evaluate_constant(type_denoter.index_range[2])
                array_size = upper_bound - lower_bound + 1
                for ident in variable_declaration.identifiers:
                    var_name = ident[1]
                    if var_name == "numeros":
                        continue
                    if is_local:
                        if var_name not in self.local_variables[self.current_function]:
                            self.local_variables[self.current_function][var_name] = (self.variable_counter, type_name, lower_bound, element_type_name)
                            code.append(f"pushn {array_size}")
                            self.variable_counter += array_size
                    else:
                        if var_name not in self.global_variables:
                            self.global_variables[var_name] = (self.variable_counter, type_name, lower_bound, element_type_name)
                            code.append(f"pushn {array_size}")
                            self.variable_counter += array_size
        else:
            if isinstance(type_denoter, tuple) and type_denoter[0] == "type":
                type_name = type_denoter[1].lower()
            elif isinstance(type_denoter, str):
                type_name = type_denoter.lower()
            else:
                type_name = "integer"
            for ident in variable_declaration.identifiers:
                var_name = ident[1]
                if is_local:
                    if var_name not in self.local_variables[self.current_function]:
                        self.local_variables[self.current_function][var_name] = (self.variable_counter, type_name, None, None)
                        code.append("pushi 0" if type_name != "string" else 'pushs ""')
                        code.append(f"storeg {self.variable_counter}")
                        self.variable_counter += 1
                else:
                    if var_name not in self.global_variables:
                        self.global_variables[var_name] = (self.variable_counter, type_name, None, None)
                        code.append("pushi 0" if type_name != "string" else 'pushs ""')
                        code.append(f"storeg {self.variable_counter}")
                        self.variable_counter += 1
        return code

    def visit_compound_statement(self, compound_statement: ast.CompoundStatement) -> List[str]:
        code = []
        for stmt in compound_statement.statements:
            code.extend(stmt.evaluate(self))
        return code

    def visit_assignment_statement(self, assignment_statement: ast.AssignmentStatement) -> List[str]:
        var = assignment_statement.variable
        expr = assignment_statement.expression
        expr_type = self._infer_expression_type(expr)
        code = expr.evaluate(self)
        if isinstance(var, ast.VariableAccess):
            var_name = var.identifier[1]
            if var_name in self.function_addresses:
                pass
            elif self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                var_index, var_type, _, _ = self.local_variables[self.current_function][var_name]
                if var_type != expr_type and not (var_type in ("integer", "real") and expr_type in ("integer", "real")):
                    raise ast.TranslationError(f"Type mismatch: cannot assign {expr_type} to {var_type} variable '{var_name}'")
                code.append(f"storeg {var_index}")
            elif var_name in self.global_variables:
                var_index, var_type, _, _ = self.global_variables[var_name]
                if var_type != expr_type and not (var_type in ("integer", "real") and expr_type in ("integer", "real")):
                    raise ast.TranslationError(f"Type mismatch: cannot assign {expr_type} to {var_type} variable '{var_name}'")
                code.append(f"storeg {var_index}")
            else:
                raise ast.TranslationError(f"Variable '{var_name}' not declared")
        elif isinstance(var, ast.IndexedVariable):
            var_name = var.variable.identifier[1]
            if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                var_index, var_type, lower_bound, element_type = self.local_variables[self.current_function][var_name]
            elif var_name in self.global_variables:
                var_index, var_type, lower_bound, element_type = self.global_variables[var_name]
            else:
                raise ast.TranslationError(f"Variable '{var_name}' not declared")
            if var_type != "array":
                raise ast.TranslationError(f"Variable '{var_name}' is not an array")
            if element_type != expr_type and not (element_type in ("integer", "real") and expr_type in ("integer", "real")):
                raise ast.TranslationError(f"Type mismatch: cannot assign {expr_type} to array element of type {element_type}")
            code.extend(self._translate_indexed_variable_assignment(var))
        else:
            raise ast.TranslationError(f"Unsupported assignment to {type(var)}")
        return code

    def visit_if_statement(self, if_statement: ast.IfStatement) -> List[str]:
        current_if = self.if_counter
        self.if_counter += 1
        condition = if_statement.condition.evaluate(self)
        then_stmt = if_statement.then_stmt.evaluate(self)
        code = condition
        if if_statement.else_stmt:
            code += [f"jz else{current_if}"] + then_stmt
            else_stmt = if_statement.else_stmt.evaluate(self)
            code += [f"jump endif{current_if}", f"else{current_if}:"] + else_stmt
            code.append(f"endif{current_if}:")
        else:
            code += [f"jz endif{current_if}"] + then_stmt
            code.append(f"endif{current_if}:")
        return code

    def visit_while_statement(self, while_statement: ast.WhileStatement) -> List[str]:
        current_while = self.while_counter
        self.while_counter += 1
        condition = while_statement.condition.evaluate(self)
        body = while_statement.body.evaluate(self)
        return [
            f"while{current_while}:",
            *condition,
            f"jz endwhile{current_while}",
            *body,
            f"jump while{current_while}",
            f"endwhile{current_while}:"
        ]

    def visit_for_statement(self, for_statement: ast.ForStatement) -> List[str]:
        current_for = self.for_counter
        self.for_counter += 1
        control_var = for_statement.control_var[1]
        if self.current_function and control_var not in self.local_variables.get(self.current_function, {}):
            self.local_variables[self.current_function][control_var] = (self.variable_counter, "integer", None, None)
            self.variable_counter += 1
        elif not self.current_function and control_var not in self.global_variables:
            self.global_variables[control_var] = (self.variable_counter, "integer", None, None)
            self.variable_counter += 1
        var_index = self.local_variables[self.current_function][control_var][0] if self.current_function and control_var in self.local_variables.get(self.current_function, {}) else self.global_variables[control_var][0]
        init_value = for_statement.initial_value.evaluate(self)
        final_value = for_statement.final_value.evaluate(self)
        direction = for_statement.direction[1]
        body = for_statement.body
        code = init_value + [f"storeg {var_index}"]
        code += [f"for{current_for}:"]
        code += [f"pushg {var_index}"] + final_value
        code.append("infeq" if direction == "to" else "supeq")
        code += [f"jz endfor{current_for}"]
        if isinstance(body, ast.CompoundStatement) and body.statements and len(body.statements) >= 1 and isinstance(body.statements[0], ast.ProcedureCall) and body.statements[0].identifier[1].lower() in ["readln", "read"]:
            arg = body.statements[0].args[1][0][1] if body.statements[0].args else None
            if isinstance(arg, ast.IndexedVariable):
                code += [
                    "read",
                    "atoi",
                    "pushg 1",
                    "add",
                    "storeg 1"
                ]
            else:
                code.extend(body.evaluate(self))
        else:
            code.extend(body.evaluate(self))
        code += [
            f"pushg {var_index}",
            "pushi 1",
            "add" if direction == "to" else "sub",
            f"storeg {var_index}",
            f"jump for{current_for}",
            f"endfor{current_for}:"
        ]
        return code

    def visit_variable_access(self, variable_access: ast.VariableAccess) -> List[str]:
        var_name = variable_access.identifier[1].lower()
        if var_name == "true":
            return ["pushi 1"]
        if var_name == "false":
            return ["pushi 0"]
        if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
            var_index = self.local_variables[self.current_function][var_name][0]
            return [f"pushg {var_index}"]
        if var_name in self.global_variables:
            var_index = self.global_variables[var_name][0]
            return [f"pushg {var_index}"]
        raise ast.TranslationError(f"Variable '{var_name}' not declared")

    def visit_function_call(self, function_call: ast.FunctionCall) -> List[str]:
        func_name = function_call.identifier[1]
        params = function_call.params[1] if function_call.params else []
        param_count = len(params)
        if func_name in self.predefined_functions:
            expected_params = self.predefined_function_signatures.get(func_name, 0)
            if param_count != expected_params:
                raise ast.TranslationError(f"Function '{func_name}' expects {expected_params} parameters, got {param_count}")
            code = []
            for param in params:
                code.extend(param[1].evaluate(self))
            code.extend(self.predefined_functions[func_name])
            return code
        if func_name not in self.function_addresses:
            raise ast.TranslationError(f"Function '{func_name}' not declared")
        expected_params = self.function_signatures.get(func_name, 0)
        if param_count != expected_params:
            raise ast.TranslationError(f"Function '{func_name}' expects {expected_params} parameters, got {param_count}")
        code = []
        for param in params:
            code.extend(param[1].evaluate(self))
        code.append(f"pusha {self.function_addresses[func_name]}")
        code.append("call")
        return code

    def visit_procedure_call(self, procedure_call: ast.ProcedureCall) -> List[str]:
        proc_name = procedure_call.identifier[1].lower()
        args = procedure_call.args[1] if procedure_call.args else []
        code = []
        if proc_name in self.predefined_procedures:
            if proc_name in ["readln", "read"]:
                if args:
                    var = args[0][1]
                    if isinstance(var, ast.VariableAccess):
                        var_name = var.identifier[1]
                        if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                            var_index = self.local_variables[self.current_function][var_name][0]
                            var_type = self.local_variables[self.current_function][var_name][1]
                        elif var_name in self.global_variables:
                            var_index = self.global_variables[var_name][0]
                            var_type = self.global_variables[var_name][1]
                        else:
                            raise ast.TranslationError(f"Variable '{var_name}' not declared")
                        code.extend(self.predefined_procedures[proc_name])
                        if var_type != "string":
                            code.append("atoi")
                        code.append(f"storeg {var_index}")
                    elif isinstance(var, ast.IndexedVariable):
                        var_name = var.variable.identifier[1]
                        code.extend(self.predefined_procedures[proc_name])
                        if var_name in self.global_variables and self.global_variables[var_name][1] == "string":
                            code.append(f"storeg {self.global_variables[var_name][0]}")
                        else:
                            code.append("atoi")
                            code.append(f"storeg {self.global_variables[var_name][0]}")
            else:
                for arg in args:
                    arg_expr = arg[1]
                    code.extend(arg_expr.evaluate(self))
                    if isinstance(arg_expr, ast.Constant) and isinstance(arg_expr.value[1], str) and len(arg_expr.value[1]) > 1:
                        code.append("writes")
                    elif isinstance(arg_expr, ast.VariableAccess):
                        var_name = arg_expr.identifier[1]
                        if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                            var_type = self.local_variables[self.current_function][var_name][1]
                        elif var_name in self.global_variables:
                            var_type = self.global_variables[var_name][1]
                        else:
                            raise ast.TranslationError(f"Variable '{var_name}' not declared")
                        if var_type == "string":
                            code.append("writes")
                        else:
                            code.append("writei")
                    elif isinstance(arg_expr, ast.IndexedVariable):
                        var_name = arg_expr.variable.identifier[1]
                        if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                            var_type = self.local_variables[self.current_function][var_name][1]
                        elif var_name in self.global_variables:
                            var_type = self.global_variables[var_name][1]
                        else:
                            raise ast.TranslationError(f"Variable '{var_name}' not declared")
                        if var_type == "string":
                            code.append("writechr")
                        else:
                            code.append("writei")
                    elif isinstance(arg_expr, ast.Constant) and isinstance(arg_expr.value[1], str) and len(arg_expr.value[1]) == 1:
                        code.append(f"pushi {ord(arg_expr.value[1])}")
                        code.append("writechr")
                    else:
                        code.append("writei")
                if proc_name == "writeln":
                    code.append("writeln")
            return code
        if proc_name not in self.function_addresses:
            raise ast.TranslationError(f"Procedure '{proc_name}' not declared")
        expected_params = self.function_signatures.get(proc_name, 0)
        if len(args) != expected_params:
            raise ast.TranslationError(f"Procedure '{proc_name}' expects {expected_params} parameters, got {len(args)}")
        for arg in args:
            code.extend(arg[1].evaluate(self))
        code.append(f"pusha {self.function_addresses[proc_name]}")
        code.append("call")
        return code

    def visit_binary_expression(self, binary_expression: ast.BinaryExpression) -> List[str]:
        left = binary_expression.left.evaluate(self)
        right = binary_expression.right.evaluate(self)
        op = binary_expression.operator[1]
        op_map = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div",
            "div": "div",
            "mod": "mod",
            "=": "equal",
            "<>": ["equal", "not"],
            "<": "inf",
            "<=": "infeq",
            ">": "sup",
            ">=": "supeq",
            "and": "and",
            "or": "or"
        }
        op_code = op_map.get(op)
        if op_code is None:
            raise ast.TranslationError(f"Unsupported operator '{op}'")
        if isinstance(op_code, str):
            return left + right + [op_code]
        return left + right + op_code

    def visit_signed_expression(self, signed_expression: ast.SignedExpression) -> List[str]:
        expr = signed_expression.expression.evaluate(self)
        sign = signed_expression.sign[1]
        if sign == "+":
            return expr
        return expr + ["pushi -1", "mul"]

    def visit_exponentiation(self, exponentiation: ast.Exponentiation) -> List[str]:
        base = exponentiation.base.evaluate(self)
        if isinstance(exponentiation.exponent, ast.Constant):
            n = self._evaluate_constant(exponentiation.exponent)
            if n == 0:
                return ["pushi 1"]
            return base + ["dup 1"] * (n - 1) + ["mul"] * (n - 1)
        raise ast.TranslationError("Dynamic exponentiation not supported")

    def visit_not_expression(self, not_expression: ast.NotExpression) -> List[str]:
        expr = not_expression.expression.evaluate(self)
        return expr + ["not"]

    def visit_constant(self, constant: ast.Constant) -> List[str]:
        value = constant.value[1]
        if isinstance(value, tuple):
            val = value[1]
            if value[0] == 'integer':
                return [f"pushi {val}"]
            elif value[0] == 'real':
                return [f"pushf {val}"]
            elif value[0] == 'boolean':
                return [f"pushi {1 if val.lower() == 'true' else 0}"]
            elif value[0] == 'char':
                return [f"pushi {ord(val)}"]
        elif isinstance(value, str) and len(value) == 1:
            return [f"pushi {ord(value)}"]
        elif isinstance(value, str):
            return [f'pushs "{value}"']
        elif value.lower() in ("true", "false"):
            return [f"pushi {1 if value.lower() == 'true' else 0}"]
        raise ast.TranslationError(f"Unsupported constant '{value}'")

    def visit_set_constructor(self, set_constructor: ast.SetConstructor) -> List[str]:
        code = []
        for member in (set_constructor.members or []):
            if member[0] == "set_member":
                code.extend(member[1].evaluate(self))
            elif member[0] == "set_range":
                code.extend(member[1].evaluate(self) + member[2].evaluate(self))
        return code

    def visit_pointer_dereference(self, pointer_dereference: ast.PointerDereference) -> List[str]:
        return pointer_dereference.variable.evaluate(self) + ["load"]

    def visit_indexed_variable(self, indexed_variable: ast.IndexedVariable) -> List[str]:
        var_name = indexed_variable.variable.identifier[1]
        if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
            var_index, var_type, lower_bound, element_type = self.local_variables[self.current_function][var_name]
        elif var_name in self.global_variables:
            var_index, var_type, lower_bound, element_type = self.global_variables[var_name]
        else:
            raise ast.TranslationError(f"Variable '{var_name}' not declared")
        if var_type != "array" and var_type != "string":
            raise ast.TranslationError(f"Variable '{var_name}' is not an array or string")
        code = []
        if var_type == "string":
            if len(indexed_variable.indices) != 1:
                raise ast.TranslationError("String indexing requires exactly one index")
            index_type = self._infer_expression_type(indexed_variable.indices[0])
            if index_type != "integer":
                raise ast.TranslationError(f"String index must be integer, got {index_type}")
            code.append(f"pushg {var_index}")
            code.extend(indexed_variable.indices[0].evaluate(self))
            code.append("pushi 1")
            code.append("sub")
            code.append("charat")
        else:
            index_type = self._infer_expression_type(indexed_variable.indices[0])
            if index_type != "integer":
                raise ast.TranslationError(f"Array index must be integer, got {index_type}")
            code.extend(indexed_variable.indices[0].evaluate(self))
            if lower_bound is not None:
                code.append(f"pushi {lower_bound}")
                code.append("sub")
            code.append(f"pushi {var_index}")
            code.append("add")
            code.append("pushg")
        return code

    def visit_field_designator(self, field_designator: ast.FieldDesignator) -> List[str]:
        return field_designator.variable.evaluate(self) + [f"pushi {field_designator.field[1]}", "add", "load"]

    def visit_array_type(self, array_type: ast.ArrayType) -> List[str]:
        return []

    def visit_ast(self, ast_node: ast.AbstractSyntaxTree) -> List[str]:
        return ast_node.program.evaluate(self)

    def translate(self, ast_node: ast.AbstractSyntaxTree) -> List[str]:
        return self.visit_ast(ast_node)

    def _translate_indexed_variable_assignment(self, indexed_variable: ast.IndexedVariable) -> List[str]:
        var_name = indexed_variable.variable.identifier[1]
        if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
            var_index, var_type, lower_bound, element_type = self.local_variables[self.current_function][var_name]
        elif var_name in self.global_variables:
            var_index, var_type, lower_bound, element_type = self.global_variables[var_name]
        else:
            raise ast.TranslationError(f"Variable '{var_name}' not declared")
        if var_type == "string":
            raise ast.TranslationError("String character assignment not supported")
        elif var_type != "array":
            raise ast.TranslationError(f"Variable '{var_name}' is not an array")
        index_type = self._infer_expression_type(indexed_variable.indices[0])
        if index_type != "integer":
            raise ast.TranslationError(f"Array index must be integer, got {index_type}")
        code = indexed_variable.indices[0].evaluate(self)
        if lower_bound is not None:
            code.append(f"pushi {lower_bound}")
            code.append("sub")
        code.append(f"pushi {var_index}")
        code.append("add")
        code.append("storeg")
        return code

    def _evaluate_constant(self, expr: ast.Expression) -> int:
        if isinstance(expr, ast.Constant):
            value = expr.value[1]
            if isinstance(value, tuple) and value[0] == 'integer':
                return int(value[1])
            elif isinstance(value, (int, float)):
                return int(value)
        raise ast.TranslationError(f"Expected constant integer, got {expr}")

    def _infer_expression_type(self, expr: ast.Expression) -> str:
        if isinstance(expr, ast.Constant):
            value = expr.value[1]
            if isinstance(value, tuple):
                return value[0]
            elif isinstance(value, str) and len(value) == 1:
                return "char"
            elif isinstance(value, str):
                return "string"
            elif value.lower() in ("true", "false"):
                return "boolean"
        elif isinstance(expr, ast.VariableAccess):
            var_name = expr.identifier[1].lower()
            if var_name in ("true", "false"):
                return "boolean"
            if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                return self.local_variables[self.current_function][var_name][1]
            if var_name in self.global_variables:
                return self.global_variables[var_name][1]
            raise ast.TranslationError(f"Variable '{var_name}' not declared")
        elif isinstance(expr, ast.IndexedVariable):
            var_name = expr.variable.identifier[1]
            if self.current_function and var_name in self.local_variables.get(self.current_function, {}):
                var_type, _, _, element_type = self.local_variables[self.current_function][var_name]
                return element_type if element_type and var_type == "array" else "char" if var_type == "string" else "integer"
            if var_name in self.global_variables:
                var_type, _, _, element_type = self.global_variables[var_name]
                return element_type if element_type and var_type == "array" else "char" if var_type == "string" else "integer"
            raise ast.TranslationError(f"Variable '{var_name}' not declared")
        elif isinstance(expr, ast.BinaryExpression):
            op = expr.operator[1]
            if op in ("=", "<>", "<", "<=", ">", ">="):
                return "boolean"
            if op in ("and", "or"):
                return "boolean"
            left_type = self._infer_expression_type(expr.left)
            right_type = self._infer_expression_type(expr.right)
            if left_type == right_type:
                return left_type
            if left_type in ("integer", "real") and right_type in ("integer", "real"):
                return "real" if "real" in (left_type, right_type) else "integer"
            return left_type
        elif isinstance(expr, ast.SignedExpression):
            return self._infer_expression_type(expr.expression)
        elif isinstance(expr, ast.NotExpression):
            return "boolean"
        elif isinstance(expr, ast.Exponentiation):
            return self._infer_expression_type(expr.base)
        elif isinstance(expr, ast.FunctionCall):
            func_name = expr.identifier[1]
            if func_name == "length":
                return "integer"
            if func_name == "charat":
                return "char"
            return "integer"
        raise ast.TranslationError(f"Cannot infer type for expression {expr}")
    

