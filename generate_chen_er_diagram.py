"""
Generate Chen Notation ER Diagram matching user's exact specification:
- Pure white background
- Soft green entity rectangles (#D5E8D4, border #274E13)
- Soft pink/peach relationship diamonds (#FCE5CD, border #B85450)
- Soft blue attribute ovals (#DAE8FC, border #6C8EBF)
- Underlined Primary Keys
- (FK) tagged Foreign Keys
- 1 and M cardinality labels on connection lines
- Dashed Legend box in bottom-right corner matching user's reference diagram
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def draw_chen_er():
    # 28 x 17 inches at 300 DPI for pristine resolution
    fig, ax = plt.subplots(figsize=(28, 17), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis('off')

    # Reference Colors matching user's image
    COLOR_ENTITY_FILL = '#D5E8D4'       # Soft pastel green
    COLOR_ENTITY_BORDER = '#274E13'     # Dark green border
    
    COLOR_REL_FILL = '#FCE5CD'          # Soft peach/pink
    COLOR_REL_BORDER = '#B85450'        # Soft dark red border
    
    COLOR_ATTR_FILL = '#DAE8FC'         # Soft sky blue
    COLOR_ATTR_BORDER = '#6C8EBF'       # Slate blue border
    
    COLOR_LINE = '#2B2B2B'              # Dark crisp connecting line

    # -------------------------------------------------------------------------
    # DRAWING HELPERS
    # -------------------------------------------------------------------------
    def draw_entity(x, y, w, h, name):
        """Draws a soft green entity rectangle"""
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.1,rounding_size=0.35",
                              edgecolor=COLOR_ENTITY_BORDER, facecolor=COLOR_ENTITY_FILL,
                              linewidth=1.8, zorder=4)
        ax.add_patch(rect)
        ax.text(x, y, name, color='#000000', fontsize=11.5, fontweight='bold',
                ha='center', va='center', zorder=5, family='sans-serif')
        return {'x': x, 'y': y, 'w': w, 'h': h}

    def draw_relationship(x, y, size_w, size_h, name):
        """Draws a soft pink relationship diamond"""
        pts = [
            [x, y + size_h/2],      # top
            [x + size_w/2, y],      # right
            [x, y - size_h/2],      # bottom
            [x - size_w/2, y]       # left
        ]
        diamond = Polygon(pts, closed=True,
                          edgecolor=COLOR_REL_BORDER, facecolor=COLOR_REL_FILL,
                          linewidth=1.6, zorder=4)
        ax.add_patch(diamond)
        ax.text(x, y, name, color='#000000', fontsize=9.5, fontweight='bold',
                ha='center', va='center', zorder=5, family='sans-serif')
        return {'x': x, 'y': y, 'w': size_w, 'h': size_h}

    def draw_attribute(x, y, w, h, name, is_pk=False, is_fk=False):
        """Draws a soft blue attribute oval"""
        ellipse = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                 boxstyle="round,pad=0.08,rounding_size=1.2",
                                 edgecolor=COLOR_ATTR_BORDER, facecolor=COLOR_ATTR_FILL,
                                 linewidth=1.2, zorder=3)
        ax.add_patch(ellipse)
        
        display_text = name
        if is_fk:
            display_text = f"{name} (FK)"
        
        t = ax.text(x, y, display_text, color='#000000',
                    fontsize=8.2, fontweight='normal',
                    ha='center', va='center', zorder=5, family='sans-serif')
        
        if is_pk:
            t.set_fontweight('bold')
            line_w = len(name) * 0.28
            ax.plot([x - line_w, x + line_w], [y - 0.45, y - 0.45],
                    color='#000000', linewidth=1.2, zorder=6)
            
        return {'x': x, 'y': y, 'w': w, 'h': h}

    def connect_attr(entity, attr):
        """Connects an entity box to an attribute oval"""
        ax.plot([entity['x'], attr['x']], [entity['y'], attr['y']],
                color=COLOR_LINE, linewidth=1.1, zorder=2)

    def connect_rel(entity, rel, card_label, label_pos=0.5, offset=(0, 0)):
        """Connects entity box to relationship diamond with 1 or M label"""
        ax.plot([entity['x'], rel['x']], [entity['y'], rel['y']],
                color=COLOR_LINE, linewidth=1.4, zorder=2)
        
        lx = entity['x'] + (rel['x'] - entity['x']) * label_pos + offset[0]
        ly = entity['y'] + (rel['y'] - entity['y']) * label_pos + offset[1]
        
        ax.text(lx, ly, card_label, color='#000000', fontsize=11, fontweight='bold',
                ha='center', va='center', zorder=6, family='sans-serif',
                bbox=dict(boxstyle="circle,pad=0.15", fc='#FFFFFF', ec='none'))

    # =========================================================================
    # 1. ENTITIES PLACEMENT
    # =========================================================================
    # Top Row
    e_patient = draw_entity(18, 48.5, 9.0, 3.2, 'Patient')
    e_appt = draw_entity(45, 48.5, 9.5, 3.2, 'Appointment')
    e_doctor = draw_entity(73, 48.5, 9.0, 3.2, 'Doctor')
    e_dept = draw_entity(92, 48.5, 9.2, 3.2, 'Department')

    # Middle Row
    e_admiss = draw_entity(18, 33.5, 9.0, 3.2, 'Admission')
    e_consult = draw_entity(45, 33.5, 10.2, 3.2, 'Consultation')
    e_schedule = draw_entity(73, 33.5, 9.8, 3.2, 'DoctorSchedule')

    # Lower-Middle Row
    e_bed = draw_entity(18, 19.5, 8.5, 3.2, 'Bed')
    e_diag = draw_entity(33, 21.0, 9.0, 3.2, 'Diagnosis')
    e_rx = draw_entity(47, 21.0, 9.2, 3.2, 'Prescription')
    e_test = draw_entity(61, 21.0, 9.0, 3.2, 'LabTest')

    # Bottom Row
    e_ward = draw_entity(18, 7.5, 8.5, 3.2, 'Ward')
    e_bill = draw_entity(45, 8.5, 8.5, 3.2, 'Bill')
    e_payment = draw_entity(67, 8.5, 8.5, 3.2, 'Payment')

    # =========================================================================
    # 2. RELATIONSHIPS (DIAMONDS & CARDINALITY)
    # =========================================================================
    # Patient --(1)-- <Books> --(M)-- Appointment
    r_books = draw_relationship(31.5, 48.5, 6.2, 2.8, 'Books')
    connect_rel(e_patient, r_books, '1', 0.5, (0, 0.7))
    connect_rel(e_appt, r_books, 'M', 0.5, (0, 0.7))

    # Doctor --(1)-- <Attends> --(M)-- Appointment
    r_attends = draw_relationship(59.0, 48.5, 6.5, 2.8, 'Attends')
    connect_rel(e_doctor, r_attends, '1', 0.5, (0, 0.7))
    connect_rel(e_appt, r_attends, 'M', 0.5, (0, 0.7))

    # Department --(1)-- <Employs> --(M)-- Doctor
    r_employs = draw_relationship(82.5, 48.5, 6.5, 2.8, 'Employs')
    connect_rel(e_dept, r_employs, '1', 0.5, (0, 0.7))
    connect_rel(e_doctor, r_employs, 'M', 0.5, (0, 0.7))

    # Doctor --(1)-- <Assigned> --(M)-- DoctorSchedule
    r_assigned = draw_relationship(73, 41.0, 6.8, 2.8, 'Assigned')
    connect_rel(e_doctor, r_assigned, '1', 0.5, (0.7, 0))
    connect_rel(e_schedule, r_assigned, 'M', 0.5, (0.7, 0))

    # Appointment --(1)-- <Results In> --(1)-- Consultation
    r_results = draw_relationship(45, 41.0, 7.0, 2.8, 'ResultsIn')
    connect_rel(e_appt, r_results, '1', 0.5, (0.7, 0))
    connect_rel(e_consult, r_results, '1', 0.5, (0.7, 0))

    # Consultation --(1)-- <Produces> --(M)-- Diagnosis
    r_produces = draw_relationship(38.5, 27.2, 6.5, 2.6, 'Produces')
    connect_rel(e_consult, r_produces, '1', 0.5, (0.5, 0.4))
    connect_rel(e_diag, r_produces, 'M', 0.5, (-0.5, -0.4))

    # Consultation --(1)-- <Generates> --(M)-- Prescription
    r_prescribes = draw_relationship(46.0, 27.2, 6.8, 2.6, 'Prescribes')
    connect_rel(e_consult, r_prescribes, '1', 0.5, (0.6, 0))
    connect_rel(e_rx, r_prescribes, 'M', 0.5, (0.6, 0))

    # Consultation --(1)-- <Orders> --(M)-- LabTest
    r_orders = draw_relationship(53.5, 27.2, 6.5, 2.6, 'Orders')
    connect_rel(e_consult, r_orders, '1', 0.5, (-0.5, 0.4))
    connect_rel(e_test, r_orders, 'M', 0.5, (0.5, -0.4))

    # Patient --(1)-- <Undergoes> --(M)-- Admission
    r_undergoes = draw_relationship(18, 41.0, 7.0, 2.8, 'Undergoes')
    connect_rel(e_patient, r_undergoes, '1', 0.5, (0.7, 0))
    connect_rel(e_admiss, r_undergoes, 'M', 0.5, (0.7, 0))

    # Bed --(1)-- <Allocated For> --(M)-- Admission
    r_alloc = draw_relationship(18, 26.5, 7.2, 2.8, 'AllocatedFor')
    connect_rel(e_bed, r_alloc, '1', 0.5, (0.7, 0))
    connect_rel(e_admiss, r_alloc, 'M', 0.5, (0.7, 0))

    # Ward --(1)-- <Houses> --(M)-- Bed
    r_houses = draw_relationship(18, 13.5, 6.5, 2.8, 'Houses')
    connect_rel(e_ward, r_houses, '1', 0.5, (0.7, 0))
    connect_rel(e_bed, r_houses, 'M', 0.5, (0.7, 0))

    # Patient --(1)-- <Billed To> --(M)-- Bill
    ax.plot([13.5, 2.0, 2.0, 40.75],
            [48.5, 48.5, 8.5, 8.5],
            color=COLOR_LINE, linewidth=1.4, zorder=2)
    r_billed = draw_relationship(2.0, 28.5, 6.2, 2.8, 'BilledTo')
    ax.text(2.0, 31.8, '1', color='#000000', fontsize=11, fontweight='bold', zorder=6, ha='center',
            bbox=dict(boxstyle="circle,pad=0.15", fc='#FFFFFF', ec='none'))
    ax.text(2.0, 25.2, 'M', color='#000000', fontsize=11, fontweight='bold', zorder=6, ha='center',
            bbox=dict(boxstyle="circle,pad=0.15", fc='#FFFFFF', ec='none'))

    # Bill --(1)-- <Paid Through> --(M)-- Payment
    r_paid = draw_relationship(56, 8.5, 7.0, 2.8, 'PaidThrough')
    connect_rel(e_bill, r_paid, '1', 0.5, (0, 0.7))
    connect_rel(e_payment, r_paid, 'M', 0.5, (0, 0.7))

    # =========================================================================
    # 3. ATTRIBUTE OVALS (RADIATING WITH CONNECTING LINES)
    # =========================================================================
    def add_attr_set(entity, attr_specs):
        for (x, y, w, h, name, is_pk, is_fk) in attr_specs:
            a = draw_attribute(x, y, w, h, name, is_pk, is_fk)
            connect_attr(entity, a)

    # PATIENT ATTRIBUTES
    p_attrs = [
        (5.5, 58.0, 6.2, 1.8, 'PatientID', True, False),
        (5.5, 55.5, 6.2, 1.8, 'FirstName', False, False),
        (5.5, 53.0, 6.2, 1.8, 'LastName', False, False),
        (5.5, 50.5, 6.2, 1.8, 'DOB', False, False),
        (5.5, 48.0, 6.2, 1.8, 'Gender', False, False),
        (5.5, 45.5, 6.2, 1.8, 'BloodGroup', False, False),
        (5.5, 43.0, 6.2, 1.8, 'Phone', False, False),
        (5.5, 40.5, 6.2, 1.8, 'Email', False, False),
        (13.5, 57.5, 6.5, 1.8, 'EmergencyContact', False, False),
        (22.0, 57.5, 5.5, 1.8, 'Address', False, False)
    ]
    add_attr_set(e_patient, p_attrs)

    # APPOINTMENT ATTRIBUTES
    appt_attrs = [
        (33.0, 57.5, 6.5, 1.8, 'AppointmentID', True, False),
        (41.0, 57.5, 6.2, 1.8, 'PatientID', False, True),
        (49.0, 57.5, 6.2, 1.8, 'DoctorID', False, True),
        (57.0, 57.5, 6.8, 1.8, 'AppointmentDate', False, False),
        (37.5, 44.5, 5.5, 1.8, 'StartTime', False, False),
        (44.0, 44.5, 5.5, 1.8, 'EndTime', False, False),
        (51.0, 44.5, 5.5, 1.8, 'Status', False, False)
    ]
    add_attr_set(e_appt, appt_attrs)

    # DOCTOR ATTRIBUTES
    doc_attrs = [
        (66.0, 57.5, 6.0, 1.8, 'DoctorID', True, False),
        (74.0, 57.5, 6.2, 1.8, 'DepartmentID', False, True),
        (82.0, 57.5, 6.2, 1.8, 'Specialization', False, False),
        (82.5, 45.0, 5.5, 1.8, 'FirstName', False, False),
        (82.5, 42.5, 5.5, 1.8, 'LastName', False, False),
        (82.5, 40.0, 6.0, 1.8, 'Qualification', False, False),
        (82.5, 37.5, 5.5, 1.8, 'Phone', False, False),
        (82.5, 35.0, 6.4, 1.8, 'ConsultationFee', False, False)
    ]
    add_attr_set(e_doctor, doc_attrs)

    # DEPARTMENT ATTRIBUTES
    dept_attrs = [
        (92.0, 57.5, 6.5, 1.8, 'DepartmentID', True, False),
        (92.0, 54.5, 6.8, 1.8, 'DepartmentName', False, False),
        (92.0, 43.0, 6.5, 1.8, 'BuildingBlock', False, False),
        (92.0, 40.5, 6.0, 1.8, 'FloorNumber', False, False),
        (92.0, 38.0, 6.5, 1.8, 'HeadDoctorID', False, True)
    ]
    add_attr_set(e_dept, dept_attrs)

    # DOCTOR SCHEDULE ATTRIBUTES
    sched_attrs = [
        (88.0, 31.5, 6.2, 1.8, 'ScheduleID', True, False),
        (88.0, 29.0, 6.0, 1.8, 'DoctorID', False, True),
        (88.0, 26.5, 6.0, 1.8, 'DayOfWeek', False, False),
        (74.0, 27.5, 5.8, 1.8, 'StartTime', False, False),
        (74.0, 25.0, 5.8, 1.8, 'EndTime', False, False),
        (74.0, 22.5, 6.2, 1.8, 'SlotDuration', False, False)
    ]
    add_attr_set(e_schedule, sched_attrs)

    # CONSULTATION ATTRIBUTES
    consult_attrs = [
        (34.0, 38.0, 6.5, 1.8, 'ConsultationID', True, False),
        (34.0, 35.5, 6.5, 1.8, 'AppointmentID', False, True),
        (56.0, 38.0, 5.5, 1.8, 'DoctorID', False, True),
        (56.0, 35.5, 5.5, 1.8, 'PatientID', False, True),
        (34.0, 33.0, 5.5, 1.8, 'Symptoms', False, False),
        (56.0, 33.0, 6.0, 1.8, 'ClinicalNotes', False, False)
    ]
    add_attr_set(e_consult, consult_attrs)

    # DIAGNOSIS ATTRIBUTES
    diag_attrs = [
        (25.0, 16.5, 6.2, 1.8, 'DiagnosisID', True, False),
        (25.0, 14.0, 6.5, 1.8, 'ConsultationID', False, True),
        (33.0, 16.5, 5.8, 1.8, 'ICD10Code', False, False),
        (33.0, 14.0, 6.2, 1.8, 'DiagnosisName', False, False),
        (33.0, 11.5, 5.5, 1.8, 'Severity', False, False)
    ]
    add_attr_set(e_diag, diag_attrs)

    # PRESCRIPTION ATTRIBUTES
    rx_attrs = [
        (44.0, 16.0, 6.5, 1.8, 'PrescriptionID', True, False),
        (44.0, 13.5, 6.5, 1.8, 'ConsultationID', False, True),
        (51.5, 16.0, 6.2, 1.8, 'MedicineName', False, False),
        (51.5, 13.5, 5.5, 1.8, 'Dosage', False, False),
        (51.5, 11.0, 5.5, 1.8, 'DurationDays', False, False)
    ]
    add_attr_set(e_rx, rx_attrs)

    # LAB TEST ATTRIBUTES
    test_attrs = [
        (61.0, 16.0, 5.8, 1.8, 'TestID', True, False),
        (61.0, 13.5, 6.2, 1.8, 'DepartmentID', False, True),
        (68.0, 18.0, 5.8, 1.8, 'TestName', False, False),
        (68.0, 15.5, 6.0, 1.8, 'StandardCost', False, False),
        (68.0, 13.0, 6.2, 1.8, 'TurnaroundHrs', False, False)
    ]
    add_attr_set(e_test, test_attrs)

    # ADMISSION ATTRIBUTES
    adm_attrs = [
        (8.5, 37.5, 6.2, 1.8, 'AdmissionID', True, False),
        (8.5, 35.0, 5.8, 1.8, 'PatientID', False, True),
        (8.5, 32.5, 5.5, 1.8, 'BedID', False, True),
        (8.5, 30.0, 5.8, 1.8, 'DoctorID', False, True),
        (26.0, 36.5, 6.2, 1.8, 'AdmissionDate', False, False),
        (26.0, 34.0, 6.2, 1.8, 'DischargeDate', False, False),
        (26.0, 31.5, 5.5, 1.8, 'Status', False, False)
    ]
    add_attr_set(e_admiss, adm_attrs)

    # BED ATTRIBUTES
    bed_attrs = [
        (8.5, 22.0, 5.5, 1.8, 'BedID', True, False),
        (8.5, 19.5, 5.8, 1.8, 'WardID', False, True),
        (8.5, 17.0, 5.8, 1.8, 'BedNumber', False, False),
        (8.5, 14.5, 5.8, 1.8, 'DailyRate', False, False)
    ]
    add_attr_set(e_bed, bed_attrs)

    # WARD ATTRIBUTES
    ward_attrs = [
        (8.5, 9.5, 5.5, 1.8, 'WardID', True, False),
        (8.5, 7.0, 6.0, 1.8, 'DepartmentID', False, True),
        (8.5, 4.5, 5.8, 1.8, 'WardName', False, False),
        (8.5, 2.0, 5.5, 1.8, 'Capacity', False, False)
    ]
    add_attr_set(e_ward, ward_attrs)

    # BILL ATTRIBUTES
    bill_attrs = [
        (35.0, 4.5, 5.5, 1.8, 'BillID', True, False),
        (35.0, 2.0, 5.8, 1.8, 'PatientID', False, True),
        (42.0, 4.5, 6.2, 1.8, 'TotalAmount', False, False),
        (42.0, 2.0, 6.2, 1.8, 'DiscountAmount', False, False),
        (49.0, 4.5, 5.8, 1.8, 'NetPayable', False, False),
        (49.0, 2.0, 5.8, 1.8, 'PaymentStatus', False, False)
    ]
    add_attr_set(e_bill, bill_attrs)

    # PAYMENT ATTRIBUTES
    pay_attrs = [
        (60.0, 4.5, 5.8, 1.8, 'PaymentID', True, False),
        (60.0, 2.0, 5.5, 1.8, 'BillID', False, True),
        (67.0, 4.5, 6.0, 1.8, 'PaymentDate', False, False),
        (67.0, 2.0, 5.8, 1.8, 'AmountPaid', False, False),
        (74.0, 4.5, 6.2, 1.8, 'PaymentMethod', False, False),
        (74.0, 2.0, 6.5, 1.8, 'TransactionRef', False, False)
    ]
    add_attr_set(e_payment, pay_attrs)

    # =========================================================================
    # 4. LEGEND BOX (EXACT MATCH TO REFERENCE IMAGE)
    # =========================================================================
    leg_box = FancyBboxPatch((80.5, 1.0), 18.5, 14.0,
                             boxstyle="round,pad=0.2,rounding_size=0.6",
                             edgecolor='#444444', facecolor='#FFFFFF',
                             linestyle='--', linewidth=1.5, zorder=10)
    ax.add_patch(leg_box)

    ax.text(89.75, 13.8, "LEGEND", color='#000000', fontsize=11.5, fontweight='bold',
            ha='center', va='center', zorder=11, family='sans-serif')

    # Legend Item 1: Entity (green box)
    leg_ent = FancyBboxPatch((82.0, 10.8), 3.4, 1.5,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                              edgecolor=COLOR_ENTITY_BORDER, facecolor=COLOR_ENTITY_FILL,
                              linewidth=1.4, zorder=11)
    ax.add_patch(leg_ent)
    ax.text(86.8, 11.5, "Entity", color='#000000', fontsize=9.5, fontweight='medium',
            ha='left', va='center', zorder=11)

    # Legend Item 2: Relationship (pink diamond)
    leg_rel_pts = [[83.7, 10.2], [85.4, 9.4], [83.7, 8.6], [82.0, 9.4]]
    leg_rel = Polygon(leg_rel_pts, closed=True,
                      edgecolor=COLOR_REL_BORDER, facecolor=COLOR_REL_FILL,
                      linewidth=1.4, zorder=11)
    ax.add_patch(leg_rel)
    ax.text(86.8, 9.4, "Relationship", color='#000000', fontsize=9.5, fontweight='medium',
            ha='left', va='center', zorder=11)

    # Legend Item 3: Attribute (blue oval)
    leg_attr = FancyBboxPatch((82.0, 6.7), 3.4, 1.4,
                              boxstyle="round,pad=0.05,rounding_size=0.8",
                              edgecolor=COLOR_ATTR_BORDER, facecolor=COLOR_ATTR_FILL,
                              linewidth=1.2, zorder=11)
    ax.add_patch(leg_attr)
    ax.text(86.8, 7.4, "Attribute", color='#000000', fontsize=9.5, fontweight='medium',
            ha='left', va='center', zorder=11)

    # Legend Explanations (right side of box)
    ax.text(91.8, 11.2, "Underlined", color='#000000', fontsize=9.2, fontweight='bold',
            ha='left', va='center', zorder=11)
    ax.plot([91.8, 96.6], [10.7, 10.7], color='#000000', linewidth=1.1, zorder=11)
    ax.text(91.8, 9.8, "= Primary Key", color='#000000', fontsize=9.0,
            ha='left', va='center', zorder=11)

    ax.text(91.8, 7.8, "(FK) = Foreign Key", color='#000000', fontsize=9.0, fontweight='bold',
            ha='left', va='center', zorder=11)
    ax.text(91.8, 5.8, "1   = One", color='#000000', fontsize=9.0,
            ha='left', va='center', zorder=11)
    ax.text(91.8, 4.0, "M  = Many", color='#000000', fontsize=9.0,
            ha='left', va='center', zorder=11)

    # Title Header (Top of Diagram)
    ax.text(50, 61.0, "HOSPITAL APPOINTMENT & PATIENT CARE MANAGEMENT SYSTEM",
            color='#0F172A', fontsize=18, fontweight='heavy', ha='center', va='center', family='sans-serif')
    ax.text(50, 59.5, "Entity-Relationship (ER) Model — Classical Chen Notation",
            color='#0D9488', fontsize=11.5, fontweight='bold', ha='center', va='center', family='sans-serif')

    output_path = "/Users/himanshu/Documents/DBMS PBL/hospital_er_diagram.png"
    plt.tight_layout(pad=0.5)
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
    plt.close()
    print(f"Classical Chen ER Diagram successfully saved to: {output_path}")

if __name__ == "__main__":
    draw_chen_er()
