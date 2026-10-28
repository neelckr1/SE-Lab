# UE24CS351A: Software Engineering Laboratory

**PES University — Department of Computer Science & Engineering**  
**Academic Year:** 2026–2027 (5th Semester)  
**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310`  
**Section:** Section F  

This repository consolidates all laboratory assignments, practical implementations, test suites, static code analysis reports, and official submission documents for the **Software Engineering Lab (UE24CS351A)**.

---

## 🗂️ Laboratory Directory & Index

| Directory | Topic / Assignment | Original Repo | Key Metrics Achieved | Submission Report |
| :--- | :--- | :--- | :---: | :---: |
| [`Lab_3/`](./Lab_3) | Software Architecture & System Design Analysis | — | Complete Architecture Review | [Lab 3 PDF](./Lab_3/PES2UG24CS310_Lab_3.pdf) |
| [`Lab_5/`](./Lab_5) | Static Code Analysis & Security Hardening (`energy_system.py`) | [`L5_03_energy_tariff`](https://github.com/neelckr1/L5_03_energy_tariff) | **Pylint: 10.00/10**<br/>Bandit: 0 vulns<br/>Flake8: 0 issues | [Lab 5 PDF](./Lab_5/PES2UG24CS310_Lab_5.pdf) |
| [`Lab_6/`](./Lab_6) | Code & Branch Coverage Analysis (`coffee_shop_order.py`) | [`L6_L7_03_coffee_shop_order`](https://github.com/neelckr1/L6_L7_03_coffee_shop_order) | **100% Line Coverage**<br/>**100% Branch Coverage** (38/38) | [Lab 6 PDF](./Lab_6/PES2UG24CS310_Lab_6.pdf) |
| [`vibe_coding/`](./vibe_coding) | Automated Game Engine & End-to-End Testing | [`vibe_coding`](https://github.com/neelckr1/vibe_coding) | 100% Unit + E2E Tests Passing | [Vibe Coding README](./vibe_coding/README.md) |

---

## 📘 Detailed Lab Summaries

### 1. [Lab 3: Architecture & System Design](./Lab_3)
* **Objective:** Comprehensive software architecture modeling, evaluating component coupling, cohesion, and structural patterns.
* **Key Deliverable:** [`Lab_3/PES2UG24CS310_Lab_3.pdf`](./Lab_3/PES2UG24CS310_Lab_3.pdf) along with the course student handout.

---

### 2. [Lab 5: Static Code Analysis & Remediation (`energy_system.py`)](./Lab_5)
* **Objective:** Detect and resolve code quality smells, architectural antipatterns, and security vulnerabilities using **Pylint**, **Bandit**, and **Flake8**.
* **Key Fixes & Improvements:**
  * **Bandit (CWE-78 / B307):** Replaced dangerous arbitrary `eval()` call with safe numeric AST parsing.
  * **Mutable Default Arguments:** Fixed `history=[]` leakage by adopting the `None` sentinel pattern.
  * **Exception Handling:** Replaced bare `except:` clauses with specific exception tuples (`FileNotFoundError`, `json.JSONDecodeError`, `OSError`).
  * **Resource Management:** Ensured all file operations utilize context managers (`with open(...)`).
  * **PEP 8 Compliance:** Formatted line lengths, imports, and docstrings.
* **Verification Metrics:**
  * **Pylint:** Rated **`10.00 / 10.00`** (baseline was 6.14/10).
  * **Bandit:** **0 Security Vulnerabilities** across 151 LOC.
  * **Flake8:** **0 PEP 8 violations** (clean exit code 0).
* **Execution:**
  ```bash
  cd Lab_5/L5_03_energy_tariff
  pylint energy_system.py
  bandit -r energy_system.py
  flake8 energy_system.py
  ```

---

### 3. [Lab 6: Code and Branch Coverage Analysis (`coffee_shop_order.py`)](./Lab_6)
* **Objective:** Measure and maximize statement and branch coverage using Python's `coverage.py` and `pytest`.
* **Application Overview:** Validates coffee orders by size, customizations (syrups, allergy safeguards), applies membership discounts, flags audits, and monitors espresso machine temperature overheat cycles.
* **Test Suites:**
  * [`CodeCoverageTest_coffee_shop_order.py`](./Lab_6/L6_L7_03_coffee_shop_order/Lab%206/CodeCoverageTest_coffee_shop_order.py): 15 tests verifying all execution paths.
  * [`BranchCoverageTest_coffee_shop_order.py`](./Lab_6/L6_L7_03_coffee_shop_order/Lab%206/BranchCoverageTest_coffee_shop_order.py): 20 tests evaluating all true/false decision outcomes, syrup price cap boundaries, and overheat streak resets.
* **Coverage Results:**
  * **Line Coverage:** **100%** (54/54 statements, 0 missed).
  * **Branch Coverage:** **100%** (38/38 branches evaluated, 0 partial/missed).
* **Deliverables:** High-resolution terminal screenshots ([Code Coverage](./Lab_6/L6_L7_03_coffee_shop_order/Lab%206/code_coverage_report.png), [Branch Coverage](./Lab_6/L6_L7_03_coffee_shop_order/Lab%206/branch_coverage_report.png)) and report PDF ([`PES2UG24CS310_Lab_6.pdf`](./Lab_6/PES2UG24CS310_Lab_6.pdf)).
* **Execution:**
  ```bash
  cd "Lab_6/L6_L7_03_coffee_shop_order/Lab 6"
  coverage run -m pytest CodeCoverageTest_coffee_shop_order.py
  coverage run --branch -m pytest BranchCoverageTest_coffee_shop_order.py
  coverage report -m
  ```

---

### 4. [Vibe Coding: Fishing Game & End-to-End Testing](./vibe_coding)
* **Objective:** Build an interactive 2D simulation game in Pygame paired with automated unit tests and end-to-end (E2E) gameplay recording verification.
* **Key Features:** Real-time casting physics, hook collision logic, fish spawning cycles, dynamic score multipliers, and game-over state transitions.
* **Automated Testing:** Test suite covering game engine cycles, hook kinematics, and E2E gameplay runs with screenshot captures and gameplay video recordings.
* **Execution:**
  ```bash
  cd vibe_coding
  pytest tests/
  python fishing/main.py
  ```

---

## 🛠️ Environment & Prerequisites

To execute test suites and tools across all laboratories:

```bash
# Clone the repository
git clone git@github.com:neelckr1/SE-Lab.git
cd SE-Lab

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pytest coverage pylint bandit flake8 pillow reportlab pygame
```

---

*Authored by **Neel Chandrakar** (`PES2UG24CS310`), Department of Computer Science & Engineering, PES University.*
