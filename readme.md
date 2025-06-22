# 🧮 Calculator CLI – Python Modular Application

![CI](https://github.com/Hanyyoussef4/Calculator_CLI_Assignment5/actions/workflows/tests.yml/badge.svg)

<p align="left">
  <a href="https://github.com/Hanyyoussef4/Calculator_CLI_Assignment5" target="_blank">
    <img src="https://img.shields.io/badge/View%20Project-Click%20Here-brightgreen?style=for-the-badge" alt="View Project Button"/>
  </a>
</p>

> ```
> This is a professional-grade command-line calculator application built in Python using object-oriented principles and modular architecture.  
> It supports basic and advanced operations (addition, subtraction, multiplication, division, modulus, power, and square root), REPL interaction,  
> history tracking, undo/redo support, and a fully-tested pipeline using GitHub Actions.
> ```

---

## 📦 Project Setup

```text
Calculator/
├── app/                  # Core logic (Calculator, Operations, Calculations)
├── history/              # CSV-based history and memento tracking
├── tests/                # Full test suite (151+ tests with 100% coverage)
├── .github/workflows/    # CI pipeline with coverage enforcement
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
├── .env                  # Config file for max history size, encoding
└── readme.md             # You're here!
```

## 📦 Features
```text
✅ REPL interface for interactive command-line usage
✅ Add, Subtract, Multiply, Divide, Modulus, Power, Square Root
✅ Undo/Redo functionality (via Memento pattern)
✅ Operation history (saved as CSV)
✅ Input validation and error handling
✅ Full test suite with 100% line coverage
✅ GitHub Actions CI to enforce test & coverage on push
```
---
## 🛠️ Setup Instructions
---

### 1. Clone the Repository

```bash

git clone git@github.com:Hanyyoussef4/Calculator_CLI_Assignment5.git
cd Calculator_CLI_Assignment5

```
### 2. Install Required Packages
```bash
pip install -r requirements.txt
```
Run the Appilcation
```bash
paython main.py
```
----
## 🧪 Test Strategy and Approach

| Test File                   | Purpose                                        | Covers                                                                                                                                                           |
| --------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_operations.py`        | Unit tests for arithmetic logic                | Basic operations: `add`, `subtract`, `multiply`, `divide`, `modulus`, `power`, `square root`. Validates correct output and error handling (e.g., divide by zero) |
| `test_calculation_extra.py` | Tests calculation class integration with logic | Confirms calculation objects (`AddCalculation`, `DivideCalculation`, etc.) return expected results via `.execute()`                                              |
| `test_calculator_handle.py` | High-level testing of calculator state         | Validates calculator stack behavior, result persistence, and batch operation evaluation                                                                          |
| `test_memento.py`           | Memento pattern testing                        | Ensures `History` and `Caretaker` classes manage undo/redo history and CSV logging correctly                                                                     |
| `test_repl.py`              | End-to-end REPL input simulation               | Simulates REPL commands like `+`, `sqrt`, `undo`, etc. Verifies correct interaction and input validation                                                         |
---
## 🧪 Testing Tools & Automation
>Framework: pytest

>Coverage: pytest-cov used to verify 100% code coverage

>CI/CD: All tests run automatically using GitHub Actions on every push to main
---

## 🔄 Why This Approach?
```text
✅ Unit isolation: Each module is tested independently to catch issues early
✅ Full traceability: Failures point directly to affected functionality
✅ Edge case handling: Custom test cases ensure invalid inputs are gracefully handled
✅ Automation: GitHub Actions provides continuous integration and quality checks
```
## ▶️ How to Run the Tests
```bash
pytest --cov=app tests/
```
This command will execute the full suite and print a coverage report. You may also view detailed HTML coverage output using:

```bash
pytest --cov=app --cov-report=html tests/
```
## 📄 Notes

```text
The .env file is used to store configuration values (e.g., max history size).
The .env file is excluded from version control via .gitignore.
```