# Lab 3: Component Modelling & Architectural Pattern Selection

**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310`  
**Section:** Section F  
**Course:** Software Engineering Laboratory (UE24CS351A)  
**Assigned Scenario:** Scenario 03 — Campus Placement and Internship Pipeline  

---

## Overview

This directory contains the component modeling, architectural pattern selection, trade-off analysis, and official submission documentation for **Lab 3**. 

The goal of this laboratory is to select, justify, and model the optimal software architecture pattern for the **Campus Placement & Internship System**.

---

## Architecture Selection: Layered Architecture Pattern

For the Campus Placement and Internship System, the **Layered (N-Tier) Architectural Pattern** was selected over alternative paradigms (such as Microservices or Event-Driven Architecture).

```
+-------------------------------------------------------------+
|                     Presentation Layer                      |
|       [User Interface: Student & Placement Officer Views]   |
+------------------------------+------------------------------+
                               | (REST / API Boundary)
                               v
+-------------------------------------------------------------+
|                       Business Layer                        |
|  [Identity & Access Manager]     [Recruitment Drive Manager]|
+------------------------------+------------------------------+
                               | (Secure Data Access)
                               v
+-------------------------------------------------------------+
|                   Data / Integration Layer                  |
|          [Pipeline Application & User Database]             |
+-------------------------------------------------------------+
```

### Architectural Tiers & Responsibilities

1. **Presentation Layer (User Interface):**
   * Encapsulates the Student View (profile submission, eligibility verification, job browsing, interview tracking) and the Placement Officer View (drive creation, shortlisting, reporting).
   * Decoupled from the database to prevent direct query execution or sensitive credential exposure.

2. **Business / Service Layer:**
   * **Identity & Access Manager:** Handles user authentication, role-based authorization (RBAC), and session validation before incoming requests reach business operations.
   * **Recruitment Drive Manager:** Encapsulates core business rules including eligibility filtering (CGPA cutoff formulas, active backlogs), application submission states, interview round scheduling, and offer letters.

3. **Data / Integration Layer:**
   * **Pipeline Application & User Database:** Stores relational entities including student profiles, recruiter drives, student applications, and placement offer records with ACID transaction guarantees.

---

## Justification & Trade-Off Analysis

| Criteria | Layered Architecture Rationale |
| :--- | :--- |
| **Separation of Concerns** | Clear boundaries between presentation logic, business rules, and persistent storage make the placement system simpler to develop, test, maintain, and audit. |
| **Domain Cohesion** | Core functions (authentication, recruitment drives, applications) are closely coupled within a coherent workflow. Layered interfaces avoid the operational complexity and network latency of distributed microservices. |
| **Security Boundary** | Restricts the presentation layer from accessing student records directly. All operations pass through the Identity & Access Manager at the service boundary, enforcing strict access controls on confidential student data. |
| **Performance Efficiency** | Common queries (drive retrieval, status checks) are processed in-process via dedicated service components, avoiding distributed serialization overhead and RPC round-trips. |

---

## Deliverables

- [`PES2UG24CS310_Lab_3.pdf`](./PES2UG24CS310_Lab_3.pdf): Official submission document containing the architecture rationale, component specifications, and UML component model.
- [`Lab_3_Architecture_Student_handout.pdf`](./Lab_3_Architecture_Student_handout.pdf): Official course handout outlining assignment guidelines and requirements.
