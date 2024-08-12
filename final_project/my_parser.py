from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call

class Parser:
    def __init__(self, tokens, bnf_file_path):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if tokens else None
        self.rules = self.load_bnf(bnf_file_path)
        self.current_lambda_expr = None  # Track current lambda expression for calls

    def load_bnf(self, file_path):
        rules = {}
        with open(file_path, 'r') as file:
            content = file.read()
            lines = content.splitlines()
            current_non_terminal = None
            for line in lines:
                if line.strip() == "":
                    continue
                if "::=" in line:
                    parts = line.split("::=")
                    current_non_terminal = parts[0].strip()
                    rules[current_non_terminal] = [p.strip() for p in parts[1].split("|")]
                else:
                    rules[current_non_terminal].extend([p.strip() for p in line.split("|")])
        return rules

    def eat(self, token_type):
        print(f"Trying to eat {token_type}, current token: {self.current_token}")  # Debug
        if self.current_token and self.current_token[0] == token_type:
            print(f"Token {self.current_token} matched {token_type}, advancing...")  # Debug
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = (None, None)
        else:
            raise Exception(f"Expected token {token_type} but got {self.current_token}")

    def parse(self):
        statements = []
        while self.current_token[0] is not None:
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
        return statements

    def parse_statement(self):
        print(f"Parsing statement with token: {self.current_token}")  # Debug
        if self.current_token[0] == 'DEFUN':
            return self.parse_function_def()
        elif self.current_token[0] == 'LAMBDA':
            return self.parse_lambda_expr()
        else:
            return self.parse_expression()

    def parse_function_def(self):
        print("Parsing function definition")  # Debug
        self.eat('DEFUN')
        self.eat('LBRACE')
        self.eat('IDENTIFIER')  # 'name'
        self.eat('COLON')
        func_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('COMMA')
        self.eat('IDENTIFIER')  # 'arguments'
        self.eat('COLON')
        params = self.parse_params()
        self.eat('RBRACE')
        body = self.parse_expression()
        return FunctionDef(func_name, params, body)

    def parse_lambda_expr(self):
        print("Parsing lambda expression")  # Debug
        self.eat('LAMBDA')
        params = []
        while self.current_token[0] == 'IDENTIFIER':
            params.append(self.current_token[1])
            print(f"Lambda parameter: {self.current_token[1]}")  # Debug
            self.eat('IDENTIFIER')
            if self.current_token[0] == 'COMMA':
                self.eat('COMMA')
        self.eat('DOT')
        body = self.parse_expression()
        lambda_expr = LambdaExpr(params, body)
        print(f"Constructed lambda expression: {lambda_expr}")  # Debug
        if self.current_token[0] == 'LPAREN':
            print("Lambda expression is followed by a call, parsing lambda call")  # Debug
            return self.parse_lambda_call(lambda_expr)
        return lambda_expr

    def parse_lambda_call(self, lambda_expr):
        print("Parsing lambda call")  # Debug
        self.eat('LPAREN')
        args = self.parse_args()  # Correctly parse all arguments
        self.eat('RPAREN')
        print(f"Lambda call with args: {args}")  # Debug
        return Call(lambda_expr, args)

    def parse_params(self):
        params = []
        self.eat('LPAREN')
        while self.current_token[0] == 'IDENTIFIER':
            params.append(self.current_token[1])
            print(f"Function parameter: {self.current_token[1]}")  # Debug
            self.eat('IDENTIFIER')
            if self.current_token[0] == 'COMMA':
                self.eat('COMMA')
        self.eat('RPAREN')
        return params

    def parse_args(self):
        args = []
        print(f"Parsing args, current token: {self.current_token}")  # Debug
        while self.current_token[0] != 'RPAREN':
            args.append(self.parse_expression())
            print(f"Added argument: {args[-1]}")  # Debug
            if self.current_token[0] == 'COMMA':
                print("Found comma, continuing to next argument")  # Debug
                self.eat('COMMA')
            elif self.current_token[0] == 'RPAREN':
                print("End of argument list found")  # Debug
                break
            else:
                raise Exception(f"Unexpected token in argument list: {self.current_token}")
        return args

    def parse_expression(self):
        print(f"Parsing expression with token: {self.current_token}")  # Debug

        def parse_term():
            if self.current_token[0] == 'IDENTIFIER':
                if (self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'LPAREN'):
                    return self.parse_function_call()  # Handle function calls, including lambda calls
                identifier = Variable(self.current_token[1])
                self.eat('IDENTIFIER')
                return identifier

            if self.current_token[0] == 'INTEGER':
                number = Number(self.current_token[1])
                self.eat('INTEGER')
                return number

            if self.current_token[0] == 'BOOLEAN':
                boolean = Boolean(self.current_token[1])
                self.eat('BOOLEAN')
                return boolean

            if self.current_token[0] == 'LPAREN':
                self.eat('LPAREN')
                expr = self.parse_expression()
                self.eat('RPAREN')
                # Check if the expression was a lambda expression and is followed by arguments (a lambda call)
                if isinstance(expr, LambdaExpr) and self.current_token[0] == 'LPAREN':
                    return self.parse_lambda_call(expr)
                return expr

            if self.current_token[0] == 'LAMBDA':
                lambda_expr = self.parse_lambda_expr()
                # Check if the lambda expression is followed by a lambda call (arguments)
                if self.current_token[0] == 'LPAREN':
                    return self.parse_lambda_call(lambda_expr)
                return lambda_expr

            raise Exception(f"Unexpected token: {self.current_token}")

        def parse_arithmetic_expr():
            left = parse_term()
            while self.current_token[0] == 'ARITH_OP':
                op = self.current_token[1]
                self.eat('ARITH_OP')
                right = parse_term()
                left = BinOp(left, op, right)
            return left

        def parse_boolean_expr():
            left = parse_arithmetic_expr()
            while self.current_token[0] == 'BOOL_OP':
                op = self.current_token[1]
                self.eat('BOOL_OP')
                right = parse_arithmetic_expr()
                left = BinOp(left, op, right)
            return left

        def parse_comparison_expr():
            left = parse_boolean_expr()
            while self.current_token[0] == 'COMP_OP':
                op = self.current_token[1]
                self.eat('COMP_OP')
                right = parse_boolean_expr()
                left = BinOp(left, op, right)
            return left

        return parse_comparison_expr()

    def parse_function_call(self):
        print(f"Parsing function call for: {self.current_token}")  # Debug
        func_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        args = self.parse_args()
        self.eat('RPAREN')
        print(f"Function call '{func_name}' with args: {args}")  # Debug
        return Call(func_name, args)
