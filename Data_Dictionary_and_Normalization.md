# Hospital DBMS — 3NF Normalization Analysis & Concise Data Dictionary
**Course:** Database Management Systems (DBMS PBL)  
**Project:** Hospital Appointment and Patient Care Management System  
**Milestone:** Review 2 (Week 11 — 5 Marks)

---

## 📐 Part 1: Relational Normalization Analysis (Up to 3NF)

### 1. The Universal Relation & 0NF (Unnormalized State)
In an unnormalized paper-based or spreadsheet hospital ledger, data is recorded as a single massive record:
$$R_{0NF}(\underline{\text{PatientPhone}}, \text{PatientName}, \text{DOB}, \text{DoctorName}, \text{DeptName}, \text{AppointmentDate}, \text{Symptoms}, \{\text{MedicineName}, \text{Dosage}, \text{Frequency}\}, \{\text{TestName}, \text{Cost}\}, \text{BedNumber}, \text{WardName}, \text{BillTotal}, \dots)$$

#### Anomalies Present in 0NF:
1. **Insertion Anomaly:** Cannot register a new department or new doctor until an appointment is booked.
2. **Update Anomaly:** If a doctor's consultation fee changes, thousands of appointment rows must be updated.
3. **Deletion Anomaly:** Deleting a patient's cancelled appointment erases doctor or ward existence.

---

### 2. First Normal Form (1NF)
> **Definition:** A relation $R$ is in 1NF if and only if all underlying attribute domains contain only **atomic (indivisible) values**, and there are **no repeating groups or multi-valued attributes**.

#### Normalization Step 1NF:
1. **Decompose Multi-Valued Attributes:**
   - Multi-valued medication lines $\{\text{MedicineName}, \text{Dosage}, \text{Frequency}, \text{Duration}\}$ are extracted into a dedicated child entity: `prescription_items`.
   - Multi-valued laboratory orders $\{\text{TestName}, \text{Status}, \text{Result}\}$ are extracted into `test_orders`.
2. **Composite Attributes Decomposed:**
   - `PatientName` decomposed into `first_name` and `last_name`.
   - `EmergencyContact` decomposed into `emergency_contact_name` and `emergency_contact_phone`.
3. **Primary Keys Established:** Unique artificial surrogates (`patient_id`, `doctor_id`, `appointment_id`, etc.) guarantee tuple uniqueness.

---

### 3. Second Normal Form (2NF)
> **Definition:** A relation $R$ is in 2NF if and only if it is in 1NF and **every non-prime attribute is fully functionally dependent on the primary key** (i.e., no partial dependencies on any composite candidate key).

#### Normalization Step 2NF:
Consider the intermediate relation `PrescriptionDetails`:
$$\text{PrescriptionDetails}(\underline{\text{prescription\_id}, \text{medicine\_id}}, \text{medicine\_name}, \text{standard\_cost}, \text{dosage}, \text{frequency})$$
- Candidate Key: $\{\text{prescription\_id}, \text{medicine\_id}\}$
- Functional Dependencies:
  - $\{\text{prescription\_id}, \text{medicine\_id}\} \to \text{dosage}, \text{frequency}$ *(Full Dependency)*
  - $\text{medicine\_id} \to \text{medicine\_name}, \text{standard\_cost}$ *(Partial Dependency on subset of Key!)*

**2NF Resolution:** Decomposed into:
1. `prescriptions` ($\underline{\text{prescription\_id}}$, consultation_id, prescription_date, advice)
2. `prescription_items` ($\underline{\text{item\_id}}$, prescription_id, medicine_name, dosage, frequency, duration, quantity)

Similarly, `test_orders` separates the ordered instance from `lab_tests` (catalog of standard test definitions and reference ranges).

---

### 4. Third Normal Form (3NF)
> **Definition:** A relation $R$ is in 3NF if and only if it is in 2NF and **no non-prime attribute is transitively dependent on any candidate key** (i.e., for every non-trivial functional dependency $X \to Y$, either $X$ is a superkey or $Y$ is a prime attribute).

