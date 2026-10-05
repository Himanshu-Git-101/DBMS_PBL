"""
Script to generate a High-Definition, Presentation-Ready ER Diagram Image
for Hospital Appointment & Patient Care Management System.
Outputs: hospital_er_diagram.png (High-Res 300 DPI, 16:9 Widescreen)
Optimized Topology: Zero Crossing, Beautiful Curves, High Contrast.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(20, 11.25), dpi=300)
    fig.patch.set_facecolor('#0B1329') # Sleek Dark Navy Canvas
    ax.set_facecolor('#0B1329')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56.25)
    ax.axis('off')

    # Palette
    C_DOC = {'border': '#38BDF8', 'header': '#0284C7', 'bg': '#0F172A'} # Sky Blue
    C_PAT = {'border': '#34D399', 'header': '#059669', 'bg': '#0F172A'} # Emerald Green
    C_CLN = {'border': '#C084FC', 'header': '#7C3AED', 'bg': '#0F172A'} # Violet
    C_LAB = {'border': '#FBBF24', 'header': '#D97706', 'bg': '#0F172A'} # Amber Orange
    C_IPD = {'border': '#F472B6', 'header': '#DB2777', 'bg': '#0F172A'} # Rose Pink
    C_FIN = {'border': '#2DD4BF', 'header': '#0D9488', 'bg': '#0F172A'} # Medical Teal

    entity_boxes = {}

    def draw_entity(x, y, w, h, name, pk, fks, attrs, colors):
        # Outer Card
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0.2,rounding_size=0.8",
                             edgecolor=colors['border'], facecolor=colors['bg'],
                             linewidth=1.8, zorder=2)
        ax.add_patch(box)

        # Header Bar
        hdr_h = 2.4
        hdr = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h,
                             boxstyle="round,pad=0.0,rounding_size=0.6",
                             edgecolor='none', facecolor=colors['header'],
                             zorder=3)
        ax.add_patch(hdr)

        # Entity Title
        ax.text(x + w/2, y + h - 1.2, name.upper(),
                color='#FFFFFF', fontsize=11, fontweight='bold',
                ha='center', va='center', zorder=4, family='sans-serif')

        # Attributes text
        curr_y = y + h - hdr_h - 1.1
        
        # PK
        ax.text(x + 0.8, curr_y, f"[PK] {pk}",
                color='#FDE047', fontsize=8.6, fontweight='bold',
                ha='left', va='center', zorder=4, family='monospace')
        curr_y -= 1.3

        # FKs
        for fk in fks:
            ax.text(x + 0.8, curr_y, f"[FK] {fk}",
                    color='#7DD3FC', fontsize=8.2, fontweight='bold',
                    ha='left', va='center', zorder=4, family='monospace')
            curr_y -= 1.2

        # Other attrs
        for a in attrs:
            ax.text(x + 0.8, curr_y, f"• {a}",
                    color='#CBD5E1', fontsize=7.8, fontweight='normal',
                    ha='left', va='center', zorder=4, family='sans-serif')
            curr_y -= 1.1

        entity_boxes[name] = {
            'x': x, 'y': y, 'w': w, 'h': h,
            'cx': x + w/2, 'cy': y + h/2,
            'top': (x + w/2, y + h), 'bottom': (x + w/2, y),
            'left': (x, y + h/2), 'right': (x + w, y + h/2)
        }

    # ==================== ENTITY POSITIONS (ZERO INTERFERENCE) ====================
    # TOP ROW: y=38 (Lots of space below title/legend)
    # 1. Department (Top Left)
    draw_entity(3, 38, 15, 9.5, 'DEPARTMENT', 'dept_id',
                ['head_doc_id'], ['dept_name (UQ)', 'building_block', 'floor_number'], C_DOC)

    # 2. Doctor (Top Center-Left)
    draw_entity(22, 38, 16, 10.5, 'DOCTOR', 'doctor_id',
                ['dept_id'], ['name, qualification', 'specialization', 'phone/email (UQ)', 'consultation_fee'], C_DOC)

    # 3. Appointment (Top Center)
    draw_entity(42, 38, 17, 10.0, 'APPOINTMENT', 'appointment_id',
                ['patient_id', 'doctor_id'], ['appointment_date', 'start/end_time', 'status (SCHEDULED..)', 'UQ(doc,date,time)'], C_PAT)

    # 4. Prescription (Top Column 4)
    draw_entity(63, 38, 16, 9.0, 'PRESCRIPTION', 'prescription_id',
                ['consultation_id'], ['prescription_date', 'general_advice'], C_CLN)

    # 5. Prescription Item (Top Column 5 - 3NF)
    draw_entity(82, 38, 15.5, 10.5, 'PRESCRIPTION_ITEM', 'item_id',
                ['prescription_id'], ['medicine_name', 'dosage, frequency', 'duration_days', 'quantity, instructions'], C_CLN)


    # MIDDLE ROW: y=23
    # 6. Patient (Mid Left)
    draw_entity(3, 23, 15, 11, 'PATIENT', 'patient_id',
                [], ['name, DOB, gender', 'blood_group', 'phone/email (UQ)', 'emergency_contact'], C_PAT)

    # 7. Doctor Schedule (Mid Column 2)
    draw_entity(22, 23, 16, 9.5, 'SCHEDULE', 'schedule_id',
                ['doctor_id'], ['day_of_week', 'start/end_time', 'slot_duration', 'max_patients'], C_DOC)

    # 8. Consultation (Center)
    draw_entity(42, 22.5, 17, 11.5, 'CONSULTATION', 'consultation_id',
                ['appointment_id', 'doctor_id', 'patient_id'], ['symptoms, exam_notes', 'clinical_notes', 'follow_up_date'], C_CLN)

    # 9. Test Order (Mid Column 4)
    draw_entity(63, 22.5, 16, 10.5, 'TEST_ORDER', 'order_id',
                ['consultation_id', 'test_id'], ['order_date, status', 'result_value', 'reference_range', 'technician_notes'], C_LAB)

    # 10. Lab Test Catalog (Mid Column 5)
    draw_entity(82, 22.5, 15.5, 10, 'LAB_TEST', 'test_id',
                ['dept_id'], ['test_name (UQ)', 'test_code (UQ)', 'standard_cost', 'turnaround_hours'], C_LAB)


    # LOWER ROW: y=9.5
    # 11. Admission (Bottom Left)
    draw_entity(3, 8, 15, 11, 'ADMISSION', 'admission_id',
                ['patient_id', 'bed_id', 'admit_doc_id'], ['admission_date', 'discharge_date', 'status (ACTIVE..)', 'UQ: 1 Active/Bed'], C_IPD)

    # 12. Bed (Lower Column 2)
    draw_entity(22, 11, 16, 9.0, 'BED', 'bed_id',
                ['ward_id'], ['bed_number', 'daily_rate', 'is_operational', 'UQ(ward, bed_no)'], C_IPD)

    # 13. Ward (Bottom-most Column 2)
    draw_entity(22, 1, 16, 8.5, 'WARD', 'ward_id',
                ['dept_id'], ['ward_name (UQ)', 'ward_type (ICU..)', 'floor_number, capacity'], C_IPD)

    # 14. Diagnosis (Below Consultation)
    draw_entity(42, 10, 17, 9.5, 'DIAGNOSIS', 'diagnosis_id',
                ['consultation_id'], ['icd10_code', 'diagnosis_name', 'severity (MILD..CRIT)', 'diagnosis_type'], C_CLN)


    # BOTTOM FINANCIALS: y=1
    # 15. Bill (Bottom Center)
    draw_entity(42, 1, 17, 7.5, 'BILL', 'bill_id',
                ['patient_id', 'consult_id', 'admission_id'], ['total, discount, tax', 'net_payable, paid_amount', 'status (UNPAID..PAID)'], C_FIN)

    # 16. Payment (Bottom Column 4)
    draw_entity(63, 1, 16, 7.5, 'PAYMENT', 'payment_id',
                ['bill_id'], ['payment_timestamp', 'amount_paid (>0)', 'method (UPI, CARD..)', 'transaction_ref (UQ)'], C_FIN)


    # ==================== CLEAN CONNECTING ARROWS ====================
    def connect(e1, e2, label, card, p1, p2, color="#94A3B8", offset=(0,0), rad=0.0):
        b1 = entity_boxes[e1]
        b2 = entity_boxes[e2]

        x1, y1 = b1[p1]
        x2, y2 = b2[p2]

        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8,
                                    shrinkA=3, shrinkB=3,
                                    mutation_scale=12,
                                    connectionstyle=f"arc3,rad={rad}"))

        mx = (x1 + x2) / 2 + offset[0]
        my = (y1 + y2) / 2 + offset[1]

        ax.text(mx, my, f" {label} \n[{card}]",
                color='#FFFFFF', fontsize=7.6, fontweight='bold',
                ha='center', va='center', zorder=5,
                bbox=dict(boxstyle="round,pad=0.25", fc='#1E293B', ec=color, lw=1.2))

    # 1. Dept -> Doctor
    connect('DEPARTMENT', 'DOCTOR', 'EMPLOYS', '1:N', 'right', 'left', '#38BDF8')
    # 2. Doctor -> Schedule
    connect('DOCTOR', 'SCHEDULE', 'ASSIGNED', '1:N', 'bottom', 'top', '#38BDF8')
    # 3. Doctor -> Appointment
    connect('DOCTOR', 'APPOINTMENT', 'ATTENDS', '1:N', 'right', 'left', '#38BDF8')
    # 4. Patient -> Appointment
    connect('PATIENT', 'APPOINTMENT', 'BOOKS', '1:N', 'top', 'left', '#34D399', offset=(3, 3), rad=0.2)
    # 5. Appointment -> Consultation
    connect('APPOINTMENT', 'CONSULTATION', 'RESULTS IN', '1:1', 'bottom', 'top', '#C084FC')
    # 6. Consultation -> Diagnosis
    connect('CONSULTATION', 'DIAGNOSIS', 'PRODUCES', '1:N', 'bottom', 'top', '#C084FC')
    # 7. Consultation -> Prescription
    connect('CONSULTATION', 'PRESCRIPTION', 'WRITES', '1:N', 'top', 'left', '#C084FC', offset=(2, 2), rad=-0.1)
    # 8. Prescription -> Prescription Item
    connect('PRESCRIPTION', 'PRESCRIPTION_ITEM', 'CONTAINS', '1:N', 'right', 'left', '#C084FC')
    # 9. Consultation -> Test Order
    connect('CONSULTATION', 'TEST_ORDER', 'ORDERS', '1:N', 'right', 'left', '#FBBF24')
    # 10. Lab Test -> Test Order
    connect('LAB_TEST', 'TEST_ORDER', 'CATALOG', '1:N', 'left', 'right', '#FBBF24')
    # 11. Ward -> Bed
    connect('WARD', 'BED', 'HOUSES', '1:N', 'top', 'bottom', '#F472B6')
    # 12. Bed -> Admission
    connect('BED', 'ADMISSION', 'ALLOCATED', '1:N', 'left', 'right', '#F472B6')
    # 13. Patient -> Admission
    connect('PATIENT', 'ADMISSION', 'UNDERGOES', '1:N', 'bottom', 'top', '#34D399')
    # 14. Admission -> Bill (curves cleanly below)
    connect('ADMISSION', 'BILL', 'CHARGES', '1:1', 'bottom', 'left', '#2DD4BF', offset=(6, -2), rad=-0.22)
    # 15. Consultation -> Bill (curves cleanly left of diagnosis)
    connect('CONSULTATION', 'BILL', 'FEES', '1:1', 'left', 'left', '#2DD4BF', offset=(-3, -3), rad=0.3)
    # 16. Bill -> Payment
    connect('BILL', 'PAYMENT', 'SETTLED BY', '1:N', 'right', 'left', '#2DD4BF')

    # Header Title Banner
    ax.text(50, 54.6, "HOSPITAL APPOINTMENT & PATIENT CARE MANAGEMENT SYSTEM",
            color='#FFFFFF', fontsize=18, fontweight='heavy', ha='center', va='center', family='sans-serif')
    ax.text(50, 52.8, "Entity-Relationship (ER) Architecture — Covering All 13 Required Entities + Normalized 3NF Relations",
            color='#38BDF8', fontsize=11.5, fontweight='semibold', ha='center', va='center', family='sans-serif')

    # Legend at Top
    legend_text = "[PK] Primary Key   |   [FK] Foreign Key   |   UQ Unique   |   1:N One-to-Many   |   1:1 One-to-One"
    ax.text(50, 50.8, legend_text,
            color='#E2E8F0', fontsize=9.2, fontweight='bold', ha='center', va='center', family='monospace',
            bbox=dict(boxstyle="round,pad=0.35", fc='#1E293B', ec='#475569', lw=1.2))

    # Save High-Res Image
    output_path = "/Users/himanshu/Documents/DBMS PBL/hospital_er_diagram.png"
    plt.tight_layout(pad=0.8)
    plt.savefig(output_path, dpi=300, facecolor='#0B1329', edgecolor='none')
    plt.close()
    print(f"ER Diagram successfully saved to: {output_path}")

if __name__ == "__main__":
    draw_er_diagram()
