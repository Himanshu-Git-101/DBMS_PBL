# PROJECT REPORT
## DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR HOSPITAL APPOINTMENT AND PATIENT CARE MANAGEMENT SYSTEM

**Course:** Database Management Systems (DBMS PBL)  
**Project Code:** PROJECT 03  
**Review Milestones:** Review 1 (Week 7), Review 2 (Week 11), Review 3 (Week 16 — Final Evaluation)  
**Academic Year:** 2025–2026  

---

## 📋 Executive Summary / Abstract

Modern hospital operations encompass interconnected clinical and administrative workflows, including patient intake, outpatient scheduling, clinical consultations, diagnostic laboratory testing, inpatient admissions, bed allocation, and financial billing. In legacy or unintegrated hospital setups, disconnected departmental records produce severe operational bottlenecks: double-booked doctor appointments, physical bed allocation conflicts, fragmented patient medical histories, delayed diagnostic fulfillment, and revenue leakage.

This project delivers the end-to-end design, normalization, implementation, and evaluation of a robust Relational Database Management System (RDBMS) paired with an interactive Python application prototype. The conceptual model is structured using Classical Chen Notation across 13 core entities. The relational schema is rigorously decomposed into Third Normal Form (3NF), eliminating all partial and transitive functional dependencies. Schema-level integrity constraints and automated database triggers mathematically prevent doctor slot overlaps, enforce single active occupancy per bed, preserve chronological admission durations, and cap financial remittance limits. A zero-dependency Python application exposes a responsive web dashboard and a command-line interface demonstrating real-time CRUD operations, live patient searching, defensive error handling, five analytical database views, and an interactive SQL execution console.

---

## 1. Introduction & Problem Analysis

### 1.1 Problem Statement
Hospitals manage thousands of discrete transactions every day across distinct operational units:
- **Scheduling Conflicts:** Simultaneous appointment bookings for the same specialist doctor.
- **Inpatient Bed Disputes:** Admitting multiple active patients to the same physical hospital bed.
- **Fragmented Medical Histories:** Doctors unable to review a patient's historical consultations, prior diagnoses, and laboratory results in a single unified view.
- **Billing Inconsistencies:** Overbilling, negative account balances, or unaccounted diagnostic investigations.

### 1.2 Project Objectives
1. **Centralize Clinical & Administrative Data:** Unify Outpatient, Inpatient, Laboratory, and Billing domains into a single relational database.
2. **Eliminate Redundancy via 3NF Normalization:** Decompose unnormalized clinical ledgers up to Third Normal Form (3NF).
3. **Enforce Business Rules at the Database Level:** Implement automated triggers and check constraints to guarantee operational validity regardless of the client application.
4. **Develop a Functional Prototype Application:** Construct a Python-based software application demonstrating real-time CRUD operations, validations, reporting views, and error handling.

---

## 2. System Scope & Role-Based Access Control (RBAC)

The system manages six key user roles with segregated duties:
1. **Hospital Administrator:** System configuration, department creation, doctor onboarding, and hospital-wide analytics.
2. **Attending Doctor / Specialist:** Duty roster viewing, appointment confirmation, consultation recording, ICD-10 diagnosis entry, prescription writing, and inpatient rounds.
3. **Patient:** Demographic registration, appointment scheduling, prescription access, and bill review.
4. **Staff Nurse / Ward In-Charge:** Real-time bed occupancy monitoring, inpatient intake assistance, and discharge care summaries.
5. **Laboratory Technician:** Diagnostic test queue inspection, sample collection acknowledgement, and result value entry.
6. **Billing Cashier:** Itemized invoice generation, payment transaction recording, receipt printing, and outstanding debt monitoring.

---

## 3. Conceptual Design: Classical Chen ER Modeling

