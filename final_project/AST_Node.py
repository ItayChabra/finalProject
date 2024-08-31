class ASTNode:
    pass

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef(name={self.name}, params={self.params}, body={self.body})"

class LambdaExpr(ASTNode):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __repr__(self):
        return f"LambdaExpr(params={self.params}, body={self.body})"

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp(left={self.left}, op={self.op}, right={self.right})"

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"UnaryOp(op={self.op}, expr={self.expr})"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable(name={self.name})"

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number(value={self.value})"

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean(value={self.value})"

class Call(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __repr__(self):
        return f"Call(func={self.func}, args={self.args})"

class Conditional(ASTNode):
    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __repr__(self):
        return (f"Conditional(condition={self.condition}, "
                f"true_expr={self.true_expr}, false_expr={self.false_expr})")

