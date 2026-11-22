# Lab 5: Static Code Analysis — Energy Consumption & Tariff Calculator

**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310`  
**Section:** Section F  
**Course:** Software Engineering Laboratory (UE24CS351A)  
**Assigned Scenario:** Scenario 03 — Energy Tariff Calculator (`energy_system.py`)  

---

## Overview

This directory contains the source code, security audit reports, issue logs, reflection write-up, and official PDF submission for **Lab 5: Static Code Analysis**. 

The target program `energy_system.py` is a utility meter tracking system that records meter readings, calculates tiered electricity tariffs, flags anomalous high consumption, and persists readings to `meters.json`.

---

## Static Analysis Metrics Achieved

| Tool | Baseline Score / Issues | Final Remediated Result | Status |
| :--- | :---: | :---: | :---: |
| **Pylint** | `6.14 / 10.00` | **`10.00 / 10.00`** | Perfect clean score |
| **Bandit** | 1 High Severity Vulnerability (B307 `eval()`) | **0 Vulnerabilities** | Secured |
| **Flake8** | Multiple PEP 8 violations | **0 Violations (Clean exit code 0)** | Compliant |

---

## Key Vulnerabilities & Code Quality Issues Remediated

1. **Dangerous Code Execution (`eval()` — CWE-78 / Bandit B307):**
   * *Problem:* `eval()` was used on user input to parse numeric power factors.
   * *Remediation:* Replaced with safe AST numeric literal parsing and explicit validation.
2. **Mutable Default Arguments (Pylint W0102):**
   * *Problem:* Functions defined with `history=[]` caused state leakage across invocations.
   * *Remediation:* Adopted the `None` sentinel pattern (`history=None: history = []`).
3. **Broad / Bare Exception Clauses (Flake8 E722 / Pylint W0702):**
   * *Problem:* Bare `except:` clauses silenced unexpected runtime crashes.
   * *Remediation:* Replaced with specific exception handling tuples (`FileNotFoundError`, `json.JSONDecodeError`, `OSError`).
4. **Unmanaged File I/O Resources:**
   * *Problem:* Files opened without context managers risked file descriptor leaks.
   * *Remediation:* Enforced `with open(...) as f:` idiom across all read/write routines.

---

## Directory Structure

```
Lab5-Energy-Tariff/
├── energy_system.py                                  # Hardened and refactored python system
├── meters.json                                       # Meter registry data store
├── pylint_report.txt                                 # Pylint output (10.00/10)
├── bandit_report.txt                                 # Bandit security analysis report (0 vulns)
├── flake8_report.txt                                 # Flake8 style report (0 violations)
├── issues.md                                         # Detailed issue tracking table & fix documentation
├── reflection.md                                     # In-depth answers to lab reflection questions
├── generate_lab5_pdf.py                              # ReportLab script generating official PDF
├── PES2UG24CS310_Lab_5.pdf                           # Official generated submission PDF
├── Lab_5_Static_Code_Analysis_Student_handout.docx   # Original lab handout
└── README.md
```

---

## Verification Commands

```bash
# Run the application
python energy_system.py

# Run static analysis verification
pylint energy_system.py
bandit -r energy_system.py
flake8 energy_system.py

# Re-generate submission PDF
python generate_lab5_pdf.py
```