The conceptual architecture models 13 core entities and their relationships:
- **Entities:** `Department`, `Doctor`, `DoctorSchedule`, `Patient`, `Appointment`, `Consultation`, `Diagnosis`, `Prescription`, `LabTest`, `Ward`, `Bed`, `Admission`, `Bill`, and `Payment`.
- **Key Relationships & Cardinalities:**
  - `Department` (1) — Manages — (M) `Doctor`
  - `Doctor` (1) — Configures — (M) `DoctorSchedule`
  - `Patient` (1) — Books — (M) `Appointment`
  - `Doctor` (1) — Conducts — (M) `Appointment`
  - `Appointment` (1) — Yields — (1) `Consultation` *(Strict 1:1)*
  - `Consultation` (1) — Concludes — (M) `Diagnosis`
  - `Consultation` (1) — Generates — (1) `Prescription`
  - `Prescription` (1) — Contains — (M) `PrescriptionItem` *(Decomposed for 1NF/3NF)*
  - `Consultation` (1) — Dispatches — (M) `TestOrder` (M) — Refers — (1) `LabTest`
  - `Ward` (1) — Contains — (M) `Bed`
  - `Patient` (1) — Admitted Under — (M) `Admission`
  - `Bed` (1) — Accommodates — (M) `Admission` *(Constrained to 1 active at any time)*
  - `Consultation` / `Admission` — Billed Via — (1) `Bill`
  - `Bill` (1) — Settled By — (M) `Payment`

---

## 4. Relational Schema & 3NF Normalization Proofs

### 4.1 First Normal Form (1NF)
- **Elimination of Repeating Groups:** Multi-valued medications within prescriptions are extracted into `prescription_items(item_id, prescription_id, medicine_name, dosage, frequency, duration, quantity)`.
- **Atomicity:** All attributes contain scalar, indivisible values. Composite attributes such as patient names are split into `first_name` and `last_name`.

### 4.2 Second Normal Form (2NF)
- **Elimination of Partial Dependencies:** In intermediate diagnostic orders, test definitions (`test_name`, `standard_cost`) are separated into `lab_tests`, while individual test requests are maintained in `test_orders`. Every non-prime attribute is fully functionally dependent on the entire candidate key.

### 4.3 Third Normal Form (3NF)
- **Elimination of Transitive Dependencies ($X \to Y \to Z$):**
  - Doctors reference `dept_id`; departmental metadata (`dept_name`, `building_block`, `floor_number`) resides solely in `departments`.
  - Beds reference `ward_id`; ward attributes (`ward_type`, `capacity`) reside solely in `wards`.
  - Every non-trivial functional dependency $X \to Y$ has a Superkey determinant $X$.

---

## 5. Critical Database Integrity Constraints & Triggers

### 5.1 No Overlapping Doctor Appointments
- **Unique Constraint:** `UNIQUE (doctor_id, appointment_date, start_time)` prevents identical starting times.
- **Overlap Trigger:**
```sql
CREATE TRIGGER trg_prevent_appointment_overlap
BEFORE INSERT ON appointments
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM appointments
    WHERE doctor_id = NEW.doctor_id
      AND appointment_date = NEW.appointment_date
      AND status NOT IN ('CANCELLED', 'NO_SHOW')
      AND (NEW.start_time < end_time AND NEW.end_time > start_time)
)
BEGIN
    SELECT RAISE(ABORT, 'INTEGRITY ERROR: Doctor already has an overlapping appointment in this time window.');
END;
```

### 5.2 One Active Patient Per Bed
- **Single Active Occupant Trigger:**
```sql
CREATE TRIGGER trg_prevent_bed_double_booking
BEFORE INSERT ON admissions
FOR EACH ROW
WHEN NEW.status = 'ACTIVE' AND EXISTS (
    SELECT 1 FROM admissions
    WHERE bed_id = NEW.bed_id AND status = 'ACTIVE'
)
BEGIN
    SELECT RAISE(ABORT, 'INTEGRITY ERROR: Selected bed currently has an active admitted patient.');
END;
```

### 5.3 Valid Chronological Dates
- `CHECK (discharge_date IS NULL OR discharge_date >= admission_date)` guarantees patients cannot be discharged prior to intake.

### 5.4 Positive Charges & Payment Limits
- `CHECK (total_amount >= 0 AND amount_paid > 0)`
- `CHECK (paid_amount <= net_payable)`
- `CHECK (net_payable = total_amount - discount_amount + tax_amount)`
- **Auto-Update Payment Trigger:** Automatically increments `paid_amount` on `payments` insert and transitions invoice status to `'PAID'` or `'PARTIALLY_PAID'`.

