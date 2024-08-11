from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call
from my_lexer import tokenize
from my_parser import Parser

class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.call_stack = []

    def execute(self, node):
        if isinstance(node, FunctionDef):
            self.global_scope[node.name] = node
        elif isinstance(node, LambdaExpr):
            return node
        elif isinstance(node, BinOp):
            left = self.execute(node.left)
            right = self.execute(node.right)
            return self.evaluate_binop(node.op, left, right)
        elif isinstance(node, UnaryOp):
            expr = self.execute(node.expr)
            return self.evaluate_unaryop(node.op, expr)
        elif isinstance(node, Variable):
            return self.lookup_variable(node.name)
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Call):
            return self.execute_call(node)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def evaluate_binop(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '&&':
            return left and right
        elif op == '||':
            return left or right
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
        else:
            raise Exception(f"Unknown unary operator: {op}")

    def lookup_variable(self, name):
        for scope in reversed(self.call_stack):
            if name in scope:
                return scope[name]
        if name in self.global_scope:
            return self.global_scope[name]
        raise Exception(f"Undefined variable: {name}")

    def execute_call(self, node):
        func = self.execute(node.func)  # Adjusted to execute the function node
        if isinstance(func, FunctionDef):
            new_scope = {param: self.execute(arg) for param, arg in zip(func.params, node.args)}
            self.call_stack.append(new_scope)
            result = self.execute(func.body)
            self.call_stack.pop()
            return result
        elif isinstance(func, LambdaExpr):
            new_scope = {param: self.execute(arg) for param, arg in zip(func.params, node.args)}
            self.call_stack.append(new_scope)
            result = self.execute(func.body)
            self.call_stack.pop()
            return result
        else:
            raise Exception(f"Unknown function: {node.func}")

    def repl(self):
        while True:
            try:
                code = input(">>> ")
                tokens = tokenize(code)
                parser = Parser(tokens, 'BNF.txt')
                ast = parser.parse()
                for node in ast:
                    result = self.execute(node)
                    print(result)
            except Exception as e:
                print(e)

    def run_program(self, file_path):
        with open(file_path, 'r') as file:
            code = file.read()
        tokens = tokenize(code)
        parser = Parser(tokens, 'BNF.txt')
        ast = parser.parse()
        for node in ast:
            result = self.execute(node)
            print(result)

# Example usage:
# interpreter = Interpreter()
# interpreter.repl()  # For interactive mode
# interpreter.run_program('example.lambda')  # For running a full program
