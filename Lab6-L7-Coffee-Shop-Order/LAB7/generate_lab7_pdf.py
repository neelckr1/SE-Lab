#!/usr/bin/env python3
"""
generate_lab7_pdf.py - Generates PES2UG24CS310_Lab_7.pdf using ReportLab
Course: UE24CS351A: Software Engineering Laboratory
Student: Neel Chandrakar (PES2UG24CS310)
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
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )

    dept_style = ParagraphStyle(
        'Dept',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#64748B')
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=6
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_code = ParagraphStyle(
        'TableCellCode',
        fontName='Courier',
        fontSize=6.5,
        leading=9,
        textColor=colors.HexColor('#0F172A')
    )

    fig_caption = ParagraphStyle(
        'FigCaption',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=3
    )

    story = []

    # ================= PAGE 1 =================
    # Title & Subtitle
    story.append(Paragraph("PES UNIVERSITY", title_style))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", dept_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("UE24CS351A: Software Engineering Laboratory — Lab 7: Fuzzing for Input Validation Bugs", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=5))

    # Student Metadata Table
    meta_data = [
        [Paragraph("Student Name:", meta_label), Paragraph("Neel Chandrakar", meta_val),
         Paragraph("SRN:", meta_label), Paragraph("PES2UG24CS310", meta_val)],
        [Paragraph("Course / Section:", meta_label), Paragraph("Software Engineering Lab (Sec F)", meta_val),
         Paragraph("Semester:", meta_label), Paragraph("5th Semester, B.Tech CSE", meta_val)],
        [Paragraph("Target Script:", meta_label), Paragraph("processor.py & test_processor.py", meta_val),
         Paragraph("Assigned Repo:", meta_label), Paragraph("neelckr1/L6_L7_03_coffee_shop_order", meta_val)]
    ]
    meta_table = Table(meta_data, colWidths=[85, 175, 80, 200])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # Section 1: Objective & Hypothesis Fuzzing Background
    story.append(Paragraph("1. Objective & Hypothesis Property-Based Fuzz Testing Methodology", h1_style))
    story.append(Paragraph(
        "<b>Objective:</b> Explore fuzz testing as an automated quality assurance and security technique by identifying "
        "and remediating input validation vulnerabilities in an order-processing pipeline (<code>processor.py</code>) using the "
        "<b>Hypothesis</b> property-based fuzzing framework in Python.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Fuzzing vs Traditional Unit Testing:</b> Traditional unit tests validate only expected inputs, standard scenarios, "
        "and developer-anticipated edge cases. In contrast, <i>Hypothesis</i> automatically generates thousands of semi-random, malformed, "
        "and boundary inputs (e.g., <code>None</code>, empty strings, Unicode characters, surrogate pairs, invalid delimiters) across "
        "strategies like <code>st.text() | st.none()</code>. When a property assertion fails, Hypothesis triggers an automated "
        "<b>shrinking algorithm</b> to find the minimal counterexample that triggers the crash, enabling rapid root-cause isolation.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Section 2: Vulnerability Analysis & Hardening Matrix
    story.append(Paragraph("2. Root Cause Analysis & Defensive Hardening Matrix", h1_style))
    vuln_headers = [
        Paragraph("Function", table_header),
        Paragraph("Fuzz Inputs / Minimal Example", table_header),
        Paragraph("Exception / Vulnerability", table_header),
        Paragraph("Root Cause", table_header),
        Paragraph("Defensive Hardening Resolution", table_header)
    ]
    vuln_rows = [
        vuln_headers,
        [
            Paragraph("<b>lookup_drink_code</b>", table_cell),
            Paragraph("• <code>s=None</code><br/>• <code>s=''</code><br/>• <code>code='MOc'</code><br/>• <code>code='XYZ'</code>", table_cell),
            Paragraph("• <code>AttributeError</code><br/>• <code>KeyError: ''</code><br/>• <code>KeyError: 'MOC'</code>", table_cell),
            Paragraph("1. Direct method call <code>.upper()</code> on <code>None</code>.<br/>2. Key indexing <code>menu_prices[...]</code> with missing keys.<br/>3. Typo key <code>'MOc'</code> in dictionary while input is converted to uppercase <code>'MOC'</code>.", table_cell),
            Paragraph("• Enforce <code>isinstance(s, str)</code>.<br/>• Strip whitespace and extract first 3 chars.<br/>• Correct dictionary key to <code>'MOC': 5.00</code>.<br/>• Use safe <code>menu_prices.get(prefix, None)</code>.", table_cell)
        ],
        [
            Paragraph("<b>calculate_average_shot_cost</b>", table_cell),
            Paragraph("• <code>s=None</code><br/>• <code>s=''</code><br/>• <code>s='1.0,abc'</code><br/>• <code>s='-2.0,nan'</code>", table_cell),
            Paragraph("• <code>AttributeError</code><br/>• <code>ValueError</code><br/>• <code>ZeroDivisionError</code>", table_cell),
            Paragraph("1. Direct <code>split(',')</code> on <code>None</code>.<br/>2. Unhandled <code>float(p)</code> parsing non-numeric strings or empty tokens.<br/>3. Dividing by <code>len(prices)</code> when list is empty yields zero division.", table_cell),
            Paragraph("• Validate string type.<br/>• Tokenize and strip whitespace.<br/>• Filter tokens via <code>try-except ValueError</code>.<br/>• Ignore NaNs, infinities, and negatives.<br/>• Gracefully return <code>0.0</code> if no valid floats exist.", table_cell)
        ],
        [
            Paragraph("<b>parse_order_modifiers</b>", table_cell),
            Paragraph("• <code>s=None</code><br/>• <code>s=''</code><br/>• <code>s='milk'</code><br/>• <code>s='a:b:c'</code>", table_cell),
            Paragraph("• <code>AttributeError</code><br/>• <code>ValueError</code> (unpack 1 value)<br/>• <code>ValueError</code> (unpack 3 values)", table_cell),
            Paragraph("1. Direct <code>split(';')</code> on <code>None</code>.<br/>2. Strict two-tuple unpack <code>k, v = item.split(':')</code> crashes if colon is missing or appears more than once.<br/>3. Trailing semicolons generate empty strings.", table_cell),
            Paragraph("• Validate string type.<br/>• Split by <code>;</code> and discard empty items.<br/>• Verify <code>':' in item</code> before parsing.<br/>• Restrict to first delimiter via <code>split(':', 1)</code>.<br/>• Strip key/val; ignore empty keys.", table_cell)
        ]
    ]

    vuln_table = Table(vuln_rows, colWidths=[95, 95, 95, 125, 130])
    vuln_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(vuln_table)
    story.append(Spacer(1, 5))

    # Section 3: Hypothesis Strategies Implemented
    story.append(Paragraph("3. Fuzzing Test Suites & Strategies Implemented", h1_style))
    story.append(Paragraph(
        "To satisfy the lab requirements and achieve exhaustive test coverage, <b>6 fuzz testing properties</b> were implemented in <code>test_processor.py</code>:<br/>"
        "• <b>Broad Crash Resilience:</b> <code>@given(st.text() | st.none())</code> applied across all three functions to guarantee that no arbitrary string or null reference triggers an unhandled exception.<br/>"
        "• <b>Targeted Drink Lookup:</b> <code>@given(st.sampled_from(...))</code> testing valid menu codes (case variants, <code>'MOc'</code>, <code>'MOC'</code>), invalid codes (<code>'XYZ'</code>), spaces, and <code>None</code>.<br/>"
        "• <b>Numeric Robustness:</b> <code>@given(st.lists(st.floats(...)))</code> generating dynamic float lists, testing boundary costs, zero-shot orders, and formatted CSV strings.<br/>"
        "• <b>Delimiter Integrity:</b> <code>@given(st.lists(st.tuples(...)))</code> synthesizing varied key-value pairs separated by semicolons and colons to ensure zero parse failures.",
        body_style
    ))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("4. Before-Fix Execution & Fuzzing Failure Verification", h1_style))
    story.append(Paragraph(
        "Below are the verified execution traces before applying defensive fixes. The original application ran successfully on the happy path "
        "but crashed immediately when presented with boundary conditions (such as the <code>'MOc'</code> casing bug or malformed CSV/modifier strings). "
        "Running Hypothesis immediately surfaced the minimal falsifying inputs:",
        body_style
    ))
    story.append(Spacer(1, 3))

    img_dir = "/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_7/L6_L7_03_coffee_shop_order/Lab 7"
    img1_path = os.path.join(img_dir, "Lab7_Original_Buggy_Output.png")
    img2_path = os.path.join(img_dir, "Lab7_Fuzz_Test_Failures.png")

    if os.path.exists(img1_path):
        story.append(Paragraph("<b>Figure 1: Buggy processor.py Terminal Output (Happy Path & Unhandled Crashes)</b>", fig_caption))
        story.append(RLImage(img1_path, width=7.2*inch, height=3.2*inch))
        story.append(Spacer(1, 8))

    if os.path.exists(img2_path):
        story.append(Paragraph("<b>Figure 2: Failing Hypothesis Fuzz Test Run (Minimal Counterexamples Discovered)</b>", fig_caption))
        story.append(RLImage(img2_path, width=7.2*inch, height=4.2*inch))
        story.append(Spacer(1, 6))

    # ================= PAGE 3 =================
    story.append(PageBreak())
    story.append(Paragraph("5. Hardened Application Execution & Passing Fuzz Tests", h1_style))
    story.append(Paragraph(
        "After applying defensive hardening and sanitization across all three functions, the application gracefully processes both valid "
        "and severely malformed inputs. Re-running the Hypothesis fuzz suite confirms that all 6 property tests pass 100% of generated test cases:",
        body_style
    ))
    story.append(Spacer(1, 3))

    img3_path = os.path.join(img_dir, "Lab7_Fixed_Application_Output.png")
    img4_path = os.path.join(img_dir, "Lab7_Passing_Fuzz_Tests.png")

    if os.path.exists(img3_path):
        story.append(Paragraph("<b>Figure 3: Hardened processor.py Terminal Output (Graceful Degradation & Fixed 'MOc')</b>", fig_caption))
        story.append(RLImage(img3_path, width=7.2*inch, height=2.8*inch))
        story.append(Spacer(1, 8))

    if os.path.exists(img4_path):
        story.append(Paragraph("<b>Figure 4: Passing Hypothesis Fuzz Tests (100% Property Verification)</b>", fig_caption))
        story.append(RLImage(img4_path, width=7.2*inch, height=2.2*inch))
        story.append(Spacer(1, 6))

    # Section 6: Technical Questions & Learning Reflection
    story.append(Paragraph("6. Technical Questions & Learning Reflection", h1_style))

    q1_text = (
        "<b>Question 1: How does property-based fuzzing differ from traditional unit testing in discovering software defects?</b><br/>"
        "• <i>Traditional Unit Testing</i> is example-based: developers write specific test inputs based on scenarios they already anticipate. "
        "Consequently, edge cases that developers overlook (e.g., <code>NoneType</code>, empty string tokens, unexpected delimiters) remain completely untested.<br/>"
        "• <i>Property-Based Fuzzing</i> specifies general invariant properties (e.g. <i>'this function must never raise an unhandled exception for any text or null input'</i>). "
        "Hypothesis explores huge combinatorial input spaces automatically and applies <b>test case shrinking</b> to isolate the absolute smallest "
        "reproducing counterexample (e.g. <code>s=''</code> instead of a 200-character random string), dramatically speeding up defect diagnosis."
    )
    story.append(Paragraph(q1_text, body_style))
    story.append(Spacer(1, 3))

    q2_text = (
        "<b>Question 2: What defensive programming practices were adopted to prevent unexpected production crashes?</b><br/>"
        "1. <i>Explicit Type and Null Safety</i>: Guarding function entries with <code>isinstance(input, str)</code> avoids uncontrolled <code>AttributeError</code> crashes.<br/>"
        "2. <i>Bounded Unpacking and Safe Access</i>: Replacing naive <code>key, val = item.split(':')</code> with <code>split(':', 1)</code> and checking <code>':' in item</code> "
        "prevents unpacking exceptions caused by extra or missing delimiters.<br/>"
        "3. <i>Fail-Safe Fallbacks</i>: Using <code>dict.get()</code> and returning neutral fallback values (such as <code>0.0</code> for empty prices or <code>{}</code> for invalid modifier strings) "
        "allows downstream application logic to continue executing cleanly without terminating abruptly."
    )
    story.append(Paragraph(q2_text, body_style))
    story.append(Spacer(1, 3))

    q3_text = (
        "<b>Question 3: Summary of Deliverables & Version Control Documentation</b><br/>"
        "• <b>Deliverable 1</b>: Comprehensive PDF Report (<code>PES2UG24CS310_Lab_7.pdf</code>) documenting methodology, vulnerability analysis, and verified terminal outputs.<br/>"
        "• <b>Deliverable 2</b>: Hardened application script (<code>processor.py</code>) incorporating type validation, dictionary fix (<code>'MOC'</code>), and safe token parsing.<br/>"
        "• <b>Deliverable 3</b>: Completed test suite (<code>test_processor.py</code>) containing 6 Hypothesis property-based fuzz tests passing 100%."
    )
    story.append(Paragraph(q3_text, body_style))

    doc.build(story)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    dest1 = '/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_7/PES2UG24CS310_Lab_7.pdf'
    dest2 = '/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_7/L6_L7_03_coffee_shop_order/Lab 7/PES2UG24CS310_Lab_7.pdf'
    build_pdf(dest1)
    build_pdf(dest2)