#### Normalization Step 3NF:
Consider un-normalized doctors and departments combined:
$$\text{DoctorDept}(\underline{\text{doctor\_id}}, \text{first\_name}, \text{specialization}, \text{dept\_id}, \text{dept\_name}, \text{building\_block}, \text{floor\_number})$$
- Primary Key: $\text{doctor\_id}$
- Functional Dependencies:
  - $\text{doctor\_id} \to \text{dept\_id}$
  - $\text{dept\_id} \to \text{dept\_name}, \text{building\_block}, \text{floor\_number}$
- **Transitive Dependency:** $\text{doctor\_id} \to \text{dept\_name}$ through $\text{dept\_id}$.

**3NF Resolution:** Decomposed into:
1. `departments` ($\underline{\text{dept\_id}}$, dept_name, building_block, floor_number, contact_ext)
2. `doctors` ($\underline{\text{doctor\_id}}$, dept_id, first_name, last_name, qualification, specialization, email, phone, fee, license)

The same resolution was applied between `wards` and `beds`, eliminating transitive dependencies ($\text{bed\_id} \to \text{ward\_id} \to \text{ward\_type}, \text{floor\_number}$).

---

### 5. Summary of Functional Dependencies (FDs)

| Table | Primary Key | Determinant ($X$) | Dependent Attributes ($Y$) | Form |
| :--- | :--- | :--- | :--- | :---: |
| `departments` | `dept_id` | `dept_id` | `dept_name, building_block, floor_number, contact_ext` | **3NF** |
| `doctors` | `doctor_id` | `doctor_id` | `dept_id, first_name, last_name, qualification, specialization, email, phone, consultation_fee, license_number, status` | **3NF** |
| `doctor_schedules` | `schedule_id` | `schedule_id` | `doctor_id, day_of_week, start_time, end_time, slot_duration_mins, max_patients, is_active` | **3NF** |
| `patients` | `patient_id` | `patient_id` | `first_name, last_name, dob, gender, blood_group, phone, email, address, emergency_contact_name, emergency_contact_phone` | **3NF** |
| `appointments` | `appointment_id` | `appointment_id` | `patient_id, doctor_id, appointment_date, start_time, end_time, status, reason` | **3NF** |
| `consultations` | `consultation_id` | `consultation_id` | `appointment_id, doctor_id, patient_id, consultation_timestamp, symptoms, physical_examination, clinical_notes, follow_up_date` | **3NF** |
| `diagnoses` | `diagnosis_id` | `diagnosis_id` | `consultation_id, icd10_code, diagnosis_name, severity, diagnosis_type, remarks` | **3NF** |
| `prescriptions` | `prescription_id` | `prescription_id` | `consultation_id, prescription_date, general_advice` | **3NF** |
| `prescription_items` | `item_id` | `item_id` | `prescription_id, medicine_name, dosage, frequency, duration_days, quantity, instructions` | **3NF** |
| `lab_tests` | `test_id` | `test_id` | `dept_id, test_name, test_code, standard_cost, sample_type, turnaround_hours` | **3NF** |
| `test_orders` | `order_id` | `order_id` | `consultation_id, test_id, order_date, status, result_value, reference_range, result_date, lab_technician_notes` | **3NF** |
| `wards` | `ward_id` | `ward_id` | `dept_id, ward_name, ward_type, floor_number, capacity` | **3NF** |
| `beds` | `bed_id` | `bed_id` | `ward_id, bed_number, daily_rate, is_operational` | **3NF** |
| `admissions` | `admission_id` | `admission_id` | `patient_id, bed_id, admitting_doctor_id, admission_date, discharge_date, admission_reason, discharge_summary, status` | **3NF** |
| `bills` | `bill_id` | `bill_id` | `patient_id, consultation_id, admission_id, bill_date, total_amount, discount_amount, tax_amount, net_payable, paid_amount, payment_status` | **3NF** |
| `payments` | `payment_id` | `payment_id` | `bill_id, payment_timestamp, amount_paid, payment_method, transaction_ref, received_by, remarks` | **3NF** |

