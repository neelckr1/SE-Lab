# PESU – Software Engineering Labs

This repository contains my Software Engineering laboratory assignments completed as part of the Computer Science and Engineering curriculum at PES University.

**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310`  
**Section:** Section F  
**Semester:** 5th Semester  
**Course Code:** UE24CS351A  
**Assigned Scenario:** Scenario 03 (Campus Placement Pipeline / Energy Tariff / Coffee Shop Order)  

---

## Repository Structure

| Lab | Project / Scenario | Description | Directory Link |
|:---|:---|:---|:---|
| **Lab 1** | Campus Placement & Internship Pipeline | Requirements specification (SRS), UML use case modeling, and actor interaction flows | [`Lab1-L2-Campus-Placement-Pipeline/`](./Lab1-L2-Campus-Placement-Pipeline) |
| **Lab 2** | Campus Placement & Internship Pipeline | Agile product backlog creation, user story management, Fibonacci story pointing, sprint planning, and sprint simulation in Jira | [`Lab1-L2-Campus-Placement-Pipeline/`](./Lab1-L2-Campus-Placement-Pipeline) |
| **Lab 3** | Campus Placement Architecture | Component modeling, architectural trade-off analysis, and layered architecture pattern selection | [`Lab3-Campus-Placement-Architecture/`](./Lab3-Campus-Placement-Architecture) |
| **Lab 4** | Fishing Game | 2D Pygame simulation, collision bug remediation, feature development (scoring, timed rounds, player casting), and automated E2E testing | [`Lab4-Fishing-Game/`](./Lab4-Fishing-Game) |
| **Lab 5** | Energy Tariff Calculator | Static code analysis and security auditing using Pylint (10.00/10), Bandit (0 vulns), and Flake8 (0 issues) | [`Lab5-Energy-Tariff/`](./Lab5-Energy-Tariff) |
| **Lab 6** | Coffee Shop Order System | Statement and branch coverage analysis using Coverage.py and Pytest, achieving 100% line and 100% branch coverage | [`Lab6-L7-Coffee-Shop-Order/LAB6/`](./Lab6-L7-Coffee-Shop-Order/LAB6) |
| **Lab 7** | Coffee Shop Order System (Processor) | Property-based fuzz testing using Hypothesis to expose input validation defects, followed by defensive code hardening | [`Lab6-L7-Coffee-Shop-Order/LAB7/`](./Lab6-L7-Coffee-Shop-Order/LAB7) |

---

## Tools and Technologies

- **Programming Language:** Python 3
- **Version Control:** Git & GitHub
- **Testing & Fuzzing Frameworks:** Pytest, Coverage.py, Hypothesis
- **Static Code Analysis & Security:** Pylint, Bandit, Flake8
- **Game Engine & Media:** Pygame, ImageIO, Pillow
- **Project Management:** Jira Software (Scrum, Epics, Sprints, Burndown Charts)
- **Modeling & Architecture:** UML Use Case & Component Diagrams (draw.io / Layered Architecture)
- **Document Generation:** ReportLab (automated PDF submission generation)

---

## Folder Structure

```
PESU-SE-Labs/
├── Lab1-L2-Campus-Placement-Pipeline/
│   ├── ES2UG24CS310-NEEL-LAB1.pdf
│   ├── Lab2_NeelChandrakar_PES2UG24CS310.pdf
│   └── README.md
├── Lab3-Campus-Placement-Architecture/
│   ├── Lab_3_Architecture_Student_handout.pdf
│   ├── PES2UG24CS310_Lab_3.pdf
│   └── README.md
├── Lab4-Fishing-Game/
│   ├── game/
│   │   ├── catch.py
│   │   ├── fish.py
│   │   ├── game_engine.py
│   │   ├── hook.py
│   │   └── renderer.py
│   ├── tests/
│   ├── e2e_screenshots/
│   ├── videos/
│   ├── e2e_game_test.py
│   ├── main.py
│   ├── pytest.ini
│   ├── record_gameplay_videos.py
│   ├── requirements.txt
│   └── README.md
├── Lab5-Energy-Tariff/
│   ├── energy_system.py
│   ├── meters.json
│   ├── pylint_report.txt
│   ├── bandit_report.txt
│   ├── flake8_report.txt
│   ├── reflection.md
│   ├── issues.md
│   ├── generate_lab5_pdf.py
│   ├── PES2UG24CS310_Lab_5.pdf
│   ├── Lab_5_Static_Code_Analysis_Student_handout.docx
│   └── README.md
├── Lab6-L7-Coffee-Shop-Order/
│   ├── LAB6/
│   │   ├── coffee_shop_order.py
│   │   ├── test_coffee_shop.py
│   │   ├── CodeCoverageTest_coffee_shop_order.py
│   │   ├── BranchCoverageTest_coffee_shop_order.py
│   │   ├── code_coverage_report.png
│   │   ├── branch_coverage_report.png
│   │   ├── generate_terminal_screenshots.py
│   │   ├── generate_lab6_pdf.py
│   │   ├── PES2UG24CS310_Lab_6.pdf
│   │   ├── Lab_6_Code_Branch_Coverage_Student_handout.pdf
│   │   └── README.md
│   ├── LAB7/
│   │   ├── processor.py
│   │   ├── test_processor.py
│   │   ├── Lab7_Original_Buggy_Output.png
│   │   ├── Lab7_Fuzz_Test_Failures.png
│   │   ├── Lab7_Fixed_Application_Output.png
│   │   ├── Lab7_Passing_Fuzz_Tests.png
│   │   ├── generate_terminal_screenshots.py
│   │   ├── generate_lab7_pdf.py
│   │   ├── PES2UG24CS310_Lab_7.pdf
│   │   ├── Lab_7_FuzzTesting_Student_Handout.pdf
│   │   └── README.md
│   ├── .gitignore
│   └── README.md
├── .gitignore
└── README.md
```

---

## Purpose

This repository serves as a consolidated collection of my Software Engineering lab implementations, architectural designs, test suites, static analysis reports, and submission documents.

**University:** PES University  
**Department:** Computer Science and Engineering  
