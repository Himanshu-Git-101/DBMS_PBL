"""
Creative & Eye-Catching PowerPoint Presentation Suite for Hospital DBMS PBL
Builds:
- Hospital_DBMS_Review1_Presentation.pptx (Creative 9-slide deck)
- Hospital_DBMS_Review2_Presentation.pptx (Creative 8-slide deck)
- Hospital_DBMS_Review3_Presentation.pptx (Creative 8-slide deck)

Design Aesthetics:
- Executive dark title & conclusion slides, crisp modern content slides
- Bold metric highlights & step numbers (01, 02, 03)
- High visual contrast (Emerald, Electric Blue, Vivid Rose, Purple, Amber)
- Concise, punchy bullet points (zero text walls)
- Speaker notes on every slide
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Color Palette
C_DARK_BG    = RGBColor(11, 19, 41)       # #0B1329 Midnight
C_DARK_CARD  = RGBColor(17, 30, 56)       # #111E38
C_LIGHT_BG   = RGBColor(248, 250, 252)    # #F8FAFC
C_WHITE      = RGBColor(255, 255, 255)    # #FFFFFF
C_BORDER     = RGBColor(226, 232, 240)    # #E2E8F0
C_DARK_LINE  = RGBColor(30, 41, 59)       # #1E293B

C_TEAL       = RGBColor(13, 148, 136)     # #0D9488
C_CYAN       = RGBColor(6, 182, 212)      # #06B6D4
C_BLUE       = RGBColor(2, 132, 199)      # #0284C7
C_PURPLE     = RGBColor(124, 58, 237)     # #7C3AED
C_ROSE       = RGBColor(225, 29, 72)      # #E11D48
C_GREEN      = RGBColor(16, 185, 129)     # #10B981
C_AMBER      = RGBColor(245, 158, 11)     # #F59E0B

C_TEXT_DARK  = RGBColor(15, 23, 42)       # #0F172A
C_TEXT_MUTED = RGBColor(100, 116, 139)    # #64748B
C_TEXT_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_slide_header(slide, badge_text, title_text, subtitle_text=None, is_dark=False):
    # Badge Pill
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.8), Inches(0.36))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(20, 184, 166) if is_dark else RGBColor(204, 251, 241)
    badge.line.color.rgb = C_TEAL
    tf = badge.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = badge_text.upper()
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(11, 19, 41) if is_dark else C_TEAL
    p.alignment = PP_ALIGN.CENTER

    # Title Text
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = C_TEXT_LIGHT if is_dark else C_TEXT_DARK

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(148, 163, 184) if is_dark else C_TEXT_MUTED
        p2.space_before = Pt(2)

def add_creative_card(slide, x, y, w, h, accent_color, title_text, items, stat_badge=None, is_dark=False):
    """Draws a modern, creative card with top colored strip, optional stat callout, and clean bullet points."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid()
    card.fill.fore_color.rgb = C_DARK_CARD if is_dark else C_WHITE
    card.line.color.rgb = C_DARK_LINE if is_dark else C_BORDER
    card.line.width = Pt(1.2)

    # Accent top strip
    strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.12))
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent_color
    strip.line.fill.background()

    # Optional Stat badge in top right
    if stat_badge:
        sb = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + w - 1.1), Inches(y + 0.18), Inches(0.9), Inches(0.32))
        sb.fill.solid()
        sb.fill.fore_color.rgb = accent_color
        sb.line.fill.background()
        tf = sb.text_frame
        p = tf.paragraphs[0]
        p.text = stat_badge
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

    tb = slide.shapes.add_textbox(Inches(x + 0.22), Inches(y + 0.18), Inches(w - (1.2 if stat_badge else 0.44)), Inches(h - 0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    # Card Title
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = accent_color

    # Items
    for item in items:
        p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(226, 232, 240) if is_dark else C_TEXT_DARK
        p.space_before = Pt(4)

    return card

# =============================================================================
# BUILD REVIEW 2 CREATIVE DECK
# =============================================================================
def build_review2():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    layout = prs.slide_layouts[6]

    # --- SLIDE 1: Title (Dark Creative) ---
    s1 = prs.slides.add_slide(layout)
    set_slide_background(s1, C_DARK_BG)

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(4.5), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_TEAL
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "DBMS PBL • REVIEW 2 (WEEK 11 — 5 MARKS)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Hospital Appointment &\nPatient Care Management System"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "3NF Relational Normalization, DDL Integrity Triggers, 5 Analytical Views & Prototype Demo"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(8)

    # 4 Stat Hero Cards
    stats = [
        ("3NF", "Zero Redundancy", "Decomposed without partial or transitive dependencies", C_TEAL),
        ("16", "Normalized Tables", "Cleanly divided into Outpatient, Clinical, and Inpatient", C_BLUE),
        ("4", "Integrity Triggers", "No slot overlap, 1 active bed, valid dates, payment limits", C_ROSE),
        ("5", "Production Views", "Abstracted queries for history, roster, labs, beds & bills", C_AMBER)
    ]
    for i, (b_stat, b_title, b_desc, b_color) in enumerate(stats):
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(4.3), Inches(2.8), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_DARK_CARD
        card.line.color.rgb = b_color
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = b_stat
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = b_color

        p2 = tf.add_paragraph()
        p2.text = b_title.upper()
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = b_desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = RGBColor(148, 163, 184)
        p3.space_before = Pt(4)

    s1.notes_slide.notes_text_frame.text = "Review 2 Title: We present our complete 3NF normalization, DDL triggers, 5 production views, and database prototype."

    # --- SLIDE 2: 3NF Normalization Pipeline ---
    s2 = prs.slides.add_slide(layout)
    set_slide_background(s2, C_LIGHT_BG)
    add_slide_header(s2, "Deliverable 1 • Normalization", "Relational Normalization Pipeline (1NF ➔ 2NF ➔ 3NF)",
                     "Systematic elimination of insertion, update, and deletion anomalies")

    cards_s2 = [
        ("01 • First Normal Form (1NF)", [
            "Atomic Domains: Indivisible scalar values in every column.",
            "Repeating Groups Extracted: Prescription lines moved to prescription_items.",
            "Diagnostics Decomposed: Multi-test orders separated into test_orders.",
            "Primary Keys: Surrogate keys guarantee absolute tuple uniqueness."
        ], "1NF", C_BLUE),
        ("02 • Second Normal Form (2NF)", [
            "1NF Satisfied + Zero Partial Functional Dependencies.",
            "Candidate Key Separation: Every non-prime attribute depends on WHOLE key.",
            "Catalog Isolation: standard_cost isolated from clinical test results.",
            "Prescription Isolation: Advice isolated from medicine quantities."
        ], "2NF", C_PURPLE),
        ("03 • Third Normal Form (3NF)", [
            "2NF Satisfied + Zero Transitive Dependencies (X ➔ Y, Y ➔ Z).",
            "Doctor & Dept Split: doctor_id ➔ dept_id; dept_id ➔ dept_name/floor.",
            "Ward & Bed Split: bed_id ➔ ward_id; ward_id ➔ capacity/ward_type.",
            "Strict Determinants: All functional determinants are Superkeys."
        ], "3NF", C_TEAL)
    ]
    for i, (title, items, badge, color) in enumerate(cards_s2):
        add_creative_card(s2, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s2.notes_slide.notes_text_frame.text = "Slide 2: 1NF removed repeating medication arrays. 2NF removed partial dependencies. 3NF removed transitive dependencies between doctor-dept and bed-ward."

    # --- SLIDE 3: Concise Data Dictionary ---
    s3 = prs.slides.add_slide(layout)
    set_slide_background(s3, C_LIGHT_BG)
    add_slide_header(s3, "Deliverable 1 • Data Dictionary", "Structured Relational Data Dictionary",
                     "Metadata definition covering primary keys, foreign keys, and domain constraints")

    dict_cards = [
        ("Outpatient & Scheduling", [
            "departments: dept_id [PK], dept_name [UQ], floor [CHK >= 0]",
            "doctors: doctor_id [PK], dept_id [FK], fee [CHK >= 0], phone [UQ]",
            "doctor_schedules: schedule_id [PK], [CHK end_time > start_time]",
            "patients: patient_id [PK], phone [UQ], dob [DATE], gender [CHK]",
            "appointments: appointment_id [PK], [UQ(doctor_id, date, start_time)]"
        ], "OPD", C_BLUE),
        ("Clinical & Diagnostics", [
            "consultations: consultation_id [PK], appointment_id [FK UQ 1:1]",
            "diagnoses: diagnosis_id [PK], icd10_code, severity [CHK In MILD..CRITICAL]",
            "prescriptions: prescription_id [PK], consultation_id [FK], date",
            "prescription_items: item_id [PK], medicine, dosage, qty [CHK > 0]",
            "lab_tests: test_id [PK], test_code [UQ], standard_cost [CHK >= 0]",
            "test_orders: order_id [PK], status [CHK In ORDERED..COMPLETED]"
        ], "LABS", C_PURPLE),
        ("Inpatient & Billing", [
            "wards: ward_id [PK], ward_name [UQ], ward_type [CHK], capacity [> 0]",
            "beds: bed_id [PK], ward_id [FK], bed_number, daily_rate [CHK >= 0]",
            "admissions: admission_id [PK], [CHK discharge_date >= admission_date]",
            "bills: bill_id [PK], [CHK paid <= net], [CHK net = total - disc + tax]",
            "payments: payment_id [PK], amount_paid [CHK > 0], method [CHK]"
        ], "IPD", C_AMBER)
    ]
    for i, (title, items, badge, color) in enumerate(dict_cards):
        add_creative_card(s3, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s3.notes_slide.notes_text_frame.text = "Slide 3: Data dictionary categorized by Outpatient, Clinical Diagnostics, and Inpatient Billing with explicit key and domain rules."

    # --- SLIDE 4: Critical Integrity Constraints & Triggers ---
    s4 = prs.slides.add_slide(layout)
    set_slide_background(s4, C_LIGHT_BG)
    add_slide_header(s4, "Deliverable 2 • Integrity Constraints", "Enforcing Critical Hospital Business Rules",
                     "Automated schema-level constraints and triggers preventing operational collisions")

    rules = [
        ("1. No Overlapping Appointments", [
            "Constraint: UNIQUE (doctor_id, appointment_date, start_time)",
            "Trigger: trg_prevent_appointment_overlap",
            "Logic: Aborts if (NEW.start < end AND NEW.end > start)",
            "Outcome: Double-booking doctor time is mathematically impossible."
        ], "SLOTS", C_ROSE),
        ("2. One Active Patient Per Bed", [
            "Trigger: trg_prevent_bed_double_booking",
            "Index: UNIQUE (bed_id) WHERE status = 'ACTIVE'",
            "Logic: Aborts admission if bed currently houses active inpatient.",
            "Outcome: Completely eliminates dual-occupancy bed disputes."
        ], "BEDS", C_TEAL),
        ("3. Valid Admission Dates", [
            "Constraint: CHECK (discharge_date IS NULL OR discharge >= admission)",
            "Temporal Guard: Disallow discharge timestamp earlier than intake.",
            "Status Consistency: Active = NULL; Discharged = Valid timestamp.",
            "Outcome: Protects chronological inpatient length of stay."
        ], "DATES", C_BLUE),
        ("4. Positive Charges & Limits", [
            "Positive Checks: total_amount >= 0, amount_paid > 0",
            "Payment Ceiling: CHECK (paid_amount <= net_payable)",
            "Trigger: trg_update_bill_on_payment auto-updates paid & PAID status.",
            "Outcome: Eliminates overpayments and negative balances."
        ], "FINANCE", C_GREEN)
    ]
    for i, (title, items, badge, color) in enumerate(rules):
        rx = 0.8 + (i % 2) * 5.95
        ry = 1.8 + (i // 2) * 2.55
        add_creative_card(s4, rx, ry, 5.75, 2.35, color, title, items, stat_badge=badge)

    s4.notes_slide.notes_text_frame.text = "Slide 4: Demonstrates our 4 critical business rules enforced via triggers and checks: no overlaps, single bed occupancy, valid dates, and payment limits."

    # --- SLIDE 5: Multi-Table Joins & Subqueries ---
    s5 = prs.slides.add_slide(layout)
    set_slide_background(s5, C_LIGHT_BG)
    add_slide_header(s5, "Deliverable 3 • SQL Demonstrations", "Advanced Relational Queries: Joins & Subqueries",
                     "Executing complex multi-table joins and nested analytical queries on clinical data")

    joins_cards = [
        ("Multi-Table Joins (5 to 6 Tables)", [
            "Patient Clinical Journey (5 Tables): Connects patients ➔ appointments ➔ doctors ➔ consultations ➔ diagnoses into a single longitudinal timeline.",
            "Inpatient Ward Census (6 Tables): Joins admissions ➔ patients ➔ beds ➔ wards ➔ doctors ➔ departments with days-admitted calculation.",
            "Diagnostic Order Tracker (4 Tables): Joins test orders ➔ lab catalog ➔ consultations ➔ clinicians with turnaround monitoring."
        ], "JOINS", C_BLUE),
        ("Scalar & Correlated Subqueries", [
            "Above-Average Billing Query: Uses scalar subquery (SELECT AVG(net_payable) FROM bills) in HAVING clause to isolate high-utilization patients.",
            "Departmental Top Caseload: Correlated subquery identifying the busiest physician within each medical division.",
            "Available Bed Finder: Uses WHERE bed_id NOT IN (SELECT bed_id FROM admissions WHERE status='ACTIVE')."
        ], "SUBQUERIES", C_PURPLE)
    ]
    for i, (title, items, badge, color) in enumerate(joins_cards):
        add_creative_card(s5, 0.8 + i * 5.95, 1.8, 5.8, 5.0, color, title, items, stat_badge=badge)

    s5.notes_slide.notes_text_frame.text = "Slide 5: Explains multi-table joins across up to 6 tables and subqueries for benchmarks and caseloads."

    # --- SLIDE 6: Aggregations & Hospital Analytics ---
    s6 = prs.slides.add_slide(layout)
    set_slide_background(s6, C_LIGHT_BG)
    add_slide_header(s6, "Deliverable 3 • Aggregations", "SQL Aggregations & Hospital Analytical KPIs",
                     "Aggregations with GROUP BY and HAVING calculating operational and financial insights")

    agg_cards = [
        ("Department Revenue Yield", [
            "Aggregates encounters, gross billed amount, and receipts per department.",
            "Formula: (SUM(paid_amount) / SUM(net_payable)) * 100",
            "Highlights top earners (Cardiology & Surgery) and unpaid receivables.",
            "Uses GROUP BY dept_id ORDER BY revenue DESC."
        ], "RECOVERY", C_TEAL),
        ("ICD-10 Morbidity Statistics", [
            "Groups diagnostic encounters by ICD-10 disease classifications.",
            "Prevalence %: (COUNT(diag_id) * 100.0 / Total Diagnoses)",
            "Identifies high-incidence conditions (Unstable Angina, Diabetes Type 2).",
            "Assists hospital epidemiological resource planning."
        ], "MORBIDITY", C_AMBER),
        ("Ward Occupancy Census Rate", [
            "Compares licensed capacity vs operational beds and active inpatients.",
            "Occupancy %: (Active Inpatients * 100.0) / Operational Beds",
            "Projected Daily Bed Revenue = SUM(daily_rate for active patients).",
            "Instant alert on high-density units (ICU, Pediatrics)."
        ], "CENSUS", C_ROSE)
    ]
    for i, (title, items, badge, color) in enumerate(agg_cards):
        add_creative_card(s6, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s6.notes_slide.notes_text_frame.text = "Slide 6: Highlights analytical aggregations: recovery rates, ICD-10 morbidity statistics, and bed census yield."

    # --- SLIDE 7: 5 Production Views ---
    s7 = prs.slides.add_slide(layout)
    set_slide_background(s7, C_LIGHT_BG)
    add_slide_header(s7, "Deliverable 3 • Database Views", "5 Production Analytical Database Views",
                     "Abstracted, compiled SQL views delivering instantaneous role-tailored intelligence")

    v_cards = [
        ("view_patient_history", [
            "Longitudinal Clinical Summary",
            "Consolidates visits, doctors, symptoms, primary diagnoses, and count of medications & tests.",
            "Instant single-patient lookup with WHERE patient_id = :id."
        ], "CLINICAL", C_BLUE),
        ("view_doctor_schedules", [
            "Clinician Shift & Slot Roster",
            "Shows shift hours, slot durations, daily capacity, and currently booked vs free slots.",
            "Powers front-desk appointment scheduling."
        ], "ROSTER", C_TEAL),
        ("view_pending_tests", [
            "Laboratory Worklist & Alerts",
            "Filters tests in ORDERED or PROCESSING state with turnaround hour monitoring.",
            "Eliminates diagnostic bottlenecks."
        ], "LABS", C_AMBER),
        ("view_bed_occupancy", [
            "Inpatient Bed Census",
            "Calculates operational capacity, active occupants, vacancy, and occupancy rate %.",
            "Critical for emergency bed management."
        ], "CENSUS", C_PURPLE),
        ("view_outstanding_bills_revenue", [
            "Financial Accounts Ledger",
            "Tracks inpatient vs outpatient invoices, total billed, paid receipts, and pending debt.",
            "Highlights unpaid receivables for cashier."
        ], "FINANCE", C_ROSE)
    ]
    for i in range(3):
        title, items, badge, color = v_cards[i]
        add_creative_card(s7, 0.8 + i * 3.95, 1.8, 3.8, 2.4, color, title, items, stat_badge=badge)
    for i in range(2):
        title, items, badge, color = v_cards[3 + i]
        add_creative_card(s7, 2.75 + i * 3.95, 4.4, 3.8, 2.4, color, title, items, stat_badge=badge)

    s7.notes_slide.notes_text_frame.text = "Slide 7: Explains our 5 production views: patient history, doctor schedules, pending tests, bed occupancy, and outstanding revenue."

    # --- SLIDE 8: Prototype Demonstration & Evaluation Readiness ---
    s8 = prs.slides.add_slide(layout)
    set_slide_background(s8, C_DARK_BG)
    add_slide_header(s8, "Deliverable 4 • Evaluation Readiness", "Implementation Progress & Prototype Demo",
                     "Milestone achievements, database execution verification, and readiness for Review 3", is_dark=True)

    demo_cards = [
        ("Review 2 Milestones (5/5)", [
            "3NF Relational Schema: 16 tables fully normalized.",
            "Integrity Triggers: Overlap, bed collision & payment checks verified.",
            "Relational Dataset: 15 patients, 12 doctors, 25 beds, 12 bills.",
            "Query Suite: 14/14 queries executed with 100% test pass rate."
        ], "VERIFIED", C_TEAL),
        ("Prototype Demonstration", [
            "Dual Modes: Interactive Web dashboard and Terminal CLI.",
            "Live Collision Interception: Rejects double-booking live.",
            "One-Click Views: Instant execution of all 5 database views.",
            "SQL Console: In-browser SQL query execution."
        ], "PROTOTYPE", C_BLUE),
        ("Roadmap to Review 3", [
            "Full Clinical GUI: Complete CRUD for intake, consultation, beds.",
            "Discharge Workflows: Summary archiving and automatic bed release.",
            "Comprehensive Report: University PBL dossier & viva preparation.",
            "Final University Evaluation: Ready for Week 16 5/5 marks defense."
        ], "WEEK 16", C_PURPLE)
    ]
    for i, (title, items, badge, color) in enumerate(demo_cards):
        add_creative_card(s8, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge, is_dark=True)

    s8.notes_slide.notes_text_frame.text = "Slide 8: Summary of Review 2 completion and transition to live demonstration."

    p_out = "Hospital_DBMS_Review2_Presentation.pptx"
    prs.save(p_out)
    print(f"[OK] Generated {p_out}")

# =============================================================================
# BUILD REVIEW 3 CREATIVE DECK
# =============================================================================
def build_review3():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    layout = prs.slide_layouts[6]

    # --- SLIDE 1: Title (Dark Creative) ---
    s1 = prs.slides.add_slide(layout)
    set_slide_background(s1, C_DARK_BG)

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(4.8), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_TEAL
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "DBMS PBL • REVIEW 3 (WEEK 16 — FINAL 5 MARKS)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Hospital Appointment &\nPatient Care Management System"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Complete Working Prototype, End-to-End Clinical Workflows, Defensive Error Handling & Final Defense"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(8)

    stats = [
        ("APP", "Python Prototype", "Zero-dependency application with Web & CLI modes", C_TEAL),
        ("CRUD", "Complete Workflows", "Intake, booking, consultation, beds, billing & receipts", C_BLUE),
        ("DEFENSE", "Integrity Triggers", "Active triggers preventing overlaps and bed collisions", C_ROSE),
        ("5/5", "Evaluation Ready", "Full PBL report, test logs, code, screens & viva Q&A", C_AMBER)
    ]
    for i, (b_stat, b_title, b_desc, b_color) in enumerate(stats):
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(4.3), Inches(2.8), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_DARK_CARD
        card.line.color.rgb = b_color
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = b_stat
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = b_color

        p2 = tf.add_paragraph()
        p2.text = b_title.upper()
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = b_desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = RGBColor(148, 163, 184)
        p3.space_before = Pt(4)

    s1.notes_slide.notes_text_frame.text = "Review 3 Title: Welcome evaluators to our final project presentation and working prototype demonstration."

    # --- SLIDE 2: Three-Tier Architecture ---
    s2 = prs.slides.add_slide(layout)
    set_slide_background(s2, C_LIGHT_BG)
    add_slide_header(s2, "Deliverable 1 • Architecture", "Three-Tier Application Architecture",
                     "Modular separation between Presentation Layer, Business Logic Engine, and Relational Database")

    arch_cards = [
        ("Tier 1: Presentation Layer", [
            "Responsive Web Dashboard: Modern CSS layout (cards, glassmorphism, responsive grid).",
            "Real-Time Interaction: Live patient search, visual bed allocation map, and modals.",
            "Interactive SQL Console: Integrated web sandbox for live query execution.",
            "Terminal CLI Mode: Lightweight menu-driven interface for fast terminal testing."
        ], "UI TIER", C_BLUE),
        ("Tier 2: Business Logic Engine", [
            "Zero-Dependency Python Controller: Built on Python standard library http.server.",
            "RESTful JSON API: Clean modular endpoints for Patients, Encounters, Beds, Bills.",
            "Transaction Management: Enforces ACID guarantees across multi-table writes.",
            "Defensive Error Interception: Translates SQL constraint aborts into clear user alerts."
        ], "LOGIC", C_PURPLE),
        ("Tier 3: Database Engine", [
            "Relational Database: Embedded SQLite / PostgreSQL with full 3NF normalization.",
            "Active DDL Triggers: Schema-level collision detection and date sanity checks.",
            "5 Production Views: Encapsulates complex joins for rapid reporting.",
            "Performance Indexes: B-Tree indexes on foreign keys and search predicates."
        ], "DATA", C_TEAL)
    ]
    for i, (title, items, badge, color) in enumerate(arch_cards):
        add_creative_card(s2, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s2.notes_slide.notes_text_frame.text = "Slide 2: 3-tier architecture: Presentation Web GUI/CLI, Python Logic Controller, and 3NF Relational Database."

    # --- SLIDE 3: Clinical CRUD Workflows ---
    s3 = prs.slides.add_slide(layout)
    set_slide_background(s3, C_LIGHT_BG)
    add_slide_header(s3, "Deliverable 2 • Clinical CRUD", "Outpatient Registration & Clinical Workflows",
                     "Seamless clinical journey: Patient Intake ➔ Appointment Booking ➔ Clinical Consultation")

    crud_cards = [
        ("1. Patient Intake & Search", [
            "Create (C): Master Patient Index intake with validation (phone uniqueness, DOB, blood group).",
            "Read (R): Real-time asynchronous search by name, phone number, or patient ID.",
            "Update (U): Patient demographics, emergency contacts, and residential addresses.",
            "Archive (D): Soft deactivation preserving historical medical continuity."
        ], "INTAKE", C_BLUE),
        ("2. Overlap-Free Slot Booking", [
            "Roster Integration: Validates doctor shifts and daily slot capacities.",
            "Collision Prevention: Trigger trg_prevent_appointment_overlap checks time intervals.",
            "Status Lifecycle: Transitions from SCHEDULED ➔ CONFIRMED ➔ COMPLETED.",
            "Cancellation: Immediate release of slots for incoming bookings."
        ], "SLOTS", C_TEAL),
        ("3. Consultation & Diagnostics", [
            "1:1 Clinical Encounter: Links directly to appointment token with symptom recording.",
            "ICD-10 Diagnoses: Standard disease coding with severity levels (Mild to Critical).",
            "3NF Prescriptions: Decomposed line items (medicine, dosage, frequency, duration).",
            "Diagnostic Lab Orders: Dispatches test orders directly to laboratory worklists."
        ], "CLINICAL", C_PURPLE)
    ]
    for i, (title, items, badge, color) in enumerate(crud_cards):
        add_creative_card(s3, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s3.notes_slide.notes_text_frame.text = "Slide 3: Outpatient continuum from patient intake, overlap-free booking, to consultation with ICD-10 and prescriptions."

    # --- SLIDE 4: Inpatient Bed Allocation & Billing ---
    s4 = prs.slides.add_slide(layout)
    set_slide_background(s4, C_LIGHT_BG)
    add_slide_header(s4, "Deliverable 2 • Inpatient & Billing", "Inpatient Bed Allocation & Billing Ledger",
                     "Ward census management with single-occupant bed locking and automated invoice settlement")

    ipd_cards = [
        ("Inpatient Bed Allocation", [
            "Interactive Bed Map: Color-coded visual grid (Green = Available, Red = Occupied).",
            "1 Active Patient Per Bed: Trigger trg_prevent_bed_double_booking aborts conflicts.",
            "Attending Clinician Link: Connects patient, bed, ward, and admitting doctor.",
            "Discharge Workflow: Validates discharge >= admit and logs clinical summary."
        ], "BEDS", C_TEAL),
        ("Consolidated Hospital Billing", [
            "OPD & IPD Invoices: Consolidates consultation fees, room rent, and lab tests.",
            "Net Payable Formula: CHECK (net = total - discount + tax).",
            "Non-Negative Balances: All line items and totals guaranteed >= 0.",
            "Audit Trail: Invoices link directly to consultation or admission."
        ], "INVOICE", C_AMBER),
        ("Remittance & Payment Limits", [
            "Multi-Channel Support: UPI, Credit Card, Debit Card, Cash, and Insurance.",
            "Ceiling Check: CHECK (paid <= net) eliminates overpayments.",
            "Automated Trigger: Increments receipts and sets PAID status.",
            "Printable Receipt: Instant itemized voucher generation."
        ], "PAYMENTS", C_GREEN)
    ]
    for i, (title, items, badge, color) in enumerate(ipd_cards):
        add_creative_card(s4, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s4.notes_slide.notes_text_frame.text = "Slide 4: Inpatient bed allocation with visual map, discharge workflow, and billing with payment ceiling limits."

    # --- SLIDE 5: Defensive Validations & Error Handling ---
    s5 = prs.slides.add_slide(layout)
    set_slide_background(s5, C_LIGHT_BG)
    add_slide_header(s5, "Deliverable 2 • Defensive Integrity", "Robust Validations & Defensive Error Handling",
                     "Dual-layer defense: Frontend form validation combined with unbreachable Database Triggers")

    val_cards = [
        ("Appointment Overlap Guard", [
            "Scenario: Booking Doctor 1 at 09:10 when a 09:00-09:20 slot exists.",
            "Database Enforcement: Trigger raises ABORT with custom exception message.",
            "Application Response: Intercepts error and displays user-friendly collision alert.",
            "Outcome: 100% protection against clinician double-booking."
        ], "OVERLAP", C_ROSE),
        ("Bed Double-Booking Guard", [
            "Scenario: Admitting a second patient to an already occupied bed.",
            "Database Enforcement: Trigger rejects insert with 'Bed currently has an active patient'.",
            "Application Response: UI highlights bed in red and blocks form submission.",
            "Outcome: Prevents physical bed occupancy conflicts."
        ], "BED LOCK", C_TEAL),
        ("Chronological & Financial", [
            "Backwards Dates: CHECK constraint rejects discharge prior to admission intake.",
            "Payment Ceiling: Rejects payments exceeding invoice net payable.",
            "Negative Values: Strict checks blocking negative consultation fees or quantities.",
            "Outcome: Preserves accounting and chronological sanity."
        ], "SANITY", C_AMBER)
    ]
    for i, (title, items, badge, color) in enumerate(val_cards):
        add_creative_card(s5, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s5.notes_slide.notes_text_frame.text = "Slide 5: Demonstrates dual-layer defense: frontend validation and database triggers preventing slot overlaps, bed conflicts, and payment breaches."

    # --- SLIDE 6: 5 Analytical Views in Action ---
    s6 = prs.slides.add_slide(layout)
    set_slide_background(s6, C_LIGHT_BG)
    add_slide_header(s6, "Deliverable 2 • Reporting", "Analytical Reporting via 5 Production Views",
                     "Instant role-tailored reports delivering clinical insights and administrative intelligence")

    rep_cards = [
        ("Clinical Reporting", [
            "view_patient_history: Comprehensive longitudinal summary of visits, doctors seen, primary diagnoses, and count of medications & lab tests.",
            "view_pending_tests: Diagnostic laboratory worklist filtering tests awaiting collection or processing with turnaround hour alerts."
        ], "CLINICAL", C_BLUE),
        ("Operational Rostering", [
            "view_doctor_schedules: Real-time duty roster displaying shift hours, max capacity, currently booked appointments, and free slots.",
            "view_bed_occupancy: Live ward bed census computing operational beds, active inpatients, vacancy, and occupancy percentage."
        ], "OPERATIONS", C_PURPLE),
        ("Financial Intelligence", [
            "view_outstanding_bills_revenue: Complete billing ledger tracking invoices, gross revenue, collections, and pending balances.",
            "Interactive SQL Console: Live query runner enabling ad-hoc SQL execution and verification."
        ], "FINANCE", C_GREEN)
    ]
    for i, (title, items, badge, color) in enumerate(rep_cards):
        add_creative_card(s6, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge)

    s6.notes_slide.notes_text_frame.text = "Slide 6: Reporting dashboard displaying the 5 production views across Clinical, Operations, and Finance."

    # --- SLIDE 7: Test Matrix & Verification ---
    s7 = prs.slides.add_slide(layout)
    set_slide_background(s7, C_LIGHT_BG)
    add_slide_header(s7, "Deliverable 3 • Test Verification", "CRUD & Integrity Test Execution Matrix",
                     "Systematic verification of all functional modules, triggers, and error recovery scenarios")

    test_cards = [
        ("Functional Test Cases (100% Passed)", [
            "TC-01: Patient registration with valid inputs ➔ Successfully created ID #11.",
            "TC-02: Search patient by phone '+91 91234 56780' ➔ Instant record match.",
            "TC-03: Booking appointment in free slot ➔ Token generated with status SCHEDULED.",
            "TC-04: Consultation entry with ICD-10 code ➔ Diagnosis & Rx items committed.",
            "TC-05: Inpatient bed allocation ➔ Bed status updated to Occupied."
        ], "PASS 5/5", C_GREEN),
        ("Integrity Constraint Tests (Active Defense)", [
            "TC-06: Overlapping appointment for Doctor 1 ➔ INTEGRITY ERROR raised & blocked.",
            "TC-07: Double-booking active Bed 1 ➔ BED ALLOCATION REJECTION blocked.",
            "TC-08: Discharge date prior to admission ➔ CHECK constraint failed & blocked.",
            "TC-09: Payment amount exceeding net bill ➔ CHECK constraint failed & blocked.",
            "TC-10: Negative consultation fee ➔ CHECK constraint failed & blocked."
        ], "BLOCKED 5/5", C_ROSE)
    ]
    for i, (title, items, badge, color) in enumerate(test_cards):
        add_creative_card(s7, 0.8 + i * 5.95, 1.8, 5.8, 5.0, color, title, items, stat_badge=badge)

    s7.notes_slide.notes_text_frame.text = "Slide 7: Test matrix verifying 5 positive CRUD operations and 5 negative integrity constraint tests."

    # --- SLIDE 8: Final Submission & Viva Readiness ---
    s8 = prs.slides.add_slide(layout)
    set_slide_background(s8, C_DARK_BG)
    add_slide_header(s8, "Deliverable 3 • Final Submission", "Project Summary & Evaluation Readiness",
                     "Complete delivery of all Review 3 University PBL guidelines (5/5 Marks Ready)", is_dark=True)

    summary_cards = [
        ("Delivered Project Assets", [
            "Working Prototype: Full Python web app and CLI mode (app.py).",
            "Production Relational DB: 3NF schema with triggers and sample data.",
            "Comprehensive Report: Full PBL dossier with ER, 3NF proofs, and SQL.",
            "Output Screens & Test Logs: Complete walkthrough and screenshots."
        ], "DELIVERED", C_TEAL),
        ("Viva-Voce Readiness", [
            "3NF Normalization: Mathematical proofs and functional dependency sets.",
            "ACID & Transactions: Rollback recovery and concurrency management.",
            "Indexing Strategy: B-Tree performance on foreign keys and lookups.",
            "Security & Views: Data encapsulation and role-based access."
        ], "VIVA PREP", C_BLUE),
        ("Live Demonstration", [
            "1. Real-time patient intake and search.",
            "2. Overlap appointment collision prevention test.",
            "3. Live clinical consultation and ICD-10 entry.",
            "4. Bed allocation and single-patient lock demo.",
            "5. Instant 5-view reporting and SQL sandbox execution."
        ], "LIVE DEMO", C_AMBER)
    ]
    for i, (title, items, badge, color) in enumerate(summary_cards):
        add_creative_card(s8, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, stat_badge=badge, is_dark=True)

    s8.notes_slide.notes_text_frame.text = "Slide 8: Conclusion and invitation to the live prototype demonstration."

    p_out = "Hospital_DBMS_Review3_Presentation.pptx"
    prs.save(p_out)
    print(f"[OK] Generated {p_out}")

if __name__ == "__main__":
    build_review2()
    build_review3()
