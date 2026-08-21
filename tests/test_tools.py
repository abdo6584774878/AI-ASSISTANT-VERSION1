from assistant.tools import TOOLS
from assistant.tools.executor import execute_tool


def test_tools_registry_contains_calculator():
    assert "calculator" in TOOLS


def test_tools_registry_contains_datetime():
    assert "datetime" in TOOLS


def test_execute_calculator():
    result = execute_tool("calculator", {"expression": "2 + 5"})

    assert result == 7


def test_execute_datetime():
    result = execute_tool("datetime", {})

    assert isinstance(result, str)


def test_execute_unknown_tool():
    try:
        execute_tool("unknown_tool", {})
    except ValueError as error:
        assert str(error) == "Unknown tool: unknown_tool"
    else:
        raise AssertionError("execute_tool should raise ValueError")


def test_execute_tool_passes_arguments():
    original = TOOLS["calculator"]

    captured = {}

    def fake_calculator(expression):
        captured["expression"] = expression
        return 42

    TOOLS["calculator"] = fake_calculator

    try:
        result = execute_tool("calculator", {"expression": "6 * 7"})
    finally:
        TOOLS["calculator"] = original

    assert captured["expression"] == "6 * 7"
    assert result == 42