---

## 6. Analytical Production Views

1. **`view_patient_history`:** Consolidated timeline of visits, attending doctors, departments, clinical symptoms, ICD-10 diagnoses, and counts of prescribed medicines and ordered tests.
2. **`view_doctor_schedules`:** Doctor shift hours, slot durations, daily capacities, and currently booked vs free slots.
3. **`view_pending_tests`:** Diagnostic worklist filtering tests awaiting collection or processing with turnaround hour benchmarks.
4. **`view_bed_occupancy`:** Ward operational capacity, active occupants, vacancy count, and occupancy percentage.
5. **`view_outstanding_bills_revenue`:** Inpatient vs outpatient invoice ledger tracking gross billed charges, discounts, taxes, payments, and outstanding balances.

---

## 7. System Architecture & Prototype Implementation

### 7.1 Architecture Design
The software implements a clean Three-Tier Architecture:
- **Presentation Layer:** Responsive HTML5/CSS3 Single Page Dashboard with live search, visual bed occupancy grids, appointment forms, and an integrated SQL console.
- **Business Logic Layer:** Python standard library `http.server` providing RESTful JSON API endpoints, transactional write orchestration, and graceful error interception.
- **Database Engine Layer:** SQLite / PostgreSQL engine with 16 3NF tables, active foreign key enforcement (`PRAGMA foreign_keys = ON;`), and triggers.

### 7.2 Prototype Execution Modes
- **Web Dashboard Mode:** Run `python3 app.py` and access `http://127.0.0.1:5000`.
- **Command-Line Interface (CLI) Mode:** Run `python3 app.py --cli` for an interactive menu-driven terminal experience.

---

## 8. Verification & Test Execution Results

| Test ID | Module | Scenario / Test Input | Expected Behavior | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Patients | Valid patient demographic input | New patient record committed with auto-increment ID | Patient #11 created | **PASS** |
| **TC-02** | Patients | Search patient by phone number | Instant match returned in table | Match displayed | **PASS** |
| **TC-03** | Appointments | Book appointment in available slot | Slot confirmed with status `SCHEDULED` | Appointment booked | **PASS** |
| **TC-04** | Appointments | Book overlapping slot for same doctor | Trigger raises `INTEGRITY ERROR` and aborts | Insert aborted, error displayed | **PASS** |
| **TC-05** | Clinical | Record consultation, diagnosis, and Rx | 1:1 encounter recorded and bill generated | Encounter committed | **PASS** |
| **TC-06** | Inpatient | Admit patient to vacant bed | Bed marked occupied, admission logged | Inpatient admitted | **PASS** |
| **TC-07** | Inpatient | Admit patient to already occupied bed | Trigger raises `BED ALLOCATION REJECTION` | Insert aborted, alert displayed | **PASS** |
| **TC-08** | Inpatient | Discharge date earlier than admission | `CHECK` constraint fails and aborts | Aborted | **PASS** |
| **TC-09** | Billing | Payment amount exceeding net payable | `CHECK` constraint fails and aborts | Aborted | **PASS** |
| **TC-10** | Reporting | Query all 5 database views | Instant compilation and table rendering | Views loaded with 100% data | **PASS** |

---

## 9. Conclusion

The Hospital Appointment and Patient Care Management System successfully fulfills all objectives set forth in the DBMS Problem Based Learning curriculum:
1. **Relational Rigor:** Conceptual design mapped through classical Chen ER notation and decomposed to 3NF.
2. **Schema Defense:** All critical real-world healthcare constraints are protected by triggers and check predicates at the database layer.
3. **Application Completeness:** A working, responsive Python application provides clinical staff and administrators with live tools to manage patients, appointments, beds, and billing without third-party dependencies.
4. **Academic Compliance:** All review milestones (Review 1: Conceptual ER & Boundaries; Review 2: 3NF Schema, Triggers, Views & Queries; Review 3: Working Application, CRUD, Test Logs & Report) are 100% complete and verified.
