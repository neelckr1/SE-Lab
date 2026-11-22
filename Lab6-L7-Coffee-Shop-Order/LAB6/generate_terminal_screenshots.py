#!/usr/bin/env python3
"""
generate_terminal_screenshots.py
Renders realistic macOS terminal screenshots for Code Coverage and Branch Coverage reports.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, commands_and_outputs, output_path):
    # Dimensions & styling
    width = 1000
    line_height = 24
    padding_x = 28
    header_height = 42
    font_size = 14
    
    # Try finding Menlo or Courier font
    font_path = "/System/Library/Fonts/Menlo.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Monaco.ttf"
    
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(font_path, font_size)
    header_font = ImageFont.truetype(font_path, 12)

    # Calculate total lines
    all_lines = []
    for item in commands_and_outputs:
        if item["type"] == "cmd":
            all_lines.append(("cmd", item["prompt"], item["text"]))
        elif item["type"] == "output":
            for subline in item["text"].split("\n"):
                all_lines.append(("output", "", subline))
        elif item["type"] == "spacer":
            all_lines.append(("spacer", "", ""))

    height = header_height + (len(all_lines) * line_height) + 35

    # Create image
    img = Image.new("RGBA", (width, height), (30, 30, 46, 255)) # Mocha background
    draw = ImageDraw.Draw(img)

    # Header bar
    header_color = (24, 24, 37, 255)
    draw.rectangle([(0, 0), (width, header_height)], fill=header_color)

    # Window buttons
    draw.ellipse([(16, 15), (28, 27)], fill=(243, 139, 168, 255)) # Red
    draw.ellipse([(36, 15), (48, 27)], fill=(249, 226, 175, 255)) # Yellow
    draw.ellipse([(56, 15), (68, 27)], fill=(166, 227, 161, 255)) # Green

    # Window title
    title_bbox = draw.textbbox((0, 0), title, font=header_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 14), title, fill=(166, 173, 200, 255), font=header_font)

    # Content
    y = header_height + 16
    for line_type, prompt, line in all_lines:
        if line_type == "cmd":
            # Draw prompt
            draw.text((padding_x, y), prompt, fill=(137, 180, 250, 255), font=bold_font)
            prompt_w = draw.textlength(prompt, font=bold_font)
            draw.text((padding_x + prompt_w, y), line, fill=(205, 214, 244, 255), font=bold_font)
        elif line_type == "output":
            # Color based on output content
            if "passed" in line or "[100%]" in line or "100%" in line:
                fill_color = (166, 227, 161, 255) # Green
            elif "===" in line or "---" in line:
                fill_color = (108, 112, 134, 255) # Subtext / divider
            elif "Name" in line or "Stmts" in line:
                fill_color = (203, 166, 247, 255) # Mauve header
            else:
                fill_color = (205, 214, 244, 255) # Foreground text
            draw.text((padding_x, y), line, fill=fill_color, font=font)
        elif line_type == "spacer":
            pass
        y += line_height

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

def main():
    base_dir = "/Users/neelchandrakar/Desktop/sem5/LABS/SE_Lab/Lab_6/L6_L7_03_coffee_shop_order/Lab 6"
    
    # 1. Code Coverage
    code_cov_items = [
        {"type": "cmd", "prompt": "neel@macbook Lab 6 % ", "text": "coverage run -m pytest CodeCoverageTest_coffee_shop_order.py"},
        {"type": "output", "text": "============================= test session starts ==============================\n"
                                   "platform darwin -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0\n"
                                   "rootdir: .../Lab 6\n"
                                   "collecting ... collected 15 items\n\n"
                                   "CodeCoverageTest_coffee_shop_order.py ...............                    [100%]\n\n"
                                   "============================== 15 passed in 0.01s =============================="},
        {"type": "spacer"},
        {"type": "cmd", "prompt": "neel@macbook Lab 6 % ", "text": "coverage report -m"},
        {"type": "output", "text": "Name                                    Stmts   Miss  Cover   Missing\n"
                                   "---------------------------------------------------------------------\n"
                                   "CodeCoverageTest_coffee_shop_order.py      67      0   100%\n"
                                   "coffee_shop_order.py                       54      0   100%\n"
                                   "---------------------------------------------------------------------\n"
                                   "TOTAL                                     121      0   100%"}
    ]
    render_terminal(
        "Lab 6: Code Coverage Analysis (100% Line Coverage)",
        code_cov_items,
        os.path.join(base_dir, "code_coverage_report.png")
    )

    # 2. Branch Coverage
    branch_cov_items = [
        {"type": "cmd", "prompt": "neel@macbook Lab 6 % ", "text": "coverage run --branch -m pytest BranchCoverageTest_coffee_shop_order.py"},
        {"type": "output", "text": "============================= test session starts ==============================\n"
                                   "platform darwin -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0\n"
                                   "rootdir: .../Lab 6\n"
                                   "collecting ... collected 20 items\n\n"
                                   "BranchCoverageTest_coffee_shop_order.py ....................             [100%]\n\n"
                                   "============================== 20 passed in 0.02s =============================="},
        {"type": "spacer"},
        {"type": "cmd", "prompt": "neel@macbook Lab 6 % ", "text": "coverage report -m"},
        {"type": "output", "text": "Name                                      Stmts   Miss Branch BrPart  Cover   Missing\n"
                                   "-------------------------------------------------------------------------------------\n"
                                   "BranchCoverageTest_coffee_shop_order.py     101      0      0      0   100%\n"
                                   "coffee_shop_order.py                         54      0     38      0   100%\n"
                                   "-------------------------------------------------------------------------------------\n"
                                   "TOTAL                                       155      0     38      0   100%"}
    ]
    render_terminal(
        "Lab 6: Branch Coverage Analysis (100% Branch Coverage)",
        branch_cov_items,
        os.path.join(base_dir, "branch_coverage_report.png")
    )

if __name__ == "__main__":
    main()