---

## 📚 Part 2: Concise Data Dictionary

### Table 1: `departments`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `dept_id` | INTEGER | No | `PK, AUTOINCREMENT` | Unique identifier for medical department |
| `dept_name` | VARCHAR(100) | No | `UNIQUE` | Department official designation (e.g. Cardiology) |
| `building_block`| VARCHAR(50) | No | — | Hospital wing/campus building |
| `floor_number` | INTEGER | No | `CHECK (>= 0)` | Floor elevation |
| `contact_ext` | VARCHAR(15) | Yes | — | Internal PBX telephone extension |
| `head_doctor_id`| INTEGER | Yes | `FK -> doctors(doctor_id)` | Clinical director / HOD |

### Table 2: `doctors`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `doctor_id` | INTEGER | No | `PK, AUTOINCREMENT` | Physician identifier |
| `dept_id` | INTEGER | No | `FK -> departments(dept_id)`| Primary clinical specialty division |
| `first_name` | VARCHAR(50) | No | — | Doctor given name |
| `last_name` | VARCHAR(50) | No | — | Doctor family name |
| `qualification` | VARCHAR(100)| No | — | Degrees (e.g. MD, DM, MCh) |
| `specialization`| VARCHAR(100)| No | — | Sub-specialty expertise |
| `email` | VARCHAR(100)| No | `UNIQUE` | Official hospital email |
| `phone` | VARCHAR(20) | No | `UNIQUE` | Contact number |
| `consultation_fee`| DECIMAL(10,2)| No| `CHECK (>= 0)` | Base outpatient evaluation fee |
| `license_number`| VARCHAR(50) | No | `UNIQUE` | State Medical Council registration |
| `status` | VARCHAR(20) | No | `CHECK IN ('ACTIVE', 'ON_LEAVE', 'RESIGNED')` | Staff roster state |

### Table 3: `doctor_schedules`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `schedule_id` | INTEGER | No | `PK, AUTOINCREMENT` | Shift roster identifier |
| `doctor_id` | INTEGER | No | `FK -> doctors(doctor_id)` | Attending doctor |
| `day_of_week` | VARCHAR(15) | No | `CHECK IN (MONDAY..SUNDAY)`| Day of recurrent duty |
| `start_time` | TIME | No | — | Shift commencement |
| `end_time` | TIME | No | `CHECK (end_time > start_time)` | Shift termination |
| `slot_duration_mins`| INTEGER | No | `CHECK (> 0), DEFAULT 15`| Time allocated per patient |
| `max_patients` | INTEGER | No | `CHECK (> 0), DEFAULT 20`| Maximum slot capacity |
| `is_active` | BOOLEAN | No | `DEFAULT 1` | Shift enablement toggle |

### Table 4: `patients`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `patient_id` | INTEGER | No | `PK, AUTOINCREMENT` | Master Patient Index (MPI) identifier |
| `first_name` | VARCHAR(50) | No | — | Patient given name |
| `last_name` | VARCHAR(50) | No | — | Patient surname |
| `dob` | DATE | No | — | Date of birth |
| `gender` | VARCHAR(10) | No | `CHECK IN ('MALE', 'FEMALE', 'OTHER')` | Biological sex |
| `blood_group` | VARCHAR(5) | Yes | `CHECK IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')` | ABO / Rh group |
| `phone` | VARCHAR(20) | No | `UNIQUE` | Primary SMS/WhatsApp contact |
| `email` | VARCHAR(100)| Yes | — | Email for electronic lab reports |
| `address` | TEXT | No | — | Residential address |
| `emergency_contact_name`| VARCHAR(100)| No | — | Next of kin name |
| `emergency_contact_phone`| VARCHAR(20)| No | — | Next of kin phone |

