#!/usr/bin/env python3
"""
=============================================================================
HOSPITAL APPOINTMENT & PATIENT CARE MANAGEMENT SYSTEM
DBMS Project - Review 3 Final Application & Working Prototype
=============================================================================
Features:
- Pure Python Standard Library (zero external pip dependencies required)
- Interactive Modern Web Interface (Dashboard, CRUD, Validations, Reports)
- Terminal CLI Mode (python3 app.py --cli)
- Full Relational Database Engine with 3NF Schema, Triggers & Views
=============================================================================
"""

import sys
import os
import sqlite3
import json
import urllib.parse
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Resolve base directory relative to this script file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "hospital_review2.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

EMBEDDED_SCHEMA_SQL = """-- =============================================================================
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
"""

EMBEDDED_SAMPLE_DATA_SQL = """-- =============================================================================
-- SAMPLE DATA SCRIPT FOR HOSPITAL APPOINTMENT & PATIENT CARE SYSTEM
-- DBMS Project - Review 2 Dataset
-- Realistic, clinically coherent, and relational constraint-compliant
-- =============================================================================

-- 1. DEPARTMENTS
INSERT INTO departments (dept_id, dept_name, building_block, floor_number, contact_ext) VALUES
(1, 'Cardiology', 'Block A - Heart Center', 2, '2101'),
(2, 'Neurology', 'Block A - Neuroscience', 3, '2102'),
(3, 'Orthopedics & Joint Care', 'Block B - Surgical Wing', 1, '2201'),
(4, 'General Medicine & Diabetology', 'Block B - OPD Plaza', 1, '2202'),
(5, 'Pediatrics & Neonatology', 'Block C - Mother & Child', 2, '2301'),
(6, 'Diagnostic Pathology & Radiology', 'Block D - Diagnostics', 0, '2401');

-- 2. DOCTORS
INSERT INTO doctors (doctor_id, dept_id, first_name, last_name, qualification, specialization, email, phone, consultation_fee, license_number, status) VALUES
(1, 1, 'Aarav', 'Sharma', 'MD, DM (Cardiology), FACC', 'Interventional Cardiology', 'aarav.sharma@hospital.org', '+91 98765 43210', 800.00, 'MCI-CARD-0891', 'ACTIVE'),
(2, 1, 'Priya', 'Nair', 'MD, DNB (Cardiology)', 'Non-Invasive Cardiology', 'priya.nair@hospital.org', '+91 98765 43211', 750.00, 'MCI-CARD-0942', 'ACTIVE'),
(3, 2, 'Vikram', 'Mehta', 'MD, DM (Neurology)', 'Stroke & Epilepsy Care', 'vikram.mehta@hospital.org', '+91 98765 43212', 900.00, 'MCI-NEUR-1102', 'ACTIVE'),
(4, 2, 'Ananya', 'Deshmukh', 'MCh (Neurosurgery)', 'Cranial & Spinal Surgery', 'ananya.deshmukh@hospital.org', '+91 98765 43213', 1000.00, 'MCI-NEUR-1145', 'ACTIVE'),
(5, 3, 'Rajesh', 'Iyer', 'MS (Ortho), MCh (Joint Repl)', 'Arthroplasty & Trauma', 'rajesh.iyer@hospital.org', '+91 98765 43214', 700.00, 'MCI-ORTH-2041', 'ACTIVE'),
(6, 3, 'Sneha', 'Patel', 'MS (Ortho), Fellowship Sports Med', 'Arthroscopy & Sports Injury', 'sneha.patel@hospital.org', '+91 98765 43215', 650.00, 'MCI-ORTH-2089', 'ACTIVE'),
(7, 4, 'Sunil', 'Verma', 'MD (Internal Medicine)', 'Metabolic Disorders & Hypertension', 'sunil.verma@hospital.org', '+91 98765 43216', 500.00, 'MCI-GMED-3011', 'ACTIVE'),
(8, 4, 'Kavita', 'Rao', 'MD, Fellowship Diabetology', 'Comprehensive Diabetes Care', 'kavita.rao@hospital.org', '+91 98765 43217', 550.00, 'MCI-GMED-3054', 'ACTIVE'),
(9, 5, 'Rohan', 'Kulkarni', 'MD (Pediatrics), DCH', 'General Pediatrics & Vaccine', 'rohan.kulkarni@hospital.org', '+91 98765 43218', 600.00, 'MCI-PEDI-4012', 'ACTIVE'),
(10, 5, 'Meera', 'Sen', 'MD (Pediatrics), DM (Neonatology)', 'Critical Neonatal Intensive Care', 'meera.sen@hospital.org', '+91 98765 43219', 850.00, 'MCI-PEDI-4078', 'ACTIVE'),
(11, 6, 'Deepak', 'Kapoor', 'MD (Pathology)', 'Histopathology & Hematology', 'deepak.kapoor@hospital.org', '+91 98765 43220', 400.00, 'MCI-PATH-5014', 'ACTIVE'),
(12, 6, 'Aditi', 'Bose', 'MD (Radiodiagnosis)', 'Cross-Sectional Imaging & MRI', 'aditi.bose@hospital.org', '+91 98765 43221', 600.00, 'MCI-RADI-5092', 'ACTIVE');

-- Update Department Heads
UPDATE departments SET head_doctor_id = 1 WHERE dept_id = 1;
UPDATE departments SET head_doctor_id = 3 WHERE dept_id = 2;
UPDATE departments SET head_doctor_id = 5 WHERE dept_id = 3;
UPDATE departments SET head_doctor_id = 7 WHERE dept_id = 4;
UPDATE departments SET head_doctor_id = 9 WHERE dept_id = 5;
UPDATE departments SET head_doctor_id = 11 WHERE dept_id = 6;

-- 3. DOCTOR SCHEDULES
INSERT INTO doctor_schedules (schedule_id, doctor_id, day_of_week, start_time, end_time, slot_duration_mins, max_patients, is_active) VALUES
(1, 1, 'MONDAY', '09:00:00', '13:00:00', 20, 12, 1),
(2, 1, 'WEDNESDAY', '09:00:00', '13:00:00', 20, 12, 1),
(3, 2, 'TUESDAY', '14:00:00', '18:00:00', 20, 12, 1),
(4, 3, 'MONDAY', '10:00:00', '14:00:00', 30, 8, 1),
(5, 4, 'THURSDAY', '11:00:00', '15:00:00', 30, 8, 1),
(6, 5, 'MONDAY', '09:00:00', '13:00:00', 15, 16, 1),
(7, 5, 'FRIDAY', '09:00:00', '13:00:00', 15, 16, 1),
(8, 7, 'MONDAY', '08:30:00', '12:30:00', 15, 16, 1),
(9, 7, 'WEDNESDAY', '08:30:00', '12:30:00', 15, 16, 1),
(10, 8, 'TUESDAY', '09:00:00', '13:00:00', 20, 12, 1),
(11, 9, 'MONDAY', '10:00:00', '14:00:00', 15, 16, 1),
(12, 10, 'SATURDAY', '09:00:00', '13:00:00', 20, 12, 1);

-- 4. PATIENTS
INSERT INTO patients (patient_id, first_name, last_name, dob, gender, blood_group, phone, email, address, emergency_contact_name, emergency_contact_phone, registration_date) VALUES
(1, 'Ramesh', 'Gupta', '1968-04-12', 'MALE', 'B+', '+91 91234 56780', 'ramesh.gupta@email.com', 'Flat 402, Lotus Towers, Pune', 'Sunita Gupta', '+91 91234 56789', '2026-01-10'),
(2, 'Sunita', 'Joshi', '1982-11-23', 'FEMALE', 'O+', '+91 91234 56781', 'sunita.j@email.com', 'B-14, Green Park Society, Mumbai', 'Nitin Joshi', '+91 91234 56788', '2026-01-15'),
(3, 'Amit', 'Chopra', '1975-06-18', 'MALE', 'A+', '+91 91234 56782', 'amit.chopra@email.com', 'Row House 5, Baner, Pune', 'Pooja Chopra', '+91 91234 56787', '2026-01-20'),
(4, 'Deepa', 'Nambiar', '1990-09-05', 'FEMALE', 'AB+', '+91 91234 56783', 'deepa.nambiar@email.com', 'A-301, Lake Vista, Thane', 'Harish Nambiar', '+91 91234 56786', '2026-02-01'),
(5, 'Karthik', 'Reddy', '1985-02-14', 'MALE', 'O-', '+91 91234 56784', 'karthik.reddy@email.com', 'Plot 88, Jubilee Enclave, Hyderabad', 'Swati Reddy', '+91 91234 56785', '2026-02-05'),
(6, 'Geeta', 'Bhat', '1955-08-30', 'FEMALE', 'A-', '+91 92345 67890', 'geeta.bhat@email.com', '12/C, Ashoka Nagar, Bengaluru', 'Vinod Bhat', '+91 92345 67899', '2026-02-10'),
(7, 'Mohit', 'Agarwal', '2001-12-03', 'MALE', 'B-', '+91 92345 67891', 'mohit.a@email.com', 'C-102, Silver Oak, Pune', 'Sanjay Agarwal', '+91 92345 67898', '2026-02-15'),
(8, 'Tanvi', 'Kaur', '1995-07-22', 'FEMALE', 'O+', '+91 92345 67892', 'tanvi.kaur@email.com', 'D-55, Defense Colony, New Delhi', 'Gurpreet Kaur', '+91 92345 67897', '2026-02-20'),
(9, 'Vijay', 'Malhotra', '1962-03-15', 'MALE', 'AB-', '+91 92345 67893', 'vijay.m@email.com', 'Villa 7, Palm Grove, Gurgaon', 'Neelam Malhotra', '+91 92345 67896', '2026-03-01'),
(10, 'Aarohi', 'Kulkarni', '2020-05-10', 'FEMALE', 'B+', '+91 92345 67894', 'parent.kulkarni@email.com', 'Flat 101, Sai Krupa, Pune', 'Sachin Kulkarni', '+91 92345 67895', '2026-03-05');

-- 5. APPOINTMENTS
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, start_time, end_time, status, reason) VALUES
(1, 1, 1, '2026-03-10', '09:00:00', '09:20:00', 'COMPLETED', 'Exertional chest heaviness and palpitations'),
(2, 2, 7, '2026-03-10', '09:00:00', '09:15:00', 'COMPLETED', 'High fasting blood glucose and fatigue'),
(3, 3, 5, '2026-03-10', '09:30:00', '09:45:00', 'COMPLETED', 'Chronic right knee swelling and osteoarthritic pain'),
(4, 4, 3, '2026-03-10', '10:30:00', '11:00:00', 'COMPLETED', 'Recurrent unilateral throbbing migraine with aura'),
(5, 5, 1, '2026-03-10', '09:40:00', '10:00:00', 'COMPLETED', 'Pre-operative cardiac clearance for elective hernia'),
(6, 6, 7, '2026-03-10', '10:00:00', '10:15:00', 'COMPLETED', 'Refractory systolic hypertension follow-up'),
(7, 7, 6, '2026-03-11', '10:00:00', '10:15:00', 'COMPLETED', 'Acute lateral ankle twist during football match'),
(8, 8, 8, '2026-03-11', '10:00:00', '10:20:00', 'COMPLETED', 'Gestational diabetes evaluation week 24'),
(9, 9, 1, '2026-03-12', '10:30:00', '10:50:00', 'COMPLETED', 'Post-PTCA stent 6-month surveillance'),
(10, 10, 9, '2026-03-12', '11:00:00', '11:15:00', 'COMPLETED', 'High-grade viral fever with dry cough in child'),
(11, 1, 1, '2026-10-10', '09:00:00', '09:20:00', 'SCHEDULED', 'Follow-up ECG and lipid review'),
(12, 2, 8, '2026-10-10', '09:30:00', '09:50:00', 'SCHEDULED', 'Quarterly HbA1c review and insulin dose titration'),
(13, 3, 5, '2026-10-12', '10:00:00', '10:15:00', 'CONFIRMED', 'Pre-admission total knee arthroplasty workup'),
(14, 4, 3, '2026-10-12', '11:00:00', '11:30:00', 'SCHEDULED', 'Review EEG report and prophylactic topiramate review'),
(15, 6, 7, '2026-10-15', '09:00:00', '09:15:00', 'CONFIRMED', 'Serum creatinine and ACE inhibitor dosage review');

-- 6. CONSULTATIONS
INSERT INTO consultations (consultation_id, appointment_id, doctor_id, patient_id, consultation_timestamp, symptoms, physical_examination, clinical_notes, follow_up_date) VALUES
(1, 1, 1, 1, '2026-03-10 09:25:00', 'Chest tight pressure radiating to left jaw on brisk walking for 2 weeks.', 'BP 150/94 mmHg, Pulse 82 bpm regular, S1/S2 heard, no murmurs.', 'Suspected unstable angina. Advised urgent admission for angiography.', '2026-03-17'),
(2, 2, 7, 2, '2026-03-10 09:20:00', 'Polydipsia, polyuria, unexplained weight loss of 3kg over a month.', 'BMI 28.4 kg/m2, BP 128/82 mmHg, systemic exam unremarkable.', 'Uncontrolled Type 2 Diabetes Mellitus with borderline dyslipidemia.', '2026-04-10'),
(3, 3, 5, 3, '2026-03-10 09:50:00', 'Severe pain walking upstairs, crepitus in right knee, morning stiffness 20 min.', 'Bilateral knee joint line tenderness, restricted terminal flexion to 110 deg.', 'Grade III Osteoarthritis right knee joint. Advised bilateral X-ray.', '2026-03-24'),
(4, 4, 3, 4, '2026-03-10 11:05:00', 'Severe pulsating hemicranial headache with photophobia and nausea.', 'Fundus normal, cranial nerves II-XII intact, no meningeal signs.', 'Chronic episodic migraine with visual aura.', '2026-04-07'),
(5, 5, 1, 5, '2026-03-10 10:05:00', 'Pre-operative fitness assessment; asymptomatic.', 'BP 122/78 mmHg, ECG normal sinus rhythm, cardiovascular normal.', 'Cardiac clearance granted for elective umbilical hernia repair.', NULL),
(6, 6, 7, 6, '2026-03-10 10:20:00', 'Headache upon waking, bilateral ankle swelling.', 'BP 164/98 mmHg, mild pedal edema grade 1+ bilaterally.', 'Stage 2 Essential Hypertension with sodium-sensitive fluid retention.', '2026-03-20'),
(7, 7, 6, 7, '2026-03-11 10:20:00', 'Inversion injury to right ankle while playing sports; painful weightbearing.', 'Marked lateral malleolus swelling and ecchymosis; anterior drawer negative.', 'Grade II Anterior Talofibular Ligament sprain.', '2026-03-25'),
(8, 8, 8, 8, '2026-03-11 10:25:00', '24 weeks gravid, fasting glucose 110 mg/dL reported from outside lab.', 'Fundal height corresponds to dates, fetal heart sounds present.', 'Gestational Diabetes Mellitus. Started medical nutrition therapy.', '2026-03-18'),
(9, 9, 1, 9, '2026-03-12 10:55:00', 'Review visit; asymptomatic, walking 4 km daily.', 'BP 118/74 mmHg, Heart rate 64 bpm.', 'Post-coronary stenting 6-month status stable. Dual antiplatelets continued.', '2026-06-12'),
(10, 10, 9, 10, '2026-03-12 11:20:00', 'Fever up to 102 F for 2 days, poor oral intake, irritable.', 'Throat hyperemic, tonsils grade 2 enlarged with exudates, chest clear.', 'Acute streptococcal pharyngotonsillitis.', '2026-03-16');

-- 7. DIAGNOSES
INSERT INTO diagnoses (diagnosis_id, consultation_id, icd10_code, diagnosis_name, severity, diagnosis_type, remarks) VALUES
(1, 1, 'I20.0', 'Unstable Angina Pectoris', 'CRITICAL', 'PRIMARY', 'High risk of acute myocardial infarction; urgent inpatient cath lab referral'),
(2, 2, 'E11.9', 'Type 2 Diabetes Mellitus without complications', 'MODERATE', 'PRIMARY', 'Target HbA1c < 6.5%'),
(3, 3, 'M17.1', 'Primary Osteoarthritis of Right Knee', 'SEVERE', 'PRIMARY', 'Functional impairment present'),
(4, 4, 'G43.1', 'Migraine with Aura', 'MODERATE', 'PRIMARY', 'Abortive therapy initiated'),
(5, 5, 'Z01.810', 'Preoperative Cardiovascular Examination', 'MILD', 'PRIMARY', 'Normal hemodynamic status'),
(6, 6, 'I10', 'Essential (Primary) Hypertension', 'SEVERE', 'PRIMARY', 'Inadequate current titration'),
(7, 7, 'S93.4', 'Sprain of Calcaneofibular / Talofibular Ligament', 'MODERATE', 'PRIMARY', 'Immobilization via pneumatic walker boot'),
(8, 8, 'O24.4', 'Gestational Diabetes Mellitus in Pregnancy', 'MODERATE', 'PRIMARY', 'Dietary monitoring and glucose diary required'),
(9, 9, 'Z95.5', 'Presence of Coronary Angioplasty Implant and Stent', 'MILD', 'PRIMARY', 'Optimal graft patency maintained'),
(10, 10, 'J03.0', 'Streptococcal Tonsillitis', 'MODERATE', 'PRIMARY', 'Oral antibiotics prescribed for 7 days');

-- 8. PRESCRIPTIONS & ITEMS
INSERT INTO prescriptions (prescription_id, consultation_id, prescription_date, general_advice) VALUES
(1, 1, '2026-03-10', 'Complete bed rest. Avoid strenuous exertion. Proceed directly to emergency room if pain recurs.'),
(2, 2, '2026-03-10', 'Low glycemic index diabetic diet. 30 min daily brisk walking. Monitor fasting glucose twice weekly.'),
(3, 3, '2026-03-10', 'Quadriceps strengthening exercises. Cold packs twice daily. Avoid squatting and cross-legged sitting.'),
(4, 4, '2026-03-10', 'Maintain regular sleep schedule. Keep a migraine trigger diary (avoid aged cheeses and caffeine withdrawal).'),
(5, 6, '2026-03-10', 'Strict low-sodium DASH diet (< 2g salt/day). Monitor morning and evening blood pressure log.'),
(6, 10, '2026-03-12', 'Frequent warm saline sips. High oral fluid hydration. Rest for 3 days.');

INSERT INTO prescription_items (item_id, prescription_id, medicine_name, dosage, frequency, duration_days, quantity, instructions) VALUES
(1, 1, 'Tablet Sorbitrate (Isosorbide Dinitrate)', '5mg', 'Sublingually SOS for chest pain', 14, 10, 'Dissolve under tongue if chest tightness starts'),
(2, 1, 'Tablet Ecosprin (Aspirin)', '150mg', '1-0-0 After breakfast', 30, 30, 'Take after heavy food'),
(3, 1, 'Tablet Atorvastatin', '40mg', '0-0-1 At bedtime', 30, 30, 'Take post-dinner'),
(4, 2, 'Tablet Metformin ER', '500mg', '1-0-1 Before meals', 30, 60, 'Swallow whole with a glass of water'),
(5, 2, 'Tablet Teneligliptin', '20mg', '1-0-0 Before breakfast', 30, 30, 'Take 15 min before first meal'),
(6, 3, 'Tablet Paracetamol ER', '1000mg', '1-0-1 After meals', 7, 14, 'Take for pain as directed'),
(7, 3, 'Diacerein & Glucosamine Capsules', '50mg/750mg', '1-0-0 After food', 30, 30, 'Nutraceutical joint supplement'),
(8, 4, 'Tablet Rizatriptan', '10mg', '1 stat at onset of migraine', 10, 5, 'Max 2 tablets in 24 hours'),
(9, 4, 'Tablet Propranolol TR', '40mg', '1-0-0 Morning', 30, 30, 'Migraine prophylaxis; do not stop abruptly'),
(10, 5, 'Tablet Telmisartan + Amlodipine', '40mg/5mg', '1-0-0 Morning', 30, 30, 'Take early morning with water'),
(11, 6, 'Syrup Amoxicillin + Clavulanic Acid (228.5mg/5ml)', '5ml', '1-0-1 After food', 7, 1, 'Complete entire 7-day course even if fever abates'),
(12, 6, 'Syrup Paracetamol (250mg/5ml)', '6ml', 'SOS Every 6 hours for fever > 100.5 F', 5, 1, 'Do not exceed 4 doses per day');

-- 9. LAB TESTS CATALOG
INSERT INTO lab_tests (test_id, dept_id, test_name, test_code, standard_cost, sample_type, turnaround_hours) VALUES
(1, 6, 'Comprehensive Metabolic Panel (CMP)', 'CMP-101', 850.00, 'Serum Blood', 6),
(2, 6, 'Complete Blood Count (CBC) with Differential', 'CBC-102', 350.00, 'Whole Blood EDTA', 4),
(3, 6, 'Fasting Blood Glucose & HbA1c Glycated Hemoglobin', 'DIA-201', 600.00, 'Sodium Fluoride Plasma & Whole Blood', 4),
(4, 6, 'Lipid Profile Comprehensive', 'LIP-202', 750.00, 'Serum Blood', 6),
(5, 6, 'High-Sensitivity Cardiac Troponin-I (hs-cTnI)', 'TRO-301', 1200.00, 'Heparinized Plasma', 2),
(6, 6, '12-Lead Electrocardiogram (ECG)', 'ECG-302', 400.00, 'Electrophysiological Trace', 1),
(7, 6, 'Digital X-Ray Right Knee (AP & Lateral Weight-bearing)', 'XRY-401', 900.00, 'Ionizing Radiation Radiograph', 2),
(8, 6, 'Brain MRI with Contrast 3.0T', 'MRI-501', 6500.00, 'Magnetic Resonance Imaging', 12),
(9, 6, 'Digital Chest X-Ray PA View', 'XRY-402', 500.00, 'Radiograph', 2),
(10, 6, 'Urine Routine & Microscopic Examination', 'URN-103', 250.00, 'Clean Catch Midstream Urine', 3);

-- 9b. TEST ORDERS
INSERT INTO test_orders (order_id, consultation_id, test_id, order_date, status, result_value, reference_range, result_date, lab_technician_notes) VALUES
(1, 1, 5, '2026-03-10 09:30:00', 'COMPLETED', '48.6 ng/L (ELEVATED)', '< 14.0 ng/L', '2026-03-10 11:00:00', 'Critical alert communicated immediately to Dr. Aarav Sharma.'),
(2, 1, 6, '2026-03-10 09:30:00', 'COMPLETED', 'ST-segment depression 1.5mm in V4-V6 with T-wave inversion', 'Normal sinus rhythm', '2026-03-10 10:00:00', 'Ischemic changes observed in anterolateral leads.'),
(3, 2, 3, '2026-03-10 09:25:00', 'COMPLETED', 'Fasting: 168 mg/dL; HbA1c: 8.9%', 'Fasting: 70-99 mg/dL; HbA1c: < 5.7%', '2026-03-10 13:00:00', 'Markedly elevated glycemic index.'),
(4, 2, 4, '2026-03-10 09:25:00', 'COMPLETED', 'Total Chol: 232 mg/dL; LDL: 154 mg/dL; Trig: 198 mg/dL', 'Total: < 200; LDL: < 100; Trig: < 150', '2026-03-10 13:00:00', 'Atherogenic lipid profile.'),
(5, 3, 7, '2026-03-10 09:55:00', 'COMPLETED', 'Marked medial joint space narrowing, subchondral sclerosis, osteophytes', 'Normal articular spacing', '2026-03-10 11:30:00', 'Kellgren-Lawrence Grade 3 findings confirmed.'),
(6, 4, 8, '2026-03-10 11:15:00', 'COMPLETED', 'No acute intracranial hemorrhage, mass lesion, or midline shift', 'Normal intracranial parenchyma', '2026-03-11 09:00:00', 'Normal scan; organic intracranial pathology excluded.'),
(7, 6, 1, '2026-03-10 10:25:00', 'COMPLETED', 'Serum Creatinine: 1.1 mg/dL; Potassium: 4.4 mEq/L', 'Creatinine: 0.7-1.3; K+: 3.5-5.0', '2026-03-10 14:00:00', 'Renal functional parameters preserved.'),
(8, 1, 4, '2026-10-04 14:00:00', 'PROCESSING', NULL, 'Total: < 200 mg/dL', NULL, 'Sample in centrifuge.'),
(9, 2, 10, '2026-10-05 08:30:00', 'ORDERED', NULL, 'Nil protein, nil sugar', NULL, 'Awaiting sample collection at counter 3.'),
(10, 6, 2, '2026-10-05 09:00:00', 'SAMPLE_COLLECTED', NULL, 'Hb: 12-16 g/dL; TLC: 4000-11000', NULL, 'Barcoded EDTA tube delivered to automated hematology analyzer.');

-- 10. WARDS
INSERT INTO wards (ward_id, dept_id, ward_name, ward_type, floor_number, capacity) VALUES
(1, 1, 'Cardiac Care Intensive Unit (ICU)', 'ICU', 2, 4),
(2, 3, 'Orthopedic Inpatient Wing', 'GENERAL', 1, 6),
(3, 4, 'Internal Medicine Male Ward', 'GENERAL', 2, 8),
(4, 4, 'Executive Single Deluxe Suites', 'PRIVATE', 3, 4),
(5, 5, 'Pediatric Observation Ward', 'GENERAL', 2, 4);

-- 11. BEDS
INSERT INTO beds (bed_id, ward_id, bed_number, daily_rate, is_operational) VALUES
-- Ward 1 (ICU)
(1, 1, 'ICU-BED-01', 5000.00, 1),
(2, 1, 'ICU-BED-02', 5000.00, 1),
(3, 1, 'ICU-BED-03', 5000.00, 1),
(4, 1, 'ICU-BED-04', 5000.00, 1),
-- Ward 2 (Ortho)
(5, 2, 'ORTHO-G-01', 1200.00, 1),
(6, 2, 'ORTHO-G-02', 1200.00, 1),
(7, 2, 'ORTHO-G-03', 1200.00, 1),
(8, 2, 'ORTHO-G-04', 1200.00, 1),
(9, 2, 'ORTHO-G-05', 1200.00, 1),
(10, 2, 'ORTHO-G-06', 1200.00, 1),
-- Ward 3 (General Med)
(11, 3, 'MED-M-01', 1000.00, 1),
(12, 3, 'MED-M-02', 1000.00, 1),
(13, 3, 'MED-M-03', 1000.00, 1),
(14, 3, 'MED-M-04', 1000.00, 1),
(15, 3, 'MED-M-05', 1000.00, 1),
-- Ward 4 (Private)
(16, 4, 'PVT-STE-101', 3500.00, 1),
(17, 4, 'PVT-STE-102', 3500.00, 1),
(18, 4, 'PVT-STE-103', 3500.00, 1),
(19, 4, 'PVT-STE-104', 3500.00, 1),
-- Ward 5 (Pediatrics)
(20, 5, 'PED-OBS-01', 1100.00, 1),
(21, 5, 'PED-OBS-02', 1100.00, 1);

-- 12. ADMISSIONS (Enforcing valid dates and single active patient per bed)
INSERT INTO admissions (admission_id, patient_id, bed_id, admitting_doctor_id, admission_date, discharge_date, admission_reason, discharge_summary, status) VALUES
-- Past Discharged Inpatients
(1, 9, 1, 1, '2026-02-01 08:00:00', '2026-02-04 16:00:00', 'Acute Coronary Syndrome for emergency stent placement', 'Coronary drug-eluting stent successfully deployed in LAD. Hemodynamically stable at discharge.', 'DISCHARGED'),
(2, 3, 5, 5, '2026-02-10 10:00:00', '2026-02-14 11:30:00', 'Left knee arthroscopic partial meniscectomy', 'Successful minimally invasive repair. Mobilizing with walker.', 'DISCHARGED'),
(3, 7, 6, 6, '2026-02-18 14:00:00', '2026-02-20 10:00:00', 'Severe ankle syndesmotic disruption closed reduction', 'Immobilization cast placed. Swelling subsided.', 'DISCHARGED'),
-- Current ACTIVE Inpatients (Only 1 active patient per unique bed_id)
(4, 1, 1, 1, '2026-03-10 11:30:00', NULL, 'Critical Unstable Angina with positive cardiac biomarkers for invasive angiography', NULL, 'ACTIVE'),
(5, 6, 11, 7, '2026-03-10 12:00:00', NULL, 'Hypertensive urgency with bilateral lower limb congestive edema', NULL, 'ACTIVE'),
(6, 4, 16, 3, '2026-03-11 08:00:00', NULL, 'Status Migrainosus refractory to oral triptans for IV DHE therapy', NULL, 'ACTIVE'),
(7, 10, 20, 9, '2026-03-12 12:30:00', NULL, 'Severe dehydration secondary to acute febrile illness requiring IV fluids', NULL, 'ACTIVE');

-- 13. BILLS (Initially inserted with paid_amount=0.00; trigger trg_update_bill_on_payment updates paid_amount and status)
INSERT INTO bills (bill_id, patient_id, consultation_id, admission_id, bill_date, total_amount, discount_amount, tax_amount, net_payable, paid_amount, payment_status) VALUES
-- Outpatient Consultation Bills
(1, 1, 1, NULL, '2026-03-10 09:30:00', 800.00, 0.00, 0.00, 800.00, 0.00, 'UNPAID'),
(2, 2, 2, NULL, '2026-03-10 09:25:00', 500.00, 50.00, 0.00, 450.00, 0.00, 'UNPAID'),
(3, 3, 3, NULL, '2026-03-10 09:55:00', 700.00, 0.00, 0.00, 700.00, 0.00, 'UNPAID'),
(4, 4, 4, NULL, '2026-03-10 11:10:00', 900.00, 0.00, 0.00, 900.00, 0.00, 'UNPAID'),
(5, 6, 6, NULL, '2026-03-10 10:25:00', 500.00, 0.00, 0.00, 500.00, 0.00, 'UNPAID'),
(6, 7, 7, NULL, '2026-03-11 10:25:00', 650.00, 0.00, 0.00, 650.00, 0.00, 'UNPAID'),
(7, 10, 10, NULL, '2026-03-12 11:25:00', 600.00, 0.00, 0.00, 600.00, 0.00, 'UNPAID'),
-- Past Inpatient Bills
(8, 9, NULL, 1, '2026-02-04 16:30:00', 85000.00, 5000.00, 4000.00, 84000.00, 0.00, 'UNPAID'),
(9, 3, NULL, 2, '2026-02-14 12:00:00', 42000.00, 2000.00, 2000.00, 42000.00, 0.00, 'UNPAID'),
-- Active Inpatient Interim Bills
(10, 1, NULL, 4, '2026-03-11 10:00:00', 35000.00, 0.00, 1750.00, 36750.00, 0.00, 'UNPAID'),
(11, 6, NULL, 5, '2026-03-11 11:00:00', 12000.00, 0.00, 600.00, 12600.00, 0.00, 'UNPAID'),
(12, 4, NULL, 6, '2026-03-12 09:00:00', 15000.00, 500.00, 725.00, 15225.00, 0.00, 'UNPAID');

-- 14. PAYMENTS
INSERT INTO payments (payment_id, bill_id, payment_timestamp, amount_paid, payment_method, transaction_ref, received_by, remarks) VALUES
(1, 1, '2026-03-10 09:32:00', 800.00, 'UPI', 'UPI-TXN-98410291', 'Frontdesk_Aakash', 'Settled via GooglePay QR'),
(2, 2, '2026-03-10 09:28:00', 450.00, 'CASH', 'CSH-REC-001091', 'Frontdesk_Aakash', 'Cash received with senior citizen discount'),
(3, 3, '2026-03-10 09:58:00', 700.00, 'DEBIT_CARD', 'POS-HDFC-8812', 'Frontdesk_Kavya', 'Card approved batch 201'),
(4, 4, '2026-03-10 11:12:00', 900.00, 'CREDIT_CARD', 'POS-ICICI-4491', 'Frontdesk_Kavya', 'Mastercard swipe'),
(5, 5, '2026-03-10 10:28:00', 500.00, 'UPI', 'UPI-TXN-11029381', 'Frontdesk_Aakash', 'PhonePe payment'),
(6, 6, '2026-03-11 10:28:00', 650.00, 'UPI', 'UPI-TXN-55910284', 'Frontdesk_Aakash', 'Instant transfer'),
(7, 7, '2026-03-12 11:28:00', 600.00, 'CASH', 'CSH-REC-001142', 'Frontdesk_Kavya', 'Cash payment'),
(8, 8, '2026-02-04 16:35:00', 84000.00, 'INSURANCE', 'TPA-STAR-CLM-8819', 'Cashier_Rakesh', 'Star Health Insurance cashless pre-auth settled'),
(9, 9, '2026-02-14 12:05:00', 42000.00, 'NET_BANKING', 'NEFT-AXIS-99210', 'Cashier_Rakesh', 'Direct NEFT transfer'),
(10, 10, '2026-03-11 10:05:00', 20000.00, 'CREDIT_CARD', 'POS-SBI-99120', 'Cashier_Rakesh', 'Initial inpatient deposit for cath lab admission'),
(11, 11, '2026-03-11 11:05:00', 5000.00, 'UPI', 'UPI-TXN-99881122', 'Cashier_Rakesh', 'Inpatient admission advance deposit');
"""

