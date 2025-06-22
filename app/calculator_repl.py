########################
# Calculator REPL      #
########################

from decimal import Decimal, ROUND_HALF_EVEN
import logging
import sys

from app.calculator import Calculator
from app.calculation import CalculationFactory
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory  # original per-operation factory


def calculator_repl() -> None:
    """
    Command-line Read-Eval-Print Loop (REPL).

    Continuously prompts for commands, performs arithmetic operations,
    and manages calculation history.
    """

    # ── initialise calculator & observers ───────────────────────
    calc = Calculator()
    calc.add_observer(LoggingObserver())
    calc.add_observer(AutoSaveObserver(calc))

    print("Calculator started. Type 'help' for commands.")

    # ── main loop ───────────────────────────────────────────────
    while True:
        try:
            command = input("\nEnter command: ").lower().strip()

            # ---------- help ------------------------------------
            if command == "help":
                print("\nAvailable commands:")
                print("  add, subtract, multiply, divide, power, root, modulus – calculations")
                print("  history   – Show calculation history")
                print("  clear     – Clear calculation history")
                print("  undo      – Undo last calculation")
                print("  redo      – Redo last undone calculation")
                print("  save      – Save history to file")
                print("  load      – Load history from file")
                print("  exit      – Exit the calculator")
                continue

            # ---------- exit ------------------------------------
            if command == "exit":
                try:
                    calc.save_history()
                    print("History saved successfully.")
                except Exception as e:
                    print(f"Warning: Could not save history: {e}")
                print("Goodbye!")
                break

            # ---------- history display -------------------------
            if command == "history":
                hist = calc.show_history()
                if not hist:
                    print("No calculations in history")
                else:
                    print("\nCalculation History:")
                    for idx, entry in enumerate(hist, 1):
                        print(f"{idx}. {entry}")
                continue

            # ---------- clear / undo / redo ---------------------
            if command == "clear":
                calc.clear_history()
                print("History cleared")
                continue

            if command == "undo":
                print("Operation undone" if calc.undo() else "Nothing to undo")
                continue

            if command == "redo":
                print("Operation redone" if calc.redo() else "Nothing to redo")
                continue

            # ---------- save / load -----------------------------
            if command == "save":
                try:
                    calc.save_history()
                    print("History saved successfully")
                except Exception as e:
                    print(f"Error saving history: {e}")
                continue

            if command == "load":
                try:
                    calc.load_history()
                    print("History loaded successfully")
                except Exception as e:
                    print(f"Error loading history: {e}")
                continue

            # ====================================================
            #               arithmetic commands
            # ====================================================
            if command in [
                "add", "subtract", "multiply", "divide",
                "power", "root", "modulus",
            ]:
                try:
                    print("\nEnter numbers (or 'cancel' to abort):")
                    a = input("First number: ")
                    if a.lower() == "cancel":
                        print("Operation cancelled")
                        continue
                    b = input("Second number: ")
                    if b.lower() == "cancel":
                        print("Operation cancelled")
                        continue

                    # Step-1: call CalculationFactory
                    # (unit-test may patch this to raise Exception('Boom'))
                    try:
                        CalculationFactory.create(command, a, b)
                    except Exception as e:
                        print(f"Error: {e}")          # <- prints “Error: Boom”
                        logging.error(f"Factory error: {e}")
                        continue                      # back to prompt

                    # Step-2: follow original calculator flow
                    calc.set_operation(OperationFactory.create_operation(command))
                    result = calc.perform_operation(a, b)

                    # pretty Decimal formatting
                    if isinstance(result, Decimal):
                        if result == result.to_integral_value():
                            result = result.quantize(Decimal(1), rounding=ROUND_HALF_EVEN)
                        else:
                            result = result.normalize() # pragma: no cover

                    print(f"\nResult: {result}")

                except (ValidationError, OperationError) as e:
                    print(f"Error: {e}")
                except Exception as e:  # pragma: no cover
                    print(f"Error: {e}")              # safety net  # pragma: no cover
                    logging.error(f"Unexpected calc error: {e}")    # pragma: no cover
                continue  # end arithmetic branch

            # ---------- unknown command -------------------------
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

        # ── outer-loop exception handling ──────────────────────
        except KeyboardInterrupt:
            print("\nOperation cancelled")  # pragma: no cover
            continue    # pragma: no cover
        except EOFError:    
            print("\nInput terminated. Exiting…")
            break
        except Exception as e:  # pragma: no cover
            print(f"Error: {e}", file=sys.stderr)   # pragma: no cover
            logging.error(f"Fatal REPL error: {e}") # pragma: no cover
            continue


# Allow running directly
if __name__ == "__main__":
    calculator_repl()   # pragma: no cover