### Table 5: `appointments`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `appointment_id`| INTEGER | No | `PK, AUTOINCREMENT` | Unique appointment token |
| `patient_id` | INTEGER | No | `FK -> patients(patient_id)` | Scheduled patient |
| `doctor_id` | INTEGER | No | `FK -> doctors(doctor_id)` | Targeted clinician |
| `appointment_date`| DATE | No | — | Scheduled consultation date |
| `start_time` | TIME | No | — | Slot start time |
| `end_time` | TIME | No | `CHECK (end_time > start_time)` | Slot end time |
| `status` | VARCHAR(20) | No | `CHECK IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')` | Appointment workflow state |
| `reason` | TEXT | Yes | — | Chief presenting complaint |

### Table 6: `admissions`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `admission_id` | INTEGER | No | `PK, AUTOINCREMENT` | Inpatient encounter ID |
| `patient_id` | INTEGER | No | `FK -> patients(patient_id)` | Admitted patient |
| `bed_id` | INTEGER | No | `FK -> beds(bed_id)` | Assigned hospital bed |
| `admitting_doctor_id`| INTEGER| No| `FK -> doctors(doctor_id)` | Primary physician in-charge |
| `admission_date`| TIMESTAMP| No | `DEFAULT CURRENT_TIMESTAMP`| Intake timestamp |
| `discharge_date`| TIMESTAMP| Yes| `CHECK (discharge_date >= admission_date)` | Discharge timestamp |
| `admission_reason`| TEXT | No | — | Clinical indication for admission |
| `discharge_summary`| TEXT | Yes| — | Medical summary upon discharge |
| `status` | VARCHAR(20) | No | `CHECK IN ('ACTIVE', 'DISCHARGED', 'TRANSFERRED', 'CANCELLED')` | Inpatient status |

### Table 7: `bills`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `bill_id` | INTEGER | No | `PK, AUTOINCREMENT` | Invoice number |
| `patient_id` | INTEGER | No | `FK -> patients(patient_id)` | Billed individual |
| `consultation_id`| INTEGER | Yes | `FK -> consultations` | Associated OPD visit (if any) |
| `admission_id` | INTEGER | Yes | `FK -> admissions` | Associated IPD stay (if any) |
| `bill_date` | TIMESTAMP| No | `DEFAULT CURRENT_TIMESTAMP`| Invoice generation timestamp |
| `total_amount` | DECIMAL(10,2)| No| `CHECK (>= 0)` | Gross unadjusted charge |
| `discount_amount`| DECIMAL(10,2)| No| `CHECK (>= 0)` | Concession / scheme discount |
| `tax_amount` | DECIMAL(10,2)| No| `CHECK (>= 0)` | Applicable GST / service tax |
| `net_payable` | DECIMAL(10,2)| No| `CHECK (net_payable = total - discount + tax)` | Final payable charge |
| `paid_amount` | DECIMAL(10,2)| No| `CHECK (paid_amount <= net_payable)` | Cumulative remittance |
| `payment_status`| VARCHAR(20) | No| `CHECK IN ('UNPAID', 'PARTIALLY_PAID', 'PAID', 'CANCELLED')` | Invoice settlement state |

### Table 8: `payments`
| Column | Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `payment_id` | INTEGER | No | `PK, AUTOINCREMENT` | Remittance receipt ID |
| `bill_id` | INTEGER | No | `FK -> bills(bill_id)` | Invoice receiving payment |
| `payment_timestamp`| TIMESTAMP| No| `DEFAULT CURRENT_TIMESTAMP`| Transaction timestamp |
| `amount_paid` | DECIMAL(10,2)| No| `CHECK (> 0)` | Amount remitted |
| `payment_method`| VARCHAR(30) | No | `CHECK IN ('CASH', 'CREDIT_CARD', 'DEBIT_CARD', 'UPI', 'NET_BANKING', 'INSURANCE')` | Channel |
| `transaction_ref`| VARCHAR(100)| Yes| `UNIQUE` | Bank reference / UTR / Auth code |
| `received_by` | VARCHAR(50) | No | — | Cashier / System account |
