"""
BLUE APP WORKS 白抜きロゴ SVG ジェネレーター
- テキスト: 白
- アイコン: 各セルの色 + 白い縁取り (ストローク)
"""

import os

# --- アイコン仕様 ---
CELL = 20
RECT_W = 100
RECT_H = 40
ICON_GAP = 10
RADIUS = 10
ICON_W = RECT_W * 3 + ICON_GAP * 2
ICON_H = RECT_H * 4 + ICON_GAP * 3

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

# --- テキスト仕様 ---
FONT_FAMILY = "Montserrat, Arial, Helvetica, sans-serif"
FONT_WEIGHT = "bold"
FONT_SIZE = 90
CAP_HEIGHT = FONT_SIZE * 0.72
TEXT_MARGIN = 20
LINE_GAP = 20
LOGO_GAP = 60
TEXT_WIDTH_EST = 440

LINE1_Y = TEXT_MARGIN + CAP_HEIGHT
LINE2_Y = LINE1_Y + LINE_GAP + CAP_HEIGHT
ICON_X = TEXT_WIDTH_EST + LOGO_GAP
TOTAL_W = TEXT_WIDTH_EST + LOGO_GAP + ICON_W
TOTAL_H = ICON_H

# 白縁取りの太さ
STROKE_W = 1.5


def generate_svg():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {TOTAL_W} {TOTAL_H}" '
        f'width="{TOTAL_W}" height="{TOTAL_H}">'
    )
    parts.append('  <title>Blue App Works Logo (White)</title>')

    # テキスト (白)
    parts.append('  <g id="logotype">')
    parts.append(
        f'    <text x="0" y="{LINE1_Y:.1f}" '
        f'font-family="{FONT_FAMILY}" font-weight="{FONT_WEIGHT}" '
        f'font-size="{FONT_SIZE}" fill="#FFFFFF" '
        f'letter-spacing="0">BLUE APP</text>'
    )
    parts.append(
        f'    <text x="0" y="{LINE2_Y:.1f}" '
        f'font-family="{FONT_FAMILY}" font-weight="{FONT_WEIGHT}" '
        f'font-size="{FONT_SIZE}" fill="#FFFFFF" '
        f'letter-spacing="0">WORKS</text>'
    )
    parts.append('  </g>')

    # アイコン (モザイクセル + 白縁取り)
    parts.append(f'  <g id="symbol" transform="translate({ICON_X},0)">')

    # クリップパス
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

    # モザイクセル (クリップ済み) + 白縁取り
    for rr in range(4):
        for rc in range(3):
            cid = f"clip-r{rr}-c{rc}"
            rx = rc * (RECT_W + ICON_GAP)
            ry = rr * (RECT_H + ICON_GAP)

            # セル描画
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

            # 白縁取り (セルの上に重ねる)
            parts.append(
                f'    <rect x="{rx}" y="{ry}" '
                f'width="{RECT_W}" height="{RECT_H}" '
                f'rx="{RADIUS}" ry="{RADIUS}" '
                f'fill="none" stroke="#FFFFFF" stroke-width="{STROKE_W}"/>'
            )

    parts.append('  </g>')
    parts.append('</svg>')
    return '\n'.join(parts)


if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'logo-white.svg')
    output_path = os.path.normpath(output_path)

    svg = generate_svg()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"Generated: {output_path}")
    print(f"ViewBox: {TOTAL_W} x {TOTAL_H}")
