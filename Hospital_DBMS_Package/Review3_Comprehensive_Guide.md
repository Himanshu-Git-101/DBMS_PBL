# DBMS PBL — Review 3 Presentation Dossier & Comprehensive Viva Guide
**Project 03:** Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System  
**Review Milestone:** Review 3 (Week 16 — Final 5 Marks)  
**Deliverables Covered:** Working Python Application Prototype (Web & CLI), End-to-End Clinical Workflows (CRUD), Integrity Verification, 5 Production Database Views, Full University PBL Project Report, and Comprehensive Viva-Voce Preparation.

---

## 📂 Quick Access to Generated Artifacts

| Artifact | File Link | Description & Key Highlights |
| :--- | :--- | :--- |
| **PowerPoint Slide Deck** | [Hospital_DBMS_Review3_Presentation.pptx](file:///Users/himanshu/Documents/DBMS%20PBL/Hospital_DBMS_Review3_Presentation.pptx) | **8-Slide Widescreen Presentation** covering 3-Tier Architecture, Clinical CRUD, Validations, Test Matrix, and Final Evaluation. |
| **Interactive HTML Slides** | [presentation_review3.html](file:///Users/himanshu/Documents/DBMS%20PBL/presentation_review3.html) | Open in any browser. Keyboard controls (`→`/`Space` next, `←` prev, `N` speaker notes, `F` fullscreen), and **Print to PDF** button. |
| **Working Python Application** | [app.py](file:///Users/himanshu/Documents/DBMS%20PBL/app.py) | **Zero-Dependency Python Application** supporting both Interactive Web Dashboard (`python3 app.py`) and Terminal CLI (`python3 app.py --cli`). |
| **Complete 3NF DDL Script** | [schema_review2.sql](file:///Users/himanshu/Documents/DBMS%20PBL/schema_review2.sql) | 16 normalized tables, CHECK constraints, slot overlap trigger, single active bed trigger, payment ceiling trigger, and 5 production views. |
| **Relational Sample Dataset** | [sample_data_review2.sql](file:///Users/himanshu/Documents/DBMS%20PBL/sample_data_review2.sql) | Comprehensive dataset with departments, doctors, patients, appointments, consultations, diagnoses, beds, and billing records. |
| **Final Project Submission Report**| [Project_Report_Final.md](file:///Users/himanshu/Documents/DBMS%20PBL/Project_Report_Final.md) | **Complete Academic PBL Report** covering abstract, system architecture, ER diagrams, 3NF mathematical proofs, DDL/DML, test cases, and conclusions. |
| **Normalization & Data Dictionary**| [Data_Dictionary_and_Normalization.md](file:///Users/himanshu/Documents/DBMS%20PBL/Data_Dictionary_and_Normalization.md) | Mathematical 1NF/2NF/3NF decomposition proofs, full functional dependencies list, and complete structured data dictionary. |

---

## 📑 Slide-by-Slide Presenter Script & Defense Notes

### Slide 1: Title Slide — *30 Seconds*
> *"Respected evaluators, welcome to Review 3: the final evaluation and working prototype demonstration of our Hospital Appointment and Patient Care Management System.  
> Over the course of the semester, we advanced from conceptual ER modeling in Review 1 to 3NF relational normalization and DDL triggers in Review 2. Today, in Review 3, we present our completed, working Python application connected directly to our relational database engine, showcasing full CRUD operations, live collision prevention, role-tailored reporting, and comprehensive test verification."*

---

### Slide 2: Three-Tier System Architecture — *45 Seconds*
> *"Our application is structured following a standard three-tier architecture:  
> - **Presentation Tier:** A responsive web dashboard with live search, an interactive ward bed map, and a built-in SQL sandbox, along with a terminal CLI mode.  
> - **Business Logic Controller:** A zero-dependency Python controller that handles REST API endpoints, coordinates transactional writes, and intercepts database errors to provide actionable user alerts.  
> - **Database Tier:** A normalized 3NF relational database with active foreign keys, integrity triggers for slot and bed collision prevention, and 5 production views."*

---

### Slide 3: Outpatient Registration & Clinical Workflows — *60 Seconds*
> *"We have implemented the complete clinical continuum:  
> 1. **Patient Registration:** Establishes a unique Master Patient Index with real-time search across names, phone numbers, and IDs.  
> 2. **Appointment Scheduling:** Front-desk staff select doctors and timeslots; our trigger `trg_prevent_appointment_overlap` actively prevents scheduling conflicts.  
> 3. **Clinical Consultations:** Attending clinicians record symptoms, assign ICD-10 diagnoses with severity ratings, formulate multi-item 3NF prescriptions, and dispatch diagnostic lab test orders."*

---

### Slide 4: Inpatient Bed Allocation & Billing Ledger — *60 Seconds*
> *"Our inpatient module manages ward infrastructure and financial accounting:  
> - **Inpatient Admissions:** Clinicians view a color-coded visual bed map (Green for Available, Red for Occupied). Our trigger `trg_prevent_bed_double_booking` strictly enforces one active patient per bed. Discharging an inpatient validates chronological dates and records discharge summaries.  
> - **Consolidated Billing:** Invoices aggregate doctor consultation fees, bed charges, and lab tests. Our check constraints enforce that `paid_amount <= net_payable` and all charges remain non-negative, while automated triggers update invoice settlement statuses."*

---

### Slide 5: Robust Validations & Defensive Error Handling — *45 Seconds*
> *"To ensure hospital data integrity, we implemented a dual-layer defense:  
> - Frontend validations capture missing fields and format discrepancies immediately.  
> - Database triggers and CHECK constraints provide an unbreachable barrier: attempting to double-book a doctor raises an explicit `INTEGRITY ERROR`, attempting to admit two patients to the same bed is rejected, backwards discharge dates fail check constraints, and payments exceeding invoice balances are blocked."*

---

### Slide 6: Analytical Reporting via 5 Production Views — *45 Seconds*
> *"Our system provides one-click reporting powered by 5 production database views:  
> - `view_patient_history`: Complete longitudinal timeline for attending doctors.  
> - `view_doctor_schedules`: Duty roster and available slot counts for receptionists.  
> - `view_pending_tests`: Laboratory worklist with turnaround time alerts.  
> - `view_bed_occupancy`: Live ward bed census computing occupancy rates.  
> - `view_outstanding_bills_revenue`: Financial accounts ledger tracking paid and pending receivables."*

---

### Slide 7: CRUD & Integrity Test Execution Matrix — *45 Seconds*
> *"We validated our system through a rigorous 10-point test matrix:  
> - All 5 positive functional tests (patient registration, search, slot booking, consultation entry, bed admission) succeeded with 100% data fidelity.  
> - All 5 negative test cases (slot overlap, bed double-booking, date reversal, payment ceiling breach, negative fee) were successfully intercepted and blocked by our database constraints."*

---

### Slide 8: Project Summary & Evaluation Readiness — *30 Seconds*
> *"In summary, our Hospital DBMS fulfills all Review 3 University PBL requirements with 5/5 marks readiness. Our source code is clean, robust, and zero-dependency; our database enforces full relational integrity; and our documentation is comprehensive. We thank you for your guidance throughout this semester and invite you to our live application demonstration."*

---

## 🖥️ Live Demonstration Script for Evaluators

When presenting the live prototype to the evaluators, run:
```bash
python3 app.py
```
Then your browser will automatically launch, or open **`http://localhost:8080`** (or `http://127.0.0.1:8080`) in Google Chrome or any browser. Follow these 5 steps:

1. **Step 1: Dashboard Overview:** Show the live statistics cards (Patients, Bed Occupancy %, Appointments, Pending Tests, Revenue Collected).
2. **Step 2: Patient Registration & Live Search:**
   - Go to **Patients** tab. Type a phone number or name in the search bar to demonstrate real-time filtering.
   - Click **+ New Patient Intake** to show the form validation.
3. **Step 3: Appointment Booking with Overlap Prevention:**
   - Go to **Appointments** tab.
   - First, show a successful booking in a free slot.
   - Next, deliberately attempt to book an overlapping slot for Doctor 1 on an existing slot: demonstrate the red alert banner: `INTEGRITY CONSTRAINT PREVENTED BOOKING: INTEGRITY ERROR: Doctor already has an overlapping appointment in this time window.`
4. **Step 4: Inpatient Bed Allocation & Single Patient Lock:**
   - Go to **Wards & Beds** tab. Point out the interactive green/red bed grid.
   - Deliberately attempt to admit a patient into Bed #1 (which is already occupied): show the immediate rejection: `BED ALLOCATION REJECTION: INTEGRITY ERROR: Selected bed currently has an active admitted patient.`
5. **Step 5: Reports & SQL Console:**
   - Go to **5 Views Reports** tab. Click through the buttons to inspect `view_patient_history`, `view_bed_occupancy`, etc.
   - Go to **SQL Console** tab. Select a preset query and click **Execute SQL** to demonstrate live relational query execution.

*(Note: If the evaluator requests a terminal demonstration, run `python3 app.py --cli` to demonstrate the exact same workflows in bash!)*

---

## 🎓 25+ Comprehensive Viva-Voce Questions & Answers

### Normalization & Relational Design

#### Q1: What is the primary motivation for normalizing a database up to 3NF?
**Answer:** The primary motivation is the elimination of data redundancy and update anomalies (insertion, modification, and deletion anomalies) while preserving all data dependencies and ensuring lossless-join decomposition. In 3NF, every non-trivial functional dependency $X \to Y$ requires that $X$ is a superkey, ensuring non-key attributes depend solely on candidate keys.

#### Q2: What is the difference between 2NF and 3NF?
**Answer:** 
- **2NF** eliminates **partial functional dependencies** on composite primary keys: every non-prime attribute must depend on the whole candidate key, not a subset.
- **3NF** goes further by eliminating **transitive dependencies**: a non-prime attribute cannot depend on another non-prime attribute ($X \to Y \to Z$ where $Z$ is non-prime).

#### Q3: When would a database designer choose Boyce-Codd Normal Form (BCNF) over 3NF?
**Answer:** BCNF is a stricter version of 3NF where for *every* functional dependency $X \to Y$, $X$ must be a superkey (3NF allows $Y$ to be a prime attribute even if $X$ is not a superkey). BCNF is preferred when a table has multiple overlapping composite candidate keys. In our hospital system, all tables have single-attribute surrogate primary keys, making 3NF and BCNF equivalent.

#### Q4: Why did you decompose prescriptions into `prescriptions` and `prescription_items`?
**Answer:** In 1NF, repeating groups or multi-valued attributes are prohibited. A single doctor prescription typically contains multiple medication lines (e.g. antibiotic + analgesic). Storing multiple medicines in a single column violates atomicity, while storing fixed columns (`med1`, `med2`, `med3`) creates null values and rigid limits. Decomposing into `prescription_items` satisfies 1NF and 3NF.

---

### Integrity Constraints & Triggers

#### Q5: What is the difference between a `CHECK` constraint and a `TRIGGER`?
**Answer:**
- A **`CHECK` constraint** evaluates an expression that depends *only* on the values of the current row being inserted or modified (e.g., `discharge_date >= admission_date`, `consultation_fee >= 0`). It cannot query other rows or tables.
- A **`TRIGGER`** executes arbitrary procedural SQL when an event occurs (`BEFORE` or `AFTER` `INSERT`, `UPDATE`, `DELETE`). Triggers can query across multiple rows and tables, allowing us to enforce cross-row constraints like overlapping appointment detection and bed occupancy conflicts.

#### Q6: How does your trigger prevent appointment overlaps?
**Answer:** The `trg_prevent_appointment_overlap` trigger runs `BEFORE INSERT ON appointments`. It checks:
```sql
WHERE doctor_id = NEW.doctor_id
  AND appointment_date = NEW.appointment_date
  AND status NOT IN ('CANCELLED', 'NO_SHOW')
  AND (NEW.start_time < end_time AND NEW.end_time > start_time)
```
If any matching row exists, the time intervals overlap, and the trigger executes `RAISE(ABORT, '...')`, rolling back the transaction.

#### Q7: How does your database enforce "one active patient per bed"?
**Answer:**
1. In PostgreSQL: A partial unique index: `CREATE UNIQUE INDEX idx_bed ON admissions(bed_id) WHERE status = 'ACTIVE'`.
2. In SQLite/MySQL: A `BEFORE INSERT` trigger `trg_prevent_bed_double_booking` that verifies no existing record in `admissions` has the same `bed_id` with `status = 'ACTIVE'`, raising an abort if true.

#### Q8: What are foreign key cascading actions and which did you apply?
**Answer:**
- `ON UPDATE CASCADE`: If a primary key changes, the foreign keys in referencing child tables update automatically.
- `ON DELETE RESTRICT`: Prevents deletion of a parent record if children exist (e.g. preventing doctor deletion if appointments exist).
- `ON DELETE CASCADE`: Automatically deletes child rows when parent is deleted (e.g. deleting `prescription_items` when a `prescription` is removed).
- `ON DELETE SET NULL`: Sets the foreign key to NULL (e.g. if a department head doctor leaves, `head_doctor_id` is set to NULL).

---

### Database Transactions & ACID Properties

#### Q9: What are ACID properties and how are they maintained in this project?
**Answer:**
- **Atomicity:** All-or-nothing execution. For example, creating a consultation, adding diagnoses, and generating a bill execute in a single transaction; if any insert fails, all changes roll back.
- **Consistency:** The database transitions only between valid states conforming to all schema constraints and triggers.
- **Isolation:** Concurrent transactions execute without dirty reads or unrepeatable reads, managed via database locking and WAL (Write-Ahead Logging).
- **Durability:** Once committed, transaction results survive system crashes or power failures.

#### Q10: What is Write-Ahead Logging (WAL)?
**Answer:** WAL is a logging protocol where changes are first recorded in an append-only log on disk before the corresponding database pages are updated. In SQLite and PostgreSQL, WAL enables concurrent readers without blocking writers and ensures recovery after unexpected termination.

---

### Indexing & Query Optimization

#### Q11: What type of index does the database create for primary keys and unique constraints?
**Answer:** Relational database systems automatically create a **B-Tree (Balanced Tree)** index for primary keys and `UNIQUE` constraints. B-Trees provide $O(\log N)$ search, insertion, and deletion complexity and support range scans.

#### Q12: Why did you create composite indexes on `appointments(doctor_id, appointment_date)`?
**Answer:** Front-desk booking and collision checks filter simultaneously by doctor and date. A composite index on `(doctor_id, appointment_date)` allows the query planner to jump directly to that doctor's day schedule using a single index seek, eliminating expensive full-table scans.

#### Q13: What is the difference between a clustered and non-clustered index?
**Answer:**
- A **clustered index** dictates the physical order of rows on disk (e.g. SQLite's integer primary key rowid). There can be only one clustered index per table.
- A **non-clustered index** is a separate data structure containing sorted index keys and pointers (rowids) back to the actual table rows.

---

### Views & Application Design

#### Q14: What is the difference between a standard view and a materialized view?
**Answer:**
- A **standard view** is a stored virtual query; it contains no physical data. Each time it is queried, the DBMS expands and executes the underlying `SELECT` statement.
- A **materialized view** physically persists the query result on disk, periodically refreshed. It is used in data warehouses for expensive analytical queries. Our 5 views are standard views to ensure real-time clinical freshness.

#### Q15: How does your Python application prevent SQL Injection?
**Answer:** We strictly use **parameterized queries** with placeholders (`?` in SQLite, `%s` in PostgreSQL). Parameterization ensures that user input is treated strictly as data literals and never parsed as executable SQL tokens, completely preventing SQL injection attacks.
