import ast

from security_analyzer.taint import TaintAnalyzer


def test_tainted_function_return_propagates_to_caller():
    source = """
def get_username():
    value = request.args.get("username")
    return value

username = get_username()
"""

    tree = ast.parse(source)
    taint = TaintAnalyzer()

    tainted_variables = taint.find_input_variables(tree)
    tainted_variables = taint.propagate_assignments(
        tree,
        tainted_variables,
    )

    tainted_functions = taint.find_tainted_return_functions(
        tree,
        tainted_variables,
    )

    tainted_variables = taint.propagate_function_returns(
        tree,
        tainted_functions,
        tainted_variables,
    )

    assert "value" in tainted_variables
    assert "get_username" in tainted_functions
    assert "username" in tainted_variables
