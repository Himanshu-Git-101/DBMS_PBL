# DBMS PBL — Review 1 Presentation Dossier & Defense Guide
**Project 03:** Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System  
**Review Milestone:** Review 1 (Week 7 — 5 Marks)  
**Format:** 9-Slide Expanded Presentation (Maximum Legibility, Zero Text Cramming)

---

## 📂 Quick Access to Generated Artifacts

| Artifact | Location | Format & Key Highlights |
| :--- | :--- | :--- |
| **PowerPoint Slide Deck** | [Hospital_DBMS_Review1_Presentation.pptx](file:///Users/himanshu/Documents/DBMS%20PBL/Hospital_DBMS_Review1_Presentation.pptx) | **9-Slide Presentation Deck** (widescreen 16:9, expanded relational schema over 3 dedicated slides with individual table cards, embedded Chen ER diagram on Slide 4, and speaker notes on every slide). Open in PowerPoint, Google Slides, or Keynote. |
| **Classical Chen ER Diagram** | [hospital_er_diagram.png](file:///Users/himanshu/Documents/DBMS%20PBL/hospital_er_diagram.png) | **Ultra-HD 300 DPI** classical Chen notation diagram: soft green entity boxes, soft pink relationship diamonds, soft blue attribute ovals, underlined PKs, `(FK)` tags, and dashed legend box. |
| **Interactive HTML Slides** | [presentation.html](file:///Users/himanshu/Documents/DBMS%20PBL/presentation.html) | Open in any browser. Keyboard controls (`→`/`Space` next, `←` prev, `N` notes, `F` fullscreen), click-to-zoom ER diagram, and **Print to PDF** button. |
| **Production SQL DDL** | [schema_review1.sql](file:///Users/himanshu/Documents/DBMS%20PBL/schema_review1.sql) | 16 normalized tables (3NF), CHECK, UNIQUE, PK/FK, partial indexes, and business rules ready for PostgreSQL / MySQL. |
| **Slide Deck Script** | [generate_deck.py](file:///Users/himanshu/Documents/DBMS%20PBL/generate_deck.py) | Python script using `python-pptx` to generate the 9-slide presentation. |
| **Chen ER Diagram Script** | [generate_chen_er_diagram.py](file:///Users/himanshu/Documents/DBMS%20PBL/generate_chen_er_diagram.py) | Python script generating the Chen notation diagram. |

---

## 📑 The 9-Slide Deck Structure

| Slide | Title | Visual Highlights | Key Content |
| :---: | :--- | :--- | :--- |
| **1** | **Title Slide** | Sleek dark theme (`#0B1329`) with 3 highlight badges | Project 03 Title, Review 1 Badge (Week 7 — 5 Marks), 13 Entities, 3NF Normalization, Strict Integrity. |
| **2** | **Problem Statement & Objectives** | 2 high-contrast cards: *Rose* (Problem) vs. *Teal* (Objectives) | 4 clear failure modes (Collisions, Fragmented Records, Bed Disputes, Billing Leakage) and 4 core database objectives. |
| **3** | **System Scope & Target Users** | 2 balanced cards: *Blue* (Scope) vs. *Purple* (RBAC) | In-scope functional modules (OPD, Encounters, Labs, Inpatient, Billing) & 6 user roles (Admin, Doctor, Patient, Nurse, Cashier, Receptionist). |
| **4** | 🌟 **Full ER Diagram Slide** | **Full-slide Classical Chen ER Diagram image** | High-resolution Chen model: soft green entity boxes, soft pink relationship diamonds, soft blue attribute ovals, underlined PKs, `(FK)` tags, and dashed legend box. |
| **5** | **Schema Part 1: Outpatient & Scheduling** | 5 dedicated table cards (3 top, 2 bottom) | `departments`, `doctors`, `doctor_schedules`, `patients`, `appointments`. Clear PKs, FKs, and the critical slot constraint. |
| **6** | **Schema Part 2: Clinical & Diagnostics** | 6 dedicated table cards (3x2 grid) | `consultations`, `diagnoses`, `prescriptions`, `prescription_items` (3NF), `lab_tests`, `test_orders` (Bridge). |
| **7** | **Schema Part 3: Inpatient & Billing** | 5 dedicated table cards (3 inpatient, 2 billing) | `wards`, `beds`, `admissions` (1 active patient lock), `bills` (consolidated invoices), `payments` (remittance ledger). |
| **8** | **Critical Business Rules** | 4 clean cards with exact SQL DDL constraints | 1. No Overlapping Slots (`UNIQUE`), 2. One Active Patient/Bed (Partial Unique Index), 3. Valid Admission Dates (`CHECK`), 4. Positive Bills (`CHECK`). |
| **9** | **Conclusion & Roadmap** | 3 roadmap cards (Review 1 → Review 2 → Final Demo) + Q&A | Summary of completed Review 1 deliverables, roadmap towards Week 11 and Week 14, and open Q&A. |

---

## 🎙️ Slide-by-Slide Presenter Script

### Slide 1: Title Slide — *30 Seconds*
> *"Good morning, respected evaluators. Today we present Review 1 for Project 03: Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System. We cover problem analysis, boundaries, classical Chen ER modeling across all 13 core entities, our 3NF relational schema across three clear domains, and database integrity rules."*

---

### Slide 2: Problem Statement & Objectives — *40 Seconds*
> *"Hospitals manage appointments, consultations, prescriptions, lab tests, admissions, beds, and billing. Disconnected records create schedule conflicts and incomplete patient histories. Our objectives are to centralize records into a single relational DBMS, enforce business rules directly at the schema level, and achieve 3NF normalization."*

---

### Slide 3: System Scope & Target Users — *40 Seconds*
> *"We demarcated clear functional boundaries: in-scope modules cover outpatient care, clinical encounters, diagnostics, bed admissions, and billing. Duties are separated across 6 distinct user roles to maintain HIPAA-inspired patient privacy and data integrity."*

---

### Slide 4: Conceptual ER Diagram (FULL VISUAL SLIDE) — *60 Seconds*
> *"Here is Deliverable 2: our Conceptual ER Diagram structured in Classical Chen Notation.
> - **Soft green rectangles** represent Entities: Patient, Doctor, Department, Schedule, Appointment, Consultation, Diagnosis, Prescription, LabTest, Admission, Bed, Ward, Bill, and Payment.
> - **Soft pink diamonds** represent Relationships with clean 1 and M cardinalities.
> - **Soft blue ovals** represent Attributes, with Primary Keys Underlined and Foreign Keys marked (FK).
> All 13 core entities plus child tables are fully mapped with zero line interference."*

---

### Slide 5: Schema Part 1: Outpatient & Scheduling — *45 Seconds*
> *"Deliverable 3: Initial Relational Schema begins with Domain 1: Outpatient & Scheduling.
> - `departments` and `doctors` link via `dept_id`.
> - `doctor_schedules` records weekly shift availability with start/end time validation.
> - `patients` stores demographics with unique phone and email indexes.
> - Most importantly, `appointments` enforces a composite unique constraint: `UNIQUE (doctor_id, appointment_date, start_time)` to mathematically eliminate double-booking."*

---

### Slide 6: Schema Part 2: Clinical & Diagnostics — *45 Seconds*
> *"Domain 2 covers Clinical Encounters and Diagnostics.
> - Every `consultation` links back to an appointment via a unique foreign key.
> - `diagnoses` captures ICD-10 condition codes and clinical severity.
> - To strictly adhere to 3NF, multi-valued medication lines are decomposed into `prescription_items`.
> - Similarly, laboratory tests are resolved through the `test_orders` associative table, tracking sample collection, results, and doctor comments."*

---

### Slide 7: Schema Part 3: Inpatient Wards, Beds & Billing — *45 Seconds*
> *"Domain 3 covers Inpatient Care and Financial Billing.
> - `wards` houses `beds` with operational status and daily room rates.
> - `admissions` enforces `discharge_date >= admission_date`, along with a PostgreSQL Partial Unique Index guaranteeing that each bed accommodates at most ONE active patient at any time.
> - `bills` consolidates doctor fees, room charges, and lab investigations into a single invoice, capped by check constraints so `paid_amount` can never exceed `net_payable`."*

---

### Slide 8: Critical Business Rules Enforcement — *45 Seconds*
> *"The problem statement emphasizes four critical business rules, which we enforce directly in SQL DDL:
> 1. **No Overlapping Appointments:** `UNIQUE (doctor_id, appointment_date, start_time)` and `CHECK (end_time > start_time)`.
> 2. **One Active Patient Per Bed:** PostgreSQL Partial Unique Index: `CREATE UNIQUE INDEX ON admissions(bed_id) WHERE status = 'ACTIVE'`.
> 3. **Valid Admission & Discharge Dates:** `CHECK (discharge_date IS NULL OR discharge_date >= admission_date)`.
> 4. **Positive Charges & Payment Limits:** `CHECK (total_amount >= 0 AND paid_amount <= net_payable AND amount_paid > 0)`."*

---

### Slide 9: Conclusion & Roadmap — *30 Seconds*
> *"All Review 1 deliverables are fulfilled: problem analysis, 13-entity Chen ER diagram, and 3NF schema with integrity rules are complete. Our roadmap progresses to Review 2 in Week 11 for database implementation, views, and triggers, culminating in the final application demo in Week 14. Thank you, and we welcome your questions."*

---

## 🎯 Top Evaluator Viva Questions & Ready Answers

1. **How do you prevent doctor double-booking?**  
   *Answer:* `UNIQUE (doctor_id, appointment_date, start_time)` in the `appointments` table plus `CHECK (end_time > start_time)`.
2. **How do you enforce one active patient per bed?**  
   *Answer:* A PostgreSQL Partial Unique Index on `admissions`: `CREATE UNIQUE INDEX ON admissions(bed_id) WHERE status = 'ACTIVE';`.
3. **Why did you separate `prescriptions` and `prescription_items`?**  
   *Answer:* Prescriptions contain multiple medicines with distinct dosages and durations. Storing them together violates 1NF; decomposing them ensures atomic attributes and 3NF compliance.
4. **How do you prevent negative bills or overpayments?**  
   *Answer:* Check constraints: `CHECK (total_amount >= 0)`, `CHECK (paid_amount <= net_payable)`, and `CHECK (amount_paid > 0)`.
