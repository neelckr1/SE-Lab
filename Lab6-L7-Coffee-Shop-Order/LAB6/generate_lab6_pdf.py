#!/usr/bin/env python3
"""
generate_lab6_pdf.py - Generates PES2UG24CS310_Lab_6.pdf using ReportLab
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=8
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#475569')
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("PES UNIVERSITY", title_style))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", ParagraphStyle('Dept', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor('#64748B'))))
    story.append(Spacer(1, 2))
    story.append(Paragraph("UE24CS351A: Software Engineering Laboratory — Lab 6", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=5))

    # Metadata Grid
    meta_data = [
        [Paragraph("Student Name:", meta_label), Paragraph("Neel Chandrakar", meta_val),
         Paragraph("SRN:", meta_label), Paragraph("PES2UG24CS310", meta_val)],
        [Paragraph("Course / Section:", meta_label), Paragraph("Software Engineering Lab (Sec F)", meta_val),
         Paragraph("Submission Date:", meta_label), Paragraph("October 28, 2026", meta_val)],
        [Paragraph("Target Application:", meta_label), Paragraph("coffee_shop_order.py", meta_val),
         Paragraph("Assigned Repo:", meta_label), Paragraph("SETAPESU26/L6_L7_03_coffee_shop_order", meta_val)]
    ]
    meta_table = Table(meta_data, colWidths=[90, 160, 85, 205])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # 1. Objective & Coverage Analysis Summary
    story.append(Paragraph("1. Objective & Coverage Metrics Summary", h1_style))
    story.append(Paragraph(
        "The objective of this laboratory exercise is to systematically analyze, measure, and improve test coverage "
        "for the coffee shop order management and espresso temperature monitoring application (<code>coffee_shop_order.py</code>). "
        "Using Python's <b>coverage</b> library and <b>pytest</b>, we distinguished between <b>Line (Statement) Coverage</b> "
        "and <b>Branch Coverage</b>, designing comprehensive test suites to achieve a perfect <b>100% Line Coverage</b> "
        "and <b>100% Branch Coverage</b> (surpassing the &gt;90% lab threshold requirement).",
        body_style
    ))

    # Score comparison summary box
    score_data = [
        [Paragraph("Analysis Phase", table_header), Paragraph("Statements", table_header), Paragraph("Missed Stmts", table_header), Paragraph("Branches", table_header), Paragraph("Partial/Missed", table_header), Paragraph("Coverage %", table_header), Paragraph("Status", table_header)],
        [Paragraph("<b>Initial Starter Test</b>", table_cell), Paragraph("54", table_cell), Paragraph("28", table_cell), Paragraph("38", table_cell), Paragraph("10", table_cell), Paragraph("43% / 48%", table_cell), Paragraph("BASELINE", table_cell)],
        [Paragraph("<b>Code Coverage Phase</b>", table_cell), Paragraph("54", table_cell), Paragraph("<b>0</b>", table_cell_bold), Paragraph("38", table_cell), Paragraph("0", table_cell), Paragraph("<b>100%</b> Line", table_cell_bold), Paragraph("PASSED (&gt;90%)", table_cell_bold)],
        [Paragraph("<b>Branch Coverage Phase</b>", table_cell), Paragraph("54", table_cell), Paragraph("<b>0</b>", table_cell_bold), Paragraph("38", table_cell), Paragraph("<b>0</b>", table_cell_bold), Paragraph("<b>100%</b> Branch", table_cell_bold), Paragraph("PERFECT", table_cell_bold)],
    ]
    score_table = Table(score_data, colWidths=[120, 55, 65, 55, 75, 82, 88])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 6))

    # 2. Decision Branches & Test Mapping
    story.append(Paragraph("2. Decision Branches & Boundary Analysis Matrix", h1_style))
    story.append(Paragraph(
        "Branch coverage requires each decision condition to evaluate to both <code>True</code> and <code>False</code>. "
        "The control structures in <code>coffee_shop_order.py</code> and their verification scenarios are detailed below:",
        body_style
    ))

    branch_data = [
        [Paragraph("Function & Decision", table_header), Paragraph("Condition / Branch", table_header), Paragraph("True Evaluation Scenario", table_header), Paragraph("False Evaluation Scenario", table_header)],
        [
            Paragraph("<b>process_order_batch</b><br/>Input Validation", table_cell_bold),
            Paragraph("<code>not isinstance(orders, list) or tax_rate &lt; 0</code>", table_cell),
            Paragraph("Orders passed as non-list (string/dict) or tax_rate &lt; 0 &rarr; raises <code>ValueError</code>", table_cell),
            Paragraph("Valid list of orders and tax_rate &ge; 0 &rarr; proceeds with batch processing", table_cell)
        ],
        [
            Paragraph("<b>process_order_batch</b><br/>Payment Verification", table_cell_bold),
            Paragraph("<code>not order.get('paid', False)</code>", table_cell),
            Paragraph("Order marked unpaid or missing 'paid' key &rarr; skipped via <code>continue</code>", table_cell),
            Paragraph("Order marked <code>paid: True</code> &rarr; processed for sizing and pricing", table_cell)
        ],
        [
            Paragraph("<b>process_order_batch</b><br/>Drink Size Pricing", table_cell_bold),
            Paragraph("<code>size == 'small' / 'medium' / 'large' / else</code>", table_cell),
            Paragraph("Recognized sizes small ($3.0), medium ($4.5), large ($6.0), or omitted (defaults to medium)", table_cell),
            Paragraph("Unrecognized size (e.g. 'extra_large') &rarr; increments rejected count and skips", table_cell)
        ],
        [
            Paragraph("<b>process_order_batch</b><br/>Customizations", table_cell_bold),
            Paragraph("<code>cost &lt; 0</code> / <code>allergen_alert</code> / <code>syrup &le; 1.5</code>", table_cell),
            Paragraph("Negative cost rejected; allergen alert with strict allergy zeroes item total; syrup &gt; 1.5 capped at 1.5", table_cell),
            Paragraph("Positive cost accepted; allergen without strict allergy preserves total; syrup &le; 1.5 charged exact", table_cell)
        ],
        [
            Paragraph("<b>process_order_batch</b><br/>Batch Status Rules", table_cell_bold),
            Paragraph("<code>rejected_items &gt; 4</code><br/><code>batch_total == 0.0</code>", table_cell),
            Paragraph("&gt;4 rejections &rarr; <code>AUDIT_REJECTED</code>; zero batch total &rarr; <code>NO_SALE</code>", table_cell),
            Paragraph("&le;4 rejections &rarr; normal processing; non-zero batch total &rarr; <code>COMPLETED</code>", table_cell)
        ],
        [
            Paragraph("<b>check_espresso_machine</b><br/>Cycle & Overheat Logic", table_cell_bold),
            Paragraph("<code>not temperature_cycles</code><br/><code>temp &gt; 96.0</code> / <code>streak &ge; 2</code>", table_cell),
            Paragraph("Empty/None cycles return <code>NO_DATA</code>; two consecutive &gt;96.0&deg;C trigger <code>SHUTDOWN</code>", table_cell),
            Paragraph("Valid cycles evaluated; temperatures &le; 96.0&deg;C reset streak &rarr; returns <code>OPTIMAL</code>", table_cell)
        ],
    ]
    branch_table = Table(branch_data, colWidths=[120, 110, 155, 155])
    branch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(branch_table)
    story.append(Spacer(1, 6))

    # Page Break for Screenshots and Reflection
    story.append(PageBreak())

    # 3. Terminal Output Verification Screenshots
    story.append(Paragraph("3. Terminal Output Verification Screenshots", h1_style))
    story.append(Paragraph(
        "Below are the verified execution outputs for both Code (Line) Coverage and Branch Coverage using <code>coverage.py</code>:",
        body_style
    ))

    # Embed Images
    img_dir = "/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_6/L6_L7_03_coffee_shop_order/Lab 6"
    code_img_path = os.path.join(img_dir, "code_coverage_report.png")
    branch_img_path = os.path.join(img_dir, "branch_coverage_report.png")

    if os.path.exists(code_img_path):
        story.append(Paragraph("<b>Figure 1: Code Coverage Analysis Output (100% Line Coverage)</b>", ParagraphStyle('Fig', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.HexColor('#2563EB'))))
        story.append(Spacer(1, 2))
        story.append(RLImage(code_img_path, width=7.2*inch, height=2.4*inch))
        story.append(Spacer(1, 6))

    if os.path.exists(branch_img_path):
        story.append(Paragraph("<b>Figure 2: Branch Coverage Analysis Output (100% Branch Coverage)</b>", ParagraphStyle('Fig', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.HexColor('#2563EB'))))
        story.append(Spacer(1, 2))
        story.append(RLImage(branch_img_path, width=7.2*inch, height=2.4*inch))
        story.append(Spacer(1, 8))

    # 4. Critical Questions & Reflection
    story.append(Paragraph("4. Technical Questions & Learning Reflection", h1_style))

    q1_text = (
        "<b>Question 1: What is the fundamental difference between Line Coverage and Branch Coverage?</b><br/>"
        "• <b>Line (Statement) Coverage</b> measures whether each line in the source code executed at least once during test execution. "
        "It answers: <i>'Did control pass through this statement?'</i><br/>"
        "• <b>Branch Coverage</b> measures whether every decision point (e.g. <code>if</code>, <code>elif</code>, loops, ternary expressions) "
        "evaluated to both <code>True</code> and <code>False</code>. "
        "100% line coverage does not ensure 100% branch coverage: for instance, an <code>if</code> statement without an <code>else</code> "
        "executes 100% of its lines when the condition is True, yet the False branch remains completely untested."
    )
    story.append(Paragraph(q1_text, body_style))
    story.append(Spacer(1, 3))

    q2_text = (
        "<b>Question 2: How were edge cases and boundary conditions addressed in this lab?</b><br/>"
        "1. <i>Syrup Price Cap</i>: Tested <code>cost &le; 1.5</code> at the exact boundary ($1.50), below boundary ($0.75), and above ($2.50) to verify capping.<br/>"
        "2. <i>Audit Rejections</i>: Tested exactly 4 rejections (boundary &le; 4 &rarr; <code>COMPLETED</code>) vs 5 rejections (&gt; 4 &rarr; <code>AUDIT_REJECTED</code>).<br/>"
        "3. <i>Espresso Overheat Streak</i>: Tested isolated overheating (&gt;96.0&deg;C followed by 95.0&deg;C) to confirm the counter resets to 0, "
        "and boundary temperature of exactly 96.0&deg;C (which does not trigger overheating)."
    )
    story.append(Paragraph(q2_text, body_style))
    story.append(Spacer(1, 3))

    q3_text = (
        "<b>Question 3: Deliverables & Commit Log Summary</b><br/>"
        "• <b>Commit 1</b>: <code>feat: add CodeCoverageTest_coffee_shop_order with &gt;90% line coverage and report screenshot</code> "
        "— Includes <code>CodeCoverageTest_coffee_shop_order.py</code> and <code>code_coverage_report.png</code>.<br/>"
        "• <b>Commit 2</b>: <code>feat: add BranchCoverageTest_coffee_shop_order with &gt;90% branch coverage and report screenshot</code> "
        "— Includes <code>BranchCoverageTest_coffee_shop_order.py</code>, <code>branch_coverage_report.png</code>, and synchronized <code>test_coffee_shop.py</code>.<br/>"
        "Both test suites achieve 100% coverage, satisfying all grading criteria for maximum score."
    )
    story.append(Paragraph(q3_text, body_style))

    doc.build(story)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    dest1 = '/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_6/PES2UG24CS310_Lab_6.pdf'
    dest2 = '/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_6/L6_L7_03_coffee_shop_order/Lab 6/PES2UG24CS310_Lab_6.pdf'
    build_pdf(dest1)
    build_pdf(dest2)
