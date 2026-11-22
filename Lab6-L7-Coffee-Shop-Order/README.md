# Lab 6 & Lab 7: Coffee Shop Order System

**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310`  
**Section:** Section F  
**Course:** Software Engineering Laboratory (UE24CS351A)  
**Assigned Scenario:** Scenario 03 — Coffee Shop Order System (`coffee_shop_order.py` & `processor.py`)  

---

## Overview

This directory encapsulates the testing, dynamic analysis, and defensive hardening assignments for **Lab 6** and **Lab 7** based on the Coffee Shop Order Processing System:

1. **`LAB6/` (Code & Branch Coverage Testing):** Measuring, designing, and achieving 100% line coverage and 100% branch coverage on `coffee_shop_order.py` using `pytest` and `coverage.py`.
2. **`LAB7/` (Hypothesis Fuzz Testing & Input Hardening):** Performing property-based fuzz testing using **Hypothesis** on `processor.py` to identify hidden crashes, data validation gaps, unhandled exceptions, and subsequent code hardening.

---

## Directory Organization

```
Lab6-L7-Coffee-Shop-Order/
├── LAB6/
│   ├── coffee_shop_order.py                              # Target application under test
│   ├── test_coffee_shop.py                               # Base unit tests
│   ├── CodeCoverageTest_coffee_shop_order.py             # 15 tests achieving 100% statement coverage
│   ├── BranchCoverageTest_coffee_shop_order.py           # 20 tests evaluating all 38 decision branches
│   ├── code_coverage_report.png                          # Terminal screenshot: 100% Line Coverage
│   ├── branch_coverage_report.png                        # Terminal screenshot: 100% Branch Coverage
│   ├── generate_terminal_screenshots.py                  # High-res terminal screenshot generator
│   ├── generate_lab6_pdf.py                              # ReportLab script generating official PDF
│   ├── PES2UG24CS310_Lab_6.pdf                           # Official generated submission PDF
│   ├── Lab_6_Code_Branch_Coverage_Student_handout.pdf   # Original lab handout
│   └── README.md                                         # Lab 6 documentation
├── LAB7/
│   ├── processor.py                                      # Defensively hardened order processor
│   ├── test_processor.py                                 # Hypothesis property-based fuzz test suite
│   ├── Lab7_Original_Buggy_Output.png                    # Terminal screenshot: Initial buggy execution
│   ├── Lab7_Fuzz_Test_Failures.png                       # Terminal screenshot: Hypothesis fuzz crash discovery
│   ├── Lab7_Fixed_Application_Output.png                 # Terminal screenshot: Hardened execution
│   ├── Lab7_Passing_Fuzz_Tests.png                       # Terminal screenshot: 100% Passing Hypothesis fuzz tests
│   ├── generate_terminal_screenshots.py                  # Terminal image generator
│   ├── generate_lab7_pdf.py                              # ReportLab script generating official PDF
│   ├── PES2UG24CS310_Lab_7.pdf                           # Official generated submission PDF
│   ├── Lab_7_FuzzTesting_Student_Handout.pdf             # Original lab handout
│   └── README.md                                         # Lab 7 documentation
├── .gitignore
└── README.md
```

---

## Lab 6: Code and Branch Coverage Analysis

### Coverage Metrics Achieved

* **Line Coverage:** **100%** (54 / 54 statements executed, 0 missed)
* **Branch Coverage:** **100%** (38 / 38 branch decisions evaluated, 0 missed / partial)
* **Status:** Passed all 35 tests across both suites without failure.

### Test Suites
- [`CodeCoverageTest_coffee_shop_order.py`](./LAB6/CodeCoverageTest_coffee_shop_order.py): Comprehensive suite targeting every statement in drink pricing, discount calculation, inventory audits, and overheat safety cycles.
- [`BranchCoverageTest_coffee_shop_order.py`](./LAB6/BranchCoverageTest_coffee_shop_order.py): Evaluates boolean truth tables, syrup cap boundary conditions, loyalty discounts, and machine cooldown streak transitions.

### Verification Commands
```bash
cd LAB6
coverage run -m pytest CodeCoverageTest_coffee_shop_order.py
coverage run --branch -m pytest BranchCoverageTest_coffee_shop_order.py
coverage report -m
```

---

## Lab 7: Fuzz Testing with Hypothesis

### Fuzzing Discoveries & Vulnerabilities Uncovered
Using property-based fuzz testing with **Hypothesis**, numerous unhandled crash vectors were exposed in the initial `processor.py`:
1. **`lookup_drink_code`**: Crashed with `AttributeError` on non-string inputs (`None`), `KeyError` on empty strings or unrecognized codes, and casing lookup mismatches (`'MOc'` vs `'MOC'`).
2. **`calculate_average_shot_cost`**: Crashed with `AttributeError` on `None`, `ValueError` attempting float conversions on non-numeric/empty string tokens, and `ZeroDivisionError` when no valid numbers were present.
3. **`parse_order_modifiers`**: Crashed with `AttributeError` on `None`, and `ValueError` unpack errors when tokens lacked colons (`:`) or contained multiple colons.

### Defensive Hardening Applied
- Strict type guards with `isinstance(val, str)` returning safe fallback defaults (`None`, `0.0`, `{}`).
- Whitespace stripping and dictionary lookup resilience using `.get()`.
- Safe numeric float parsing with NaN / Infinity filtering and zero-division guards.
- Delimiter existence validation (`':' in token`) with bounded `split(':', 1)`.

### Verification Commands
```bash
cd LAB7
pytest test_processor.py -v
python processor.py
```
