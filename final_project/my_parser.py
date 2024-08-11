from AST_Node import ASTNode, FunctionDef, LambdaExpr, BinOp, UnaryOp, Variable, Number, Boolean, Call, IfExpr


class Parser:
    def __init__(self, tokens, bnf_file_path):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if tokens else None
        self.rules = self.load_bnf(bnf_file_path)

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
        if self.current_token and self.current_token[0] == token_type:
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
        print(f"Parsing statement with token: {self.current_token}")  # Debug print
        if self.current_token[0] == 'FN':
            return self.parse_function_def()
        elif self.current_token[0] == 'LAMBDA':
            return self.parse_lambda_expr()
        elif self.current_token[0] == 'IF':
            return self.parse_if_expr()
        elif self.current_token[0] == 'REC':
            return self.parse_recursion()
        else:
            return self.parse_expression()

    def parse_function_def(self):
        self.eat('FN')
        func_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        params = self.parse_params()
        self.eat('RPAREN')
        self.eat('ASSIGN')
        body = self.parse_expression()
        return FunctionDef(func_name, params, body)

    def parse_lambda_expr(self):
        self.eat('LAMBDA')
        params = self.parse_params()
        self.eat('COLON')  # assuming there is a COLON token for lambda syntax
        body = self.parse_expression()
        return LambdaExpr(params, body)

    def parse_if_expr(self):
        self.eat('IF')
        condition = self.parse_expression()
        self.eat('THEN')
        then_branch = self.parse_expression()
        self.eat('ELSE')
        else_branch = self.parse_expression()
        return IfExpr(condition, then_branch, else_branch)

    def parse_recursion(self):
        self.eat('REC')
        func_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        params = self.parse_params()
        self.eat('RPAREN')
        self.eat('ASSIGN')
        body = self.parse_expression()
        return FunctionDef(func_name, params, body)  # or another ASTNode for recursion

    def parse_params(self):
        params = []
        while self.current_token[0] == 'IDENTIFIER':
            params.append(self.current_token[1])
            self.eat('IDENTIFIER')
            if self.current_token[0] == 'COMMA':
                self.eat('COMMA')
        return params

    def parse_args(self):
        args = []
        while self.current_token[0] in ['IDENTIFIER', 'INTEGER', 'BOOLEAN']:
            args.append(self.parse_expression())
            if self.current_token[0] == 'COMMA':
                self.eat('COMMA')
        return args

    def parse_expression(self):
        print(f"Parsing expression with token: {self.current_token}")  # Debug print

        def parse_term():
            if self.current_token[0] == 'IDENTIFIER':
                if (self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'LPAREN'):
                    return self.parse_function_call()
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
                return expr

            if self.current_token[0] == 'LAMBDA':
                return self.parse_lambda_expr()

            if self.current_token[0] == 'IF':
                return self.parse_if_expr()

            raise Exception(f"Unexpected token: {self.current_token}")

        def parse_arithmetic_expr():
            left = parse_term()

            while self.current_token[0] == 'ARITH_OP':
                op = self.current_token[1]
                self.eat('ARITH_OP')
                print(f"Parsing right term for operator {op}")
                right = parse_term()
                left = BinOp(left, op, right)
                print(f"Parsed binary operation: {left}")

            return left

        def parse_boolean_expr():
            left = parse_arithmetic_expr()

            while self.current_token[0] == 'BOOL_OP':
                op = self.current_token[1]
                self.eat('BOOL_OP')
                print(f"Parsing right boolean expression for operator {op}")
                right = parse_arithmetic_expr()
                left = BinOp(left, op, right)
                print(f"Parsed boolean operation: {left}")

            return left

        def parse_comparison_expr():
            left = parse_boolean_expr()

            while self.current_token[0] == 'COMP_OP':
                op = self.current_token[1]
                self.eat('COMP_OP')
                print(f"Parsing right comparison expression for operator {op}")
                right = parse_boolean_expr()
                left = BinOp(left, op, right)
                print(f"Parsed comparison operation: {left}")

            return left

        return parse_comparison_expr()

    def parse_function_call(self):
        func_name = self.current_token[1]
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        args = self.parse_args()
        self.eat('RPAREN')
        return Call(func_name, args)
