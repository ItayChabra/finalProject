from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call, Conditional
from my_lexer import tokenize
from my_parser import Parser


class Closure:
    def __init__(self, func, env):
        self.func = func
        self.env = env


class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.call_stack = []

    def execute(self, node):
        # print(f"Executing node: {node}")  # Debug print
        if isinstance(node, FunctionDef):
            self.global_scope[node.name] = node
        elif isinstance(node, LambdaExpr):
            return Closure(node, self.global_scope.copy())
        elif isinstance(node, BinOp):
            if node.op == '||':
                left = self.execute(node.left)
                if left:
                    return left
                return self.execute(node.right)
            elif node.op == '&&':
                left = self.execute(node.left)
                if not left:
                    return left
                return self.execute(node.right)
            else:
                left = self.execute(node.left)
                right = self.execute(node.right)
                return self.evaluate_binop(node.op, left, right)
        elif isinstance(node, UnaryOp):
            expr = self.execute(node.expr)
            return self.evaluate_unaryop(node.op, expr)
        elif isinstance(node, Variable):
            value = self.lookup_variable(node.name)
            # print(f"Variable {node.name} = {value}")  # Debug print
            return value
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Call):
            return self.execute_call(node)
        elif isinstance(node, Conditional):
            condition = self.execute(node.condition)
            if condition:
                return self.execute(node.true_expr)
            else:
                return self.execute(node.false_expr)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def evaluate_binop(self, op, left, right):
        if op == '&&':
            return left and right
        elif op == '||':
            return left or right
        elif op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("Error: Cannot divide by zero")
            return left // right
        elif op == '%':
            return left % right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right
        else:
            raise Exception(f"Unknown operator: {op}")

    def evaluate_unaryop(self, op, expr):
        if op == '!':
            return not expr
        elif op == '-':
            return -expr
        else:
            raise Exception(f"Unknown unary operator: {op}")

    def lookup_variable(self, name):
        # Check the current scope first
        if name in self.global_scope:
            return self.global_scope[name]
        # Check the call stack for closures
        for scope in reversed(self.call_stack):
            if name in scope:
                return scope[name]
        raise Exception(f"Undefined variable: {name}")

    def execute_call(self, node):
        if isinstance(node.func, Closure):
            func = node.func.func
            env = node.func.env
        elif isinstance(node.func, LambdaExpr):
            func = node.func
            env = self.global_scope.copy()
        else:
            func = self.lookup_variable(node.func)
            env = self.global_scope.copy()

        # Check if the function is a named FunctionDef (not a lambda)
        if isinstance(func, FunctionDef):
            # Perform argument count check only for named functions
            if len(node.args) != len(func.params):
                raise Exception(f"Error: {func.name} expects {len(func.params)} arguments but got {len(node.args)}")

        if isinstance(func, FunctionDef) or isinstance(func, LambdaExpr):
            evaluated_args = [self.execute(arg) for arg in node.args]

            if isinstance(func, FunctionDef):
                func_params = func.params
                func_body = func.body
            else:  # LambdaExpr
                func_params = func.params
                func_body = func.body

            new_scope = env.copy()
            new_scope.update(dict(zip(func_params, evaluated_args)))
            self.call_stack.append(self.global_scope.copy())
            self.global_scope = new_scope

            result = self.execute(func_body)

            self.global_scope = self.call_stack.pop()

            # If the result is another Closure, execute it with the remaining arguments
            while isinstance(result, Closure) and len(node.args) > len(func_params):
                remaining_args = node.args[len(func_params):]
                result = self.execute(Call(func=result, args=remaining_args))

            return result
        else:
            raise Exception(f"Unknown function: {node.func}")

    def repl(self):
        while True:
            try:
                code = input(">>> ")
                tokens = tokenize(code)
                parser = Parser(tokens)
                ast = parser.parse()
                print(ast)
                for node in ast:
                    result = self.execute(node)
                    if (result != None):
                        print(result)  # Ensure this line is present
                        print()
            except Exception as e:
                print(e)
                print()


    def run_program(self, file_path):
        with open(file_path, 'r') as file:
            code = file.read()
            tokens = tokenize(code)
            parser = Parser(tokens)
            ast = parser.parse()
        for node in ast:
            print(node)
            try:
                result = self.execute(node)
                if (result != None):
                    print(result)  # Ensure this line is present
                    print()
            except Exception as e:
                print(e)
                print()

