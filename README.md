# 🏥 Hospital Appointment & Patient Care Management System (CarePulse DBMS)

[![DBMS PBL](https://img.shields.io/badge/Course-DBMS%20PBL%20Project%2003-0D9488?style=for-the-badge)](https://github.com/Himanshu-Git-101/DBMS_PBL)
[![Status](https://img.shields.io/badge/Review%20Milestones-Review%201%20|%202%20|%203%20(Completed)-0284C7?style=for-the-badge)](https://github.com/Himanshu-Git-101/DBMS_PBL)
[![Python](https://img.shields.io/badge/Python-3.8%2B%20(Zero%20Dependencies)-7C3AED?style=for-the-badge&logo=python)](https://github.com/Himanshu-Git-101/DBMS_PBL)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20/%20PostgreSQL%20(3NF)-10B981?style=for-the-badge&logo=sqlite)](https://github.com/Himanshu-Git-101/DBMS_PBL)

A comprehensive, production-grade Relational Database Management System (RDBMS) paired with an interactive Python application prototype for hospital appointments, clinical consultations, diagnostics, ward bed allocation, and financial billing.

Designed, normalized up to **Third Normal Form (3NF)**, and verified across all semester review milestones (**Review 1**, **Review 2**, and **Review 3**).

---

## 📌 Table of Contents
1. [Project Overview & Problem Statement](#-project-overview--problem-statement)
2. [Review Presentations Suite (1st, 2nd & 3rd)](#-review-presentations-suite)
3. [System Architecture & 3NF Schema](#-system-architecture--3nf-schema)
4. [How to Use and Run `app.py`](#-how-to-use-and-run-apppy)
5. [Interactive Demo Data & 1-Click Evaluation Features](#-interactive-demo-data--1-click-evaluation-features)
6. [5 Production Database Views](#-5-production-database-views)
7. [Repository File Structure](#-repository-file-structure)

---

## 🏥 Project Overview & Problem Statement

Modern hospitals handle thousands of concurrent transactions across distinct medical departments. In legacy or unintegrated hospital setups, disconnected departmental records produce operational bottlenecks:
- **Scheduling Conflicts:** Multiple patients booked for the same specialist doctor in overlapping time windows.
- **Bed Disputes:** Concurrent admission of two active patients to the same physical hospital bed.
- **Fragmented Medical Histories:** Doctors unable to inspect a patient's historical consultations, prior diagnoses, and lab results in a unified view.
- **Revenue Leakage:** Overbilling, uncollected diagnostic fees, and inaccurate payment tracking.

### Core Objectives:
1. **Centralize Clinical & Administrative Data:** Connect Outpatient, Inpatient, Diagnostics, and Accounts into a unified relational database.
2. **Eliminate Redundancy via 3NF Normalization:** Decompose data to eliminate insertion, update, and deletion anomalies.
3. **Database-Level Integrity Defense:** Implement database triggers and check constraints that mathematically reject slot overlaps, dual bed occupancy, backwards dates, and payment overruns.
4. **Interactive Working Prototype:** Deliver a zero-dependency Python application with both a responsive Web Dashboard and a terminal CLI.

---

## 📊 Review Presentations Suite

The repository contains PowerPoint (`.pptx`) decks and browser-based interactive slides (`.html`) for all three reviews:

| Milestone | Deck Title & File | Format | Key Highlights |
| :--- | :--- | :---: | :--- |
| **Review 1**<br>*(Week 7 — 5 Marks)* | [Hospital_DBMS_Review1_Presentation.pptx](Hospital_DBMS_Review1_Presentation.pptx)<br>[presentation.html](presentation.html) | `.pptx`<br>`.html` | • System boundaries, scope & 6 user roles<br>• Classical Chen Notation ER Diagram (300 DPI)<br>• Initial Relational Schema across 3 domains<br>• 4 critical business rules & constraints |
| **Review 2**<br>*(Week 11 — 5 Marks)* | [Hospital_DBMS_Review2_Presentation.pptx](Hospital_DBMS_Review2_Presentation.pptx)<br>[presentation_review2.html](presentation_review2.html) | `.pptx`<br>`.html` | • 1NF ➔ 2NF ➔ 3NF Normalization pipeline<br>• Structured Data Dictionary & Functional Dependencies<br>• DDL triggers (Overlap, Bed Lock, Payments)<br>• 14 Demonstration queries (Joins, Subqueries, Aggregations, 5 Views) |
| **Review 3**<br>*(Week 16 — Final 5 Marks)* | [Hospital_DBMS_Review3_Presentation.pptx](Hospital_DBMS_Review3_Presentation.pptx)<br>[presentation_review3.html](presentation_review3.html) | `.pptx`<br>`.html` | • 3-Tier Application Architecture<br>• Full Clinical CRUD workflows (Intake ➔ Booking ➔ Diagnosis ➔ Beds ➔ Billing)<br>• Defensive Error Handling demonstration<br>• 10-Point Test Execution Matrix & Viva defense |

---

## 🏗️ System Architecture & 3NF Schema

The system uses a clean Three-Tier Architecture:
1. **Presentation Layer:** Responsive HTML5/CSS3 Single Page Dashboard with live patient search, interactive bed maps, modals, and an integrated SQL sandbox.
2. **Business Logic Layer:** Zero-dependency Python application controller (`app.py`) managing RESTful JSON API endpoints, transactional operations, and defensive error translation.
3. **Database Layer:** 3NF relational database (`hospital_review2.db`) enforcing foreign key cascades, triggers, check constraints, and 5 compiled views.

```
       [ Client Browser / CLI Terminal ]
                       │
                       ▼ HTTP Requests / JSON API
             [ app.py Controller ]
           (Zero External Dependencies)
                       │
                       ▼ SQLite3 / PostgreSQL Engine
      ┌──────────────────────────────────────────────┐
      │  3NF Relational Schema (16 Tables)           │
      │  ├── Outpatient: doctors, schedules, appts   │
      │  ├── Clinical: consultations, diagnoses, rx  │
      │  ├── Diagnostics: lab_tests, test_orders     │
      │  ├── Inpatient: wards, beds, admissions      │
      │  └── Financial: bills, payments              │
      │                                              │
      │  Active Triggers & Integrity Constraints     │
      │  ├── trg_prevent_appointment_overlap         │
      │  ├── trg_prevent_bed_double_booking          │
      │  └── trg_update_bill_on_payment              │
      │                                              │
      │  5 Production Views                          │
      └──────────────────────────────────────────────┘
```

---

## 💻 How to Use and Run `app.py`

`app.py` is self-contained and built entirely using standard Python libraries (`http.server`, `sqlite3`, `json`, `webbrowser`). **No `pip install` or external packages are required!**

### 1. Launching the Web Dashboard (Recommended)

Run the script from your terminal:
```bash
python3 app.py
```

The application will initialize the database (if not already created) and **automatically open your default web browser** to:
👉 **`http://localhost:8080`** *(or `http://127.0.0.1:8080`)*

*(Note: Custom ports can be specified with `python3 app.py --port 8000`)*

---

### 2. Navigating the Web Dashboard Modules

- **Overview Tab:** Real-time KPI statistics cards (Registered Patients, Ward Bed Occupancy %, Daily Encounters, Pending Lab Tests, Total Revenue Collected) and ward bed summaries.
- **Patients Tab (CRUD):** 
  - Real-time search by patient name, phone number, or ID.
  - Click **`+ New Patient Intake`** to add a new Master Patient Index record.
- **Appointments Tab:**
  - Schedule specialist doctor appointments.
  - Prevents doctor slot overlaps with live visual alerts.
  - Cancel / reschedule appointments in 1 click.
- **Clinical Tab:**
  - Record consultations linked 1:1 to appointments.
  - Assign ICD-10 diagnostic codes with clinical severity (Mild, Moderate, Severe, Critical).
  - Prescribe multi-item medication lines (decomposed to satisfy 3NF).
- **Wards & Beds Tab:**
  - **Interactive Visual Bed Map:** Live color-coded grid (**Green = Available**, **Red = Occupied**).
  - Admit inpatients with single-occupant bed locking.
  - Discharge inpatients with clinical summary notes, automatically freeing the bed.
- **Billing Tab:**
  - Consolidated invoice ledger for consultations and inpatient stays.
  - Record payments via UPI, Credit Card, Debit Card, Cash, or Insurance.
  - Enforces payment ceiling constraints (`paid_amount <= net_payable`).
- **5 Views Reports Tab:**
  - One-click inspection and data table rendering of all 5 production database views.
- **SQL Console Tab:**
  - Built-in SQL sandbox allowing you to run custom SQL queries directly against the database with instant table results.
  - Includes a dropdown preloaded with the Review 2 demonstration queries.

---

### 3. Launching the Terminal CLI Mode

If you prefer testing directly in your terminal, run:
```bash
python3 app.py --cli
```
This launches a menu-driven terminal interface:
```text
======================================================================
 HOSPITAL MANAGEMENT SYSTEM — REVIEW 3 TERMINAL PROTOTYPE
======================================================================
MAIN MENU:
1. Search & View Patients
2. Register New Patient
3. View Doctor Schedules & Free Slots
4. Book Appointment (With Overlap Collision Check)
5. Ward Bed Census & Inpatient Allocation
6. Admit Inpatient (With 1-Active-Patient-Per-Bed Check)
7. Billing & Payment Settlement
8. View 5 Production Analytical Views
9. Launch Web Dashboard (Browser GUI)
0. Exit
```

---

## ⚡ Interactive Demo Data & 1-Click Evaluation Features

To facilitate rapid, flawless demonstrations during evaluation, every modal form includes **1-Click Auto-Fill Demo Buttons**:

1. **Patient Registration Form:**
   - Click **`⚡ Auto-Fill Demo Patient`**: Populates valid, realistic demographic data.
2. **Appointment Scheduling Form:**
   - Click **`⚡ Fill Demo Slot (Valid)`**: Populates an available slot for tomorrow.
   - Click **`⚡ Fill Conflict Slot (Triggers Overlap)`**: Populates a slot colliding with Doctor 1's existing schedule, immediately triggering:
     ```
     INTEGRITY CONSTRAINT PREVENTED BOOKING: INTEGRITY ERROR: Doctor already has an overlapping appointment in this time window.
     ```
3. **Clinical Consultation Form:**
   - Click **`⚡ Auto-Fill Demo Clinical Data`**: Populates consultation notes, ICD-10 code (`I25.10`), and medication lines.
4. **Bed Admission Form:**
   - Click **`⚡ Fill Demo Admission (Vacant Bed #2)`**: Allocates a vacant ICU bed.
   - Click **`⚡ Fill Conflict Test (Occupied Bed #1)`**: Attempts to allocate an occupied bed, immediately triggering:
     ```
     BED ALLOCATION REJECTION: INTEGRITY ERROR: Selected bed currently has an active admitted patient.
     ```
5. **Billing Payment Form:**
   - Click **`⚡ Fill Demo Payment`**: Fills a valid installment against an active bill.
   - Click **`⚡ Fill Overrun Test (> Balance)`**: Attempts an excessive payment, demonstrating:
     ```
     PAYMENT CEILING REJECTION: CHECK constraint failed: paid_amount <= net_payable
     ```

---

## 📈 5 Production Database Views

The database includes 5 precompiled views providing abstracted, role-tailored access:
1. **`view_patient_history`:** Consolidated timeline of visits, doctors seen, primary diagnoses, and count of medications & ordered tests.
2. **`view_doctor_schedules`:** Doctor shift hours, slot durations, daily capacity, and currently booked vs free slots.
3. **`view_pending_tests`:** Diagnostic laboratory worklist tracking tests awaiting sample collection or processing with turnaround hour alerts.
4. **`view_bed_occupancy`:** Live ward bed census computing operational beds, active occupants, vacancy count, and occupancy percentage.
5. **`view_outstanding_bills_revenue`:** Inpatient vs outpatient financial ledger tracking gross billed charges, discounts, receipts, and outstanding debt.

---

## 📁 Repository File Structure

```
DBMS_PBL/
├── README.md                                # Comprehensive Project & Usage Guide
├── app.py                                   # Working Prototype Python Application (Web & CLI)
│
├── 📊 PowerPoint Presentations (.pptx)
│   ├── Hospital_DBMS_Review1_Presentation.pptx  # Review 1 Deck (9 slides, Chen ER & Schema)
│   ├── Hospital_DBMS_Review2_Presentation.pptx  # Review 2 Deck (8 slides, 3NF, Triggers, Views)
│   └── Hospital_DBMS_Review3_Presentation.pptx  # Review 3 Final Deck (8 slides, Architecture & Demo)
│
├── 🌐 Interactive Web Presentations (.html)
│   ├── presentation.html                    # Review 1 interactive slides (with 300 DPI Chen ER)
│   ├── presentation_review2.html            # Review 2 interactive slides
│   ├── presentation_review3.html            # Review 3 interactive slides
│   └── hospital_er_diagram.png              # High-resolution classical Chen ER diagram
│
├── 💾 Database Scripts & Live Engine
│   ├── hospital_review2.db                  # Pre-populated live SQLite relational database
│   ├── schema_review1.sql                   # Review 1 initial relational schema DDL
│   ├── schema_review2.sql                   # Review 2 production 3NF DDL with triggers & 5 views
│   ├── sample_data_review2.sql              # Realistic clinical sample dataset
│   └── queries_review2.sql                  # 14 demonstration queries suite
│
├── 📑 Reports & Viva Defense Dossiers
│   ├── Project_Report_Final.md              # Complete University PBL Final Project Report
│   ├── Data_Dictionary_and_Normalization.md # 3NF decomposition proofs & structured data dictionary
│   ├── Review1_Comprehensive_Guide.md       # Review 1 Presenter script & defense notes
│   ├── Review2_Comprehensive_Guide.md       # Review 2 Presenter script & query guide
│   └── Review3_Comprehensive_Guide.md       # Review 3 Presenter script & 25+ Viva Q&A
│
└── 📦 Hospital_DBMS_Package/                # Standalone packaged distribution folder
```

---

## 👥 Contributors & Academic Credits
- **Project Title:** Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System
- **Repository:** [Himanshu-Git-101/DBMS_PBL](https://github.com/Himanshu-Git-101/DBMS_PBL)
- **Course:** Database Management Systems (DBMS PBL)
