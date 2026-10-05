# 🏥 CarePulse Hospital DBMS — Final Project Package
### Comprehensive Deliverables Dossier for Reviews 1, 2, 3 & Working Prototype

**Project Title:** Design and Implementation of a Database Management System for Hospital Appointment and Patient Care Management System  
**Course:** Database Management Systems (DBMS PBL — Project 03)  
**Evaluation Scope:** Review 1 (Week 7), Review 2 (Week 11), Review 3 (Week 16 — Final 5 Marks)  

---

## 📂 Master Directory Contents

### 1. 📊 PowerPoint Presentations (.pptx)
Widescreen 16:9 modern, creative decks with bold stat badges, color-coded domain cards, and speaker notes on every slide:
- **`Hospital_DBMS_Review1_Presentation.pptx`**: Review 1 Deck (9 slides: Problem, Scope, 6 User Roles, Classical Chen ER Diagram, 3NF Schema over 3 Domains, Business Rules).
- **`Hospital_DBMS_Review2_Presentation.pptx`**: Review 2 Deck (8 slides: 1NF➔2NF➔3NF Pipeline, Data Dictionary, 4 DDL Triggers, Joins & Subqueries, Aggregations, 5 Views, Prototype Demo).
- **`Hospital_DBMS_Review3_Presentation.pptx`**: Review 3 Final Deck (8 slides: 3-Tier Architecture, Clinical CRUD, Inpatient Beds & Billing, Defensive Error Handling, Views, 10-Point Test Matrix, Viva Checklist).

### 2. 🌐 Interactive Browser Presentations (.html)
Open directly in Chrome, Safari, or Edge. Keyboard controls (`→`/`Space` next, `←` prev, `N` speaker notes, `F` fullscreen), plus **Print to PDF** button:
- **`presentation_review1.html`**: Interactive presentation for Review 1 with embedded 300 DPI Chen ER diagram.
- **`presentation_review2.html`**: Interactive presentation for Review 2 with dark executive theme.
- **`presentation_review3.html`**: Interactive presentation for Review 3 with final demonstration controls.
- **`hospital_er_diagram.png`**: High-resolution 300 DPI Classical Chen notation ER diagram.

### 3. 💻 Final Working Prototype Application
Zero-dependency Python application with dual execution modes:
- **`app.py`**: Main application file.
- **`hospital_review2.db`**: Preloaded SQLite relational database file.
- **`schema_review2.sql`**: Production DDL script with 16 tables, 4 triggers, and 5 views.
- **`sample_data_review2.sql`**: Comprehensive relational dataset with realistic clinical data.
- **`queries_review2.sql`**: 14 demonstration queries (Joins, Subqueries, Aggregations, Views).

#### 🚀 How to Run the Prototype:
```bash
# Mode 1: Interactive Web Dashboard (Recommended)
python3 app.py
# Automatically opens: http://localhost:8080
# Or navigate manually to: http://127.0.0.1:8080

# Mode 2: Terminal Command-Line Interface (CLI)
python3 app.py --cli
```

### 4. 📄 Documentation, Guides & Viva Defense Dossiers
- **`Project_Report_Final.md`**: Complete University PBL final submission report covering Abstract, Introduction, System Requirements, Conceptual Design, 3NF Proofs, DDL/DML, Module Details, Test Matrix, and Conclusions.
- **`Data_Dictionary_and_Normalization.md`**: Formal 1NF/2NF/3NF decomposition proofs, functional dependency sets ($F$), and structured data dictionary.
- **`Review1_Comprehensive_Guide.md`**: Review 1 presenter script, slide timings, and defense notes.
- **`Review2_Comprehensive_Guide.md`**: Review 2 presenter script, DDL trigger walkthrough, and query explanations.
- **`Review3_Comprehensive_Guide.md`**: Review 3 presenter script, 5-step live demo script, and **25+ deep Viva-Voce Questions & Answers** (covering BCNF/3NF, triggers vs check constraints, ACID transactions, WAL logging, B-Tree indexes, partial indexes, and SQL injection prevention).

---

## ⚡ Quick Evaluation Checklist

| Requirement | Artifact | Verification Status |
| :--- | :--- | :---: |
| **Normalized Schema (3NF)** | `schema_review2.sql` / `Data_Dictionary_and_Normalization.md` | ✅ Verified |
| **Integrity Triggers** | No overlaps, 1 patient per bed, valid dates, payment limits | ✅ Verified |
| **14 Demonstration Queries** | `queries_review2.sql` (Joins, Subqueries, Aggregations, Views) | ✅ 14/14 Passed |
| **5 Production Views** | Patient History, Doctor Schedules, Tests, Beds, Revenue | ✅ 5/5 Functional |
| **Working Python Application** | `app.py` (Web Dashboard & CLI modes) | ✅ Verified (Port 5000) |
| **PBL Final Project Report** | `Project_Report_Final.md` | ✅ Complete |
| **Review Presentations** | Review 1, 2, 3 in both `.pptx` and `.html` formats | ✅ Complete |
| **Viva-Voce Preparation** | `Review3_Comprehensive_Guide.md` (25+ Q&A) | ✅ Complete |
