-- =============================================================================
-- DATABASE MANAGEMENT SYSTEM FOR HOSPITAL APPOINTMENT & PATIENT CARE SYSTEM
-- DBMS Project - Review 2 Relational Schema & Integrity Constraints (DDL)
-- Compliant with 3rd Normal Form (3NF) & Business Rule Integrity Verification
-- Compatible with PostgreSQL 12+, MySQL 8.0+, and SQLite 3.30+
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. DEPARTMENTS
-- FD: dept_id -> dept_name, building_block, floor_number, contact_ext
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    building_block VARCHAR(50) NOT NULL,
    floor_number INTEGER NOT NULL CHECK (floor_number >= 0),
    contact_ext VARCHAR(15),
    head_doctor_id INTEGER NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2. DOCTORS
-- FD: doctor_id -> dept_id, first_name, last_name, qualification, specialization,
--                  email, phone, consultation_fee, license_number, status
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
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
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 3. DOCTOR SCHEDULES (Duty Roster & Slot Configuration)
-- FD: schedule_id -> doctor_id, day_of_week, start_time, end_time, slot_duration_mins, max_patients
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctor_schedules (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    day_of_week VARCHAR(15) NOT NULL CHECK (day_of_week IN ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_duration_mins INTEGER NOT NULL DEFAULT 15 CHECK (slot_duration_mins > 0),
    max_patients INTEGER NOT NULL DEFAULT 20 CHECK (max_patients > 0),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK (end_time > start_time),
    UNIQUE (doctor_id, day_of_week, start_time)
);

-- -----------------------------------------------------------------------------
-- 4. PATIENTS
-- FD: patient_id -> first_name, last_name, dob, gender, blood_group, phone, email, address, emergency contact
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    blood_group VARCHAR(5) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    address TEXT NOT NULL,
    emergency_contact_name VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    registration_date DATE DEFAULT (DATE('now'))
);

-- -----------------------------------------------------------------------------
-- 5. APPOINTMENTS
-- Business Rule 1: No overlapping doctor appointments
-- FD: appointment_id -> patient_id, doctor_id, appointment_date, start_time, end_time, status, reason
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CHECK (end_time > start_time),
    UNIQUE (doctor_id, appointment_date, start_time)
);

