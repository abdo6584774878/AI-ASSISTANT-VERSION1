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


def test_taint_propagates_through_expressions():
    source = """
user_input = request.args.get("url")
url = "https://example.com/?target=" + user_input
"""

    tree = ast.parse(source)
    taint = TaintAnalyzer()

    tainted_variables = taint.find_input_variables(tree)

    tainted_variables = taint.propagate_expressions(
        tree,
        tainted_variables,
    )

    assert "user_input" in tainted_variables
    assert "url" in tainted_variables


def test_taint_propagates_through_f_strings():
    source = """
user_input = request.args.get("url")
url = f"https://example.com/?target={user_input}"
"""

    tree = ast.parse(source)
    taint = TaintAnalyzer()

    tainted_variables = taint.find_input_variables(tree)

    tainted_variables = taint.propagate_expressions(
        tree,
        tainted_variables,
    )

    assert "user_input" in tainted_variables
    assert "url" in tainted_variables


def test_taint_propagates_through_function_arguments_and_expressions():
    source = """
def fetch(url):
    final_url = "https://proxy.com/?target=" + url
    return final_url

user_url = request.args.get("url")
result = fetch(user_url)
"""

    tree = ast.parse(source)
    taint = TaintAnalyzer()

    tainted_variables = taint.find_input_variables(tree)

    tainted_variables = taint.propagate_assignments(
        tree,
        tainted_variables,
    )

    tainted_variables = taint.propagate_function_arguments(
        tree,
        tainted_variables,
    )

    tainted_variables = taint.propagate_expressions(
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

    assert "user_url" in tainted_variables
    assert "url" in tainted_variables
    assert "final_url" in tainted_variables
    assert "result" in tainted_variables


def test_find_dynamic_variables():
    source = """
user_input = request.args.get("url")
url = "https://example.com/?target=" + user_input
"""

    tree = ast.parse(source)
    taint = TaintAnalyzer()

    tainted_variables = taint.find_input_variables(tree)

    dynamic_variables = taint.find_dynamic_variables(
        tree,
        tainted_variables,
    )

    assert "url" in dynamic_variables
    assert "user_input" not in dynamic_variables
