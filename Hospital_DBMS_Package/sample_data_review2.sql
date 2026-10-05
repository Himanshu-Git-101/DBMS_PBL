-- =============================================================================
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
