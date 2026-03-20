"""
Snowflake Platform Architecture Blueprint SVG Generator

Generates a hand-drawn blueprint-style SVG diagram showing
the Snowflake platform architecture with wobbly lines and
sketch aesthetics.

Output: images/blueprint.svg
"""

import os
import random

# Fixed seed for reproducibility
random.seed(42)

# --- Constants ---
WIDTH = 800
HEIGHT = 600
BG_COLOR = "#1a3a5c"
LINE_COLOR = "#FFFFFF"
FONT_FAMILY = "'Architects Daughter', 'Comic Sans MS', cursive"
WOBBLE = 2.5  # max pixel offset for hand-drawn effect


def wobble_offset():
    """Return a small random offset for hand-drawn feel."""
    return random.uniform(-WOBBLE, WOBBLE)


def rough_line(x1, y1, x2, y2, opacity=0.9):
    """Draw a hand-drawn line using quadratic bezier with slight wobble.
    Draws twice with slight offset for sketchy double-line effect."""
    paths = []
    for _ in range(2):
        ox1 = x1 + wobble_offset() * 0.3
        oy1 = y1 + wobble_offset() * 0.3
        ox2 = x2 + wobble_offset() * 0.3
        oy2 = y2 + wobble_offset() * 0.3
        mx = (ox1 + ox2) / 2 + wobble_offset()
        my = (oy1 + oy2) / 2 + wobble_offset()
        d = f"M {ox1:.1f},{oy1:.1f} Q {mx:.1f},{my:.1f} {ox2:.1f},{oy2:.1f}"
        paths.append(
            f'<path d="{d}" fill="none" stroke="{LINE_COLOR}" '
            f'stroke-width="1.5" stroke-opacity="{opacity}" '
            f'stroke-linecap="round"/>'
        )
    return "\n".join(paths)


def rough_rect(x, y, w, h, opacity=0.85):
    """Draw a rectangle with wobbly edges, drawn twice for sketch effect."""
    corners = [
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h),
    ]
    lines = []
    for i in range(4):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        lines.append(rough_line(x1, y1, x2, y2, opacity))
    return "\n".join(lines)


def rough_text(x, y, text, size=16, opacity=0.95, anchor="middle", weight="normal"):
    """Render text with a slight hand-drawn offset."""
    ox = wobble_offset() * 0.3
    oy = wobble_offset() * 0.3
    safe_text = text.replace("&", "&amp;")
    return (
        f'<text x="{x + ox:.1f}" y="{y + oy:.1f}" '
        f'font-family="{FONT_FAMILY}" font-size="{size}" '
        f'font-weight="{weight}" '
        f'fill="{LINE_COLOR}" fill-opacity="{opacity}" '
        f'text-anchor="{anchor}">{safe_text}</text>'
    )


def rough_arrow(x1, y1, x2, y2, opacity=0.85):
    """Draw a hand-drawn arrow from (x1,y1) to (x2,y2) with arrowhead."""
    parts = [rough_line(x1, y1, x2, y2, opacity)]

    # Determine arrow direction for head
    dx = x2 - x1
    dy = y2 - y1
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        return parts[0]
    ux, uy = dx / length, dy / length
    # Perpendicular
    px, py = -uy, ux

    head_len = 10
    # Two lines forming arrowhead
    ax = x2 - ux * head_len + px * head_len * 0.4
    ay = y2 - uy * head_len + py * head_len * 0.4
    bx = x2 - ux * head_len - px * head_len * 0.4
    by = y2 - uy * head_len - py * head_len * 0.4

    parts.append(rough_line(x2, y2, ax, ay, opacity))
    parts.append(rough_line(x2, y2, bx, by, opacity))
    return "\n".join(parts)


def rough_dashed_line(x1, y1, x2, y2, opacity=0.7):
    """Draw a dashed hand-drawn line."""
    paths = []
    for _ in range(2):
        ox1 = x1 + wobble_offset() * 0.3
        oy1 = y1 + wobble_offset() * 0.3
        ox2 = x2 + wobble_offset() * 0.3
        oy2 = y2 + wobble_offset() * 0.3
        mx = (ox1 + ox2) / 2 + wobble_offset()
        my = (oy1 + oy2) / 2 + wobble_offset()
        d = f"M {ox1:.1f},{oy1:.1f} Q {mx:.1f},{my:.1f} {ox2:.1f},{oy2:.1f}"
        paths.append(
            f'<path d="{d}" fill="none" stroke="{LINE_COLOR}" '
            f'stroke-width="1.2" stroke-opacity="{opacity}" '
            f'stroke-linecap="round" stroke-dasharray="6,4"/>'
        )
    return "\n".join(paths)


