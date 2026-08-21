import ast


def calculate(expression):
    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


def evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise ValueError("Invalid value")
        
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value")

    if isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)

        if isinstance(node.op, ast.Add):
            return left + right

        if isinstance(node.op, ast.Sub):
            return left - right

        if isinstance(node.op, ast.Mult):
            return left * right

        if isinstance(node.op, ast.Div):
            return left / right

        if isinstance(node.op, ast.Pow):
            return left**right

        if isinstance(node.op, ast.Mod):
            return left % right

        if isinstance(node.op, ast.FloorDiv):
            return left // right

        raise ValueError("Unsupported operator")

    if isinstance(node, ast.UnaryOp):
        operand = evaluate(node.operand)

        if isinstance(node.op, ast.USub):
            return -operand

        if isinstance(node.op, ast.UAdd):
            return operand

        raise ValueError("Unsupported operator")

    raise ValueError("Unsupported expression")