-- -----------------------------------------------------------------------------
-- 6. CONSULTATIONS
-- FD: consultation_id -> appointment_id, doctor_id, patient_id, symptoms, examination, notes
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS consultations (
    consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL UNIQUE,
    doctor_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    consultation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    symptoms TEXT NOT NULL,
    physical_examination TEXT,
    clinical_notes TEXT,
    follow_up_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 7. DIAGNOSES
-- FD: diagnosis_id -> consultation_id, icd10_code, diagnosis_name, severity, diagnosis_type
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id INTEGER NOT NULL,
    icd10_code VARCHAR(20),
    diagnosis_name VARCHAR(150) NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'MODERATE' CHECK (severity IN ('MILD', 'MODERATE', 'SEVERE', 'CRITICAL')),
    diagnosis_type VARCHAR(20) NOT NULL DEFAULT 'PRIMARY' CHECK (diagnosis_type IN ('PRIMARY', 'SECONDARY', 'PROVISIONAL', 'FINAL')),
    remarks TEXT,
    FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 8. PRESCRIPTIONS
-- FD: prescription_id -> consultation_id, prescription_date, general_advice
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id INTEGER NOT NULL,
    prescription_date DATE DEFAULT (DATE('now')),
    general_advice TEXT,
    FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 8b. PRESCRIPTION ITEMS (Decomposed to satisfy 1NF & 3NF)
-- FD: item_id -> prescription_id, medicine_name, dosage, frequency, duration_days, quantity
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prescription_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER NOT NULL,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    duration_days INTEGER NOT NULL CHECK (duration_days > 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    instructions VARCHAR(200),
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 9. LAB TESTS (Test Catalog)
-- FD: test_id -> dept_id, test_name, test_code, standard_cost, sample_type, turnaround_hours
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lab_tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    test_name VARCHAR(100) NOT NULL UNIQUE,
    test_code VARCHAR(20) NOT NULL UNIQUE,
    standard_cost DECIMAL(10, 2) NOT NULL CHECK (standard_cost >= 0),
    sample_type VARCHAR(50) NOT NULL,
    turnaround_hours INTEGER NOT NULL CHECK (turnaround_hours > 0),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 9b. TEST ORDERS (Diagnostic Orders & Results)
-- FD: order_id -> consultation_id, test_id, order_date, status, result_value, reference_range
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS test_orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'ORDERED' CHECK (status IN ('ORDERED', 'SAMPLE_COLLECTED', 'PROCESSING', 'COMPLETED', 'CANCELLED')),
    result_value TEXT,
    reference_range VARCHAR(100),
    result_date TIMESTAMP,
    lab_technician_notes TEXT,
    FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES lab_tests(test_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 10. WARDS
-- FD: ward_id -> dept_id, ward_name, ward_type, floor_number, capacity
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wards (
    ward_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    ward_name VARCHAR(50) NOT NULL UNIQUE,
    ward_type VARCHAR(30) NOT NULL CHECK (ward_type IN ('GENERAL', 'SEMI_PRIVATE', 'PRIVATE', 'ICU', 'EMERGENCY', 'MATERNITY')),
    floor_number INTEGER NOT NULL CHECK (floor_number >= 0),
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 11. BEDS
-- FD: bed_id -> ward_id, bed_number, daily_rate, is_operational
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS beds (
    bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ward_id INTEGER NOT NULL,
    bed_number VARCHAR(20) NOT NULL,
    daily_rate DECIMAL(10, 2) NOT NULL CHECK (daily_rate >= 0),
    is_operational BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (ward_id, bed_number)
);

-- -----------------------------------------------------------------------------
-- 12. ADMISSIONS
-- Business Rule 2: One active patient per bed
-- Business Rule 3: Valid admission & discharge dates (discharge_date >= admission_date)
-- FD: admission_id -> patient_id, bed_id, admitting_doctor_id, admission_date, discharge_date, status
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admissions (
    admission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    bed_id INTEGER NOT NULL,
    admitting_doctor_id INTEGER NOT NULL,
    admission_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    discharge_date TIMESTAMP NULL,
    admission_reason TEXT NOT NULL,
    discharge_summary TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'DISCHARGED', 'TRANSFERRED', 'CANCELLED')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (bed_id) REFERENCES beds(bed_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (admitting_doctor_id) REFERENCES doctors(doctor_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CHECK (discharge_date IS NULL OR discharge_date >= admission_date)
);

-- -----------------------------------------------------------------------------
-- 13. BILLS
-- Business Rule 4: Positive charges, paid_amount <= net_payable
-- FD: bill_id -> patient_id, consultation_id, admission_id, bill_date, total_amount, discount_amount, tax_amount, net_payable, paid_amount, payment_status
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    consultation_id INTEGER NULL,
    admission_id INTEGER NULL,
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (total_amount >= 0),
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (discount_amount >= 0),
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (tax_amount >= 0),
    net_payable DECIMAL(10, 2) NOT NULL CHECK (net_payable >= 0),
    paid_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (paid_amount >= 0),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'UNPAID' CHECK (payment_status IN ('UNPAID', 'PARTIALLY_PAID', 'PAID', 'CANCELLED')),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CHECK (paid_amount <= net_payable),
    CHECK (net_payable = (total_amount - discount_amount + tax_amount))
);

-- -----------------------------------------------------------------------------
-- 14. PAYMENTS
-- Business Rule 5: Positive payments linked to bill
-- FD: payment_id -> bill_id, payment_timestamp, amount_paid, payment_method, transaction_ref, received_by
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    payment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount_paid DECIMAL(10, 2) NOT NULL CHECK (amount_paid > 0),
    payment_method VARCHAR(30) NOT NULL CHECK (payment_method IN ('CASH', 'CREDIT_CARD', 'DEBIT_CARD', 'UPI', 'NET_BANKING', 'INSURANCE')),
    transaction_ref VARCHAR(100) UNIQUE,
    received_by VARCHAR(50) NOT NULL,
    remarks VARCHAR(255),
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- =============================================================================
-- TRIGGERS FOR ADVANCED INTEGRITY CONSTRAINTS
-- =============================================================================

-- TRIGGER 1: PREVENT OVERLAPPING APPOINTMENTS FOR THE SAME DOCTOR
CREATE TRIGGER IF NOT EXISTS trg_prevent_appointment_overlap
BEFORE INSERT ON appointments
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM appointments
    WHERE doctor_id = NEW.doctor_id
      AND appointment_date = NEW.appointment_date
      AND status NOT IN ('CANCELLED', 'NO_SHOW')
      AND (
          (NEW.start_time < end_time AND NEW.end_time > start_time)
      )
)
BEGIN
    SELECT RAISE(ABORT, 'INTEGRITY ERROR: Doctor already has an overlapping appointment in this time window.');
END;

-- TRIGGER 2: PREVENT MORE THAN ONE ACTIVE PATIENT PER BED
CREATE TRIGGER IF NOT EXISTS trg_prevent_bed_double_booking
BEFORE INSERT ON admissions
FOR EACH ROW
WHEN NEW.status = 'ACTIVE' AND EXISTS (
    SELECT 1 FROM admissions
    WHERE bed_id = NEW.bed_id
      AND status = 'ACTIVE'
)
BEGIN
    SELECT RAISE(ABORT, 'INTEGRITY ERROR: Selected bed currently has an active admitted patient.');
END;

-- TRIGGER 3: AUTO-UPDATE BILL PAID AMOUNT AND PAYMENT STATUS ON PAYMENT INSERT
CREATE TRIGGER IF NOT EXISTS trg_update_bill_on_payment
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    UPDATE bills
    SET paid_amount = paid_amount + NEW.amount_paid,
        payment_status = CASE 
            WHEN (paid_amount + NEW.amount_paid) >= net_payable THEN 'PAID'
            WHEN (paid_amount + NEW.amount_paid) > 0 THEN 'PARTIALLY_PAID'
            ELSE 'UNPAID'
        END
    WHERE bill_id = NEW.bill_id;
END;

-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_doctors_dept ON doctors(dept_id);
CREATE INDEX IF NOT EXISTS idx_patients_phone ON patients(phone);
CREATE INDEX IF NOT EXISTS idx_appointments_doc_date ON appointments(doctor_id, appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_consultations_patient ON consultations(patient_id);
CREATE INDEX IF NOT EXISTS idx_admissions_bed_status ON admissions(bed_id, status);
CREATE INDEX IF NOT EXISTS idx_test_orders_status ON test_orders(status);
CREATE INDEX IF NOT EXISTS idx_bills_status ON bills(payment_status);

-- =============================================================================
-- 5 PRODUCTION DATABASE VIEWS (REQUIRED FOR REVIEW 2)
-- =============================================================================

-- VIEW 1: PATIENT LONGITUDINAL MEDICAL HISTORY
-- Consolidates patient profile, visits, doctor seen, primary diagnosis, and meds count
CREATE VIEW IF NOT EXISTS view_patient_history AS
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.dob,
    p.gender,
    p.blood_group,
    p.phone,
    a.appointment_id,
    a.appointment_date,
    a.start_time,
    d.first_name || ' ' || d.last_name AS doctor_name,
    dept.dept_name,
    c.consultation_id,
    c.symptoms,
    diag.diagnosis_name,
    diag.severity AS diagnosis_severity,
    COUNT(DISTINCT pi.item_id) AS medicines_prescribed_count,
    COUNT(DISTINCT tor.order_id) AS lab_tests_ordered_count
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN departments dept ON d.dept_id = dept.dept_id
LEFT JOIN consultations c ON a.appointment_id = c.appointment_id
LEFT JOIN diagnoses diag ON c.consultation_id = diag.consultation_id AND diag.diagnosis_type = 'PRIMARY'
LEFT JOIN prescriptions rx ON c.consultation_id = rx.consultation_id
LEFT JOIN prescription_items pi ON rx.prescription_id = pi.prescription_id
LEFT JOIN test_orders tor ON c.consultation_id = tor.consultation_id
GROUP BY p.patient_id, a.appointment_id, c.consultation_id, diag.diagnosis_id;

-- VIEW 2: DOCTOR SCHEDULES & ROSTER AVAILABILITY
-- Shows doctor shifts, weekly capacity, and booked vs available appointments
CREATE VIEW IF NOT EXISTS view_doctor_schedules AS
SELECT 
    d.doctor_id,
    d.first_name || ' ' || d.last_name AS doctor_name,
    dept.dept_name,
    d.specialization,
    ds.day_of_week,
    ds.start_time AS shift_start,
    ds.end_time AS shift_end,
    ds.slot_duration_mins,
    ds.max_patients AS daily_slot_capacity,
    COUNT(CASE WHEN a.status IN ('SCHEDULED', 'CONFIRMED') THEN 1 END) AS currently_booked_appointments,
    (ds.max_patients - COUNT(CASE WHEN a.status IN ('SCHEDULED', 'CONFIRMED') THEN 1 END)) AS available_slots_remaining
FROM doctors d
JOIN departments dept ON d.dept_id = dept.dept_id
JOIN doctor_schedules ds ON d.doctor_id = ds.doctor_id
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id 
    AND UPPER(STRFTIME('%w', a.appointment_date)) = CASE ds.day_of_week
        WHEN 'SUNDAY' THEN '0'
        WHEN 'MONDAY' THEN '1'
        WHEN 'TUESDAY' THEN '2'
        WHEN 'WEDNESDAY' THEN '3'
        WHEN 'THURSDAY' THEN '4'
        WHEN 'FRIDAY' THEN '5'
        WHEN 'SATURDAY' THEN '6'
    END
WHERE ds.is_active = 1
GROUP BY d.doctor_id, ds.schedule_id;

-- VIEW 3: PENDING DIAGNOSTIC TESTS & LAB TRACKER
-- Monitors test queue, sample collection status, and turnaround alerts
CREATE VIEW IF NOT EXISTS view_pending_tests AS
SELECT 
    tor.order_id,
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.phone AS patient_phone,
    lt.test_code,
    lt.test_name,
    lt.sample_type,
    lt.turnaround_hours,
    tor.order_date,
    tor.status AS test_status,
    dept.dept_name AS lab_department,
    d.first_name || ' ' || d.last_name AS requesting_doctor
FROM test_orders tor
JOIN lab_tests lt ON tor.test_id = lt.test_id
JOIN departments dept ON lt.dept_id = dept.dept_id
JOIN consultations c ON tor.consultation_id = c.consultation_id
JOIN patients p ON c.patient_id = p.patient_id
JOIN doctors d ON c.doctor_id = d.doctor_id
WHERE tor.status IN ('ORDERED', 'SAMPLE_COLLECTED', 'PROCESSING');

-- VIEW 4: WARD BED OCCUPANCY & INPATIENT CENSUS
-- Aggregates ward-level bed capacity, active occupants, vacancy, and occupancy rate
CREATE VIEW IF NOT EXISTS view_bed_occupancy AS
SELECT 
    w.ward_id,
    w.ward_name,
    w.ward_type,
    w.floor_number,
    dept.dept_name AS managing_dept,
    w.capacity AS total_ward_capacity,
    COUNT(b.bed_id) AS operational_beds_count,
    COUNT(CASE WHEN adm.status = 'ACTIVE' THEN 1 END) AS occupied_beds_count,
    (COUNT(b.bed_id) - COUNT(CASE WHEN adm.status = 'ACTIVE' THEN 1 END)) AS vacant_beds_count,
    ROUND(
        (COUNT(CASE WHEN adm.status = 'ACTIVE' THEN 1 END) * 100.0) / NULLIF(COUNT(b.bed_id), 0), 
        1
    ) AS occupancy_rate_percentage
FROM wards w
JOIN departments dept ON w.dept_id = dept.dept_id
LEFT JOIN beds b ON w.ward_id = b.ward_id AND b.is_operational = 1
LEFT JOIN admissions adm ON b.bed_id = adm.bed_id AND adm.status = 'ACTIVE'
GROUP BY w.ward_id;

-- VIEW 5: OUTSTANDING BILLS & REVENUE ANALYSIS
-- Summarizes financial positions, billed charges, collections, and pending balances
CREATE VIEW IF NOT EXISTS view_outstanding_bills_revenue AS
SELECT 
    b.bill_id,
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.phone AS patient_phone,
    b.bill_date,
    CASE 
        WHEN b.admission_id IS NOT NULL THEN 'INPATIENT'
        ELSE 'OUTPATIENT'
    END AS billing_category,
    b.total_amount AS gross_amount,
    b.discount_amount,
    b.tax_amount,
    b.net_payable,
    b.paid_amount,
    (b.net_payable - b.paid_amount) AS outstanding_balance,
    b.payment_status
FROM bills b
JOIN patients p ON b.patient_id = p.patient_id;
