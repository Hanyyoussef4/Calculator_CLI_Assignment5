"""
Extra edge-case tests for app.calculation.Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Covers the last uncovered branches in app/calculation.py:

• Division-by-zero helper
• Unknown-operation branch (line 83)
• Invalid-root helper (neg x, y = 0, generic) (line 224)
• __str__ / __repr__
• Happy-path sanity checks (modulus, power)
• __eq__ NotImplemented branch (line 224)
"""

from decimal import Decimal
import pytest

from app.calculation import Calculation
from app.exceptions import OperationError


# ──────────────────────────────────────────────────────────────────────────────
# Division-by-zero → OperationError
# ──────────────────────────────────────────────────────────────────────────────
def test_divide_by_zero_raises():
    with pytest.raises(OperationError):
        Calculation("Division", Decimal(3), Decimal(0))


# ──────────────────────────────────────────────────────────────────────────────
# Unknown operation name → OperationError   (line 83 before our overflow test)
# ──────────────────────────────────────────────────────────────────────────────
def test_unknown_operation_raises():
    with pytest.raises(OperationError):
        Calculation("Square", Decimal(2), Decimal(2))


# ──────────────────────────────────────────────────────────────────────────────
# Trigger *overflow* inside the Power lambda → ArithmeticError → hits line 83
# ──────────────────────────────────────────────────────────────────────────────
def test_power_overflow_hits_line_83():
    big      = Decimal("1e308")     # huge float when cast
    huge_exp = Decimal("2")         # still overflows as 1e308 ** 2
    with pytest.raises(OperationError):
        Calculation("Power", big, huge_exp)


# ──────────────────────────────────────────────────────────────────────────────
# Invalid-root helper via lambda  (neg x and y = 0 cases)
# ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    "radicand, degree",
    [
        (Decimal("-8"), Decimal("3")),   # negative radicand
        (Decimal("8"),  Decimal("0")),   # zero degree
    ],
)
def test_invalid_root_lambda_raises(radicand, degree):
    with pytest.raises(OperationError):
        Calculation("Root", radicand, degree)


# Generic fall-through inside helper (x >= 0 and y ≠ 0) – hits line 224 too
def test_invalid_root_generic_branch():
    with pytest.raises(OperationError):
        Calculation._raise_invalid_root(Decimal(8), Decimal(-2))


# ──────────────────────────────────────────────────────────────────────────────
# __str__ / __repr__ include meaningful details
# ──────────────────────────────────────────────────────────────────────────────
def test_repr_and_str_include_details():
    calc = Calculation("Multiplication", Decimal(2), Decimal(5))
    text = str(calc)
    assert "Multiplication" in text and "2" in text and "5" in text
    assert "Calculation(" in repr(calc)


# ──────────────────────────────────────────────────────────────────────────────
# Happy-path sanity checks
# ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("Modulus", Decimal("9"), Decimal("4"), Decimal("1")),
        ("Power",   Decimal("2"), Decimal("3"), Decimal("8")),
    ],
)
def test_various_operations(op, a, b, expected):
    assert Calculation(op, a, b).result == expected


# ──────────────────────────────────────────────────────────────────────────────
# __eq__ must return NotImplemented for non-Calculation operand (line 224)
# ──────────────────────────────────────────────────────────────────────────────
def test_eq_with_non_calculation_returns_notimplemented():
    calc = Calculation("Addition", Decimal("1"), Decimal("1"))
    assert calc.__eq__("not a calc") is NotImplemented
