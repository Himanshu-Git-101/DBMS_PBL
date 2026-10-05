-- =============================================================================
-- SQL QUERIES SUITE FOR HOSPITAL APPOINTMENT & PATIENT CARE SYSTEM
-- DBMS Project - Review 2 Demonstration Query Suite
-- Demonstrating: Joins, Subqueries, Aggregations, and 5 Dedicated Views
-- =============================================================================

-- =============================================================================
-- SECTION 1: COMPLEX MULTI-TABLE JOINS
-- =============================================================================

-- Query 1.1: Complete Patient Longitudinal Clinical Journey (5-Table Join)
-- Connects Patient -> Appointment -> Doctor -> Department -> Consultation -> Diagnosis
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.phone,
    a.appointment_date,
    a.start_time,
    d.first_name || ' ' || d.last_name AS doctor_name,
    dept.dept_name,
    c.symptoms,
    diag.icd10_code,
    diag.diagnosis_name,
    diag.severity
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN departments dept ON d.dept_id = dept.dept_id
LEFT JOIN consultations c ON a.appointment_id = c.appointment_id
LEFT JOIN diagnoses diag ON c.consultation_id = diag.consultation_id
ORDER BY a.appointment_date DESC, a.start_time DESC;

-- Query 1.2: Active Inpatient Ward Census & Attending Clinician (6-Table Join)
-- Connects Admission -> Patient -> Bed -> Ward -> Department -> Attending Doctor
SELECT 
    adm.admission_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.blood_group,
    w.ward_name,
    w.ward_type,
    b.bed_number,
    b.daily_rate,
    adm.admission_date,
    ROUND((JULIANDAY('now') - JULIANDAY(adm.admission_date)), 1) AS days_admitted,
    d.first_name || ' ' || d.last_name AS attending_physician,
    dept.dept_name AS physician_dept,
    adm.admission_reason
FROM admissions adm
JOIN patients p ON adm.patient_id = p.patient_id
JOIN beds b ON adm.bed_id = b.bed_id
JOIN wards w ON b.ward_id = w.ward_id
JOIN doctors d ON adm.admitting_doctor_id = d.doctor_id
JOIN departments dept ON d.dept_id = dept.dept_id
WHERE adm.status = 'ACTIVE'
ORDER BY adm.admission_date ASC;

-- Query 1.3: Diagnostic Laboratory Fulfillment Audit (4-Table Join)
-- Connects Test Order -> Lab Test -> Consultation -> Requesting Doctor
SELECT 
    tor.order_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    lt.test_code,
    lt.test_name,
    lt.standard_cost,
    tor.status AS test_status,
    tor.order_date,
    tor.result_date,
    tor.result_value,
    d.first_name || ' ' || d.last_name AS requested_by_doctor
FROM test_orders tor
JOIN lab_tests lt ON tor.test_id = lt.test_id
JOIN consultations c ON tor.consultation_id = c.consultation_id
JOIN patients p ON c.patient_id = p.patient_id
JOIN doctors d ON c.doctor_id = d.doctor_id
ORDER BY tor.order_date DESC;

-- =============================================================================
-- SECTION 2: SUBQUERIES (CORRELATED, SCALAR & IN-CLAUSE)
-- =============================================================================

-- Query 2.1: Patients with Total Invoiced Bills Above Hospital Overall Average
-- Demonstrates Scalar Subquery in WHERE clause
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.phone,
    SUM(b.net_payable) AS total_patient_billed,
    (SELECT ROUND(AVG(net_payable), 2) FROM bills) AS hospital_avg_bill
FROM patients p
JOIN bills b ON p.patient_id = b.patient_id
GROUP BY p.patient_id
HAVING SUM(b.net_payable) > (SELECT AVG(net_payable) FROM bills)
ORDER BY total_patient_billed DESC;

-- Query 2.2: Doctors With Highest Patient Caseload in Their Respective Department
-- Demonstrates Correlated Subquery comparing doctor count against departmental max
SELECT 
    d.doctor_id,
    d.first_name || ' ' || d.last_name AS doctor_name,
    dept.dept_name,
    COUNT(a.appointment_id) AS appointment_count
FROM doctors d
JOIN departments dept ON d.dept_id = dept.dept_id
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id
HAVING COUNT(a.appointment_id) >= (
    SELECT MAX(sub_counts.cnt)
    FROM (
        SELECT d2.dept_id, COUNT(a2.appointment_id) AS cnt
        FROM doctors d2
        LEFT JOIN appointments a2 ON d2.doctor_id = a2.doctor_id
        GROUP BY d2.doctor_id
    ) AS sub_counts
    WHERE sub_counts.dept_id = d.dept_id
)
ORDER BY dept.dept_name;

-- Query 2.3: Inactive or Available Beds Currently NOT Occupied by Active Patients
-- Demonstrates NOT IN subquery
SELECT 
    b.bed_id,
    w.ward_name,
    w.ward_type,
    b.bed_number,
    b.daily_rate
FROM beds b
JOIN wards w ON b.ward_id = w.ward_id
WHERE b.is_operational = 1
  AND b.bed_id NOT IN (
      SELECT bed_id FROM admissions WHERE status = 'ACTIVE'
  )
