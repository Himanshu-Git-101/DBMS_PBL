"""
Hospital DBMS - Review 2 (Week 11 - 5 Marks) Presentation Generator
Generates widescreen 16:9 PowerPoint presentation.
Concise, visual, high-contrast cards, and speaker notes on every slide.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_review2_deck():
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
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.6), Inches(0.36))
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

        tb = slide.shapes.add_textbox(Inches(x + 0.22), Inches(y + 0.16), Inches(w - 0.44), Inches(h - 0.28))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = border_top_color

        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(11)
            p.font.color.rgb = RGBColor(226, 232, 240) if is_dark else C_TEXT_DARK
            p.space_before = Pt(4)

        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Executive Theme)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_DARK_BG)

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(4.5), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_TEAL
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "DBMS PBL • REVIEW 2 (WEEK 11 — 5 MARKS)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Hospital Appointment &\nPatient Care Management System"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "3NF Relational Normalization, DDL Integrity Triggers, Advanced SQL Queries & Prototype Demo"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(10)

    # 4 Highlight Badges
    badges = [
        ("3NF NORMALIZATION", "Zero redundancy & full functional dependencies", C_TEAL),
        ("INTEGRITY CONSTRAINTS", "No overlap slots, 1 patient/bed, positive bills", C_BLUE),
        ("5 ANALYTICAL VIEWS", "Patient journey, doctor roster, labs, bed census, revenue", C_PURPLE),
        ("WORKING PROTOTYPE", "Live database engine with full CRUD & test suite", C_AMBER)
    ]
    for i, (b_title, b_desc, b_color) in enumerate(badges):
        bx = 0.8 + i * 2.95
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(4.4), Inches(2.8), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        card.line.color.rgb = b_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = b_color

        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = RGBColor(203, 213, 225)
        p2.space_before = Pt(8)

    s1.notes_slide.notes_text_frame.text = (
        "Review 2 Presenter Script:\n"
        "Welcome evaluators. Today we present Review 2 for our Hospital DBMS project. "
        "We have rigorously normalized our relational schema to 3NF, implemented production DDL with triggers "
        "enforcing all critical business rules, created 5 database views, executed comprehensive joins/subqueries, "
        "and established our working database prototype."
    )

    # ==========================================
    # SLIDE 2: 3NF NORMALIZATION & FUNCTIONAL DEPENDENCIES
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_LIGHT_BG)
    add_header(s2, "Deliverable 1: Normalization", "Relational Normalization Up to 3NF", 
               "Systematic decomposition eliminating insertion, update, and deletion anomalies")

    cards_s2 = [
        ("1st Normal Form (1NF)", [
            "Atomic Values: All attribute values are indivisible scalars.",
            "Repeating Groups Removed: Prescription medication lines decomposed into prescription_items.",
            "Diagnostic Orders Decomposed: Multi-test orders extracted into test_orders bridge table.",
            "Primary Keys Identified: Artificial surrogate keys guarantee tuple uniqueness."
        ], C_BLUE),
        ("2nd Normal Form (2NF)", [
            "1NF Satisfied + No Partial Dependencies on composite candidate keys.",
            "Separated Prescription Details: prescription_id -> date, item_id -> dosage & duration.",
            "Separated Diagnostic Details: test_id -> standard test cost, order_id -> clinical result.",
            "Every non-prime attribute depends on the WHOLE candidate key."
        ], C_PURPLE),
        ("3rd Normal Form (3NF)", [
            "2NF Satisfied + No Transitive Dependencies (X -> Y, Y -> Z).",
            "Doctor & Department Split: doctor_id -> dept_id, dept_id -> dept_name/floor.",
            "Ward & Bed Split: bed_id -> ward_id, ward_id -> capacity/type.",
            "All functional dependencies have a Superkey as the determinant."
        ], C_TEAL)
    ]
    for i, (title, items, color) in enumerate(cards_s2):
        add_card(s2, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items)

    s2.notes_slide.notes_text_frame.text = (
        "Slide 2 Script: Normalization up to 3NF.\n"
        "We decomposed our universal clinical ledger through 1NF, 2NF, and 3NF. "
        "In 1NF, repeating medications and test lists were split into child tables. "
        "In 2NF, partial dependencies on composite keys were eliminated. "
        "In 3NF, transitive dependencies such as doctor to department name or bed to ward type were resolved into dedicated master tables."
    )

    # ==========================================
    # SLIDE 3: CONCISE DATA DICTIONARY
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_LIGHT_BG)
    add_header(s3, "Deliverable 1: Data Dictionary", "Concise Data Dictionary Across Core Modules", 
               "Structured metadata definition of primary entities, data types, constraints, and relationships")

    dict_cards = [
        ("Outpatient Domain", [
            "departments: dept_id (PK), dept_name (UQ), building_block, floor_number (CHECK >= 0)",
            "doctors: doctor_id (PK), dept_id (FK), fee (CHECK >= 0), email (UQ), license (UQ)",
            "doctor_schedules: schedule_id (PK), doctor_id (FK), shift hours (CHECK end > start)",
            "patients: patient_id (PK), phone (UQ), dob (DATE), gender (CHECK IN Male/Female/Other)",
            "appointments: appointment_id (PK), patient_id (FK), doctor_id (FK), UQ(doc, date, slot)"
        ], C_BLUE),
        ("Clinical & Diagnostics", [
            "consultations: consultation_id (PK), appointment_id (FK, UQ 1:1), symptoms, notes",
            "diagnoses: diagnosis_id (PK), consultation_id (FK), icd10_code, severity (CHECK)",
            "prescriptions: prescription_id (PK), consultation_id (FK), prescription_date",
            "prescription_items: item_id (PK), prescription_id (FK), medicine, dosage, quantity > 0",
            "lab_tests: test_id (PK), dept_id (FK), test_code (UQ), standard_cost (CHECK >= 0)",
            "test_orders: order_id (PK), consultation_id (FK), test_id (FK), status, result_value"
        ], C_PURPLE),
        ("Inpatient & Billing", [
            "wards: ward_id (PK), dept_id (FK), ward_name (UQ), ward_type (CHECK), capacity > 0",
            "beds: bed_id (PK), ward_id (FK), bed_number, daily_rate >= 0, UQ(ward_id, bed_number)",
            "admissions: admission_id (PK), patient_id (FK), bed_id (FK), CHECK(discharge >= admit)",
            "bills: bill_id (PK), patient_id (FK), CHECK(paid <= net), CHECK(net = total - disc + tax)",
            "payments: payment_id (PK), bill_id (FK), amount_paid (CHECK > 0), payment_method (CHECK)"
        ], C_AMBER)
    ]
    for i, (title, items, color) in enumerate(dict_cards):
        add_card(s3, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items)

    s3.notes_slide.notes_text_frame.text = (
        "Slide 3 Script: Concise Data Dictionary.\n"
        "Here is our structured data dictionary spanning our three operational domains. "
        "Every table defines precise data types, non-null requirements, foreign key cascading rules, "
        "and domain CHECK constraints to safeguard relational integrity."
    )

    # ==========================================
    # SLIDE 4: CRITICAL INTEGRITY CONSTRAINTS & DDL
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_LIGHT_BG)
    add_header(s4, "Deliverable 2: Integrity Verification", "Enforcing Critical Hospital Business Rules", 
               "Automated schema-level constraints and triggers preventing operational conflicts")

    rules = [
        ("Rule 1: No Overlapping Appointments", [
            "Constraint: UNIQUE (doctor_id, appointment_date, start_time)",
            "DDL Trigger: trg_prevent_appointment_overlap",
            "Logic: Rejects booking if new_start < existing_end AND new_end > existing_start for active doctor slots.",
            "Result: Mathematically eliminates double-booking clinician time."
        ], C_ROSE),
        ("Rule 2: One Active Patient Per Bed", [
            "Constraint: Partial Unique Index on bed_id WHERE status='ACTIVE'",
            "DDL Trigger: trg_prevent_bed_double_booking",
            "Logic: ABORTS admission if the bed currently has an ACTIVE admitted inpatient.",
            "Result: Completely eliminates dual-occupancy bed disputes."
        ], C_TEAL),
        ("Rule 3: Valid Admission & Discharge Dates", [
            "Constraint: CHECK (discharge_date IS NULL OR discharge_date >= admission_date)",
            "Temporal Logic: Inpatients cannot be discharged prior to intake timestamp.",
            "Status Consistency: Active patients have NULL discharge; discharged have valid timestamp.",
            "Result: Protects chronological inpatient length of stay."
        ], C_BLUE),
        ("Rule 4: Financial Integrity & Limits", [
            "Positive Charges: CHECK (total_amount >= 0 AND amount_paid > 0)",
            "Payment Ceiling: CHECK (paid_amount <= net_payable)",
            "Automated Trigger: trg_update_bill_on_payment increments paid_amount & sets PAID status.",
            "Result: Eliminates billing overpayments and negative balances."
        ], C_GREEN)
    ]
    for i, (title, items, color) in enumerate(rules):
        rx = 0.8 + (i % 2) * 5.95
        ry = 1.8 + (i // 2) * 2.55
        add_card(s4, rx, ry, 5.75, 2.35, color, title, items)

    s4.notes_slide.notes_text_frame.text = (
        "Slide 4 Script: Business Rules Enforcement.\n"
        "We implemented four foundational business rules directly in SQL DDL: "
        "First, overlapping appointments are blocked via unique slots and overlap triggers. "
        "Second, beds are protected by single-active-occupant constraints. "
        "Third, admission dates are strictly validated. "
        "Fourth, financial constraints and payment triggers ensure accurate accounting with zero negative balances."
    )

    # ==========================================
    # SLIDE 5: DEMONSTRATION SQL QUERIES — JOINS & SUBQUERIES
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_LIGHT_BG)
    add_header(s5, "Deliverable 3: SQL Demonstrations", "Advanced SQL: Multi-Table Joins & Subqueries", 
               "Executing complex joins and nested subqueries on populated clinical datasets")

    joins_cards = [
        ("Multi-Table Joins (5 to 6 Entities)", [
            "Patient Clinical Journey: Combines patients, appointments, doctors, departments, consultations, and diagnoses into a single longitudinal timeline.",
            "Inpatient Ward Census: Joins admissions, beds, wards, doctors, and departments to track active patients and attending consultants.",
            "Diagnostic Order Fulfillment: Joins test orders, lab catalog, consultations, and requesting clinicians with sample statuses."
        ], C_BLUE),
        ("Scalar & Correlated Subqueries", [
            "Above-Average Billing Query: Uses a scalar subquery (SELECT AVG(net_payable) FROM bills) in the HAVING clause to identify high-utilization patients.",
            "Departmental Top Caseload: Uses a correlated subquery comparing doctor appointment volume against their specific department's maximum.",
            "Unoccupied Bed Finder: Uses a NOT IN subquery to filter beds not currently linked to active inpatient admissions."
        ], C_PURPLE)
    ]
    for i, (title, items, color) in enumerate(joins_cards):
        add_card(s5, 0.8 + i * 5.95, 1.8, 5.8, 5.0, color, title, items)

    s5.notes_slide.notes_text_frame.text = (
        "Slide 5 Script: Joins & Subqueries.\n"
        "We developed a suite of 14 advanced demonstration queries. "
        "Our multi-table joins link up to 6 entities to reconstruct complete patient histories and ward censuses. "
        "Our subqueries demonstrate scalar calculations for revenue benchmarks and correlated subqueries for doctor caseload analysis."
    )

    # ==========================================
    # SLIDE 6: DEMONSTRATION SQL QUERIES — AGGREGATIONS & METRICS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_LIGHT_BG)
    add_header(s6, "Deliverable 3: Aggregations", "SQL Aggregation & Hospital Analytical Metrics", 
               "Aggregations with GROUP BY and HAVING revealing operational and financial insights")

    agg_cards = [
        ("Departmental Financial Yield", [
            "Aggregates total appointments, gross billed amounts, discounts, and collections by department.",
            "Formula: Collection Recovery % = (SUM(paid_amount) / SUM(net_payable)) * 100",
            "Identifies highest revenue generators (Cardiology & Surgery) and outstanding receivables.",
            "Uses GROUP BY dept_id and ORDER BY revenue DESC."
        ], C_TEAL),
        ("ICD-10 Morbidity Statistics", [
            "Aggregates patient consultation volume by ICD-10 disease codes.",
            "Prevalence % = (COUNT(diag_id) * 100.0 / Total Diagnoses)",
            "Ranks primary disease incidence (Unstable Angina, Diabetes Type 2, Knee Osteoarthritis, Hypertension).",
            "Supports hospital epidemiological capacity planning."
        ], C_AMBER),
        ("Ward Occupancy Census Rate", [
            "Ward-level licensed capacity vs operational beds count.",
            "Occupancy % = (Active Inpatients * 100.0) / Operational Beds",
            "Projected Daily Room Revenue = SUM(daily_rate for active patients)",
            "Real-time alert on high-occupancy units (e.g. ICU at 25%, Pediatrics at 50%)."
        ], C_ROSE)
    ]
    for i, (title, items, color) in enumerate(agg_cards):
        add_card(s6, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items)

    s6.notes_slide.notes_text_frame.text = (
        "Slide 6 Script: Aggregations.\n"
        "Our aggregation queries calculate vital hospital performance indicators: "
        "collection recovery percentage by clinical department, disease morbidity prevalence by ICD-10, "
        "and ward occupancy rates with daily bed revenue yield."
    )

    # ==========================================
    # SLIDE 7: 5 PRODUCTION DATABASE VIEWS
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, C_LIGHT_BG)
    add_header(s7, "Deliverable 3: Views", "5 Production Analytical Database Views", 
               "Pre-compiled database views providing abstracted, secure, and fast data access")

    view_cards = [
        ("view_patient_history", [
            "Longitudinal Clinical Summary",
            "Consolidates visits, doctors, departments, primary diagnoses, and count of medicines & lab tests.",
            "Instant single-patient lookup with WHERE patient_id = :id."
        ], C_BLUE),
        ("view_doctor_schedules", [
            "Clinician Shift & Slot Roster",
            "Shows shift hours, slot duration, maximum patient capacity, and currently booked vs free slots.",
            "Powers front-desk appointment booking."
        ], C_TEAL),
        ("view_pending_tests", [
            "Laboratory Worklist & Alerts",
            "Filters tests in ORDERED, SAMPLE_COLLECTED, or PROCESSING state with turnaround times.",
            "Prevents diagnostic bottlenecks in labs."
        ], C_AMBER),
        ("view_bed_occupancy", [
            "Inpatient Bed Census",
            "Calculates operational capacity, active occupants, vacancy, and occupancy rate % per ward.",
            "Essential for emergency bed allocation."
        ], C_PURPLE),
        ("view_outstanding_bills_revenue", [
            "Financial Accounts Ledger",
            "Tracks inpatient vs outpatient invoices, total billed, paid amounts, and outstanding balance.",
            "Highlights unpaid receivables for follow-up."
        ], C_ROSE)
    ]
    # Place 3 cards on top, 2 on bottom
    for i in range(3):
        title, items, color = view_cards[i]
        add_card(s7, 0.8 + i * 3.95, 1.8, 3.8, 2.4, color, title, items)
    for i in range(2):
        title, items, color = view_cards[3 + i]
        add_card(s7, 2.75 + i * 3.95, 4.4, 3.8, 2.4, color, title, items)

    s7.notes_slide.notes_text_frame.text = (
        "Slide 7 Script: 5 Production Views.\n"
        "To abstract complex multi-table joins from end-user applications, we created 5 production views: "
        "Patient History, Doctor Schedules, Pending Tests, Bed Occupancy, and Outstanding Bills Revenue. "
        "These views enable instantaneous querying and reporting."
    )

    # ==========================================
    # SLIDE 8: PROTOTYPE DEMONSTRATION & CONCLUSION
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, C_DARK_BG)
    add_header(s8, "Deliverable 4: Evaluation Readiness", "Implementation Progress & Prototype Demo", 
               "Milestone achievements, database execution verification, and readiness for Review 3", is_dark=True)

    demo_cards = [
        ("Review 2 Milestone Status", [
            "3NF Relational Schema: 16 normalized tables fully implemented.",
            "Integrity Triggers: Overlap, bed double-booking & payment ceiling verified.",
            "Populated Dataset: 15 patients, 12 doctors, 20 appointments, 25 beds, 12 bills.",
            "Query Suite: 14 demonstration queries executed with 100% success."
        ], C_TEAL),
        ("Live Prototype Capabilities", [
            "Integrated SQLite Engine: Zero-dependency local and cloud database.",
            "Enforced Foreign Keys & Triggers: Active runtime validation.",
            "Interactive Reports: 1-click execution of all 5 database views.",
            "Web & CLI Interface: Dual demonstration modes for evaluation."
        ], C_BLUE),
        ("Roadmap to Review 3 (Week 16)", [
            "End-to-End Application: Full Python clinical web dashboard.",
            "CRUD Operations: Patient registration, slot booking, consultation entry.",
            "Lab & Inpatient Workflows: Sample tracking, bed discharge, and invoice printing.",
            "Final University PBL Report: Documentation, viva-voce prep & test cases."
        ], C_PURPLE)
    ]
    for i, (title, items, color) in enumerate(demo_cards):
        add_card(s8, 0.8 + i * 3.95, 1.8, 3.8, 5.0, color, title, items, is_dark=True)

    s8.notes_slide.notes_text_frame.text = (
        "Slide 8 Script: Review 2 Conclusion.\n"
        "In summary, all Review 2 objectives have been thoroughly achieved with 5/5 marks readiness. "
        "Our database schema is normalized to 3NF, critical constraints and triggers are verified, "
        "complex queries and views are functional, and our prototype is ready for live evaluation. "
        "We are ready for your questions and the live demonstration."
    )

    output_path = "Hospital_DBMS_Review2_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_review2_deck()
