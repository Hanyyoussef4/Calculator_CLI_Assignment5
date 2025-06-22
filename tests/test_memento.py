from decimal import Decimal
from app.calculator_memento import CalculatorMemento as Memento   # ← correct name
from app.calculation import Calculation


def test_memento_roundtrip():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    snap = Memento(history=[c])
    round_tripped = Memento.from_dict(snap.to_dict())

    assert round_tripped.history[0] == c
    assert "CalculatorMemento" in repr(round_tripped)
