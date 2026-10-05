-- =============================================================================
-- DATABASE MANAGEMENT SYSTEM FOR HOSPITAL APPOINTMENT & PATIENT CARE SYSTEM
-- DBMS Project - Review 1 Relational Schema (DDL)
-- Compliant with 3rd Normal Form (3NF) & Strict Business Rule Constraints
-- Target DBMS: PostgreSQL / MySQL 8.0+ compatible
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. DEPARTMENT
-- -----------------------------------------------------------------------------
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    building_block VARCHAR(50) NOT NULL,
    floor_number INT NOT NULL CHECK (floor_number >= 0),
    contact_ext VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2. DOCTOR
-- -----------------------------------------------------------------------------
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    dept_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    qualification VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    consultation_fee DECIMAL(10, 2) NOT NULL CHECK (consultation_fee >= 0),
    license_number VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'ON_LEAVE', 'RESIGNED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_doctor_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Circular reference: add head_doctor_id to department after doctor table creation
ALTER TABLE departments ADD COLUMN head_doctor_id INT NULL;
ALTER TABLE departments ADD CONSTRAINT fk_dept_head FOREIGN KEY (head_doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3. DOCTOR SCHEDULE (Duty roster / Available shifts)
-- -----------------------------------------------------------------------------
CREATE TABLE doctor_schedules (
    schedule_id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL CHECK (day_of_week IN ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_duration_mins INT NOT NULL DEFAULT 15 CHECK (slot_duration_mins > 0),
    max_patients INT NOT NULL DEFAULT 20 CHECK (max_patients > 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_schedule_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_schedule_time CHECK (end_time > start_time),
    CONSTRAINT uq_doctor_day_shift UNIQUE (doctor_id, day_of_week, start_time)
);

-- -----------------------------------------------------------------------------
-- 4. PATIENT
-- -----------------------------------------------------------------------------
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL CHECK (dob <= CURRENT_DATE),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    blood_group VARCHAR(5) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    address TEXT NOT NULL,
    emergency_contact_name VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    registration_date DATE DEFAULT CURRENT_DATE
);

-- -----------------------------------------------------------------------------
-- 5. APPOINTMENT
-- Business Rule: No overlapping doctor appointments
-- -----------------------------------------------------------------------------
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL CHECK (appointment_date >= CURRENT_DATE),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_appt_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_appt_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_appt_duration CHECK (end_time > start_time),
    -- Prevent exact same doctor booked at the same date and start_time
    CONSTRAINT uq_doctor_slot UNIQUE (doctor_id, appointment_date, start_time)
);

-- -----------------------------------------------------------------------------
-- 6. CONSULTATION
-- -----------------------------------------------------------------------------
CREATE TABLE consultations (
    consultation_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL UNIQUE, -- 1:1 relationship with appointment
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    consultation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    symptoms TEXT NOT NULL,
    physical_examination TEXT,
    clinical_notes TEXT,
    follow_up_date DATE CHECK (follow_up_date IS NULL OR follow_up_date > CURRENT_DATE),
    CONSTRAINT fk_consult_appt FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_consult_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_consult_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 7. DIAGNOSIS
-- -----------------------------------------------------------------------------
CREATE TABLE diagnoses (
    diagnosis_id SERIAL PRIMARY KEY,
    consultation_id INT NOT NULL,
    icd10_code VARCHAR(20),
    diagnosis_name VARCHAR(150) NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'MODERATE' CHECK (severity IN ('MILD', 'MODERATE', 'SEVERE', 'CRITICAL')),
    diagnosis_type VARCHAR(20) NOT NULL DEFAULT 'PRIMARY' CHECK (diagnosis_type IN ('PRIMARY', 'SECONDARY', 'PROVISIONAL', 'FINAL')),
    remarks TEXT,
    CONSTRAINT fk_diag_consult FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 8. PRESCRIPTION
-- -----------------------------------------------------------------------------
CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    consultation_id INT NOT NULL,
    prescription_date DATE DEFAULT CURRENT_DATE,
    general_advice TEXT,
    CONSTRAINT fk_rx_consult FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 8b. PRESCRIPTION ITEM (Normalized Medication Lines - 3NF compliance)
-- -----------------------------------------------------------------------------
CREATE TABLE prescription_items (
    item_id SERIAL PRIMARY KEY,
    prescription_id INT NOT NULL,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL, -- e.g., '500mg'
    frequency VARCHAR(50) NOT NULL, -- e.g., '1-0-1 after meals'
    duration_days INT NOT NULL CHECK (duration_days > 0),
    quantity INT NOT NULL CHECK (quantity > 0),
    instructions VARCHAR(200),
    CONSTRAINT fk_rxitem_rx FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 9. LAB TEST CATALOG (Master list of tests)
-- -----------------------------------------------------------------------------
CREATE TABLE lab_tests (
    test_id SERIAL PRIMARY KEY,
    dept_id INT NOT NULL,
    test_name VARCHAR(100) NOT NULL UNIQUE,
    test_code VARCHAR(20) NOT NULL UNIQUE,
    standard_cost DECIMAL(10, 2) NOT NULL CHECK (standard_cost >= 0),
    sample_type VARCHAR(50) NOT NULL, -- Blood, Urine, Sputum, etc.
    turnaround_hours INT NOT NULL CHECK (turnaround_hours > 0),
    CONSTRAINT fk_test_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 9b. TEST ORDER & RESULT (Diagnostic Execution)
-- -----------------------------------------------------------------------------
CREATE TABLE test_orders (
    order_id SERIAL PRIMARY KEY,
    consultation_id INT NOT NULL,
    test_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'ORDERED' CHECK (status IN ('ORDERED', 'SAMPLE_COLLECTED', 'PROCESSING', 'COMPLETED', 'CANCELLED')),
    result_value TEXT,
    reference_range VARCHAR(100),
    result_date TIMESTAMP,
    lab_technician_notes TEXT,
    CONSTRAINT fk_order_consult FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_order_test FOREIGN KEY (test_id) REFERENCES lab_tests(test_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 10. WARD (Inpatient Infrastructure)
-- -----------------------------------------------------------------------------
CREATE TABLE wards (
    ward_id SERIAL PRIMARY KEY,
    dept_id INT NOT NULL,
    ward_name VARCHAR(50) NOT NULL UNIQUE,
    ward_type VARCHAR(30) NOT NULL CHECK (ward_type IN ('GENERAL', 'SEMI_PRIVATE', 'PRIVATE', 'ICU', 'EMERGENCY', 'MATERNITY')),
    floor_number INT NOT NULL CHECK (floor_number >= 0),
    capacity INT NOT NULL CHECK (capacity > 0),
    CONSTRAINT fk_ward_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 11. BED
-- -----------------------------------------------------------------------------
CREATE TABLE beds (
    bed_id SERIAL PRIMARY KEY,
    ward_id INT NOT NULL,
    bed_number VARCHAR(20) NOT NULL,
    daily_rate DECIMAL(10, 2) NOT NULL CHECK (daily_rate >= 0),
    is_operational BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_bed_ward FOREIGN KEY (ward_id) REFERENCES wards(ward_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT uq_ward_bed UNIQUE (ward_id, bed_number)
);

-- -----------------------------------------------------------------------------
-- 12. ADMISSION
-- Business Rules: Valid dates (discharge >= admission), 1 active patient per bed
-- -----------------------------------------------------------------------------
CREATE TABLE admissions (
    admission_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    bed_id INT NOT NULL,
    admitting_doctor_id INT NOT NULL,
    admission_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    discharge_date TIMESTAMP NULL,
    admission_reason TEXT NOT NULL,
    discharge_summary TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'DISCHARGED', 'TRANSFERRED', 'CANCELLED')),
    CONSTRAINT fk_adm_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_adm_bed FOREIGN KEY (bed_id) REFERENCES beds(bed_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_adm_doctor FOREIGN KEY (admitting_doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    -- Discharge date must be after or equal to admission date
    CONSTRAINT chk_adm_dates CHECK (discharge_date IS NULL OR discharge_date >= admission_date)
);

-- PostgreSQL Partial Unique Index: Ensures at most ONE active admission per bed!
-- (For MySQL, this can be enforced via a trigger or unique active status table)
CREATE UNIQUE INDEX idx_uq_active_bed_admission ON admissions (bed_id) WHERE status = 'ACTIVE';

-- -----------------------------------------------------------------------------
-- 13. BILLING
-- Business Rules: Positive amounts, net_payable calculation, non-negative balances
-- -----------------------------------------------------------------------------
CREATE TABLE bills (
    bill_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    consultation_id INT NULL,
    admission_id INT NULL,
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (total_amount >= 0),
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (discount_amount >= 0),
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (tax_amount >= 0),
    net_payable DECIMAL(10, 2) NOT NULL CHECK (net_payable >= 0),
    paid_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (paid_amount >= 0),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'UNPAID' CHECK (payment_status IN ('UNPAID', 'PARTIALLY_PAID', 'PAID', 'CANCELLED')),
    CONSTRAINT fk_bill_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_bill_consult FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_bill_admission FOREIGN KEY (admission_id) REFERENCES admissions(admission_id) ON UPDATE CASCADE ON DELETE SET NULL,
    -- Paid amount cannot exceed net payable
    CONSTRAINT chk_bill_paid_ceiling CHECK (paid_amount <= net_payable),
    -- Net payable calculation sanity
    CONSTRAINT chk_bill_calc CHECK (net_payable = (total_amount - discount_amount + tax_amount))
);

-- -----------------------------------------------------------------------------
-- 14. PAYMENT
-- Business Rules: Valid payment amount > 0, linked to invoice
-- -----------------------------------------------------------------------------
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    bill_id INT NOT NULL,
    payment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount_paid DECIMAL(10, 2) NOT NULL CHECK (amount_paid > 0),
    payment_method VARCHAR(30) NOT NULL CHECK (payment_method IN ('CASH', 'CREDIT_CARD', 'DEBIT_CARD', 'UPI', 'NET_BANKING', 'INSURANCE')),
    transaction_ref VARCHAR(100) UNIQUE,
    received_by VARCHAR(50) NOT NULL,
    remarks VARCHAR(255),
    CONSTRAINT fk_payment_bill FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- PERFORMANCE INDEXES (Optimized for frequent joins and query lookups)
-- -----------------------------------------------------------------------------
CREATE INDEX idx_doctor_dept ON doctors(dept_id);
CREATE INDEX idx_doctor_specialization ON doctors(specialization);
CREATE INDEX idx_patient_phone ON patients(phone);
CREATE INDEX idx_patient_dob ON patients(dob);
CREATE INDEX idx_appt_doctor_date ON appointments(doctor_id, appointment_date);
CREATE INDEX idx_appt_patient ON appointments(patient_id);
CREATE INDEX idx_consult_patient ON consultations(patient_id);
CREATE INDEX idx_test_order_consult ON test_orders(consultation_id);
CREATE INDEX idx_test_order_status ON test_orders(status);
CREATE INDEX idx_admission_patient ON admissions(patient_id);
CREATE INDEX idx_admission_status ON admissions(status);
CREATE INDEX idx_bill_patient_status ON bills(patient_id, payment_status);
