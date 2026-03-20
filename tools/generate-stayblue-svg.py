"""
"STAY BLUE, STAY CURIOUS" キャッチコピー SVG ジェネレーター

方式:
  1. 全文を1つの <text> + <tspan> で描画 (ベースレイヤー)
  2. 同じ全文テキストを clipPath にし、さらに BLUE 領域の rect で二重クリップ
  3. モザイクセルを二重クリップで重ねる → BLUE の文字だけモザイクになる
"""

import os

# --- フォント仕様 ---
TEXT_COLOR = "#2C4356"   # ブルーグレー (元画像の雰囲気に合わせた色)
FONT_FAMILY = "Montserrat, Arial, Helvetica, sans-serif"
FONT_SIZE = 48

# ウェイト
WEIGHT_NORMAL = "600"    # STAY, STAY CURIOUS 部分
WEIGHT_BOLD = "800"      # BLUE 部分

# viewBox
VB_W = 800
VB_H = 70
BASELINE_Y = 46

# BLUE の推定位置 (rect クリップ用、多少のずれは許容される)
# Montserrat 600 weight "STAY " ≈ 115px, Montserrat 800 "BLUE" ≈ 130px
BLUE_RECT_X = 130
BLUE_RECT_W = 141

# モザイクセル
CELL = 10
MOSAIC_COLS = BLUE_RECT_W // CELL + 4  # 少し余裕
MOSAIC_ROWS = VB_H // CELL

# アイコンから間引いた5行パレット (行1,3,5,7,8)
MOSAIC_COLORS = [
    ["#99D1E9","#97D0E9","#98D0E7","#AADAEB","#C0E3F0",
     "#ADDFEA","#9AD4DD","#99D2DC","#9BD5DD","#7FC5D7",
     "#81C3D5","#75B6D6","#63A0CE","#62A1CD","#62A1CD"],
    ["#5EAEDC","#60B0DE","#5FAFDE","#6EB9D6","#88C9D8",
     "#75C0D6","#55BDD5","#54BDD3","#6CC2D7","#47AFD2",
     "#45ACCE","#2E97C3","#2178B2","#207AB1","#227BB2"],
    ["#467DB6","#477DB4","#477CB5","#4F8EC3","#59A3C8",
     "#4B95C6","#3781BB","#3585BE","#3992C0","#3381BA",
     "#307FB9","#295FA2","#274B9A","#254897","#264998"],
    ["#313C89","#313D8D","#2E3D8B","#3A589F","#4171B0",
     "#2B599C","#2A4781","#294781","#28528E","#2A4D8A",
     "#27437D","#1F356B","#1B2050","#1C2151","#1B2353"],
    ["#2F3174","#2E3176","#303078","#3B428B","#41589F",
     "#31458A","#26386A","#283A70","#2E437B","#2B4071",
     "#24346A","#1C245A","#141D4A","#151D4C","#161C49"],
]


def get_color(col, row):
    icon_col = int(col * 14 / max(MOSAIC_COLS - 1, 1))
    icon_col = min(icon_col, 14)
    color_row = min(row, len(MOSAIC_COLORS) - 1)
    return MOSAIC_COLORS[color_row][icon_col]


def text_with_spans(x, y, extra_attrs=""):
    """全文テキストを tspan 付きで生成"""
    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="{FONT_FAMILY}" '
        f'font-size="{FONT_SIZE}" '
        f'letter-spacing="0"{extra_attrs}>'
        f'<tspan font-weight="{WEIGHT_NORMAL}" fill="{TEXT_COLOR}">STAY </tspan>'
        f'<tspan font-weight="{WEIGHT_BOLD}" fill="{TEXT_COLOR}">BLUE</tspan>'
        f'<tspan font-weight="{WEIGHT_NORMAL}" fill="{TEXT_COLOR}">, STAY CURIOUS</tspan>'
        f'</text>'
    )


def generate_svg():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {VB_W} {VB_H}" '
        f'width="{VB_W}" height="{VB_H}">'
    )
    parts.append('  <title>Stay Blue, Stay Curious</title>')

    # --- defs ---
    parts.append('  <defs>')
    # clipPath 1: 全文テキストの形状 (全文字がクリップ領域)
    parts.append('    <clipPath id="text-shape">')
    parts.append(f'      {text_with_spans(0, BASELINE_Y)}')
    parts.append('    </clipPath>')
    # clipPath 2: BLUE 領域の矩形 (BLUE のある範囲だけに制限)
    parts.append('    <clipPath id="blue-region">')
    parts.append(
        f'      <rect x="{BLUE_RECT_X}" y="0" '
        f'width="{BLUE_RECT_W}" height="{VB_H}"/>'
    )
    parts.append('    </clipPath>')
    parts.append('  </defs>')

    # --- ベースレイヤー: 全文テキスト (ブルーグレー) ---
    parts.append(f'  {text_with_spans(0, BASELINE_Y)}')

    # --- モザイクオーバーレイ: テキスト形状 × BLUE領域 の二重クリップ ---
    parts.append('  <g clip-path="url(#text-shape)">')
    parts.append('    <g clip-path="url(#blue-region)">')
    for row in range(MOSAIC_ROWS):
        for col in range(MOSAIC_COLS):
            color = get_color(col, row)
            cx = BLUE_RECT_X - CELL + col * CELL  # 少し手前から開始
            cy = row * CELL
            parts.append(
                f'      <rect x="{cx}" y="{cy}" '
                f'width="{CELL}" height="{CELL}" fill="{color}"/>'
            )
    parts.append('    </g>')
    parts.append('  </g>')

    parts.append('</svg>')
    return '\n'.join(parts)


if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'stayblue-staycurious.svg')
    output_path = os.path.normpath(output_path)

    svg = generate_svg()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"Generated: {output_path}")
    print(f"ViewBox: {VB_W} x {VB_H}")
    print(f"Text color: {TEXT_COLOR} (blue-gray)")
    print(f"Font weights: STAY/CURIOUS={WEIGHT_NORMAL}, BLUE={WEIGHT_BOLD}")
    print(f"BLUE region: x={BLUE_RECT_X}, w={BLUE_RECT_W}")
    print(f"Mosaic: {MOSAIC_COLS} x {MOSAIC_ROWS} cells ({CELL}px)")
