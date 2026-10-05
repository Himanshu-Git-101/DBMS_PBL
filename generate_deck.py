"""
Hospital DBMS - Review 1 (Week 7) Presentation Generator
Expanded Schema over 3 dedicated, highly legible, spacious slides (9 slides total).
Everything clearly visible with zero cramming.
Slide 4: Classical Chen ER Diagram (hospital_er_diagram.png).
Slides 5, 6, 7: Relational Schema split into 3 clear domains.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_expanded_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_DARK_BG    = RGBColor(11, 19, 41)      # #0B1329
    C_LIGHT_BG   = RGBColor(248, 250, 252)   # #F8FAFC
    C_CARD_BG    = RGBColor(255, 255, 255)   # #FFFFFF
    C_BORDER     = RGBColor(203, 213, 225)   # #CBD5E1
    
    C_TEAL       = RGBColor(13, 148, 136)    # #0D9488
    C_BLUE       = RGBColor(2, 132, 199)     # #0284C7
    C_PURPLE     = RGBColor(124, 58, 237)    # #7C3AED
    C_AMBER      = RGBColor(217, 119, 6)     # #D97706
    C_ROSE       = RGBColor(219, 39, 119)    # #DB2777
    C_GREEN      = RGBColor(5, 150, 105)     # #059669

    C_TEXT_DARK  = RGBColor(15, 23, 42)      # #0F172A
    C_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
    C_TEXT_LIGHT = RGBColor(255, 255, 255)   # #FFFFFF

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text=None, is_dark=False):
        # Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.4), Inches(0.36))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(20, 184, 166) if is_dark else RGBColor(230, 255, 250)
        badge.line.color.rgb = C_TEAL
        tf = badge.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = badge_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(11, 19, 41) if is_dark else C_TEAL
        p.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(23)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = C_TEXT_LIGHT if is_dark else C_TEXT_DARK

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(12)
            p2.font.color.rgb = RGBColor(148, 163, 184) if is_dark else C_TEXT_MUTED
            p2.space_before = Pt(2)

    def add_card(slide, x, y, w, h, border_top_color, title_text, items, is_dark=False):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42) if is_dark else C_CARD_BG
        card.line.color.rgb = RGBColor(30, 41, 59) if is_dark else C_BORDER
        card.line.width = Pt(1.2)

        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = border_top_color
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(x + 0.25), Inches(y + 0.18), Inches(w - 0.5), Inches(h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = border_top_color

        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"•  {item}"
            p_item.font.size = Pt(12.5)
            p_item.font.color.rgb = RGBColor(226, 232, 240) if is_dark else RGBColor(51, 65, 85)
            p_item.space_before = Pt(7)

    def add_table_box(slide, x, y, w, h, color, table_name, pk_col, fk_list, attr_list, rule=None):
        """Creates an expanded, highly readable card dedicated to a single table"""
        # Outer Card
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.2)

        # Header Strip with Table Name
        header = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.48))
        header.fill.solid()
        header.fill.fore_color.rgb = color
        header.line.fill.background()
        
        tf_h = header.text_frame
        tf_h.word_wrap = True
        p_h = tf_h.paragraphs[0]
        p_h.text = f"TABLE : {table_name.upper()}"
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = C_TEXT_LIGHT
        p_h.alignment = PP_ALIGN.CENTER

        # Content Box
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.52), Inches(w - 0.3), Inches(h - 0.56))
        tf = tb.text_frame
        tf.word_wrap = True

        # Primary Key
        p_pk = tf.paragraphs[0]
        p_pk.text = f"🔑 Primary Key : {pk_col}"
        p_pk.font.size = Pt(11.5)
        p_pk.font.bold = True
        p_pk.font.color.rgb = RGBColor(180, 83, 9) # Dark Amber for PK
        p_pk.space_before = Pt(2)

        # Foreign Keys
        if fk_list:
            p_fk = tf.add_paragraph()
            p_fk.text = f"🔗 Foreign Keys : {', '.join(fk_list)}"
            p_fk.font.size = Pt(11)
            p_fk.font.bold = True
            p_fk.font.color.rgb = RGBColor(2, 132, 199) # Blue for FK
            p_fk.space_before = Pt(4)

        # Attributes
        p_at = tf.add_paragraph()
        p_at.text = f"📋 Attributes : {', '.join(attr_list)}"
        p_at.font.size = Pt(11)
        p_at.font.color.rgb = RGBColor(51, 65, 85)
        p_at.space_before = Pt(4)

        # Constraint Rule (if any)
        if rule:
            p_r = tf.add_paragraph()
            p_r.text = f"⚡ Constraint : {rule}"
            p_r.font.size = Pt(10.5)
            p_r.font.bold = True
            p_r.font.color.rgb = RGBColor(219, 39, 119) # Rose for rules
            p_r.space_before = Pt(4)

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_DARK_BG)

    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(3.8), Inches(0.42))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(13, 148, 136)
    b1.line.fill.background()
    p = b1.text_frame.paragraphs[0]
    p.text = "PROJECT 03 • DBMS PBL • REVIEW 1"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "Hospital Appointment & Patient Care\nManagement System"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "Conceptual Design, Chen ER Architecture & 3NF Relational Schema"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(56, 189, 248)
    p2.space_before = Pt(12)

    highlights = [
        (C_BLUE, "13 CORE ENTITIES", "Patients, Doctors, Appointments, Beds, Billing & Care"),
        (C_PURPLE, "3NF RELATIONAL SCHEMA", "16 Normalized tables with zero functional redundancy"),
        (C_TEAL, "SCHEMA-LEVEL INTEGRITY", "No double bookings, 1 patient/bed, valid billing limits")
    ]
    card_w = 3.55
    for i, (col, title, desc) in enumerate(highlights):
        cx = 1.0 + i * (card_w + 0.33)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(4.2), Inches(card_w), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = s1.shapes.add_textbox(Inches(cx + 0.2), Inches(4.35), Inches(card_w - 0.4), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = col

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(11)
        pd.font.color.rgb = RGBColor(203, 213, 225)
        pd.space_before = Pt(6)

    tb_foot = s1.shapes.add_textbox(Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.5))
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.text = "Evaluator Milestone: Week 7 (5 Marks)  •  Designed for MySQL / PostgreSQL"
    p_foot.font.size = Pt(11)
    p_foot.font.color.rgb = RGBColor(148, 163, 184)

    s1.notes_slide.notes_text_frame.text = (
        "Welcome evaluators. Today we present Review 1 for Project 03: Design and Implementation of a "
        "Database Management System for Hospital Appointment and Patient Care Management System. "
        "We cover problem identification, system boundaries, our classical Chen ER diagram, "
        "our 3NF relational schema across three clear domains, and database integrity constraints."
    )

    # =========================================================================
    # SLIDE 2: Problem Statement & Objectives
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_LIGHT_BG)
    add_header(s2, "Context & Goals", "Problem Statement & Project Objectives",
               "Solving operational chaos in disconnected hospital management systems")

    add_card(s2, 0.8, 1.8, 5.7, 5.0, C_ROSE, "The Core Problem: Disconnected Silos", [
        "Schedule Collisions: Doctors double-booked for the same time slot causing severe patient wait times.",
        "Fragmented Records: Medical history, prescriptions, and lab reports scattered across departmental logs.",
        "Bed Allocation Conflicts: No real-time synchronization between patient discharge and ward occupancy.",
        "Financial Billing Leakage: Incomplete billing failing to consolidate room charges, tests, and pharmacy."
    ])

    add_card(s2, 6.8, 1.8, 5.7, 5.0, C_TEAL, "The Project Objectives", [
        "Centralize Records: Unify all 13 clinical and administrative entities into a single relational DBMS.",
        "Enforce Schema Rules: Guarantee zero appointment overlaps and one-patient-per-bed at DDL level.",
        "Normalize to 3NF: Eliminate insert, update, and deletion anomalies while ensuring lossless joins.",
        "End-to-End Workflow: Integrate outpatient booking, consultations, admissions, and consolidated billing."
    ])

    s2.notes_slide.notes_text_frame.text = (
        "Hospitals manage appointments, consultations, prescriptions, lab tests, admissions, beds, and billing. "
        "Disconnected records create schedule conflicts and incomplete patient histories. Our objectives are to "
        "centralize these operations, enforce business rules directly at the schema level, and normalize the schema to 3NF."
    )

    # =========================================================================
    # SLIDE 3: System Scope & Target User Roles
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_LIGHT_BG)
    add_header(s3, "System Boundaries & RBAC", "System Scope & Target Users",
               "Clear functional boundaries and role-based access control (RBAC)")

    add_card(s3, 0.8, 1.8, 5.7, 5.0, C_BLUE, "Functional Scope (In-Scope Modules)", [
        "Patient Demographic & Medical Profiles: Unique IDs, contact, blood group.",
        "Doctor Rostering & Appointment Engine: Collision-free time slots.",
        "Clinical Encounters & ICD-10 Coding: Diagnosis and symptom tracking.",
        "Digital Prescriptions & Lab Investigations: Normalized item catalogs.",
        "Inpatient Ward & Bed Inventory: Strict 1-active-patient-per-bed constraint.",
        "Consolidated Invoicing: Total charges, tax, discounts, and payments."
    ])

    add_card(s3, 6.8, 1.8, 5.7, 5.0, C_PURPLE, "Target Users & Access Roles (RBAC)", [
        "Administrator: Configures hospital departments, doctors, wards, and audit logs.",
        "Doctor / Clinician: Consults patients, logs diagnoses, issues prescriptions & tests.",
        "Patient: Books appointment slots, accesses personal prescriptions & invoices.",
        "Receptionist: Registers walk-ins and handles daily appointment check-ins.",
        "Ward Nurse: Manages inpatient admissions, bed assignments, and discharges.",
        "Billing Cashier: Generates itemized bills and processes multi-mode payments."
    ])

    s3.notes_slide.notes_text_frame.text = (
        "We have demarcated clear functional boundaries: in-scope modules cover outpatient care, clinical encounters, "
        "diagnostics, bed admissions, and billing. Duties are separated across 6 distinct user roles to maintain "
        "HIPAA-inspired patient privacy and data integrity."
    )

    # =========================================================================
    # SLIDE 4: FULL VISUAL ER DIAGRAM (Classical Chen Notation)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, RGBColor(255, 255, 255))
    add_header(s4, "Deliverable 2 • Conceptual Design", "Conceptual ER Diagram: Classical Chen Notation",
               "Soft Green = Entity  |  Soft Pink = Relationship  |  Soft Blue = Attribute  |  Underlined = PK  |  (FK) = Foreign Key")

    er_img_path = "/Users/himanshu/Documents/DBMS PBL/hospital_er_diagram.png"
    if os.path.exists(er_img_path):
        s4.shapes.add_picture(er_img_path, Inches(0.6), Inches(1.45), Inches(12.133), Inches(5.65))

    s4.notes_slide.notes_text_frame.text = (
        "This is our complete Conceptual ER Diagram structured in Classical Chen Notation. "
        "Green rectangles represent Entities; Pink diamonds represent Relationships with 1 and M cardinalities; "
        "Blue ovals represent Attributes, with Primary Keys Underlined and Foreign Keys marked (FK). "
        "It covers all 13 required entities: Patient, Doctor, Department, Schedule, Appointment, Consultation, "
        "Diagnosis, Prescription, LabTest, Admission, Bed, Bill, and Payment, plus normalized child entities."
    )

    # =========================================================================
    # SLIDE 5: EXPANDED SCHEMA 1 - OUTPATIENT & SCHEDULING (5 Tables)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_LIGHT_BG)
    add_header(s5, "Deliverable 3 • Relational Schema (Part 1)", "Domain 1: Outpatient & Scheduling Tables",
               "Departments, Doctors, Shift Schedules, Patients, and Collision-Free Appointments")

    # Top Row: 3 Tables (departments, doctors, doctor_schedules)
    w3 = 3.7
    h_top = 2.45
    add_table_box(s5, 0.8, 1.75, w3, h_top, C_BLUE, "departments",
                  "dept_id (SERIAL)",
                  ["head_doctor_id → doctors (NULLABLE)"],
                  ["dept_name (VARCHAR, UQ)", "building_block", "floor_number"])

    add_table_box(s5, 4.8, 1.75, w3, h_top, C_BLUE, "doctors",
                  "doctor_id (SERIAL)",
                  ["dept_id → departments"],
                  ["first_name", "last_name", "specialization", "consultation_fee >= 0", "license_no (UQ)", "phone", "email"])

    add_table_box(s5, 8.8, 1.75, w3, h_top, C_BLUE, "doctor_schedules",
                  "schedule_id (SERIAL)",
                  ["doctor_id → doctors"],
                  ["day_of_week", "start_time", "end_time", "slot_duration_minutes", "max_patients_quota"],
                  "CHECK (end_time > start_time)")

    # Bottom Row: 2 Wide Tables (patients, appointments)
    w2 = 5.7
    h_bot = 2.5
    add_table_box(s5, 0.8, 4.45, w2, h_bot, C_BLUE, "patients",
                  "patient_id (SERIAL)",
                  [],
                  ["first_name", "last_name", "date_of_birth", "gender", "blood_group", "phone (UQ)", "email", "address", "emergency_contact"],
                  "phone & email have UNIQUE index")

    add_table_box(s5, 6.8, 4.45, w2, h_bot, C_BLUE, "appointments",
                  "appointment_id (SERIAL)",
                  ["patient_id → patients", "doctor_id → doctors"],
                  ["appointment_date", "start_time", "end_time", "status (BOOKED, COMPLETED, CANCELLED)", "reason"],
                  "CRITICAL: UNIQUE (doctor_id, appointment_date, start_time)")

    s5.notes_slide.notes_text_frame.text = (
        "Slide 5 details the Outpatient and Scheduling Domain. "
        "Notice how departments, doctors, and doctor schedules link seamlessly. "
        "Most importantly, the appointments table enforces a composite UNIQUE constraint on doctor_id, appointment_date, "
        "and start_time, mathematically preventing any doctor double-booking."
    )

    # =========================================================================
    # SLIDE 6: EXPANDED SCHEMA 2 - CLINICAL & DIAGNOSTICS (6 Tables)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_LIGHT_BG)
    add_header(s6, "Deliverable 3 • Relational Schema (Part 2)", "Domain 2: Clinical Encounters & Diagnostics (3NF)",
               "Consultations, ICD-10 Diagnoses, Multi-Item Prescriptions, and Lab Investigations")

    # 3x2 Grid for 6 Tables
    w_grid = 3.7
    h_grid = 2.45

    # Row 1
    add_table_box(s6, 0.8, 1.75, w_grid, h_grid, C_PURPLE, "consultations",
                  "consultation_id (SERIAL)",
                  ["appointment_id → appointments (UQ)", "doctor_id → doctors", "patient_id → patients"],
                  ["consultation_date", "symptoms", "physical_examination", "clinical_notes", "follow_up_date"],
                  "1:1 with appointment_id (UQ)")

    add_table_box(s6, 4.8, 1.75, w_grid, h_grid, C_PURPLE, "diagnoses",
                  "diagnosis_id (SERIAL)",
                  ["consultation_id → consultations"],
                  ["icd10_code", "diagnosis_name", "severity (MILD, MODERATE, SEVERE, CRITICAL)", "diagnosis_type (PROVISIONAL, FINAL)"])

    add_table_box(s6, 8.8, 1.75, w_grid, h_grid, C_AMBER, "lab_tests (Catalog)",
                  "test_id (SERIAL)",
                  ["dept_id → departments"],
                  ["test_name", "test_code (UQ)", "sample_type", "standard_cost >= 0", "turnaround_hours"],
                  "Standardized clinical diagnostic catalog")

    # Row 2
    add_table_box(s6, 0.8, 4.45, w_grid, h_grid, C_PURPLE, "prescriptions",
                  "prescription_id (SERIAL)",
                  ["consultation_id → consultations"],
                  ["prescription_date", "general_advice", "created_at"],
                  "Header table for patient prescription")

    add_table_box(s6, 4.8, 4.45, w_grid, h_grid, C_PURPLE, "prescription_items (3NF)",
                  "item_id (SERIAL)",
                  ["prescription_id → prescriptions (ON DELETE CASCADE)"],
                  ["medicine_name", "dosage", "frequency", "duration_days > 0", "instructions"],
                  "Decomposed multi-valued medicines (1NF/3NF)")

    add_table_box(s6, 8.8, 4.45, w_grid, h_grid, C_AMBER, "test_orders (Bridge)",
                  "order_id (SERIAL)",
                  ["consultation_id → consultations", "test_id → lab_tests"],
                  ["order_date", "status (ORDERED, SAMPLE_COLLECTED, COMPLETED)", "result_value", "normal_range", "doctor_comments"],
                  "Associative table resolving M:N relationship")

    s6.notes_slide.notes_text_frame.text = (
        "Slide 6 details Clinical Care and Diagnostics. "
        "To adhere strictly to 3NF, multi-valued medication lines are decomposed into prescription_items, "
        "and lab tests are resolved through the test_orders bridge table. "
        "Every consultation links back to an appointment via a UNIQUE foreign key."
    )

    # =========================================================================
    # SLIDE 7: EXPANDED SCHEMA 3 - INPATIENT & BILLING (5 Tables)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, C_LIGHT_BG)
    add_header(s7, "Deliverable 3 • Relational Schema (Part 3)", "Domain 3: Inpatient Beds & Consolidated Billing",
               "Wards, Bed Inventory, Inpatient Admissions, Itemized Invoices, and Payment Ledger")

    # Top Row: Inpatient (wards, beds, admissions)
    w_inp = 3.7
    h_inp = 2.45
    add_table_box(s7, 0.8, 1.75, w_inp, h_inp, C_ROSE, "wards",
                  "ward_id (SERIAL)",
                  ["dept_id → departments"],
                  ["ward_name (UQ)", "ward_type (GENERAL, ICU, PRIVATE)", "floor_number", "capacity > 0"])

    add_table_box(s7, 4.8, 1.75, w_inp, h_inp, C_ROSE, "beds",
                  "bed_id (SERIAL)",
                  ["ward_id → wards"],
                  ["bed_number", "daily_rate >= 0", "is_operational DEFAULT TRUE"],
                  "UNIQUE (ward_id, bed_number)")

    add_table_box(s7, 8.8, 1.75, w_inp, h_inp, C_ROSE, "admissions",
                  "admission_id (SERIAL)",
                  ["patient_id → patients", "bed_id → beds", "doctor_id → doctors"],
                  ["admission_date", "discharge_date", "admission_reason", "status (ACTIVE, DISCHARGED)"],
                  "PARTIAL UQ: 1 active patient per bed!")

    # Bottom Row: Financials (bills, payments)
    w_fin = 5.7
    h_fin = 2.5
    add_table_box(s7, 0.8, 4.45, w_fin, h_fin, C_TEAL, "bills (Consolidated Invoices)",
                  "bill_id (SERIAL)",
                  ["patient_id → patients", "consultation_id → consultations (NULLABLE)", "admission_id → admissions (NULLABLE)"],
                  ["bill_date", "total_amount >= 0", "discount_amount >= 0", "tax_amount >= 0", "net_payable", "paid_amount", "status"],
                  "CHECK: paid_amount <= net_payable")

    add_table_box(s7, 6.8, 4.45, w_fin, h_fin, C_TEAL, "payments (Remittance Ledger)",
                  "payment_id (SERIAL)",
                  ["bill_id → bills"],
                  ["payment_timestamp DEFAULT NOW()", "amount_paid > 0", "payment_method (CASH, CARD, UPI)", "transaction_ref (UQ)", "received_by"],
                  "Supports installment payments without exceeding net_payable")

    s7.notes_slide.notes_text_frame.text = (
        "Slide 7 details Inpatient Wards, Beds, and Financials. "
        "Admissions enforces two major rules: discharge_date >= admission_date, and a PostgreSQL partial unique index "
        "guaranteeing only ONE active patient per bed. "
        "The bills table consolidates room charges, doctor consultations, and lab tests into a single verifiable invoice."
    )

    # =========================================================================
    # SLIDE 8: Critical Business Rules Enforcement
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, C_LIGHT_BG)
    add_header(s8, "Business Rules Enforcement", "Enforcing Critical Hospital Business Rules",
               "Translating administrative mandates into database constraints and indexes")

    add_card(s8, 0.8, 1.8, 5.7, 2.35, C_BLUE, "1. No Overlapping Appointments", [
        "Rule: A doctor cannot be scheduled twice for the exact same slot.",
        "SQL Constraint: UNIQUE (doctor_id, appointment_date, start_time)"
    ])

    add_card(s8, 6.8, 1.8, 5.7, 2.35, C_ROSE, "2. One Active Patient Per Bed", [
        "Rule: A physical bed can accommodate at most ONE active patient.",
        "SQL Index: CREATE UNIQUE INDEX ON admissions(bed_id) WHERE status = 'ACTIVE'"
    ])

    add_card(s8, 0.8, 4.45, 5.7, 2.35, C_AMBER, "3. Valid Admission & Discharge Dates", [
        "Rule: Discharge date cannot precede admission date.",
        "SQL Constraint: CHECK (discharge_date IS NULL OR discharge_date >= admission_date)"
    ])

    add_card(s8, 6.8, 4.45, 5.7, 2.35, C_GREEN, "4. Positive Charges & Payment Limits", [
        "Rule: Zero negative bills; cumulative payments cannot exceed net payable.",
        "SQL Constraint: CHECK (total_amount >= 0 AND paid_amount <= net_payable)"
    ])

    s8.notes_slide.notes_text_frame.text = (
        "The project brief explicitly emphasizes four business rules: no overlapping doctor appointments, "
        "one active patient per bed, valid admission/discharge dates, and positive charges with payment limits. "
        "We enforce all four directly at the database DDL level via UNIQUE constraints, partial indexes, and CHECK constraints."
    )

    # =========================================================================
    # SLIDE 9: Conclusion & Roadmap (Dark Theme)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, C_DARK_BG)

    add_header(s9, "Milestone Summary & Defense", "Conclusion & Project Roadmap",
               "Review 1 deliverables fulfilled • Prepared for Review 2 (Week 11)", is_dark=True)

    roadmap = [
        (C_GREEN, "Review 1 (Week 7)  [5 Marks]", [
            "Problem identification & system boundaries",
            "Classical Chen ER Model (13 entities)",
            "3NF Relational Schema across 3 domains",
            "STATUS: COMPLETED"
        ]),
        (C_BLUE, "Review 2 (Week 11)  [Next]", [
            "DDL implementation in MySQL / PostgreSQL",
            "Complex multi-table join queries & reporting",
            "Analytical views: Bed Occupancy & Revenue",
            "Triggers for appointment conflict checks"
        ]),
        (C_PURPLE, "Final Review (Week 14)", [
            "Full-stack application integration",
            "Front-end UI for reception, doctors & billing",
            "Role-based authentication & patient portal",
            "End-to-end live demonstration"
        ])
    ]

    r_w = 3.65
    for i, (col, title, items) in enumerate(roadmap):
        rx = 0.8 + i * (r_w + 0.38)
        add_card(s9, rx, 1.8, r_w, 4.3, col, title, items, is_dark=True)

    tb_end = s9.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.6))
    p_end = tb_end.text_frame.paragraphs[0]
    p_end.text = "Thank You  •  Open for Evaluator Questions & Discussion"
    p_end.font.size = Pt(16)
    p_end.font.bold = True
    p_end.font.color.rgb = RGBColor(20, 184, 166)
    p_end.alignment = PP_ALIGN.CENTER

    s9.notes_slide.notes_text_frame.text = (
        "In conclusion, all deliverables for Review 1 are fulfilled: the problem analysis, 13-entity Chen ER diagram, "
        "and 3NF schema with integrity rules are complete. Our roadmap progresses to Review 2 in Week 11 for "
        "database implementation, views, and triggers, culminating in the final application demo in Week 14. "
        "Thank you, and we welcome your questions."
    )

    output_path = "/Users/himanshu/Documents/DBMS PBL/Hospital_DBMS_Review1_Presentation.pptx"
    prs.save(output_path)
    print(f"Expanded presentation (9 slides) successfully saved to: {output_path}")

if __name__ == "__main__":
    create_expanded_deck()
