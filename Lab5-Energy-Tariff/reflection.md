# Lab 5: Reflection on Static Code Analysis

**Student Name**: Neel Chandrakar  
**SRN**: PES2UG24CS310  
**Course**: Software Engineering Laboratory (UE24CS351A)  
**Assigned Repository**: [SETAPESU26/L5_03_energy_tariff](https://github.com/SETAPESU26/L5_03_energy_tariff)  
**File Analyzed**: `energy_system.py`  

---

## Question 1: Purpose & Scope of Static Code Analysis in the SDLC

### Reflection:
Static code analysis involves the automated inspection of source code without executing the program. In modern Software Development Life Cycles (SDLC), particularly within Continuous Integration and Continuous Delivery (CI/CD) pipelines, static analysis acts as the first line of defense ("shift-left" testing).

* **Complementary to Dynamic Testing**: While dynamic testing (unit, integration, and end-to-end tests) evaluates runtime behavior, state transitions, and business logic execution, it requires executable test cases and comprehensive code coverage. Static analysis, by contrast, examines 100% of the reachable syntax paths instantly.
* **Early Defect Detection**: Static analysis catches syntactic bugs, design smells, type mismatches, and compliance violations during development or pull request reviews—long before code reaches staging or production environments. This drastically reduces the cost and remediation overhead of defect resolution.
* **Scope & Boundaries**: Static analysis tools excel at identifying structural and semantic patterns (e.g., dead code, unsafe calls, naming standard violations). However, they cannot verify whether a system satisfies the end-user's domain requirements (such as whether an electricity tariff tier formula accurately reflects utility regulations), proving that static analysis must work in tandem with functional testing.

---

## Question 2: Comparative Analysis of Tools — Pylint, Bandit, and Flake8

### Reflection:
Each of the three industry-standard tools employed in this lab targets distinct facets of code quality:

| Tool | Core Role & Specialization | Analysis Mechanism | Strengths & Nuances |
| :--- | :--- | :--- | :--- |
| **Pylint** | *The Strict Code Reviewer* | Parses the Abstract Syntax Tree (AST), constructs dependency graphs, and inspects object semantics. | Detects subtle logical bugs (mutable default arguments, unreachable statements, duplicate code), design flaws (global variable mutation, high cyclomatic complexity), and docstring omissions. Assigns a quantitative quality score (e.g., from 6.14/10 to 10.00/10). |
| **Bandit** | *The Security Guard* | Scans AST nodes specifically against vulnerability rule sets and Common Weakness Enumeration (CWE) patterns. | Pinpoints critical security anti-patterns (arbitrary execution via `eval()`, hardcoded credentials, unsafe temp files, insecure cryptographic hashing). Ranks findings by Severity (Low/Medium/High) and Confidence. |
| **Flake8** | *The Style & Formatting Linter* | Combines PyFlakes (syntax/logical errors), pycodestyle (PEP 8 compliance), and Ned Batchelder's McCabe complexity. | Extremely fast linter enforcing team-wide consistency: line length limits (≤79 characters), blank line spacing (`E302`/`E305`), unused imports (`F401`), and bare exceptions (`E722`). |

**Key Takeaway**: Relying on any single tool leaves blind spots. For instance, Flake8 missed the dangerous mutable default list and Pylint was less targeted about CWE vulnerabilities than Bandit. Running all three in tandem provides holistic coverage across style, architecture, and security.

---

## Question 3: Analysis of Identified Issues & Resolution Strategies

### Reflection on Specific Bugs in `energy_system.py`:

1. **Mutable Default Arguments (`history=[]` on Line 12)**:
   * *Problem*: In Python, default parameter expressions are evaluated once when the function definition is executed, not at each call. A mutable object like a list or dictionary is retained across successive invocations. In `energy_system.py`, all meter recordings were silently aggregating into the same shared list, leaking state between separate test calls.
   * *Fix*: Set default to `history=None` and initialize `history = []` inside the function body only if `history is None`.

2. **Insecure Execution via `eval()` (Line 63)**:
   * *Problem*: Accepting an expression string from standard input and executing it directly via `eval(adjustment)` creates a Remote Code Execution (RCE) vulnerability (Bandit B307 / CWE-78). A malicious user could input `__import__('os').system('rm -rf /')` or read arbitrary system files.
   * *Fix*: Replaced `eval()` with structured numerical parsing (`safe_parse_expression`) that isolates numeric values, supports basic arithmetic (`10 + 20`), and gracefully rejects non-numeric payloads without invoking a dynamic interpreter.

3. **Overly Broad Exception Handling (`except:` on Line 44)**:
   * *Problem*: A bare `except:` block catches `BaseException`, silently swallowing system interruptions like `KeyboardInterrupt` (Ctrl+C), `SystemExit`, and unrelated memory or syntax errors. This prevents clean process termination and masks genuine bugs.
   * *Fix*: Replaced with a targeted exception tuple: `except (FileNotFoundError, json.JSONDecodeError, OSError)`.

4. **Resource Leaks in File Operations (Lines 42, 48)**:
   * *Problem*: Using raw `f = open(...)` without a context manager risks leaving file descriptors open if an exception occurs prior to `f.close()`. Additionally, omitting explicit encoding (`encoding="utf-8"`) causes platform-dependent encoding mismatches.
   * *Fix*: Refactored to `with open(file, "r", encoding="utf-8") as file_handle:`.

5. **Domain Logic Flaw (Unflagged Negative Consumption)**:
   * *Problem*: Static linters check code syntax and patterns, but they do not know that electricity meter readings cannot physically be negative. `record_reading("M-03", -50)` resulted in a negative electricity bill (`-192.50`).
   * *Fix*: Added input validation in `record_reading` to flag negative values and safeguard billing logic.

---

## Question 4: Long-Term Impact on Maintainability, Security, and Code Quality

### Reflection:
Adopting automated static code analysis fundamentally transforms software engineering practices:

* **Preventing Technical Debt**: Coding shortcuts (e.g., unclosed file handles, global variables, copy-pasted blocks) quickly compound into technical debt. Linters enforce architectural cleanliness and modularity continuously, preventing erosion of codebase health over time.
* **Proactive Security Posture**: Security should never be an afterthought. Integrating tools like Bandit into pre-commit hooks prevents dangerous patterns (such as injection vulnerabilities or credential leakage) from ever entering version control.
* **Streamlined Code Reviews & Onboarding**: Automating formatting and PEP 8 enforcement via Flake8 eliminates bikeshedding during peer code reviews, freeing developers to focus on architectural decisions and business logic.
* **Self-Documenting Codebase**: Enforcing comprehensive docstrings (`C0114`, `C0116`) and type annotations ensures that modules remain transparent, maintainable, and verifiable as team sizes scale.
