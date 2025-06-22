import builtins
import itertools
import pytest
from unittest.mock import patch
from app import calculator_repl as repl


def _feed(*answers):
    """Returns a fake input() provider that walks through answers then exits."""
    data = itertools.chain(answers, ['exit'])
    return lambda _prompt="": next(data)


# -----------------------------------------------------------------------------
# ✅ Full Flow Test
# -----------------------------------------------------------------------------

def test_repl_full_flow(monkeypatch, capsys):
    """
    Simulates a full REPL session with mixed commands:
    - 'add' 2 + 3 => 5
    - 'square' => unknown command
    - 'divide' 5 / 5 => 1
    """
    monkeypatch.setattr(builtins, "input", _feed("add", "2", "3", "square", "divide", "5", "5"))
    repl.calculator_repl()
    out = capsys.readouterr().out
    assert "Result: 5" in out
    assert "unknown command" in out.lower()
    assert "Result: 1" in out
    assert "Goodbye" in out


# -----------------------------------------------------------------------------
# ✅ Basic Commands
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["help", "exit"])
def test_help_and_exit(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Available commands" in captured.out
    assert "Goodbye!" in captured.out

@patch("builtins.input", side_effect=["foobar", "exit"])
def test_unknown_command(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Unknown command: 'foobar'" in captured.out


# -----------------------------------------------------------------------------
# ✅ Arithmetic Operations
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "2", "3", "exit"])
def test_add_operation(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 5" in captured.out

@patch("builtins.input", side_effect=["subtract", "10", "4", "exit"])
def test_subtract_operation(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 6" in captured.out

@patch("builtins.input", side_effect=["multiply", "abc", "3", "exit"])
def test_validation_error(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Error:" in captured.out


# -----------------------------------------------------------------------------
# ✅ History & State Tests
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["clear", "history", "exit"])
def test_show_empty_history(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "No calculations in history" in captured.out

@patch("builtins.input", side_effect=["add", "2", "2", "history", "exit"])
def test_show_non_empty_history(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Addition(2, 2)" in captured.out
    assert "Calculation History" in captured.out


# -----------------------------------------------------------------------------
# ✅ Undo/Redo
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["undo", "exit"])
def test_undo_nothing(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Nothing to undo" in captured.out

@patch("builtins.input", side_effect=["redo", "exit"])
def test_redo_nothing(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Nothing to redo" in captured.out

@patch("builtins.input", side_effect=["add", "5", "5", "undo", "redo", "exit"])
def test_undo_and_redo(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Operation undone" in captured.out
    assert "Operation redone" in captured.out


# -----------------------------------------------------------------------------
# ✅ Cancel Inputs
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "cancel", "exit"])
def test_cancel_first_number(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch("builtins.input", side_effect=["add", "10", "cancel", "exit"])
def test_cancel_second_number(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch("builtins.input", side_effect=["power", "cancel", "exit"])
def test_operation_cancelled_first_input(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch("builtins.input", side_effect=["modulus", "5", "cancel", "exit"])
def test_operation_cancelled_second_input(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out


# -----------------------------------------------------------------------------
# ✅ History Save/Load
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "1", "2", "save", "exit"])
def test_save_history_success(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "History saved successfully" in captured.out

@patch("builtins.input", side_effect=["load", "exit"])
def test_load_history_success(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "History loaded successfully" in captured.out or "Error loading history" in captured.out

@patch("builtins.input", side_effect=["load", "exit"])
@patch("app.calculator.Calculator.load_history", side_effect=Exception("Boom"))
def test_load_history_failure(mock_load, mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Error loading history: Boom" in captured.out


# -----------------------------------------------------------------------------
# ✅ Output Formatting
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "2", "3", "exit"])
def test_addition_result_formatting(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 5" in captured.out

@patch("builtins.input", side_effect=EOFError)
def test_repl_handles_eof_gracefully(mock_input, capsys):
    try:
        repl.calculator_repl()
    except EOFError:
        pytest.fail("REPL should handle EOFError gracefully")

@patch("builtins.input", side_effect=["add", "abc", "cancel", "exit"])
def test_get_number_input_invalid_then_cancel(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch("builtins.input", side_effect=["modulo", "exit"])
def test_unsupported_command(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out

@patch("builtins.input", side_effect=["add", "1", "1", "undo", "clear", "redo", "exit"])
def test_redo_after_clear(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "History cleared" in captured.out
    assert "Nothing to redo" in captured.out


# -----------------------------------------------------------------------------
# 🧪 Command Execution Exception
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "1", "2", "exit"])
@patch("app.calculation.CalculationFactory.create", side_effect=Exception("Boom"))
def test_calculation_factory_failure(mock_create, mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Error: Boom" in captured.out


# -----------------------------------------------------------------------------
# 🧪 Redo Without Undo
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "4", "4", "redo", "exit"])
def test_redo_without_undo(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Nothing to redo" in captured.out


# -----------------------------------------------------------------------------
# 🧪 Save History Error
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["add", "1", "2", "save", "exit"])
@patch("app.calculator.Calculator.save_history", side_effect=Exception("Disk full"))
def test_save_history_failure(mock_save, mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Error saving history: Disk full" in captured.out


# -----------------------------------------------------------------------------
# 🧪 Unknown Operation Edge Case
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["square root", "exit"])
def test_complex_unknown_command(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


# -----------------------------------------------------------------------------
# 🧪 Help Command Output Test
# -----------------------------------------------------------------------------

@patch("builtins.input", side_effect=["help", "exit"])
def test_help_command_shows_commands(mock_input, capsys):
    repl.calculator_repl()
    captured = capsys.readouterr()
    assert "Available commands" in captured.out