def generate_svg():
    """Generate the full blueprint SVG content."""
    elements = []

    # --- Layout constants ---
    margin = 40
    col_gap = 30
    row_gap = 25
    col_w = (WIDTH - 2 * margin - col_gap) / 2  # ~365
    row_h = 110

    # Column x positions
    left_x = margin
    right_x = margin + col_w + col_gap

    # Row y positions
    row1_y = 95
    row2_y = row1_y + row_h + row_gap  # ~230
    row3_y = row2_y + row_h + row_gap  # ~365

    # === Title ===
    elements.append(rough_text(WIDTH / 2, 55, "Snowflake Platform", size=30, weight="bold"))
    # Underline
    elements.append(rough_line(WIDTH / 2 - 160, 65, WIDTH / 2 + 160, 65, opacity=0.4))

    # === Row 1: AI boxes ===

    # Left: AI & Operational Applications
    elements.append(rough_rect(left_x, row1_y, col_w, row_h))
    elements.append(rough_text(left_x + col_w / 2, row1_y + 28,
                               "AI & Operational Applications", size=14, weight="bold"))
    # Container label
    elements.append(rough_dashed_line(left_x + 20, row1_y + 65, left_x + col_w - 20, row1_y + 65))
    elements.append(rough_text(left_x + col_w / 2, row1_y + 85,
                               "Managed Container (SPCS)", size=11, opacity=0.6))

    # Right: Analytical AI & Apps
    elements.append(rough_rect(right_x, row1_y, col_w, row_h))
    elements.append(rough_text(right_x + col_w / 2, row1_y + 28,
                               "Analytical AI & Apps", size=14, weight="bold"))
    elements.append(rough_text(right_x + col_w / 2, row1_y + 60,
                               "AI & Analytics", size=13, opacity=0.8))

    # === Row 2: Warehouse (right side) ===
    # Left side: just connection lines pass through
    # Right: Analytical Warehouse
    elements.append(rough_rect(right_x, row2_y, col_w, row_h))
    elements.append(rough_text(right_x + col_w / 2, row2_y + 28,
                               "Analytical Warehouse", size=14, weight="bold"))
    elements.append(rough_text(right_x + col_w / 2, row2_y + 58,
                               "Virtual Warehouse", size=12, opacity=0.8))

    # Left side row 2: label area for SPCS infrastructure
    elements.append(rough_rect(left_x, row2_y, col_w, row_h, opacity=0.5))
    elements.append(rough_text(left_x + col_w / 2, row2_y + 28,
                               "Compute Pool (SPCS)", size=14, weight="bold", opacity=0.7))
    elements.append(rough_text(left_x + col_w / 2, row2_y + 55,
                               "Container Runtime", size=12, opacity=0.55))
    elements.append(rough_text(left_x + col_w / 2, row2_y + 78,
                               "GPU / CPU Nodes", size=11, opacity=0.45))

    # === Row 3: Databases (full width, two sub-boxes) ===
    db_y = row3_y + 20
    db_h = 100
    db_left_w = col_w - 10
    db_right_w = col_w - 10

    # Outer frame spanning full width
    elements.append(rough_rect(left_x - 5, db_y - 15, WIDTH - 2 * margin + 10, db_h + 30, opacity=0.3))
    elements.append(rough_text(WIDTH / 2, db_y - 2, "Data Layer", size=12, opacity=0.45))

    # Left: Operational Database
    elements.append(rough_rect(left_x, db_y, db_left_w, db_h))
    elements.append(rough_text(left_x + db_left_w / 2, db_y + 30,
                               "Operational Database", size=14, weight="bold"))
    elements.append(rough_text(left_x + db_left_w / 2, db_y + 58,
                               "PostgreSQL", size=16, opacity=0.85))

    # Right: Analytical Database
    elements.append(rough_rect(right_x + 10, db_y, db_right_w, db_h))
    elements.append(rough_text(right_x + 10 + db_right_w / 2, db_y + 30,
                               "Analytical Database", size=14, weight="bold"))
    elements.append(rough_text(right_x + 10 + db_right_w / 2, db_y + 58,
                               "Snowflake", size=16, opacity=0.85))

    # === Arrows ===

    # Arrow: Left AI box -> Compute Pool (SPCS)
    elements.append(rough_arrow(
        left_x + col_w / 2, row1_y + row_h,
        left_x + col_w / 2, row2_y
    ))

    # Arrow: Right AI box -> Analytical Warehouse
    elements.append(rough_arrow(
        right_x + col_w / 2, row1_y + row_h,
        right_x + col_w / 2, row2_y
    ))

    # Arrow: Compute Pool -> Operational Database
    elements.append(rough_arrow(
        left_x + col_w / 2, row2_y + row_h,
        left_x + db_left_w / 2, db_y
    ))

    # Arrow: Analytical Warehouse -> Analytical Database
    elements.append(rough_arrow(
        right_x + col_w / 2, row2_y + row_h,
        right_x + 10 + db_right_w / 2, db_y
    ))

    # Horizontal arrow: PostgreSQL -> Snowflake (Zero ETL)
    arrow_y = db_y + db_h / 2
    arr_x1 = left_x + db_left_w + 5
    arr_x2 = right_x + 5
    elements.append(rough_arrow(arr_x1, arrow_y, arr_x2, arrow_y, opacity=0.9))
    # Label above arrow
    elements.append(rough_text(
        (arr_x1 + arr_x2) / 2, arrow_y - 10,
        "Zero ETL", size=11, opacity=0.7
    ))

    # === Grid dots (blueprint background texture) ===
    dots = []
    for gx in range(0, WIDTH, 30):
        for gy in range(0, HEIGHT, 30):
            dots.append(
                f'<circle cx="{gx}" cy="{gy}" r="0.5" '
                f'fill="{LINE_COLOR}" fill-opacity="0.08"/>'
            )

    # === Assemble SVG ===
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {WIDTH} {HEIGHT}"
     width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Architects+Daughter');
    </style>
  </defs>

  <!-- Blueprint background -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BG_COLOR}" rx="4"/>

  <!-- Grid dots -->
  {"".join(dots)}

  <!-- Architecture diagram -->
  {chr(10).join(elements)}
</svg>"""

    return svg


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_path = os.path.join(project_dir, "images", "blueprint.svg")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    svg_content = generate_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated: {output_path}")
    print(f"Size: {len(svg_content):,} bytes")


if __name__ == "__main__":
    main()