def init_database():
    """Ensure database schema, triggers, sample data, and views are present."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if doctors table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='doctors';")
    if not cursor.fetchone():
        print(f"[INIT] Initializing database at: {DB_FILE}")
        
        schema_path = os.path.join(BASE_DIR, "schema_review2.sql")
        if not os.path.exists(schema_path):
            schema_path = "schema_review2.sql"
            
        sample_path = os.path.join(BASE_DIR, "sample_data_review2.sql")
        if not os.path.exists(sample_path):
            sample_path = "sample_data_review2.sql"

        if os.path.exists(schema_path):
            print(f"[INIT] Loading schema from: {schema_path}")
            with open(schema_path, "r") as f:
                cursor.executescript(f.read())
        else:
            print("[INIT] Loading built-in 3NF relational schema, views, and triggers...")
            cursor.executescript(EMBEDDED_SCHEMA_SQL)

        if os.path.exists(sample_path):
            print(f"[INIT] Loading sample data from: {sample_path}")
            with open(sample_path, "r") as f:
                cursor.executescript(f.read())
        else:
            print("[INIT] Loading built-in clinical sample dataset...")
            cursor.executescript(EMBEDDED_SAMPLE_DATA_SQL)

        conn.commit()
        print("[INIT] Database initialized successfully.")
    conn.close()

# =============================================================================
# CLI PROTOTYPE MODE
# =============================================================================
def run_cli():
    init_database()
    print("\n" + "="*70)
    print(" HOSPITAL MANAGEMENT SYSTEM — REVIEW 3 TERMINAL PROTOTYPE")
    print("="*70)
    
    while True:
        print("\nMAIN MENU:")
        print("1. Search & View Patients")
        print("2. Register New Patient")
        print("3. View Doctor Schedules & Free Slots")
        print("4. Book Appointment (With Overlap Collision Check)")
        print("5. Ward Bed Census & Inpatient Allocation")
        print("6. Admit Inpatient (With 1-Active-Patient-Per-Bed Check)")
        print("7. Billing & Payment Settlement")
        print("8. View 5 Production Analytical Views")
        print("9. Launch Web Dashboard (Browser GUI)")
        print("0. Exit")
        
        choice = input("\nEnter choice [0-9]: ").strip()
        conn = get_db_connection()
        cur = conn.cursor()
        
        if choice == "1":
            q = input("Enter Patient Name or Phone (or press Enter for all): ").strip()
            if q:
                cur.execute("SELECT patient_id, first_name, last_name, dob, gender, blood_group, phone FROM patients WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ?", (f"%{q}%", f"%{q}%", f"%{q}%"))
            else:
                cur.execute("SELECT patient_id, first_name, last_name, dob, gender, blood_group, phone FROM patients LIMIT 10")
            rows = cur.fetchall()
            print(f"\nFound {len(rows)} patient(s):")
            print(f"{'ID':<4} | {'Name':<22} | {'DOB':<10} | {'Gender':<7} | {'Blood':<5} | {'Phone'}")
            print("-" * 65)
            for r in rows:
                name = f"{r['first_name']} {r['last_name']}"
                print(f"{r['patient_id']:<4} | {name:<22} | {r['dob']:<10} | {r['gender']:<7} | {r['blood_group'] or 'N/A':<5} | {r['phone']}")

        elif choice == "2":
            print("\nREGISTER NEW PATIENT:")
            fn = input("First Name: ").strip()
            ln = input("Last Name: ").strip()
            dob = input("DOB (YYYY-MM-DD): ").strip()
            gender = input("Gender (MALE/FEMALE/OTHER): ").strip().upper()
            bg = input("Blood Group (e.g. O+, B+, A-): ").strip().upper()
            phone = input("Phone Number: ").strip()
            addr = input("Address: ").strip()
            ec_name = input("Emergency Contact Name: ").strip()
            ec_phone = input("Emergency Contact Phone: ").strip()
            try:
                cur.execute("""
                    INSERT INTO patients (first_name, last_name, dob, gender, blood_group, phone, address, emergency_contact_name, emergency_contact_phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (fn, ln, dob, gender, bg, phone, addr, ec_name, ec_phone))
                conn.commit()
                print(f"SUCCESS: Patient registered with ID: {cur.lastrowid}")
            except Exception as e:
                print(f"ERROR: {e}")

        elif choice == "3":
            cur.execute("""
                SELECT doctor_name, dept_name, day_of_week, shift_start, shift_end, daily_slot_capacity, available_slots_remaining
                FROM view_doctor_schedules
                ORDER BY dept_name, day_of_week
            """)
            rows = cur.fetchall()
            print(f"\n{'Doctor':<18} | {'Department':<22} | {'Day':<9} | {'Shift':<17} | {'Avail Slots'}")
            print("-" * 80)
            for r in rows:
                shift = f"{r['shift_start'][:5]} - {r['shift_end'][:5]}"
                print(f"{r['doctor_name']:<18} | {r['dept_name']:<22} | {r['day_of_week']:<9} | {shift:<17} | {r['available_slots_remaining']}")

        elif choice == "4":
            print("\nBOOK APPOINTMENT:")
            pid = int(input("Patient ID: ").strip())
            did = int(input("Doctor ID: ").strip())
            dt = input("Date (YYYY-MM-DD): ").strip()
            st = input("Start Time (HH:MM:SS): ").strip()
            et = input("End Time (HH:MM:SS): ").strip()
            reason = input("Reason for Consultation: ").strip()
            try:
                cur.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date, start_time, end_time, status, reason)
                    VALUES (?, ?, ?, ?, ?, 'SCHEDULED', ?)
                """, (pid, did, dt, st, et, reason))
                conn.commit()
                print(f"SUCCESS: Appointment booked with Token ID: {cur.lastrowid}")
            except Exception as e:
                print(f"TRIGGER REJECTION: {e}")

        elif choice == "5":
            cur.execute("""
                SELECT ward_name, ward_type, total_ward_capacity, operational_beds_count, occupied_beds_count, vacant_beds_count, occupancy_rate_percentage
                FROM view_bed_occupancy
            """)
            rows = cur.fetchall()
            print(f"\n{'Ward Name':<30} | {'Type':<12} | {'Beds':<5} | {'Occupied':<8} | {'Vacant':<6} | {'Occupancy %'}")
            print("-" * 80)
            for r in rows:
                print(f"{r['ward_name']:<30} | {r['ward_type']:<12} | {r['operational_beds_count']:<5} | {r['occupied_beds_count']:<8} | {r['vacant_beds_count']:<6} | {r['occupancy_rate_percentage']}%")

        elif choice == "6":
            print("\nADMIT INPATIENT:")
            pid = int(input("Patient ID: ").strip())
            bid = int(input("Bed ID: ").strip())
            did = int(input("Admitting Doctor ID: ").strip())
            reason = input("Admission Reason: ").strip()
            try:
                cur.execute("""
                    INSERT INTO admissions (patient_id, bed_id, admitting_doctor_id, admission_date, status, admission_reason)
                    VALUES (?, ?, ?, datetime('now'), 'ACTIVE', ?)
                """, (pid, bid, did, reason))
                conn.commit()
                print(f"SUCCESS: Patient admitted with Admission ID: {cur.lastrowid}")
            except Exception as e:
                print(f"BED ALLOCATION REJECTION: {e}")

        elif choice == "7":
            cur.execute("SELECT bill_id, patient_name, billing_category, net_payable, paid_amount, outstanding_balance, payment_status FROM view_outstanding_bills_revenue")
            rows = cur.fetchall()
            print(f"\n{'Bill ID':<7} | {'Patient Name':<18} | {'Type':<10} | {'Net':<8} | {'Paid':<8} | {'Balance':<8} | {'Status'}")
            print("-" * 75)
            for r in rows:
                print(f"{r['bill_id']:<7} | {r['patient_name']:<18} | {r['billing_category']:<10} | {r['net_payable']:<8} | {r['paid_amount']:<8} | {r['outstanding_balance']:<8} | {r['payment_status']}")

        elif choice == "8":
            print("\nSELECT VIEW TO INSPECT:")
            print("1. view_patient_history")
            print("2. view_doctor_schedules")
            print("3. view_pending_tests")
            print("4. view_bed_occupancy")
            print("5. view_outstanding_bills_revenue")
            vchoice = input("Enter choice (1-5): ").strip()
            vnames = {
                "1": "view_patient_history",
                "2": "view_doctor_schedules",
                "3": "view_pending_tests",
                "4": "view_bed_occupancy",
                "5": "view_outstanding_bills_revenue"
            }
            if vchoice in vnames:
                vname = vnames[vchoice]
                cur.execute(f"SELECT * FROM {vname} LIMIT 10")
                rows = cur.fetchall()
                if rows:
                    cols = [col[0] for col in cur.description]
                    print(f"\n--- VIEW: {vname} ---")
                    print(" | ".join(cols[:6]))
                    print("-" * 80)
                    for r in rows:
                        print(" | ".join(str(r[c])[:15] for c in cols[:6]))
            else:
                print("Invalid view selection.")

        elif choice == "9":
            conn.close()
            start_web_server()
            break

        elif choice == "0":
            conn.close()
            print("Exiting. Thank you!")
            sys.exit(0)

        conn.close()

# =============================================================================
# WEB DASHBOARD (HTML / CSS / JS EMBEDDED)
# =============================================================================
WEB_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hospital DBMS — Live Clinical Application & Prototype</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0B1329;
      --surface: #111E38;
      --surface-light: #1A2C50;
      --border: #233866;
      --text: #F8FAFC;
      --muted: #94A3B8;
      --teal: #0D9488;
      --teal-accent: #14B8A6;
      --blue: #0284C7;
      --purple: #7C3AED;
      --rose: #E11D48;
      --green: #10B981;
      --amber: #F59E0B;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-icon {
      background: linear-gradient(135deg, var(--teal), var(--blue));
      width: 38px;
      height: 38px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(13, 148, 136, 0.4);
    }
    .brand-text h1 { font-size: 16px; font-weight: 800; letter-spacing: -0.3px; }
    .brand-text p { font-size: 11px; color: var(--muted); }

    .nav-tabs {
      display: flex;
      gap: 6px;
      background: var(--bg);
      padding: 4px;
      border-radius: 10px;
      border: 1px solid var(--border);
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--muted);
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tab-btn:hover { color: var(--text); background: var(--surface-light); }
    .tab-btn.active { background: var(--teal); color: #FFF; box-shadow: 0 2px 8px rgba(13, 148, 136, 0.4); }

    main {
      flex: 1;
      padding: 24px 28px;
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
    }

    /* KPI STATS ROW */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .stat-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }
    .stat-card::after {
      content: '';
      position: absolute;
      top: 0; left: 0; bottom: 0; width: 4px;
      background: var(--stat-color, var(--teal));
    }
    .stat-title { font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-val { font-size: 24px; font-weight: 800; margin: 6px 0 2px 0; color: #FFF; }
    .stat-sub { font-size: 11px; color: var(--muted); }

    /* TAB CONTENT */
    .tab-pane { display: none; }
    .tab-pane.active { display: block; animation: fadeIn 0.2s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

    /* CARDS & TABLES */
    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
    }
    .panel-title { font-size: 16px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
    .table-container { overflow-x: auto; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      text-align: left;
    }
    th {
      background: var(--surface-light);
      color: var(--muted);
      font-weight: 700;
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-transform: uppercase;
      font-size: 10px;
      letter-spacing: 0.5px;
    }
    td {
      padding: 12px;
      border-bottom: 1px solid rgba(35, 56, 102, 0.4);
      color: #E2E8F0;
    }
    tr:hover td { background: rgba(255, 255, 255, 0.02); }

    /* BADGES */
    .tag {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.3px;
    }
    .tag-green { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .tag-blue { background: rgba(2, 132, 199, 0.15); color: #38BDF8; border: 1px solid rgba(2, 132, 199, 0.3); }
    .tag-amber { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .tag-rose { background: rgba(225, 29, 72, 0.15); color: #FB7185; border: 1px solid rgba(225, 29, 72, 0.3); }
    .tag-purple { background: rgba(124, 58, 237, 0.15); color: #C084FC; border: 1px solid rgba(124, 58, 237, 0.3); }

    /* FORMS */
    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 16px;
    }
    .form-group { display: flex; flex-direction: column; gap: 6px; }
    label { font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; }
    input, select, textarea {
      background: var(--bg);
      border: 1px solid var(--border);
      color: #FFF;
      padding: 9px 12px;
      border-radius: 6px;
      font-size: 13px;
      font-family: inherit;
    }
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--teal);
      box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.2);
    }
    button.btn {
      background: var(--teal);
      color: #FFF;
      border: none;
      padding: 9px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    button.btn:hover { background: var(--teal-accent); }
    button.btn-secondary { background: var(--surface-light); color: var(--text); border: 1px solid var(--border); }
    button.btn-secondary:hover { background: #233866; }

    /* ALERTS */
    .alert-box {
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 16px;
      font-size: 13px;
      display: none;
    }
    .alert-success { background: rgba(16, 185, 129, 0.1); border: 1px solid var(--green); color: #34D399; }
    .alert-error { background: rgba(225, 29, 72, 0.1); border: 1px solid var(--rose); color: #FB7185; }

    /* BED GRID VISUAL */
    .bed-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 12px;
      margin-top: 12px;
    }
    .bed-box {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      text-align: center;
      transition: all 0.2s;
    }
    .bed-vacant { background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.3); }
    .bed-occupied { background: rgba(225, 29, 72, 0.08); border-color: rgba(225, 29, 72, 0.3); }
    .bed-num { font-size: 14px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .bed-status { font-size: 10px; font-weight: 700; margin-top: 4px; text-transform: uppercase; }

    /* SQL SANDBOX */
    .sql-editor {
      width: 100%;
      height: 100px;
      background: #020617;
      color: #38BDF8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      resize: vertical;
      margin-bottom: 12px;
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-icon">⚕</div>
      <div class="brand-text">
        <h1>CarePulse Hospital DBMS</h1>
        <p>Review 3 Final Application &amp; Working Prototype (Week 16)</p>
      </div>
    </div>

    <div class="nav-tabs">
      <button class="tab-btn active" onclick="showTab('dashboard')">Overview</button>
      <button class="tab-btn" onclick="showTab('patients')">Patients</button>
      <button class="tab-btn" onclick="showTab('appointments')">Appointments</button>
      <button class="tab-btn" onclick="showTab('consultations')">Clinical</button>
      <button class="tab-btn" onclick="showTab('inpatient')">Wards &amp; Beds</button>
      <button class="tab-btn" onclick="showTab('billing')">Billing</button>
      <button class="tab-btn" onclick="showTab('reports')">5 Views Reports</button>
      <button class="tab-btn" onclick="showTab('sandbox')">SQL Console</button>
    </div>
  </header>

  <main>
    <!-- TOP STATS -->
    <div class="stats-row">
      <div class="stat-card" style="--stat-color: var(--blue);">
        <span class="stat-title">Registered Patients</span>
        <span class="stat-val" id="stat-patients">--</span>
        <span class="stat-sub">Active Master Patient Index</span>
      </div>
      <div class="stat-card" style="--stat-color: var(--teal);">
        <span class="stat-title">Bed Occupancy</span>
        <span class="stat-val" id="stat-occupancy">--</span>
        <span class="stat-sub" id="stat-beds-sub">--</span>
      </div>
      <div class="stat-card" style="--stat-color: var(--purple);">
        <span class="stat-title">Total Encounters</span>
        <span class="stat-val" id="stat-appointments">--</span>
        <span class="stat-sub">OPD &amp; Inpatient Visits</span>
      </div>
      <div class="stat-card" style="--stat-color: var(--amber);">
        <span class="stat-title">Pending Lab Tests</span>
        <span class="stat-val" id="stat-pending-tests">--</span>
        <span class="stat-sub">In-flight diagnostic orders</span>
      </div>
      <div class="stat-card" style="--stat-color: var(--green);">
        <span class="stat-title">Revenue Collected</span>
        <span class="stat-val" id="stat-revenue">--</span>
        <span class="stat-sub">Actual settled receipts</span>
      </div>
    </div>

    <!-- TAB 1: DASHBOARD -->
    <div id="tab-dashboard" class="tab-pane active">
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">Recent Clinical Appointments</div>
            <button class="btn btn-secondary" onclick="showTab('appointments')">View All</button>
          </div>
          <div class="table-container">
            <table id="tbl-recent-appts">
              <thead><tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Date &amp; Slot</th><th>Status</th><th>Reason</th></tr></thead>
              <tbody><tr><td colspan="6">Loading recent visits...</td></tr></tbody>
            </table>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">Ward Occupancy Summary</div>
            <button class="btn btn-secondary" onclick="showTab('inpatient')">Manage Beds</button>
          </div>
          <div class="table-container">
            <table id="tbl-ward-summary">
              <thead><tr><th>Ward</th><th>Beds</th><th>Occupied</th><th>Rate</th></tr></thead>
              <tbody><tr><td colspan="4">Loading ward census...</td></tr></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: PATIENTS -->
    <div id="tab-patients" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Patient Directory &amp; Registration (CRUD)</div>
          <button class="btn" onclick="toggleForm('patient-reg-form')">+ New Patient Intake</button>
        </div>

        <div id="patient-alert" class="alert-box"></div>

        <!-- NEW PATIENT FORM -->
        <div id="patient-reg-form" style="display:none; background: var(--surface-light); padding: 16px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--border);">
          <h3 style="font-size: 14px; margin-bottom: 12px; color: var(--teal-accent);">Master Patient Index Intake Form</h3>
          <div class="form-grid">
            <div class="form-group"><label>First Name</label><input type="text" id="p-fn" placeholder="Aarav"></div>
            <div class="form-group"><label>Last Name</label><input type="text" id="p-ln" placeholder="Sharma"></div>
            <div class="form-group"><label>Date of Birth</label><input type="date" id="p-dob"></div>
            <div class="form-group">
              <label>Gender</label>
              <select id="p-gender">
                <option value="MALE">MALE</option>
                <option value="FEMALE">FEMALE</option>
                <option value="OTHER">OTHER</option>
              </select>
            </div>
            <div class="form-group">
              <label>Blood Group</label>
              <select id="p-bg">
                <option value="A+">A+</option><option value="A-">A-</option>
                <option value="B+">B+</option><option value="B-">B-</option>
                <option value="AB+">AB+</option><option value="AB-">AB-</option>
                <option value="O+">O+</option><option value="O-">O-</option>
              </select>
            </div>
            <div class="form-group"><label>Phone (Unique)</label><input type="text" id="p-phone" placeholder="+91 91234 56789"></div>
            <div class="form-group"><label>Address</label><input type="text" id="p-addr" placeholder="Apartment / City"></div>
            <div class="form-group"><label>Emergency Contact</label><input type="text" id="p-ecn" placeholder="Name"></div>
            <div class="form-group"><label>Emergency Phone</label><input type="text" id="p-ecp" placeholder="Phone"></div>
          </div>
          <div style="display:flex; gap:10px;">
            <button class="btn" onclick="registerPatient()">Save Patient Record</button>
            <button type="button" class="btn btn-secondary" onclick="fillDemoPatient()">⚡ Auto-Fill Demo Patient</button>
          </div>
        </div>

        <!-- SEARCH BAR -->
        <div style="display: flex; gap: 12px; margin-bottom: 16px;">
          <input type="text" id="patient-search-input" placeholder="Search by patient name, phone, or ID..." style="flex:1;" oninput="filterPatients()">
        </div>

        <div class="table-container">
          <table id="tbl-patients">
            <thead><tr><th>ID</th><th>Name</th><th>DOB</th><th>Gender</th><th>Blood</th><th>Phone</th><th>Emergency Contact</th><th>Action</th></tr></thead>
            <tbody><tr><td colspan="8">Loading patients...</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: APPOINTMENTS -->
    <div id="tab-appointments" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Doctor Scheduling &amp; Overlap-Free Booking</div>
          <button class="btn" onclick="toggleForm('booking-form')">+ Book Appointment</button>
        </div>

        <div id="booking-alert" class="alert-box"></div>

        <!-- APPOINTMENT FORM -->
        <div id="booking-form" style="display:none; background: var(--surface-light); padding: 16px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--border);">
          <h3 style="font-size: 14px; margin-bottom: 12px; color: var(--teal-accent);">Schedule Consultation (Enforces Overlap Trigger)</h3>
          <div class="form-grid">
            <div class="form-group"><label>Patient ID</label><input type="number" id="b-pid" placeholder="e.g. 1"></div>
            <div class="form-group"><label>Doctor ID</label><input type="number" id="b-did" placeholder="e.g. 1 (Dr. Aarav Sharma)"></div>
            <div class="form-group"><label>Appointment Date</label><input type="date" id="b-date"></div>
            <div class="form-group"><label>Start Time</label><input type="time" id="b-st" value="09:00"></div>
            <div class="form-group"><label>End Time</label><input type="time" id="b-et" value="09:20"></div>
            <div class="form-group" style="grid-column: span 2;"><label>Chief Presenting Complaint / Reason</label><input type="text" id="b-reason" placeholder="e.g. Follow-up consultation"></div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <button class="btn" onclick="bookAppointment()">Confirm &amp; Validate Booking</button>
            <button type="button" class="btn btn-secondary" onclick="fillDemoAppointment(false)">⚡ Fill Demo Slot (Valid)</button>
            <button type="button" class="btn btn-secondary" style="border-color:var(--rose); color:#FB7185;" onclick="fillDemoAppointment(true)">⚡ Fill Conflict Slot (Triggers Overlap)</button>
          </div>
        </div>

        <div class="table-container">
          <table id="tbl-appointments">
            <thead><tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Date</th><th>Slot Time</th><th>Status</th><th>Complaint</th><th>Actions</th></tr></thead>
            <tbody><tr><td colspan="8">Loading appointments...</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 4: CLINICAL CONSULTATIONS -->
    <div id="tab-consultations" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Clinical Consultation Entry &amp; Diagnostics</div>
        </div>
        <div id="consult-alert" class="alert-box"></div>

        <div style="background: var(--surface-light); padding: 16px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--border);">
          <h3 style="font-size: 14px; margin-bottom: 12px; color: var(--teal-accent);">Record Clinical Encounter (1:1 with Appointment)</h3>
          <div class="form-grid">
            <div class="form-group"><label>Appointment ID</label><input type="number" id="c-aid" placeholder="Appointment ID"></div>
            <div class="form-group"><label>Doctor ID</label><input type="number" id="c-did" placeholder="Doctor ID"></div>
            <div class="form-group"><label>Patient ID</label><input type="number" id="c-pid" placeholder="Patient ID"></div>
            <div class="form-group"><label>Primary Diagnosis (ICD-10)</label><input type="text" id="c-diag" placeholder="e.g. I20.0 Unstable Angina"></div>
            <div class="form-group">
              <label>Severity</label>
              <select id="c-sev">
                <option value="MILD">MILD</option>
                <option value="MODERATE" selected>MODERATE</option>
                <option value="SEVERE">SEVERE</option>
                <option value="CRITICAL">CRITICAL</option>
              </select>
            </div>
            <div class="form-group"><label>Follow-Up Date</label><input type="date" id="c-fup"></div>
            <div class="form-group" style="grid-column: span 2;"><label>Symptoms</label><input type="text" id="c-sym" placeholder="Clinical history..."></div>
            <div class="form-group" style="grid-column: span 2;"><label>Prescription Medicine (3NF Item)</label><input type="text" id="c-rx" placeholder="Medicine, Dosage, Duration"></div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <button class="btn" onclick="saveConsultation()">Record Clinical Encounter</button>
            <button type="button" class="btn btn-secondary" onclick="fillDemoConsultation()">⚡ Auto-Fill Demo Clinical Data</button>
          </div>
        </div>

        <div class="table-container">
          <table id="tbl-consult-history">
            <thead><tr><th>Consult ID</th><th>Patient</th><th>Doctor</th><th>Symptoms</th><th>Diagnosis</th><th>Severity</th></tr></thead>
            <tbody><tr><td colspan="6">Loading clinical encounters...</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 5: WARDS & BEDS -->
    <div id="tab-inpatient" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Inpatient Bed Allocation &amp; Ward Census</div>
          <button class="btn" onclick="toggleForm('admit-form')">+ Admit Patient (IPD)</button>
        </div>

        <div id="admit-alert" class="alert-box"></div>

        <!-- ADMIT FORM -->
        <div id="admit-form" style="display:none; background: var(--surface-light); padding: 16px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--border);">
          <h3 style="font-size: 14px; margin-bottom: 12px; color: var(--teal-accent);">Inpatient Admission (Enforces 1 Active Patient Per Bed)</h3>
          <div class="form-grid">
            <div class="form-group"><label>Patient ID</label><input type="number" id="adm-pid" placeholder="Patient ID"></div>
            <div class="form-group"><label>Bed ID</label><input type="number" id="adm-bid" placeholder="Bed ID (Select Vacant Bed)"></div>
            <div class="form-group"><label>Admitting Doctor ID</label><input type="number" id="adm-did" placeholder="Doctor ID"></div>
            <div class="form-group" style="grid-column: span 2;"><label>Clinical Admission Reason</label><input type="text" id="adm-reason" placeholder="Indication for hospitalization"></div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <button class="btn" onclick="admitPatient()">Execute Inpatient Admission</button>
            <button type="button" class="btn btn-secondary" onclick="fillDemoAdmission(false)">⚡ Fill Demo Admission (Vacant Bed #2)</button>
            <button type="button" class="btn btn-secondary" style="border-color:var(--rose); color:#FB7185;" onclick="fillDemoAdmission(true)">⚡ Fill Conflict Test (Occupied Bed #1)</button>
          </div>
        </div>

        <!-- VISUAL BED MAP -->
        <h3 style="font-size: 14px; margin-bottom: 8px;">Interactive Bed Map (Green = Available, Red = Occupied)</h3>
        <div class="bed-grid" id="bed-map-container">
          Loading beds...
        </div>

        <h3 style="font-size: 14px; margin: 24px 0 8px 0;">Active Inpatients</h3>
        <div class="table-container">
          <table id="tbl-active-admissions">
            <thead><tr><th>Adm ID</th><th>Patient</th><th>Ward</th><th>Bed</th><th>Admitted Date</th><th>Physician</th><th>Action</th></tr></thead>
            <tbody><tr><td colspan="7">Loading inpatients...</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 6: BILLING -->
    <div id="tab-billing" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Hospital Billing &amp; Payment Ledger</div>
          <button class="btn" onclick="toggleForm('payment-form')">+ Record Payment</button>
        </div>

        <div id="billing-alert" class="alert-box"></div>

        <!-- PAYMENT FORM -->
        <div id="payment-form" style="display:none; background: var(--surface-light); padding: 16px; border-radius: 8px; margin-bottom: 20px; border: 1px solid var(--border);">
          <h3 style="font-size: 14px; margin-bottom: 12px; color: var(--teal-accent);">Remit Payment (Enforces Ceiling &le; Net Payable)</h3>
          <div class="form-grid">
            <div class="form-group"><label>Bill ID</label><input type="number" id="pay-bid" placeholder="Invoice #"></div>
            <div class="form-group"><label>Amount (CHECK &gt; 0)</label><input type="number" id="pay-amt" placeholder="e.g. 500.00" step="0.01"></div>
            <div class="form-group">
              <label>Payment Method</label>
              <select id="pay-method">
                <option value="UPI">UPI</option>
                <option value="CREDIT_CARD">CREDIT CARD</option>
                <option value="DEBIT_CARD">DEBIT CARD</option>
                <option value="CASH">CASH</option>
                <option value="INSURANCE">INSURANCE</option>
              </select>
            </div>
            <div class="form-group"><label>Transaction Ref / UTR</label><input type="text" id="pay-ref" placeholder="TXN-ID"></div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <button class="btn" onclick="recordPayment()">Submit Payment Transaction</button>
            <button type="button" class="btn btn-secondary" onclick="fillDemoPayment(false)">⚡ Fill Demo Payment</button>
            <button type="button" class="btn btn-secondary" style="border-color:var(--rose); color:#FB7185;" onclick="fillDemoPayment(true)">⚡ Fill Overrun Test (> Balance)</button>
          </div>
        </div>

        <div class="table-container">
          <table id="tbl-bills">
            <thead><tr><th>Bill ID</th><th>Patient</th><th>Category</th><th>Total Amount</th><th>Discount</th><th>Net Payable</th><th>Paid Amount</th><th>Balance</th><th>Status</th></tr></thead>
            <tbody><tr><td colspan="9">Loading billing records...</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 7: 5 VIEWS REPORTS -->
    <div id="tab-reports" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">5 Production Database Views (Review 2 &amp; 3 Requirement)</div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" onclick="loadView('view_patient_history')">1. Patient History</button>
            <button class="btn btn-secondary" onclick="loadView('view_doctor_schedules')">2. Doctor Schedules</button>
            <button class="btn btn-secondary" onclick="loadView('view_pending_tests')">3. Pending Tests</button>
            <button class="btn btn-secondary" onclick="loadView('view_bed_occupancy')">4. Bed Occupancy</button>
            <button class="btn btn-secondary" onclick="loadView('view_outstanding_bills_revenue')">5. Revenue Ledger</button>
          </div>
        </div>

        <h3 id="view-title" style="font-size: 14px; margin-bottom: 12px; color: var(--teal-accent);">view_patient_history</h3>
        <div class="table-container">
          <table id="tbl-view-data">
            <thead><tr id="view-thead"><th>Click a view above to inspect compiled data</th></tr></thead>
            <tbody id="view-tbody"><tr><td>Select a view above</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 8: SQL CONSOLE -->
    <div id="tab-sandbox" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Interactive SQL Query Sandbox</div>
          <div style="display:flex; gap:8px;">
            <select id="sample-query-select" onchange="loadPresetQuery()" style="max-width:320px;">
              <option value="">-- Load Demonstration Query --</option>
              <option value="1">Q1: Patient History (5-Table Join)</option>
              <option value="2">Q2: Inpatient Ward Census (6-Table Join)</option>
              <option value="3">Q3: Above-Average Bills (Scalar Subquery)</option>
              <option value="4">Q4: Top Caseload Doctor (Correlated Subquery)</option>
              <option value="5">Q5: Department Revenue Recovery %</option>
              <option value="6">Q6: Ward Occupancy Rate &amp; Daily Yield</option>
            </select>
            <button class="btn" onclick="executeCustomSql()">Execute SQL (Ctrl+Enter)</button>
          </div>
        </div>

        <textarea id="sql-input" class="sql-editor">SELECT * FROM view_bed_occupancy;</textarea>
        <div id="sql-alert" class="alert-box"></div>

        <div class="table-container">
          <table id="tbl-sql-results">
            <thead><tr id="sql-thead"><th>Execute a query above</th></tr></thead>
            <tbody id="sql-tbody"><tr><td>No query executed yet.</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>

  </main>

  <script>
    // Tab switching
    function showTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      const targetPane = document.getElementById(`tab-${tabId}`);
      if (targetPane) targetPane.classList.add('active');
      const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.textContent.toLowerCase().includes(tabId.substring(0, 4)));
      if (activeBtn) activeBtn.classList.add('active');

      if (tabId === 'patients') loadPatients();
      if (tabId === 'appointments') loadAppointments();
      if (tabId === 'consultations') loadConsultations();
      if (tabId === 'inpatient') { loadBedMap(); loadActiveAdmissions(); }
      if (tabId === 'billing') loadBills();
      if (tabId === 'reports') loadView('view_patient_history');
      if (tabId === 'dashboard') loadDashboard();
    }

    function toggleForm(id) {
      const el = document.getElementById(id);
      el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
    }

    function showAlert(boxId, msg, isError = false) {
      const el = document.getElementById(boxId);
      el.textContent = msg;
      el.className = `alert-box ${isError ? 'alert-error' : 'alert-success'}`;
      el.style.display = 'block';
      setTimeout(() => { el.style.display = 'none'; }, 6000);
    }

    // API Helper
    async function apiCall(endpoint, method = 'GET', data = null) {
      const opts = { method, headers: { 'Content-Type': 'application/json' } };
      if (data) opts.body = JSON.stringify(data);
      const res = await fetch(`/api/${endpoint}`, opts);
      return await res.json();
    }

    // Load Dashboard Stats
    async function loadDashboard() {
      const res = await apiCall('dashboard_stats');
      if (res.success) {
        document.getElementById('stat-patients').textContent = res.patients_count;
        document.getElementById('stat-occupancy').textContent = `${res.occupancy_rate}%`;
        document.getElementById('stat-beds-sub').textContent = `${res.occupied_beds} / ${res.total_beds} beds occupied`;
        document.getElementById('stat-appointments').textContent = res.appointments_count;
        document.getElementById('stat-pending-tests').textContent = res.pending_tests_count;
        document.getElementById('stat-revenue').textContent = `₹${res.revenue_collected.toLocaleString('en-IN')}`;

        // Recent appointments
        const tbAppts = document.querySelector('#tbl-recent-appts tbody');
        tbAppts.innerHTML = res.recent_appointments.map(a => `
          <tr>
            <td><strong>#${a.appointment_id}</strong></td>
            <td>${a.patient_name}</td>
            <td>${a.doctor_name}</td>
            <td>${a.appointment_date} <span style="color:var(--muted)">(${a.start_time.substring(0,5)})</span></td>
            <td><span class="tag ${a.status === 'COMPLETED' ? 'tag-green' : 'tag-blue'}">${a.status}</span></td>
            <td>${a.reason || 'Routine'}</td>
          </tr>
        `).join('');

        // Ward summary
        const tbWards = document.querySelector('#tbl-ward-summary tbody');
        tbWards.innerHTML = res.ward_occupancy.map(w => `
          <tr>
            <td><strong>${w.ward_name}</strong></td>
            <td>${w.operational_beds_count}</td>
            <td>${w.occupied_beds_count}</td>
            <td><span class="tag ${w.occupancy_rate_percentage > 30 ? 'tag-rose' : 'tag-teal'}">${w.occupancy_rate_percentage}%</span></td>
          </tr>
        `).join('');
      }
    }

    // PATIENTS MODULE
    let patientsData = [];
    async function loadPatients() {
      const res = await apiCall('patients');
      if (res.success) {
        patientsData = res.data;
        renderPatientsTable(patientsData);
      }
    }

    function renderPatientsTable(list) {
      const tbody = document.querySelector('#tbl-patients tbody');
      if (list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8">No matching patients found.</td></tr>';
        return;
      }
      tbody.innerHTML = list.map(p => `
        <tr>
          <td><strong>#${p.patient_id}</strong></td>
          <td>${p.first_name} ${p.last_name}</td>
          <td>${p.dob}</td>
          <td><span class="tag tag-purple">${p.gender}</span></td>
          <td><strong>${p.blood_group || 'N/A'}</strong></td>
          <td>${p.phone}</td>
          <td>${p.emergency_contact_name} <span style="color:var(--muted)">(${p.emergency_contact_phone})</span></td>
          <td><button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="selectPatientForAppt(${p.patient_id})">Book</button></td>
        </tr>
      `).join('');
    }

    function filterPatients() {
      const q = document.getElementById('patient-search-input').value.toLowerCase();
      const filtered = patientsData.filter(p => 
        p.first_name.toLowerCase().includes(q) || 
        p.last_name.toLowerCase().includes(q) || 
        p.phone.includes(q) ||
        p.patient_id.toString().includes(q)
      );
      renderPatientsTable(filtered);
    }

    async function registerPatient() {
      const payload = {
        first_name: document.getElementById('p-fn').value.trim(),
        last_name: document.getElementById('p-ln').value.trim(),
        dob: document.getElementById('p-dob').value,
        gender: document.getElementById('p-gender').value,
        blood_group: document.getElementById('p-bg').value,
        phone: document.getElementById('p-phone').value.trim(),
        address: document.getElementById('p-addr').value.trim(),
        emergency_contact_name: document.getElementById('p-ecn').value.trim(),
        emergency_contact_phone: document.getElementById('p-ecp').value.trim(),
      };
      if (!payload.first_name || !payload.last_name || !payload.dob || !payload.phone) {
        showAlert('patient-alert', 'Please complete all required fields.', true);
        return;
      }
      const res = await apiCall('patients', 'POST', payload);
      if (res.success) {
        showAlert('patient-alert', `Patient registered successfully with ID: ${res.patient_id}`);
        toggleForm('patient-reg-form');
        loadPatients();
        loadDashboard();
      } else {
        showAlert('patient-alert', `Error: ${res.error}`, true);
      }
    }

    function selectPatientForAppt(pid) {
      showTab('appointments');
      document.getElementById('b-pid').value = pid;
      toggleForm('booking-form');
    }

    // APPOINTMENTS MODULE
    async function loadAppointments() {
      const res = await apiCall('appointments');
      if (res.success) {
        const tbody = document.querySelector('#tbl-appointments tbody');
        tbody.innerHTML = res.data.map(a => `
          <tr>
            <td><strong>#${a.appointment_id}</strong></td>
            <td>${a.patient_name} <span style="color:var(--muted)">(#${a.patient_id})</span></td>
            <td>${a.doctor_name}</td>
            <td>${a.appointment_date}</td>
            <td><code>${a.start_time.substring(0,5)} - ${a.end_time.substring(0,5)}</code></td>
            <td><span class="tag ${a.status === 'COMPLETED' ? 'tag-green' : (a.status === 'CANCELLED' ? 'tag-rose' : 'tag-blue')}">${a.status}</span></td>
            <td>${a.reason || 'N/A'}</td>
            <td>
              ${a.status === 'SCHEDULED' ? `
                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="cancelAppt(${a.appointment_id})">Cancel</button>
              ` : '—'}
            </td>
          </tr>
        `).join('');
      }
    }

    async function bookAppointment() {
      const payload = {
        patient_id: parseInt(document.getElementById('b-pid').value),
        doctor_id: parseInt(document.getElementById('b-did').value),
        appointment_date: document.getElementById('b-date').value,
        start_time: document.getElementById('b-st').value + ':00',
        end_time: document.getElementById('b-et').value + ':00',
        reason: document.getElementById('b-reason').value.trim()
      };
      if (!payload.patient_id || !payload.doctor_id || !payload.appointment_date) {
        showAlert('booking-alert', 'Missing required appointment fields.', true);
        return;
      }
      const res = await apiCall('appointments', 'POST', payload);
      if (res.success) {
        showAlert('booking-alert', `Appointment successfully booked with ID: ${res.appointment_id}`);
        toggleForm('booking-form');
        loadAppointments();
        loadDashboard();
      } else {
        // Trigger or constraint caught!
        showAlert('booking-alert', `INTEGRITY CONSTRAINT PREVENTED BOOKING: ${res.error}`, true);
      }
    }

    async function cancelAppt(aid) {
      if (!confirm(`Cancel appointment #${aid}?`)) return;
      const res = await apiCall(`appointments/${aid}/cancel`, 'POST');
      if (res.success) {
        loadAppointments();
        loadDashboard();
      } else {
        alert(res.error);
      }
    }

    // CLINICAL CONSULTATIONS
    async function loadConsultations() {
      const res = await apiCall('consultations');
      if (res.success) {
        const tbody = document.querySelector('#tbl-consult-history tbody');
        tbody.innerHTML = res.data.map(c => `
          <tr>
            <td><strong>#${c.consultation_id}</strong></td>
            <td>${c.patient_name}</td>
            <td>${c.doctor_name}</td>
            <td>${c.symptoms}</td>
            <td><strong>${c.diagnosis_name || 'Under Evaluation'}</strong></td>
            <td><span class="tag ${c.severity === 'CRITICAL' ? 'tag-rose' : 'tag-amber'}">${c.severity || 'N/A'}</span></td>
          </tr>
        `).join('');
      }
    }

    async function saveConsultation() {
      const payload = {
        appointment_id: parseInt(document.getElementById('c-aid').value),
        doctor_id: parseInt(document.getElementById('c-did').value),
        patient_id: parseInt(document.getElementById('c-pid').value),
        symptoms: document.getElementById('c-sym').value.trim(),
        diagnosis_name: document.getElementById('c-diag').value.trim(),
        severity: document.getElementById('c-sev').value,
        follow_up_date: document.getElementById('c-fup').value || null,
        medicine_name: document.getElementById('c-rx').value.trim()
      };
      if (!payload.appointment_id || !payload.symptoms) {
        showAlert('consult-alert', 'Please provide appointment ID and symptoms.', true);
        return;
      }
      const res = await apiCall('consultations', 'POST', payload);
      if (res.success) {
        showAlert('consult-alert', `Clinical consultation #${res.consultation_id} and diagnosis recorded!`);
        loadConsultations();
        loadDashboard();
      } else {
        showAlert('consult-alert', res.error, true);
      }
    }

    // INPATIENT WARDS & BEDS
    async function loadBedMap() {
      const res = await apiCall('beds');
      if (res.success) {
        const container = document.getElementById('bed-map-container');
        container.innerHTML = res.data.map(b => `
          <div class="bed-box ${b.is_occupied ? 'bed-occupied' : 'bed-vacant'}">
            <div class="bed-num">${b.bed_number}</div>
            <div style="font-size:11px; color:var(--muted); margin: 2px 0;">${b.ward_name}</div>
            <div class="bed-status" style="color: ${b.is_occupied ? '#FB7185' : '#34D399'}">
              ${b.is_occupied ? `Occupied (#${b.patient_id})` : 'Available'}
            </div>
            <div style="font-size:10px; color:var(--muted); margin-top:4px;">₹${b.daily_rate}/day</div>
          </div>
        `).join('');
      }
    }

    async function loadActiveAdmissions() {
      const res = await apiCall('admissions');
      if (res.success) {
        const tbody = document.querySelector('#tbl-active-admissions tbody');
        tbody.innerHTML = res.data.map(adm => `
          <tr>
            <td><strong>#${adm.admission_id}</strong></td>
            <td>${adm.patient_name} <span style="color:var(--muted)">(#${adm.patient_id})</span></td>
            <td>${adm.ward_name}</td>
            <td><code>${adm.bed_number}</code></td>
            <td>${adm.admission_date}</td>
            <td>${adm.doctor_name}</td>
            <td>
              <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="dischargePatient(${adm.admission_id})">Discharge</button>
            </td>
          </tr>
        `).join('');
      }
    }

    async function admitPatient() {
      const payload = {
        patient_id: parseInt(document.getElementById('adm-pid').value),
        bed_id: parseInt(document.getElementById('adm-bid').value),
        admitting_doctor_id: parseInt(document.getElementById('adm-did').value),
        admission_reason: document.getElementById('adm-reason').value.trim()
      };
      if (!payload.patient_id || !payload.bed_id || !payload.admitting_doctor_id) {
        showAlert('admit-alert', 'Please provide patient ID, bed ID, and doctor ID.', true);
        return;
      }
      const res = await apiCall('admissions', 'POST', payload);
      if (res.success) {
        showAlert('admit-alert', `Inpatient admission #${res.admission_id} confirmed.`);
        toggleForm('admit-form');
        loadBedMap();
        loadActiveAdmissions();
        loadDashboard();
      } else {
        showAlert('admit-alert', `BED ALLOCATION REJECTION: ${res.error}`, true);
      }
    }

    async function dischargePatient(admId) {
      const summary = prompt('Enter discharge summary notes:');
      if (!summary) return;
      const res = await apiCall(`admissions/${admId}/discharge`, 'POST', { discharge_summary: summary });
      if (res.success) {
        loadBedMap();
        loadActiveAdmissions();
        loadDashboard();
      } else {
        alert(res.error);
      }
    }

    // BILLING MODULE
    async function loadBills() {
      const res = await apiCall('bills');
      if (res.success) {
        const tbody = document.querySelector('#tbl-bills tbody');
        tbody.innerHTML = res.data.map(b => `
          <tr>
            <td><strong>#${b.bill_id}</strong></td>
            <td>${b.patient_name}</td>
            <td><span class="tag tag-purple">${b.billing_category}</span></td>
            <td>₹${b.total_amount.toLocaleString('en-IN')}</td>
            <td>₹${b.discount_amount.toLocaleString('en-IN')}</td>
            <td><strong>₹${b.net_payable.toLocaleString('en-IN')}</strong></td>
            <td>₹${b.paid_amount.toLocaleString('en-IN')}</td>
            <td style="color:${b.outstanding_balance > 0 ? '#FB7185' : '#34D399'}"><strong>₹${b.outstanding_balance.toLocaleString('en-IN')}</strong></td>
            <td><span class="tag ${b.payment_status === 'PAID' ? 'tag-green' : (b.payment_status === 'PARTIALLY_PAID' ? 'tag-amber' : 'tag-rose')}">${b.payment_status}</span></td>
          </tr>
        `).join('');
      }
    }

    async function recordPayment() {
      const payload = {
        bill_id: parseInt(document.getElementById('pay-bid').value),
        amount_paid: parseFloat(document.getElementById('pay-amt').value),
        payment_method: document.getElementById('pay-method').value,
        transaction_ref: document.getElementById('pay-ref').value.trim() || `TXN-${Date.now()}`
      };
      if (!payload.bill_id || !payload.amount_paid || payload.amount_paid <= 0) {
        showAlert('billing-alert', 'Enter a valid positive payment amount.', true);
        return;
      }
      const res = await apiCall('payments', 'POST', payload);
      if (res.success) {
        showAlert('billing-alert', `Payment receipt #${res.payment_id} recorded. Bill updated!`);
        toggleForm('payment-form');
        loadBills();
        loadDashboard();
      } else {
        showAlert('billing-alert', `PAYMENT CEILING REJECTION: ${res.error}`, true);
      }
    }

    // ==========================================
    // AUTO-FILL DEMO HELPERS (FOR EVALUATION)
    // ==========================================
    function fillDemoPatient() {
      const randNum = Math.floor(1000 + Math.random() * 9000);
      document.getElementById('p-fn').value = 'Vikram';
      document.getElementById('p-ln').value = 'Singhania';
      document.getElementById('p-dob').value = '1988-06-24';
      document.getElementById('p-gender').value = 'MALE';
      document.getElementById('p-bg').value = 'O+';
      document.getElementById('p-phone').value = `+91 98450 ${randNum}`;
      document.getElementById('p-addr').value = 'Skyline Residency, Koregaon Park, Pune';
      document.getElementById('p-ecn').value = 'Anjali Singhania';
      document.getElementById('p-ecp').value = '+91 98450 99881';
      showAlert('patient-alert', '⚡ Demo Patient data auto-filled into form. Click "Save Patient Record" to commit.');
    }

    function fillDemoAppointment(isConflict = false) {
      if (isConflict) {
        // Doctor 1 has an active appointment on 2026-10-10 from 09:00 to 09:20!
        document.getElementById('b-pid').value = 2;
        document.getElementById('b-did').value = 1;
        document.getElementById('b-date').value = '2026-10-10';
        document.getElementById('b-st').value = '09:10';
        document.getElementById('b-et').value = '09:30';
        document.getElementById('b-reason').value = 'Conflict Test: Intentional overlap with existing 09:00-09:20 slot';
        showAlert('booking-alert', '⚡ Overlap Conflict demo data filled! Click "Confirm & Validate Booking" to see the trigger reject it.', true);
      } else {
        const tmrw = new Date(Date.now() + 86400000).toISOString().split('T')[0];
        document.getElementById('b-pid').value = 3;
        document.getElementById('b-did').value = 1;
        document.getElementById('b-date').value = tmrw;
        document.getElementById('b-st').value = '11:00';
        document.getElementById('b-et').value = '11:20';
        document.getElementById('b-reason').value = 'Follow-up Cardiology consultation and ECG evaluation';
        showAlert('booking-alert', '⚡ Valid appointment demo data filled! Click "Confirm & Validate Booking" to book.');
      }
    }

    function fillDemoConsultation() {
      document.getElementById('c-aid').value = 11;
      document.getElementById('c-did').value = 1;
      document.getElementById('c-pid').value = 1;
      document.getElementById('c-diag').value = 'I25.10 Atherosclerotic Heart Disease';
      document.getElementById('c-sev').value = 'MODERATE';
      const fup = new Date(Date.now() + 14 * 86400000).toISOString().split('T')[0];
      document.getElementById('c-fup').value = fup;
      document.getElementById('c-sym').value = 'Mild exertional dyspnea on climbing 2 flights of stairs';
      document.getElementById('c-rx').value = 'Tablet Atorvastatin 20mg (0-0-1) + Tablet Aspirin 75mg (1-0-0)';
      showAlert('consult-alert', '⚡ Demo clinical consultation data filled! Click "Record Clinical Encounter" to save.');
    }

    function fillDemoAdmission(isConflict = false) {
      if (isConflict) {
        // Bed 1 (ICU-BED-01) is already OCCUPIED by Patient 1!
        document.getElementById('adm-pid').value = 2;
        document.getElementById('adm-bid').value = 1;
        document.getElementById('adm-did').value = 1;
        document.getElementById('adm-reason').value = 'Conflict Test: Attempting to double-book active ICU Bed 1';
        showAlert('admit-alert', '⚡ Double-booking conflict data filled! Click "Execute Inpatient Admission" to see the bed lock trigger reject it.', true);
      } else {
        // Bed 2 is VACANT!
        document.getElementById('adm-pid').value = 2;
        document.getElementById('adm-bid').value = 2;
        document.getElementById('adm-did').value = 1;
        document.getElementById('adm-reason').value = 'Acute Coronary Syndrome surveillance in vacant ICU-BED-02';
        showAlert('admit-alert', '⚡ Valid admission data filled for vacant Bed #2! Click "Execute Inpatient Admission" to confirm.');
      }
    }

    function fillDemoPayment(isOverrun = false) {
      // Bill 10 has a net payable of 36,750 with 20,000 paid (16,750 outstanding)
      document.getElementById('pay-bid').value = 10;
      document.getElementById('pay-method').value = 'UPI';
      document.getElementById('pay-ref').value = `UPI-DEMO-${Date.now().toString().slice(-6)}`;
      if (isOverrun) {
        document.getElementById('pay-amt').value = 99999.00;
        showAlert('billing-alert', '⚡ Payment overrun data filled (₹99,999 > remaining balance)! Click submit to see the ceiling trigger reject it.', true);
      } else {
        document.getElementById('pay-amt').value = 5000.00;
        showAlert('billing-alert', '⚡ Valid installment payment filled (₹5,000)! Click "Submit Payment Transaction" to record.');
      }
    }

    // 5 VIEWS LOADER
    async function loadView(viewName) {
      document.getElementById('view-title').textContent = viewName;
      const res = await apiCall(`views/${viewName}`);
      if (res.success && res.data.length > 0) {
        const cols = Object.keys(res.data[0]);
        document.getElementById('view-thead').innerHTML = cols.map(c => `<th>${c.replace(/_/g, ' ')}</th>`).join('');
        document.getElementById('view-tbody').innerHTML = res.data.map(row => `
          <tr>${cols.map(c => `<td>${row[c] !== null ? row[c] : '<span style="color:var(--muted)">NULL</span>'}</td>`).join('')}</tr>
        `).join('');
      } else {
        document.getElementById('view-thead').innerHTML = '<th>Status</th>';
        document.getElementById('view-tbody').innerHTML = '<tr><td>No data available in this view.</td></tr>';
      }
    }

    // SQL SANDBOX
    const presetQueries = {
      "1": `SELECT p.patient_id, p.first_name || ' ' || p.last_name AS patient_name, a.appointment_date, d.first_name || ' ' || d.last_name AS doctor, c.symptoms, diag.diagnosis_name FROM patients p JOIN appointments a ON p.patient_id = a.patient_id JOIN doctors d ON a.doctor_id = d.doctor_id LEFT JOIN consultations c ON a.appointment_id = c.appointment_id LEFT JOIN diagnoses diag ON c.consultation_id = diag.consultation_id LIMIT 10;`,
      "2": `SELECT adm.admission_id, p.first_name || ' ' || p.last_name AS patient, w.ward_name, b.bed_number, d.first_name || ' ' || d.last_name AS doctor FROM admissions adm JOIN patients p ON adm.patient_id = p.patient_id JOIN beds b ON adm.bed_id = b.bed_id JOIN wards w ON b.ward_id = w.ward_id JOIN doctors d ON adm.admitting_doctor_id = d.doctor_id WHERE adm.status = 'ACTIVE';`,
      "3": `SELECT p.first_name || ' ' || p.last_name AS patient, SUM(b.net_payable) AS total_billed FROM patients p JOIN bills b ON p.patient_id = b.patient_id GROUP BY p.patient_id HAVING SUM(b.net_payable) > (SELECT AVG(net_payable) FROM bills);`,
      "4": `SELECT d.first_name || ' ' || d.last_name AS doctor, dept.dept_name, COUNT(a.appointment_id) AS total_appts FROM doctors d JOIN departments dept ON d.dept_id = dept.dept_id LEFT JOIN appointments a ON d.doctor_id = a.doctor_id GROUP BY d.doctor_id;`,
      "5": `SELECT dept.dept_name, SUM(b.net_payable) AS gross_billed, SUM(b.paid_amount) AS collected, ROUND((SUM(b.paid_amount)*100.0)/NULLIF(SUM(b.net_payable),0), 1) AS recovery_pct FROM departments dept JOIN doctors d ON dept.dept_id = d.dept_id LEFT JOIN appointments a ON d.doctor_id = a.doctor_id LEFT JOIN consultations c ON a.appointment_id = c.appointment_id LEFT JOIN bills b ON c.consultation_id = b.consultation_id GROUP BY dept.dept_id;`,
      "6": `SELECT ward_name, operational_beds_count, occupied_beds_count, occupancy_rate_percentage FROM view_bed_occupancy;`
    };

    function loadPresetQuery() {
      const qVal = document.getElementById('sample-query-select').value;
      if (presetQueries[qVal]) {
        document.getElementById('sql-input').value = presetQueries[qVal];
      }
    }

    async function executeCustomSql() {
      const sql = document.getElementById('sql-input').value.trim();
      if (!sql) return;
      const res = await apiCall('sql_sandbox', 'POST', { query: sql });
      if (res.success) {
        showAlert('sql-alert', `Query executed successfully (${res.rows_count} rows returned).`);
        if (res.data.length > 0) {
          const cols = Object.keys(res.data[0]);
          document.getElementById('sql-thead').innerHTML = cols.map(c => `<th>${c}</th>`).join('');
          document.getElementById('sql-tbody').innerHTML = res.data.map(r => `
            <tr>${cols.map(c => `<td>${r[c] !== null ? r[c] : 'NULL'}</td>`).join('')}</tr>
          `).join('');
        } else {
          document.getElementById('sql-thead').innerHTML = '<th>Result</th>';
          document.getElementById('sql-tbody').innerHTML = '<tr><td>Statement executed successfully (0 rows returned).</td></tr>';
        }
      } else {
        showAlert('sql-alert', `SQL ERROR: ${res.error}`, true);
      }
    }

    // Init on page load
    window.addEventListener('DOMContentLoaded', () => {
      loadDashboard();
      document.getElementById('b-date').valueAsDate = new Date();
      document.getElementById('c-fup').valueAsDate = new Date(Date.now() + 7*24*60*60*1000);
    });
  </script>
</body>
</html>
"""

