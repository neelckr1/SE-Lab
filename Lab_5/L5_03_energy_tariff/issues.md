# Lab 5: Identified Static Code Analysis Issues

**Student Name**: Neel Chandrakar  
**SRN**: PES2UG24CS310  
**Repository**: [SETAPESU26/L5_03_energy_tariff](https://github.com/SETAPESU26/L5_03_energy_tariff)  
**File Analyzed**: `energy_system.py`  

---

## Issue Documentation Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Insecure `eval()` Execution** | Security (Bandit B307 / CWE-78, Pylint W0123) | 63 | `eval(adjustment)` parses user-supplied string directly with `eval()`, allowing arbitrary code execution (RCE). | Replace `eval()` with safe numeric casting (`float()` or `ast.literal_eval()`) wrapped in `try/except ValueError`. |
| **Mutable Default Argument** | Bug / Logic (Pylint W0102) | 12 | `history=[]` creates a single shared list across all function invocations, leaking state across calls. | Change default argument to `history=None` and initialize `history = []` inside the function body. |
| **Bare `except:` Clause** | Bug / Robustness (Pylint W0702, Flake8 E722) | 44 | `except:` catches all exceptions, masking critical interruptions (`KeyboardInterrupt`, `SystemExit`) and runtime errors. | Replace with explicit exception tuple: `except (FileNotFoundError, json.JSONDecodeError, OSError) as err:`. |
| **Unmanaged File Handles & Missing Encoding** | Resource Leak (Pylint R1732, W1514) | 42, 48 | `open()` is called without a context manager (`with`) and without explicit encoding, risking resource exhaustion on errors. | Refactor to `with open(file, "r", encoding="utf-8") as f:` and `with open(file, "w", encoding="utf-8") as f:`. |
| **Unused Import (`sys`)** | Code Smell (Pylint W0611, Flake8 F401) | 2 | `import sys` is imported but never used anywhere in the script. | Remove the unused `import sys` statement. |
| **Global State Mutation** | Architecture / Smell (Pylint W0603) | 27, 40 | `global` keyword used to mutate module-level variables (`RATE_TIER_*`, `meters`), making functions impure and hard to test. | Encapsulate state into an `EnergySystem` class or maintain controlled module access functions. |
| **Old-Style `%` String Formatting** | Style (Pylint C0209) | 59, 60, 66 | C-style `%` string interpolation used instead of modern, readable Python 3 f-strings. | Convert to PEP 498 f-strings: `f"Bill {meter_id}: {total:.2f}"`. |
| **Unnecessary `elif` after `return`** | Style / Complexity (Pylint R1705) | 19 | Redundant `elif` blocks immediately following `return` statements create unnecessary nesting depth. | Flatten branching by replacing `elif` with `if` after `return`. |
| **Missing Docstrings** | Documentation (Pylint C0114, C0116) | 1, 12, 17, 26, 32, 39, 47, 52 | Module and functions lack docstrings describing purpose, arguments, and return values. | Add comprehensive PEP 257 compliant docstrings to module and all functions/methods. |
| **PEP 8 Formatting & Line Length** | Style (Flake8 E302, E305, E501) | 12, 17, 24, 26, 32, 39, 47, 52, 62, 68 | Insufficient blank lines between functions (1 found, 2 required) and lines exceeding 79 characters. | Format code with exactly 2 blank lines between top-level definitions and wrap long statements. |
| **Negative Reading Domain Bug** | Functional Bug (Domain Logic) | 14, 55 | `record_reading("M-03", -50)` permits negative consumption, generating negative billing (`-192.50`), which is invalid. | Add input validation to ensure `units >= 0`; raise `ValueError` for negative consumption. |
