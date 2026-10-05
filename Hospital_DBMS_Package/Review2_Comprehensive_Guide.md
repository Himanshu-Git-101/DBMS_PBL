# DBMS PBL — Review 2 Presentation Dossier & Defense Guide
**Project 03:** Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System  
**Review Milestone:** Review 2 (Week 11 — 5 Marks)  
**Deliverables Covered:** 3NF Normalization & Functional Dependencies, Concise Data Dictionary, DDL with Constraints & Triggers, Sample Data & SQL Queries (Joins, Subqueries, Aggregations, 5 Views), and Working Database Prototype.

---

## 📂 Quick Access to Generated Artifacts

| Artifact | File Link | Description & Key Highlights |
| :--- | :--- | :--- |
| **PowerPoint Slide Deck** | [Hospital_DBMS_Review2_Presentation.pptx](file:///Users/himanshu/Documents/DBMS%20PBL/Hospital_DBMS_Review2_Presentation.pptx) | **8-Slide Widescreen Presentation** with sleek modern cards, zero cramming, high contrast color coding, and speaker notes on every slide. |
| **Interactive HTML Slides** | [presentation_review2.html](file:///Users/himanshu/Documents/DBMS%20PBL/presentation_review2.html) | Open in any browser. Keyboard controls (`→`/`Space` next, `←` prev, `N` speaker notes, `F` fullscreen), and **Print to PDF** button. |
| **Complete 3NF DDL Script** | [schema_review2.sql](file:///Users/himanshu/Documents/DBMS%20PBL/schema_review2.sql) | 16 normalized tables, CHECK predicates, slot overlap trigger, single active bed trigger, payment ceiling trigger, and 5 production views. |
| **Relational Sample Dataset** | [sample_data_review2.sql](file:///Users/himanshu/Documents/DBMS%20PBL/sample_data_review2.sql) | Populated with 6 departments, 12 doctors, 10 patients, 15 appointments, 10 consultations, ICD-10 diagnoses, lab tests, 25 beds, admissions, and bills. |
| **Demonstration Queries Suite**| [queries_review2.sql](file:///Users/himanshu/Documents/DBMS%20PBL/queries_review2.sql) | 14 production queries demonstrating multi-table joins, scalar & correlated subqueries, aggregations with GROUP BY & HAVING, and view queries. |
| **Normalization & Data Dictionary**| [Data_Dictionary_and_Normalization.md](file:///Users/himanshu/Documents/DBMS%20PBL/Data_Dictionary_and_Normalization.md) | Formal 1NF/2NF/3NF mathematical decomposition proofs, full functional dependencies list, and complete structured data dictionary. |
| **Live Database File** | [hospital_review2.db](file:///Users/himanshu/Documents/DBMS%20PBL/hospital_review2.db) | Fully populated SQLite relational database ready for live command-line query execution during viva. |

---

## 📑 Slide-by-Slide Presenter Script & Defense Notes

### Slide 1: Title Slide — *30 Seconds*
> *"Respected evaluators, welcome to Review 2 of Project 03: Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System.  
> In Review 1, we established our conceptual Chen ER model. In this review, we present our complete 3NF normalization proofs, our concise data dictionary, our production DDL with integrity triggers enforcing all business rules, our 14 demonstration queries, 5 permanent database views, and our verified database prototype."*

---

### Slide 2: Relational Normalization Up to 3NF — *60 Seconds*
> *"We decomposed the unnormalized clinical record through 1NF, 2NF, and 3NF:  
> - **1NF:** We eliminated repeating medication groups and lab order arrays by decomposing them into dedicated child entities: `prescription_items` and `test_orders`. All attributes are atomic scalars.  
> - **2NF:** We eliminated partial dependencies on composite candidate keys. For instance, in prescription lines, medicine descriptions and standard costs are isolated from individual dosage/duration records.  
> - **3NF:** We eliminated transitive dependencies ($X \to Y$ and $Y \to Z$). Doctors only hold `dept_id`, while department attributes reside in `departments`. Similarly, beds reference `ward_id` without duplicating ward types or capacities. Every functional dependency has a Superkey determinant."*

---

### Slide 3: Concise Data Dictionary — *45 Seconds*
> *"Our data dictionary defines our 16 relational tables categorized into three distinct operational domains:  
> - **Outpatient Domain:** `departments`, `doctors`, `doctor_schedules`, `patients`, and `appointments` with slot uniqueness.  
> - **Clinical & Diagnostics Domain:** `consultations` (1:1 with appointments), `diagnoses` (with ICD-10 codes and severity checks), `prescriptions`, `prescription_items`, `lab_tests`, and `test_orders`.  
> - **Inpatient & Billing Domain:** `wards`, `beds`, `admissions`, `bills` (capped by mathematical check constraints), and `payments`. Every foreign key specifies explicit cascading rules."*

---

### Slide 4: Critical Business Rules Enforcement — *60 Seconds*
> *"The project specification mandates four critical business rules, which we enforce directly in DDL and triggers:  
> 1. **No Overlapping Appointments:** Enforced via `UNIQUE (doctor_id, appointment_date, start_time)` and trigger `trg_prevent_appointment_overlap` which aborts any insert where the requested interval overlaps an existing active booking.  
> 2. **One Active Patient Per Bed:** Enforced via trigger `trg_prevent_bed_double_booking` and partial unique index, guaranteeing no two active admissions share a bed.  
> 3. **Valid Admission / Discharge Dates:** Enforced via `CHECK (discharge_date IS NULL OR discharge_date >= admission_date)`.  
> 4. **Positive Charges & Payment Limits:** Enforced via `CHECK (total_amount >= 0)`, `CHECK (amount_paid > 0)`, and `CHECK (paid_amount <= net_payable)`. An automated payment trigger increments paid amounts and transitions invoice status to `PAID`."*

---

### Slide 5: Advanced SQL Queries: Joins & Subqueries — *45 Seconds*
> *"Our query suite demonstrates advanced relational retrieval:  
> - **Multi-Table Joins:** We executed a 5-table join reconstructing the patient's complete clinical encounter journey, and a 6-table join for the active inpatient ward census with length of stay calculation.  
> - **Subqueries:** We used scalar subqueries in `HAVING` to isolate patients whose billed expenditure exceeds the overall hospital average, and correlated subqueries to determine the clinician handling the highest caseload within each respective department."*

---

### Slide 6: Aggregations & Analytical Metrics — *45 Seconds*
> *"Using `GROUP BY` and `HAVING`, we calculated essential hospital Key Performance Indicators:  
> - **Departmental Revenue Recovery:** Aggregates gross charges against collections, computing recovery percentages (e.g. 100% in cardiology and surgery).  
> - **ICD-10 Morbidity Statistics:** Calculates disease prevalence percentages across all clinical consultations.  
> - **Ward Bed Occupancy Rate:** Formula $(Active Inpatients \times 100.0) / Total Beds$, calculating unit census and projected daily bed revenues."*

---

### Slide 7: 5 Production Analytical Views — *45 Seconds*
> *"To provide role-tailored and secure abstractions, we implemented 5 production views:  
> 1. `view_patient_history`: Complete longitudinal timeline for attending doctors.  
> 2. `view_doctor_schedules`: Clinician shifts and real-time available slots for front-desk receptionists.  
> 3. `view_pending_tests`: Laboratory backlog and turnaround hour tracking for technicians.  
> 4. `view_bed_occupancy`: Live ward bed census for emergency and nursing supervisors.  
> 5. `view_outstanding_bills_revenue`: Ledger of paid vs unpaid receivables for the accounts desk."*

---

### Slide 8: Implementation Progress & Demonstration — *30 Seconds*
> *"In conclusion, all Review 2 deliverables are 100% fulfilled: 3NF normalization proofs, full DDL with triggers, 14 verified queries, 5 views, and an active prototype. We are fully on track for our Review 3 final application delivery in Week 16. We now welcome your questions and invite you to inspect the live prototype."*

---

## 🎯 Review 2 Viva-Voce Defense Questions & Answers

### Q1: Why is BCNF or 3NF chosen over 2NF?
**Answer:** In 2NF, transitive dependencies ($X \to Y$ and $Y \to Z$ where $Z$ is a non-prime attribute) can still exist. For example, if `doctor_id -> dept_id` and `dept_id -> dept_name`, updating the department name would require updating every doctor in that department, risking data inconsistency. 3NF removes all transitive dependencies so non-key attributes depend solely on candidate keys.

### Q2: How did you implement "no overlapping doctor appointments" in SQL?
**Answer:** We implemented dual-layer protection:
1. `UNIQUE (doctor_id, appointment_date, start_time)` prevents exact duplicate slot bookings.
2. A `BEFORE INSERT` trigger `trg_prevent_appointment_overlap` verifies interval overlap:
   $$\text{NEW.start\_time} < \text{existing.end\_time} \quad \text{AND} \quad \text{NEW.end\_time} > \text{existing.start\_time}$$
   for all non-cancelled appointments for that doctor on that date, raising an integrity abort if an overlap exists.

### Q3: How is "one active patient per bed" enforced when patients get discharged?
**Answer:** A bed will have many past historical admissions, so a plain `UNIQUE (bed_id)` constraint cannot be used. We solve this using:
- **PostgreSQL / SQLite Trigger:** `trg_prevent_bed_double_booking` checks `WHEN NEW.status = 'ACTIVE'` and aborts if `EXISTS (SELECT 1 FROM admissions WHERE bed_id = NEW.bed_id AND status = 'ACTIVE')`.
- **PostgreSQL Partial Unique Index:** `CREATE UNIQUE INDEX ON admissions(bed_id) WHERE status = 'ACTIVE'`.

### Q4: Why use Views instead of writing complex joins in application code?
**Answer:** Views provide three key advantages:
1. **Abstraction & Simplicity:** Developers and front-desk modules can run `SELECT * FROM view_bed_occupancy` rather than writing 6-table joins.
2. **Security & Access Control:** We can grant nursing staff access to `view_bed_occupancy` without granting them raw `SELECT` permissions on clinical bills or doctor salaries.
3. **Query Optimization:** The DBMS query planner optimizes and caches the compiled view plan.
