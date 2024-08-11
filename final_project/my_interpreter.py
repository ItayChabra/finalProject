from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call
from my_lexer import tokenize
from my_parser import Parser

class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.call_stack = []

    def execute(self, node):
        print(f"Executing node: {node}")  # Debug print
        if isinstance(node, FunctionDef):
            self.global_scope[node.name] = node
        elif isinstance(node, LambdaExpr):
            return node
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
            print(f"Variable {node.name} = {value}")  # Debug print
            return value
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Call):
            return self.execute_call(node)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def evaluate_binop(self, op, left, right):
        if op == '&&':
            return left and right
        elif op == '||':
            # Short-circuit evaluation for '||'
            if left:
                return left
            else:
                return right
        elif op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
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
        func = self.lookup_variable(node.func)
        if isinstance(func, FunctionDef):
            # Create a new scope for function execution
            new_scope = dict(zip(func.params, [self.execute(arg) for arg in node.args]))
            self.call_stack.append(new_scope)
            result = self.execute(func.body)
            self.call_stack.pop()
            return result
        elif isinstance(func, LambdaExpr):
            new_scope = dict(zip(func.params, [self.execute(arg) for arg in node.args]))
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


