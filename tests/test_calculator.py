import pytest

from assistant.tools.calculator import calculate


def test_addition():
    assert calculate("2 + 5") == 7


def test_subtraction():
    assert calculate("10 - 3") == 7


def test_multiplication():
    assert calculate("6 * 7") == 42


def test_division():
    assert calculate("20 / 5") == 4


def test_parentheses():
    assert calculate("(10 + 5) * 2") == 30


def test_exponentiation():
    assert calculate("2 ** 10") == 1024


def test_modulo():
    assert calculate("17 % 5") == 2


def test_negative_number():
    assert calculate("-5 + 10") == 5


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("10 / 0")


def test_invalid_expression():
    with pytest.raises(ValueError):
        calculate("hello")


def test_unsupported_operator():
    with pytest.raises(ValueError):
        calculate("2 @ 3")


def test_invalid_value():
    with pytest.raises(ValueError):
        calculate("'hello'")


def test_unary_minus():
    assert calculate("-10") == -10


def test_unary_plus():
    assert calculate("+10") == 10


def test_floor_division():
    assert calculate("17 // 5") == 3


def test_floor_division_negative():
    assert calculate("-17 // 5") == -4


def test_nested_expression():
    assert calculate("2 + 3 * (4 ** 2)") == 50


def test_decimal_numbers():
    assert calculate("2.5 * 4") == 10.0


def test_decimal_division():
    assert calculate("7.5 / 2.5") == 3.0


def test_boolean_is_rejected():
    with pytest.raises(ValueError):
        calculate("True")


def test_string_is_rejected():
    with pytest.raises(ValueError):
        calculate('"hello"')


def test_function_call_is_rejected():
    with pytest.raises(ValueError):
        calculate("__import__('os').system('echo hacked')")


def test_variable_is_rejected():
    with pytest.raises(ValueError):
        calculate("x + 5")