# =============================================================================
# HTTP API HANDLER
# =============================================================================
class HospitalRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path

        if path in ["/", "/index.html"]:
            self._send_html(WEB_DASHBOARD_HTML)
            return

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            if path == "/api/dashboard_stats":
                cur.execute("SELECT COUNT(*) FROM patients")
                p_cnt = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*), SUM(CASE WHEN status='ACTIVE' THEN 1 ELSE 0 END) FROM beds b LEFT JOIN admissions a ON b.bed_id = a.bed_id AND a.status='ACTIVE' WHERE b.is_operational = 1")
                b_stats = cur.fetchone()
                total_beds = b_stats[0]
                occ_beds = b_stats[1] or 0
                occ_rate = round((occ_beds * 100.0) / max(total_beds, 1), 1)

                cur.execute("SELECT COUNT(*) FROM appointments")
                a_cnt = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM test_orders WHERE status IN ('ORDERED', 'SAMPLE_COLLECTED', 'PROCESSING')")
                t_cnt = cur.fetchone()[0]

                cur.execute("SELECT SUM(amount_paid) FROM payments")
                rev = cur.fetchone()[0] or 0.0

                # Recent appointments
                cur.execute("""
                    SELECT a.appointment_id, p.first_name || ' ' || p.last_name AS patient_name,
                           d.first_name || ' ' || d.last_name AS doctor_name,
                           a.appointment_date, a.start_time, a.status, a.reason
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    ORDER BY a.appointment_date DESC, a.start_time DESC LIMIT 5
                """)
                recent_appts = [dict(r) for r in cur.fetchall()]

                cur.execute("SELECT * FROM view_bed_occupancy")
                ward_occ = [dict(r) for r in cur.fetchall()]

                self._send_json({
                    "success": True,
                    "patients_count": p_cnt,
                    "total_beds": total_beds,
                    "occupied_beds": occ_beds,
                    "occupancy_rate": occ_rate,
                    "appointments_count": a_cnt,
                    "pending_tests_count": t_cnt,
                    "revenue_collected": rev,
                    "recent_appointments": recent_appts,
                    "ward_occupancy": ward_occ
                })

            elif path == "/api/patients":
                cur.execute("SELECT * FROM patients ORDER BY patient_id DESC")
                self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})

            elif path == "/api/appointments":
                cur.execute("""
                    SELECT a.appointment_id, a.patient_id, a.doctor_id,
                           p.first_name || ' ' || p.last_name AS patient_name,
                           d.first_name || ' ' || d.last_name AS doctor_name,
                           a.appointment_date, a.start_time, a.end_time, a.status, a.reason
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    ORDER BY a.appointment_date DESC, a.start_time DESC
                """)
                self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})

            elif path == "/api/consultations":
                cur.execute("""
                    SELECT c.consultation_id, c.appointment_id,
                           p.first_name || ' ' || p.last_name AS patient_name,
                           d.first_name || ' ' || d.last_name AS doctor_name,
                           c.symptoms, diag.diagnosis_name, diag.severity
                    FROM consultations c
                    JOIN patients p ON c.patient_id = p.patient_id
                    JOIN doctors d ON c.doctor_id = d.doctor_id
                    LEFT JOIN diagnoses diag ON c.consultation_id = diag.consultation_id
                    ORDER BY c.consultation_id DESC
                """)
                self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})

            elif path == "/api/beds":
                cur.execute("""
                    SELECT b.bed_id, b.bed_number, b.daily_rate, w.ward_name,
                           CASE WHEN adm.admission_id IS NOT NULL THEN 1 ELSE 0 END AS is_occupied,
                           adm.patient_id
                    FROM beds b
                    JOIN wards w ON b.ward_id = w.ward_id
                    LEFT JOIN admissions adm ON b.bed_id = adm.bed_id AND adm.status = 'ACTIVE'
                    WHERE b.is_operational = 1
                    ORDER BY w.ward_id, b.bed_number
                """)
                self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})

            elif path == "/api/admissions":
                cur.execute("""
                    SELECT adm.admission_id, adm.patient_id,
                           p.first_name || ' ' || p.last_name AS patient_name,
                           w.ward_name, b.bed_number, adm.admission_date,
                           d.first_name || ' ' || d.last_name AS doctor_name
                    FROM admissions adm
                    JOIN patients p ON adm.patient_id = p.patient_id
                    JOIN beds b ON adm.bed_id = b.bed_id
                    JOIN wards w ON b.ward_id = w.ward_id
                    JOIN doctors d ON adm.admitting_doctor_id = d.doctor_id
                    WHERE adm.status = 'ACTIVE'
                    ORDER BY adm.admission_date DESC
                """)
                self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})

            elif path == "/api/bills":
                cur.execute("SELECT * FROM view_outstanding_bills_revenue ORDER BY bill_id DESC")
                self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})

            elif path.startswith("/api/views/"):
                view_name = path.replace("/api/views/", "").strip()
                valid_views = [
                    "view_patient_history", "view_doctor_schedules",
                    "view_pending_tests", "view_bed_occupancy",
                    "view_outstanding_bills_revenue"
                ]
                if view_name in valid_views:
                    cur.execute(f"SELECT * FROM {view_name} LIMIT 50")
                    self._send_json({"success": True, "data": [dict(r) for r in cur.fetchall()]})
                else:
                    self._send_json({"success": False, "error": "Invalid view name"}, 400)

            else:
                self._send_json({"success": False, "error": "Not Found"}, 404)
        except Exception as e:
            self._send_json({"success": False, "error": str(e)}, 500)
        finally:
            conn.close()

    def do_POST(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except:
            payload = {}

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            if path == "/api/patients":
                cur.execute("""
                    INSERT INTO patients (first_name, last_name, dob, gender, blood_group, phone, address, emergency_contact_name, emergency_contact_phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    payload["first_name"], payload["last_name"], payload["dob"],
                    payload["gender"], payload["blood_group"], payload["phone"],
                    payload["address"], payload["emergency_contact_name"], payload["emergency_contact_phone"]
                ))
                conn.commit()
                self._send_json({"success": True, "patient_id": cur.lastrowid})

            elif path == "/api/appointments":
                cur.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date, start_time, end_time, status, reason)
                    VALUES (?, ?, ?, ?, ?, 'SCHEDULED', ?)
                """, (
                    payload["patient_id"], payload["doctor_id"], payload["appointment_date"],
                    payload["start_time"], payload["end_time"], payload.get("reason", "")
                ))
                conn.commit()
                self._send_json({"success": True, "appointment_id": cur.lastrowid})

            elif path.startswith("/api/appointments/") and path.endswith("/cancel"):
                aid = int(path.split("/")[3])
                cur.execute("UPDATE appointments SET status = 'CANCELLED' WHERE appointment_id = ?", (aid,))
                conn.commit()
                self._send_json({"success": True})

            elif path == "/api/consultations":
                cur.execute("""
                    INSERT INTO consultations (appointment_id, doctor_id, patient_id, symptoms, follow_up_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    payload["appointment_id"], payload["doctor_id"], payload["patient_id"],
                    payload["symptoms"], payload.get("follow_up_date")
                ))
                cid = cur.lastrowid

                if payload.get("diagnosis_name"):
                    cur.execute("""
                        INSERT INTO diagnoses (consultation_id, diagnosis_name, severity, diagnosis_type)
                        VALUES (?, ?, ?, 'PRIMARY')
                    """, (cid, payload["diagnosis_name"], payload.get("severity", "MODERATE")))

                if payload.get("medicine_name"):
                    cur.execute("""
                        INSERT INTO prescriptions (consultation_id) VALUES (?)
                    """, (cid,))
                    rx_id = cur.lastrowid
                    cur.execute("""
                        INSERT INTO prescription_items (prescription_id, medicine_name, dosage, frequency, duration_days, quantity)
                        VALUES (?, ?, 'As directed', '1-0-1', 7, 14)
                    """, (rx_id, payload["medicine_name"]))

                # Mark appointment as completed
                cur.execute("UPDATE appointments SET status = 'COMPLETED' WHERE appointment_id = ?", (payload["appointment_id"],))

                # Create consultation bill
                cur.execute("SELECT consultation_fee FROM doctors WHERE doctor_id = ?", (payload["doctor_id"],))
                fee = cur.fetchone()[0] or 500.00
                cur.execute("""
                    INSERT INTO bills (patient_id, consultation_id, total_amount, discount_amount, tax_amount, net_payable, paid_amount, payment_status)
                    VALUES (?, ?, ?, 0.0, 0.0, ?, 0.0, 'UNPAID')
                """, (payload["patient_id"], cid, fee, fee))

                conn.commit()
                self._send_json({"success": True, "consultation_id": cid})

            elif path == "/api/admissions":
                cur.execute("""
                    INSERT INTO admissions (patient_id, bed_id, admitting_doctor_id, admission_date, status, admission_reason)
                    VALUES (?, ?, ?, datetime('now'), 'ACTIVE', ?)
                """, (
                    payload["patient_id"], payload["bed_id"], payload["admitting_doctor_id"], payload["admission_reason"]
                ))
                conn.commit()
                self._send_json({"success": True, "admission_id": cur.lastrowid})

            elif path.startswith("/api/admissions/") and path.endswith("/discharge"):
                adm_id = int(path.split("/")[3])
                summary = payload.get("discharge_summary", "Discharged in stable condition.")
                cur.execute("""
                    UPDATE admissions
                    SET status = 'DISCHARGED', discharge_date = datetime('now'), discharge_summary = ?
                    WHERE admission_id = ?
                """, (summary, adm_id))
                conn.commit()
                self._send_json({"success": True})

            elif path == "/api/payments":
                cur.execute("""
                    INSERT INTO payments (bill_id, amount_paid, payment_method, transaction_ref, received_by)
                    VALUES (?, ?, ?, ?, 'WebDesk_Cashier')
                """, (
                    payload["bill_id"], payload["amount_paid"], payload["payment_method"], payload["transaction_ref"]
                ))
                conn.commit()
                self._send_json({"success": True, "payment_id": cur.lastrowid})

            elif path == "/api/sql_sandbox":
                query = payload.get("query", "").strip()
                if not query:
                    self._send_json({"success": False, "error": "Query cannot be empty"}, 400)
                    return
                # Check query
                cur.execute(query)
                if query.upper().startswith("SELECT") or query.upper().startswith("PRAGMA"):
                    rows = cur.fetchall()
                    data = [dict(r) for r in rows]
                    self._send_json({"success": True, "rows_count": len(data), "data": data})
                else:
                    conn.commit()
                    self._send_json({"success": True, "rows_count": cur.rowcount, "data": []})

            else:
                self._send_json({"success": False, "error": "Not Found"}, 404)
        except Exception as e:
            self._send_json({"success": False, "error": str(e)}, 400)
        finally:
            conn.close()

def start_web_server(port=8080):
    init_database()
    server_address = ('', port)
    try:
        httpd = HTTPServer(server_address, HospitalRequestHandler)
        url_local = f"http://localhost:{port}"
        url_ip = f"http://127.0.0.1:{port}"
        
        print("\n" + "="*70)
        print("  CAREPULSE HOSPITAL DBMS — WEB DASHBOARD & PROTOTYPE")
        print("="*70)
        print(f"  Status: RUNNING")
        print(f"  👉 Open in your browser: {url_local}")
        print(f"  👉 Network URL:          {url_ip}")
        print(f"  Press Ctrl+C to stop the server.")
        print("="*70 + "\n")
        
        # Automatically launch default browser in background
        def open_browser():
            import time
            time.sleep(0.6)
            try:
                webbrowser.open(url_local)
            except:
                pass
        threading.Thread(target=open_browser, daemon=True).start()
        
        httpd.serve_forever()
    except OSError as e:
        fallback_ports = [8000, 8088, 5050, 3000]
        next_port = None
        for fp in fallback_ports:
            if fp > port:
                next_port = fp
                break
        if next_port:
            print(f"[PORT NOTICE] Port {port} unavailable, switching to port {next_port}...")
            start_web_server(next_port)
        else:
            print(f"[ERROR] Could not start server: {e}")

if __name__ == "__main__":
    # Check for custom port
    custom_port = 8080
    if "--port" in sys.argv:
        try:
            idx = sys.argv.index("--port")
            custom_port = int(sys.argv[idx + 1])
        except:
            pass

    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        start_web_server(custom_port)