ORDER BY w.ward_name, b.bed_number;

-- =============================================================================
-- SECTION 3: ADVANCED AGGREGATIONS & GROUP BY WITH HAVING
-- =============================================================================

-- Query 3.1: Financial Performance & Collections by Clinical Department
SELECT 
    dept.dept_name,
    COUNT(DISTINCT d.doctor_id) AS active_doctors,
    COUNT(DISTINCT a.appointment_id) AS total_encounters,
    ROUND(SUM(b.total_amount), 2) AS gross_billed_amount,
    ROUND(SUM(b.discount_amount), 2) AS discounts_granted,
    ROUND(SUM(b.paid_amount), 2) AS actual_revenue_collected,
    ROUND(SUM(b.net_payable - b.paid_amount), 2) AS outstanding_receivables,
    ROUND((SUM(b.paid_amount) / NULLIF(SUM(b.net_payable), 0)) * 100.0, 1) AS collection_recovery_pct
FROM departments dept
JOIN doctors d ON dept.dept_id = d.dept_id
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
LEFT JOIN consultations c ON a.appointment_id = c.appointment_id
LEFT JOIN bills b ON c.consultation_id = b.consultation_id
GROUP BY dept.dept_id
ORDER BY actual_revenue_collected DESC;

-- Query 3.2: Top Diagnosed Medical Conditions (ICD-10 Morbidity Statistics)
SELECT 
    diag.icd10_code,
    diag.diagnosis_name,
    diag.severity,
    COUNT(diag.diagnosis_id) AS case_frequency,
    ROUND(COUNT(diag.diagnosis_id) * 100.0 / (SELECT COUNT(*) FROM diagnoses), 1) AS morbidity_prevalence_pct
FROM diagnoses diag
GROUP BY diag.icd10_code, diag.diagnosis_name, diag.severity
ORDER BY case_frequency DESC;

-- Query 3.3: Inpatient Bed Occupancy & Revenue Yield by Ward
SELECT 
    w.ward_name,
    w.ward_type,
    w.capacity AS licensed_capacity,
    COUNT(DISTINCT b.bed_id) AS operational_beds,
    COUNT(DISTINCT CASE WHEN adm.status = 'ACTIVE' THEN adm.admission_id END) AS active_inpatients,
    ROUND((COUNT(DISTINCT CASE WHEN adm.status = 'ACTIVE' THEN adm.admission_id END) * 100.0) / NULLIF(COUNT(DISTINCT b.bed_id), 0), 1) AS occupancy_rate_pct,
    ROUND(SUM(CASE WHEN adm.status = 'ACTIVE' THEN b.daily_rate ELSE 0 END), 2) AS projected_daily_bed_revenue
FROM wards w
LEFT JOIN beds b ON w.ward_id = b.ward_id AND b.is_operational = 1
LEFT JOIN admissions adm ON b.bed_id = adm.bed_id AND adm.status = 'ACTIVE'
GROUP BY w.ward_id
ORDER BY occupancy_rate_pct DESC;

-- =============================================================================
-- SECTION 4: QUERIES DEMONSTRATING THE 5 DESIGNATED VIEWS
-- =============================================================================

-- View Query 4.1: Patient History for an Individual (Filtering View 1)
SELECT 
    patient_id,
    patient_name,
    appointment_date,
    doctor_name,
    dept_name,
    symptoms,
    diagnosis_name,
    medicines_prescribed_count,
    lab_tests_ordered_count
FROM view_patient_history
WHERE patient_id = 1
ORDER BY appointment_date DESC;

-- View Query 4.2: Available Doctor Slots Across All Departments (Filtering View 2)
SELECT 
    doctor_name,
    dept_name,
    day_of_week,
    shift_start,
    shift_end,
    daily_slot_capacity,
    currently_booked_appointments,
    available_slots_remaining
FROM view_doctor_schedules
WHERE available_slots_remaining > 0
ORDER BY dept_name, day_of_week;

-- View Query 4.3: Urgent Lab Investigations Pending Sample Processing (Filtering View 3)
SELECT 
    order_id,
    patient_name,
    test_code,
    test_name,
    turnaround_hours,
    order_date,
    test_status,
    requesting_doctor
FROM view_pending_tests
ORDER BY turnaround_hours ASC;

-- View Query 4.4: Inpatient Bed Census Alert (Filtering View 4)
SELECT 
    ward_name,
    ward_type,
    total_ward_capacity,
    occupied_beds_count,
    vacant_beds_count,
    occupancy_rate_percentage
FROM view_bed_occupancy
WHERE occupancy_rate_percentage > 0
ORDER BY occupancy_rate_percentage DESC;

-- View Query 4.5: Outstanding Hospital Debts Requiring Cashier Follow-up (Filtering View 5)
SELECT 
    bill_id,
    patient_name,
    patient_phone,
    billing_category,
    net_payable,
    paid_amount,
    outstanding_balance,
    payment_status
FROM view_outstanding_bills_revenue
WHERE outstanding_balance > 0
ORDER BY outstanding_balance DESC;
