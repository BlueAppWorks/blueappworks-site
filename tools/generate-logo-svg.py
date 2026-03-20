"""
BLUE APP WORKS フルロゴ SVG ジェネレーター
左: ロゴタイプ（BLUE APP / WORKS）  右: シンボルマーク（icon）

仕様書:
  - docs/logo-specification.md
  - docs/icon-specification.md
"""

import os
import sys

# --- アイコン仕様 (icon-specification.md 準拠) ---
CELL = 20
RECT_W = 100
RECT_H = 40
ICON_GAP = 10
RADIUS = 10
ICON_W = RECT_W * 3 + ICON_GAP * 2   # 320
ICON_H = RECT_H * 4 + ICON_GAP * 3   # 190

COLORS = [
    ["#99D1E9","#97D0E9","#98D0E7","#AADAEB","#C0E3F0",
     "#ADDFEA","#9AD4DD","#99D2DC","#9BD5DD","#7FC5D7",
     "#81C3D5","#75B6D6","#63A0CE","#62A1CD","#62A1CD"],
    ["#7FC0E4","#83C2E4","#81C2E5","#92CEE6","#A8D8E7",
     "#95D1E4","#7ACCDB","#78CADB","#82CDD9","#65BFD8",
     "#65BBD5","#64A9D2","#4F9BCF","#4F9BCF","#4E9ACF"],
    ["#5EAEDC","#60B0DE","#5FAFDE","#6EB9D6","#88C9D8",
     "#75C0D6","#55BDD5","#54BDD3","#6CC2D7","#47AFD2",
     "#45ACCE","#2E97C3","#2178B2","#207AB1","#227BB2"],
    ["#4A8DC1","#4B8EC3","#4E8FC3","#5E9FCC","#74B3D5",
     "#58A6D3","#38A5D3","#3CA6D4","#45AFDC","#419BCD",
     "#399ACA","#377BB4","#2C6BAB","#2C6AAA","#2C6CA9"],
    ["#467DB6","#477DB4","#477CB5","#4F8EC3","#59A3C8",
     "#4B95C6","#3781BB","#3585BE","#3992C0","#3381BA",
     "#307FB9","#295FA2","#274B9A","#254897","#264998"],
    ["#3A5CA1","#3A5DA5","#3B5DA4","#4572B5","#4F8BC2",
     "#4275B2","#2567A7","#276CAA","#3278B2","#356CAF",
     "#2F69A9","#2F529A","#2B4282","#2B4283","#2C4586"],
    ["#313C89","#313D8D","#2E3D8B","#3A589F","#4171B0",
     "#2B599C","#2A4781","#294781","#28528E","#2A4D8A",
     "#27437D","#1F356B","#1B2050","#1C2151","#1B2353"],
    ["#2F3174","#2E3176","#303078","#3B428B","#41589F",
     "#31458A","#26386A","#283A70","#2E437B","#2B4071",
     "#24346A","#1C245A","#141D4A","#151D4C","#161C49"],
]

# --- ロゴタイプ仕様 (logo-specification.md 準拠) ---
TEXT_COLOR = "#0E2A47"
FONT_FAMILY = "Montserrat, Arial, Helvetica, sans-serif"
FONT_WEIGHT = "bold"

# レイアウト計算
# テキスト上下端はアイコン上下端から20px内側
TEXT_MARGIN = 20
LINE_GAP = 20                             # 行間 20px

# TEXT_MARGIN*2 + CAP_HEIGHT*2 + LINE_GAP = ICON_H
# → CAP_HEIGHT = (190 - 40 - 20) / 2 = 65
CAP_HEIGHT = (ICON_H - TEXT_MARGIN * 2 - LINE_GAP) / 2  # 65
FONT_SIZE = round(CAP_HEIGHT / 0.72)      # 90 (Montserrat Bold キャップハイト比)
CAP_HEIGHT = FONT_SIZE * 0.72             # 再計算: 64.8

# テキストとアイコンの間隔 (仕様: ロゴタイプ高さの約1倍)
LOGO_GAP = 60

# テキストの推定幅 (Montserrat Bold caps)
TEXT_WIDTH_EST = 440  # "BLUE APP" の推定幅 (90px)

# 全体サイズ
TOTAL_W = TEXT_WIDTH_EST + LOGO_GAP + ICON_W  # ~825
TOTAL_H = ICON_H  # 190

