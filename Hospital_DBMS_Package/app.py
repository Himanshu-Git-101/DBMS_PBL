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

def init_database():
    """Ensure database schema, triggers, sample data, and views are present."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if doctors table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='doctors';")
    if not cursor.fetchone():
        print(f"[INIT] Initializing database at: {DB_FILE}")
        
        # Locate schema file
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
        if os.path.exists(sample_path):
            print(f"[INIT] Loading sample data from: {sample_path}")
            with open(sample_path, "r") as f:
                cursor.executescript(f.read())
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
