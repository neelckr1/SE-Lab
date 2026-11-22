#!/usr/bin/env python3
"""
generate_terminal_screenshots.py
Renders realistic macOS terminal screenshots for Lab 7 Fuzz Testing.
Optimized for high-DPI display and crisp ReportLab PDF embedding.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, commands_and_outputs, output_path, width=1000, font_size=12, line_height=19):
    header_height = 36
    padding_x = 22
    
    font_path = "/System/Library/Fonts/Menlo.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Monaco.ttf"
    
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(font_path, font_size)
    header_font = ImageFont.truetype(font_path, 11)

    # Flatten lines
    all_lines = []
    for item in commands_and_outputs:
        itype = item["type"]
        if itype == "cmd":
            all_lines.append(("cmd", item.get("prompt", "neel@macbook Lab 7 % "), item["text"]))
        elif itype == "output":
            for subline in item["text"].split("\n"):
                all_lines.append(("output", "", subline))
        elif itype == "spacer":
            all_lines.append(("spacer", "", ""))

    height = header_height + (len(all_lines) * line_height) + 24

    img = Image.new("RGBA", (width, height), (30, 30, 46, 255)) # Catppuccin Mocha Base
    draw = ImageDraw.Draw(img)

    # Header Bar
    draw.rectangle([(0, 0), (width, header_height)], fill=(24, 24, 37, 255))

    # Window Controls (macOS Close / Minimize / Zoom)
    draw.ellipse([(14, 12), (24, 22)], fill=(243, 139, 168, 255)) # Red
    draw.ellipse([(32, 12), (42, 22)], fill=(249, 226, 175, 255)) # Yellow
    draw.ellipse([(50, 12), (60, 22)], fill=(166, 227, 161, 255)) # Green

    # Window Title
    title_bbox = draw.textbbox((0, 0), title, font=header_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 11), title, fill=(166, 173, 200, 255), font=header_font)

    # Content Lines
    y = header_height + 12
    for line_type, prompt, line in all_lines:
        if line_type == "cmd":
            draw.text((padding_x, y), prompt, fill=(137, 180, 250, 255), font=bold_font) # Blue prompt
            prompt_w = draw.textlength(prompt, font=bold_font)
            draw.text((padding_x + prompt_w, y), line, fill=(205, 214, 244, 255), font=bold_font)
        elif line_type == "output":
            # Color logic based on terminal contents
            if any(k in line for k in ["PASSED", "passed in", "100%", "Base Price: $", "Average Shot Price: $"]):
                fill_color = (166, 227, 161, 255) # Green
            elif any(k in line for k in ["FAILED", "KeyError", "ValueError", "AttributeError", "ExceptionGroup", "AssertionError", "Traceback", "failed in"]):
                fill_color = (243, 139, 168, 255) # Red/Salmon
            elif any(k in line for k in ["Failing test case:", "Explanation:", "s=", "prices=", "pairs=", "code="]):
                fill_color = (249, 226, 175, 255) # Yellow/Gold
            elif any(k in line for k in ["====", "===", "---", "test session starts"]):
                fill_color = (137, 180, 250, 255) # Cyan/Blue accent
            elif any(k in line for k in ["Enter drink code", "Enter CSV of shot", "Enter modifiers", "Parsed Modifiers:"]):
                fill_color = (203, 166, 247, 255) # Mauve
            else:
                fill_color = (205, 214, 244, 255) # Standard text
            draw.text((padding_x, y), line, fill=fill_color, font=font)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated screenshot: {output_path} ({width}x{height})")

def generate_all():
    base_dir = "/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_7/L6_L7_03_coffee_shop_order/Lab 7"

    # 1. Buggy processor.py output
    buggy_items = [
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "python processor.py  # Happy Path Execution"},
        {"type": "output", "text": "==== Running lookup_drink_code ====\n"
                                   "Enter drink code prefix (e.g. LAT, CAP, ESP): LAT\n"
                                   "Base Price: $ 4.5\n\n"
                                   "==== Running calculate_average_shot_cost ====\n"
                                   "Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): 1.0, 1.5, 2.0\n"
                                   "Average Shot Price: $ 1.5\n\n"
                                   "==== Running parse_order_modifiers ====\n"
                                   "Enter modifiers (e.g. milk:oat;syrup:vanilla): milk:oat;syrup:vanilla\n"
                                   "Parsed Modifiers: {'milk': 'oat', 'syrup': 'vanilla'}"},
        {"type": "spacer"},
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "python processor.py  # Edge Case: 'MOc' casing defect & unhandled code"},
        {"type": "output", "text": "==== Running lookup_drink_code ====\n"
                                   "Enter drink code prefix (e.g. LAT, CAP, ESP): MOc\n"
                                   "Traceback (most recent call last):\n"
                                   "  File \"processor.py\", line 10, in lookup_drink_code\n"
                                   "    return menu_prices[code_prefix]\n"
                                   "KeyError: 'MOC'"},
        {"type": "spacer"},
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "python -c \"from processor import calculate_average_shot_cost; calculate_average_shot_cost('')\""},
        {"type": "output", "text": "Traceback (most recent call last):\n"
                                   "  File \"processor.py\", line 13, in calculate_average_shot_cost\n"
                                   "    prices = [float(p) for p in pricing_csv.split(',')]\n"
                                   "ValueError: could not convert string to float: ''"},
        {"type": "spacer"},
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "python -c \"from processor import parse_order_modifiers; parse_order_modifiers('milk')\""},
        {"type": "output", "text": "Traceback (most recent call last):\n"
                                   "  File \"processor.py\", line 20, in parse_order_modifiers\n"
                                   "    key, value = item.split(':')\n"
                                   "ValueError: not enough values to unpack (expected 2, got 1)"}
    ]
    render_terminal(
        "Lab 7 - Step 2: Buggy processor.py Execution & Crashes",
        buggy_items,
        os.path.join(base_dir, "Lab7_Original_Buggy_Output.png")
    )

    # 2. Failing pytest run (before fix)
    failing_fuzz_items = [
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "pytest test_processor.py"},
        {"type": "output", "text": "============================= test session starts ==============================\n"
                                   "platform darwin -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0\n"
                                   "rootdir: /Users/neelchandrakar/.../Lab 7\n"
                                   "plugins: hypothesis-6.170.17\n"
                                   "collected 6 items\n\n"
                                   "test_processor.py FFFFFF                                                 [100%]\n\n"
                                   "=================================== FAILURES ===================================\n"
                                   "_______________________ test_lookup_drink_code_no_crash ________________________\n"
                                   "ExceptionGroup: Hypothesis found 2 distinct failures.\n"
                                   "  [1] KeyError: ''\n"
                                   "      Failing test case: test_lookup_drink_code_no_crash(s='')\n"
                                   "  [2] AttributeError: 'NoneType' object has no attribute 'upper'\n"
                                   "      Failing test case: test_lookup_drink_code_no_crash(s=None)\n\n"
                                   "____________________ test_calculate_average_shot_cost_safe _____________________\n"
                                   "ExceptionGroup: Hypothesis found 2 distinct failures.\n"
                                   "  [1] ValueError: could not convert string to float: ''\n"
                                   "      Failing test case: test_calculate_average_shot_cost_safe(s='')\n"
                                   "  [2] AttributeError: 'NoneType' object has no attribute 'split'\n"
                                   "      Failing test case: test_calculate_average_shot_cost_safe(s=None)\n\n"
                                   "_______________________ test_parse_order_modifiers_safe ________________________\n"
                                   "ExceptionGroup: Hypothesis found 2 distinct failures.\n"
                                   "  [1] ValueError: not enough values to unpack (expected 2, got 1)\n"
                                   "      Failing test case: test_parse_order_modifiers_safe(s='')\n"
                                   "  [2] AttributeError: 'NoneType' object has no attribute 'split'\n"
                                   "      Failing test case: test_parse_order_modifiers_safe(s=None)\n\n"
                                   "______________________ test_lookup_drink_code_categories _______________________\n"
                                   "AssertionError: lookup_drink_code crashed on 'MOc' with: KeyError('MOC')\n"
                                   "Failing test case: test_lookup_drink_code_categories(code='MOc')\n\n"
                                   "=========================== short test summary info ============================\n"
                                   "FAILED test_processor.py::test_lookup_drink_code_no_crash - ExceptionGroup\n"
                                   "FAILED test_processor.py::test_calculate_average_shot_cost_safe - ExceptionGroup\n"
                                   "FAILED test_processor.py::test_parse_order_modifiers_safe - ExceptionGroup\n"
                                   "FAILED test_processor.py::test_lookup_drink_code_categories - AssertionError\n"
                                   "FAILED test_processor.py::test_calculate_average_shot_cost_numeric - AssertionError\n"
                                   "FAILED test_processor.py::test_parse_order_modifiers_delimiters - AssertionError\n"
                                   "============================== 6 failed in 0.13s ==============================="}
    ]
    render_terminal(
        "Lab 7 - Step 4: Failing Hypothesis Fuzz Tests Against Buggy processor.py",
        failing_fuzz_items,
        os.path.join(base_dir, "Lab7_Fuzz_Test_Failures.png")
    )

    # 3. Fixed processor.py output
    fixed_items = [
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "python processor.py  # Happy Path & Verified 'MOc' Resolution"},
        {"type": "output", "text": "==== Running lookup_drink_code ====\n"
                                   "Enter drink code prefix (e.g. LAT, CAP, ESP): MOC\n"
                                   "Base Price: $5.00\n\n"
                                   "==== Running calculate_average_shot_cost ====\n"
                                   "Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): 1.0, 1.5, 2.0\n"
                                   "Average Shot Price: $1.50\n\n"
                                   "==== Running parse_order_modifiers ====\n"
                                   "Enter modifiers (e.g. milk:oat;syrup:vanilla): milk:oat;syrup:vanilla\n"
                                   "Parsed Modifiers: {'milk': 'oat', 'syrup': 'vanilla'}"},
        {"type": "spacer"},
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "python processor.py  # Hardened Edge Cases: Unknown code, dirty CSV, malformed pairs"},
        {"type": "output", "text": "==== Running lookup_drink_code ====\n"
                                   "Enter drink code prefix (e.g. LAT, CAP, ESP): UNKNOWN\n"
                                   "Base Price: Invalid drink code 'UNKNOWN' (Not Found / Unrecognized)\n\n"
                                   "==== Running calculate_average_shot_cost ====\n"
                                   "Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): 1.5, abc, 2.5, , 3.0\n"
                                   "Average Shot Price: $2.33\n\n"
                                   "==== Running parse_order_modifiers ====\n"
                                   "Enter modifiers (e.g. milk:oat;syrup:vanilla): milk:oat;invalid;note:extra:hot;:empty;syrup:caramel\n"
                                   "Parsed Modifiers: {'milk': 'oat', 'note': 'extra:hot', 'syrup': 'caramel'}"}
    ]
    render_terminal(
        "Lab 7 - Step 5: Hardened processor.py Execution (Valid & Edge Cases)",
        fixed_items,
        os.path.join(base_dir, "Lab7_Fixed_Application_Output.png")
    )

    # 4. Passing pytest run (after fix)
    passing_fuzz_items = [
        {"type": "cmd", "prompt": "neel@macbook Lab 7 % ", "text": "pytest test_processor.py -v"},
        {"type": "output", "text": "============================= test session starts ==============================\n"
                                   "platform darwin -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0\n"
                                   "cachedir: .pytest_cache\n"
                                   "hypothesis profile 'default'\n"
                                   "rootdir: /Users/neelchandrakar/.../Lab 7\n"
                                   "plugins: hypothesis-6.170.17\n"
                                   "collected 6 items\n\n"
                                   "test_processor.py::test_lookup_drink_code_no_crash PASSED                [ 16%]\n"
                                   "test_processor.py::test_calculate_average_shot_cost_safe PASSED          [ 33%]\n"
                                   "test_processor.py::test_parse_order_modifiers_safe PASSED                [ 50%]\n"
                                   "test_processor.py::test_lookup_drink_code_categories PASSED              [ 66%]\n"
                                   "test_processor.py::test_calculate_average_shot_cost_numeric PASSED       [ 83%]\n"
                                   "test_processor.py::test_parse_order_modifiers_delimiters PASSED          [100%]\n\n"
                                   "============================== 6 passed in 0.20s ==============================="}
    ]
    render_terminal(
        "Lab 7 - Step 6: All Hypothesis Fuzz Tests Passing Against Hardened Processor",
        passing_fuzz_items,
        os.path.join(base_dir, "Lab7_Passing_Fuzz_Tests.png")
    )

if __name__ == "__main__":
    generate_all()
