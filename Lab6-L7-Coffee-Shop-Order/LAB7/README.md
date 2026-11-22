# L6_L7_03 — Coffee Shop Order

**Lab 7: Fuzzing for Input Validation Bugs with Hypothesis**  
**Course:** UE24CS351A: Software Engineering Laboratory  
**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310` | **Section:** F  

---

## 📌 Overview

This laboratory explores **fuzz testing** as a dynamic security and quality assurance technique using Python's **Hypothesis** property-based testing library. We detect, isolate, and remediate input validation vulnerabilities, boundary crashes, and unhandled exceptions in `processor.py`.

---

## 📂 Deliverables & Repository Structure

| File | Description |
| :--- | :--- |
| [`processor.py`](./processor.py) | Hardened order processor script with defensive validation, casing fixes, and safe parsing |
| [`test_processor.py`](./test_processor.py) | Comprehensive Hypothesis fuzz testing suite (6 property-based test cases) |
| [`generate_terminal_screenshots.py`](./generate_terminal_screenshots.py) | High-resolution terminal capture and rendering utility |
| [`generate_lab7_pdf.py`](./generate_lab7_pdf.py) | Automated ReportLab PDF report generation script |
| [`PES2UG24CS310_Lab_7.pdf`](./PES2UG24CS310_Lab_7.pdf) | Official laboratory submission report |
| `Lab7_Original_Buggy_Output.png` | Terminal screenshot: Buggy processor execution & crashes |
| `Lab7_Fuzz_Test_Failures.png` | Terminal screenshot: Hypothesis fuzz testing failures on buggy code |
| `Lab7_Fixed_Application_Output.png` | Terminal screenshot: Hardened processor handling valid & edge-case inputs |
| `Lab7_Passing_Fuzz_Tests.png` | Terminal screenshot: 100% passing Hypothesis test suite |

---

## 🔍 Vulnerabilities Identified & Remediations Applied

| Function | Discovered Vulnerabilities | Root Cause | Defensive Hardening Fix |
| :--- | :--- | :--- | :--- |
| `lookup_drink_code` | `AttributeError` on `NoneType`, `KeyError` on `''` and `'MOc'` | Direct `.upper()` on `None`; typo `'MOc'` in dictionary while query normalized to uppercase `'MOC'`; raw dict index `menu_prices[...]` | Type guard `isinstance(s, str)`; whitespace stripping; corrected `'MOC': 5.00`; safe access via `dict.get(prefix, None)` |
| `calculate_average_shot_cost` | `AttributeError` on `NoneType`, `ValueError` on empty/non-numeric tokens, `ZeroDivisionError` on empty price list | Direct `.split(',')` on `None`; unhandled `float()` conversion; dividing by `len(prices) == 0` | Type guard; token stripping; `try-except ValueError` float conversion; NaN/Inf/negative filtering; safe fallback `0.0` |
| `parse_order_modifiers` | `AttributeError` on `NoneType`, `ValueError` on unpack (missing or multiple `:`) | Direct `.split(';')` on `None`; strict 2-element unpack `k, v = item.split(':')` | Type guard; verify `':' in item`; bounded `item.split(':', 1)`; key/val whitespace stripping; empty key filtering |

---

## 🚀 Execution Instructions

### 1. Run the Hardened Processor
```bash
python processor.py
```

### 2. Run Hypothesis Fuzz Test Suite
```bash
pytest test_processor.py -v
```

### 3. Regenerate Terminal Screenshots & PDF Report
```bash
python generate_terminal_screenshots.py
python generate_lab7_pdf.py
```