# テキストの垂直位置 (上端から10px)
TEXT_TOP = TEXT_MARGIN
LINE1_Y = TEXT_TOP + CAP_HEIGHT           # "BLUE APP" ベースライン
LINE2_Y = LINE1_Y + LINE_GAP + CAP_HEIGHT  # "WORKS" ベースライン

# アイコンの水平オフセット
ICON_X = TEXT_WIDTH_EST + LOGO_GAP


def generate_icon_group(offset_x=0, offset_y=0):
    """アイコン部分のSVGグループを生成"""
    parts = []
    parts.append(f'  <g id="symbol" transform="translate({offset_x},{offset_y})">')

    # クリップパス定義
    parts.append('    <defs>')
    for rr in range(4):
        for rc in range(3):
            cid = f"clip-r{rr}-c{rc}"
            rx = rc * (RECT_W + ICON_GAP)
            ry = rr * (RECT_H + ICON_GAP)
            parts.append(
                f'      <clipPath id="{cid}">'
                f'<rect x="{rx}" y="{ry}" width="{RECT_W}" height="{RECT_H}" '
                f'rx="{RADIUS}" ry="{RADIUS}"/></clipPath>'
            )
    parts.append('    </defs>')

    # 12個の長方形グループ
    for rr in range(4):
        for rc in range(3):
            cid = f"clip-r{rr}-c{rc}"
            parts.append(f'    <g clip-path="url(#{cid})">')
            for cr in range(2):
                for cc in range(5):
                    gc = rc * 5 + cc
                    gr = rr * 2 + cr
                    color = COLORS[gr][gc]
                    cx = rc * (RECT_W + ICON_GAP) + cc * CELL
                    cy = rr * (RECT_H + ICON_GAP) + cr * CELL
                    parts.append(
                        f'      <rect x="{cx}" y="{cy}" '
                        f'width="{CELL}" height="{CELL}" fill="{color}"/>'
                    )
            parts.append('    </g>')

    parts.append('  </g>')
    return '\n'.join(parts)


def generate_logo_svg(line1="BLUE APP", line2="WORKS", title="Blue App Works Logo",
                      text_width_est=TEXT_WIDTH_EST):
    """フルロゴSVGを生成"""
    icon_x = text_width_est + LOGO_GAP
    total_w = text_width_est + LOGO_GAP + ICON_W

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {total_w} {TOTAL_H}" '
        f'width="{total_w}" height="{TOTAL_H}">'
    )
    parts.append(f'  <title>{title}</title>')

    # ロゴタイプ (テキスト)
    parts.append('  <g id="logotype">')
    parts.append(
        f'    <text x="0" y="{LINE1_Y:.1f}" '
        f'font-family="{FONT_FAMILY}" font-weight="{FONT_WEIGHT}" '
        f'font-size="{FONT_SIZE}" fill="{TEXT_COLOR}" '
        f'letter-spacing="0">{line1}</text>'
    )
    parts.append(
        f'    <text x="0" y="{LINE2_Y:.1f}" '
        f'font-family="{FONT_FAMILY}" font-weight="{FONT_WEIGHT}" '
        f'font-size="{FONT_SIZE}" fill="{TEXT_COLOR}" '
        f'letter-spacing="0">{line2}</text>'
    )
    parts.append('  </g>')

    # シンボルマーク
    parts.append(generate_icon_group(icon_x, 0))

    parts.append('</svg>')
    return '\n'.join(parts)


LOGOS = [
    {
        "file": "logo.svg",
        "line1": "BLUE APP",
        "line2": "WORKS",
        "title": "Blue App Works Logo",
        "text_width_est": 440,
    },
    {
        "file": "logo-gallery.svg",
        "line1": "BLUE APP",
        "line2": "GALLERY",
        "title": "Blue App Gallery Logo",
        "text_width_est": 470,
    },
]

if __name__ == '__main__':
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'images')

    for logo in LOGOS:
        output_path = os.path.normpath(os.path.join(base_dir, logo["file"]))
        svg = generate_logo_svg(
            line1=logo["line1"],
            line2=logo["line2"],
            title=logo["title"],
            text_width_est=logo["text_width_est"],
        )
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        total_w = logo["text_width_est"] + LOGO_GAP + ICON_W
        print(f"Generated: {output_path}  ({total_w} x {TOTAL_H})")
    print(f"Line 1 baseline: {LINE1_Y:.1f}")
    print(f"Line 2 baseline: {LINE2_Y:.1f}")
    print(f"Icon offset: x={ICON_X}")
    print()
    print("Note: Text width depends on font availability.")
    print("Open in Figma/Inkscape/Illustrator to fine-tune text positioning.")
