import math
import pytest
from decimal import Decimal

from app.calculator import Calculator
from app.operations import OperationFactory
from app.exceptions import ValidationError, OperationError


def calc_via_factory(cmd: str, a: str, b: str):
    """Mirror the REPL flow: set the operation, then perform it."""
    calc = Calculator()
    calc.set_operation(OperationFactory.create_operation(cmd))
    return calc.perform_operation(a, b)


# ---------- happy paths ------------------------------------------------------
@pytest.mark.parametrize(
    "cmd,a,b,expected",
    [
        ("add",      "2", "3", 5),
        ("subtract", "5", "1", 4),
        ("multiply", "4", "2", 8),
        ("divide",   "8", "4", 2),
        ("modulus",  "9", "4", 1),
        ("power",    "2", "3", 8),
        ("root",     "9", "2", 3),
    ],
)
def test_all_operations(cmd, a, b, expected):
    result = calc_via_factory(cmd, a, b)
    assert math.isclose(float(result), float(expected))


# ---------- unknown command --------------------------------------------------
def test_unknown_command_raises():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.set_operation(OperationFactory.create_operation("square"))


# ---------- non-numeric input ------------------------------------------------
@pytest.mark.parametrize("bad", ["abc", "", None])
def test_non_numeric_raises(bad):
    with pytest.raises((ValidationError, OperationError)):
        calc_via_factory("add", bad, "2")
