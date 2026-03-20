"""
"BLUE" モザイクテキスト SVG ジェネレーター
文字の形をクリップマスクにして、アイコンと同じ青系モザイクセルで塗りつぶす
"""

import os

# --- フォント仕様 (logo-specification.md 準拠) ---
TEXT_COLOR = "#0E2A47"
FONT_FAMILY = "Montserrat, Arial, Helvetica, sans-serif"
FONT_WEIGHT = "bold"
FONT_SIZE = 90

# テキスト領域の推定サイズ
TEXT_W = 260   # "BLUE" 4文字の推定幅 (90px Montserrat Bold)
TEXT_H = 66    # キャップハイト (90 * 0.72 ≈ 65)

# セルサイズ: モザイク感を残しつつ濃い色まで含める
# テキスト高さ66px ÷ 4行 = 16.5px → 16px セルで4行 + 余白で全域カバー
CELL = 16

# グリッドサイズ
COLS = (TEXT_W // CELL) + 2   # 18列
ROWS = 5                       # 4行+1で確実にカバー

# アイコン全8行から4行に間引き (行1, 3, 5, 7 → 薄い〜濃いの全域)
MOSAIC_COLORS = [
    # icon 行1 (薄い)
    ["#99D1E9","#97D0E9","#98D0E7","#AADAEB","#C0E3F0",
     "#ADDFEA","#9AD4DD","#99D2DC","#9BD5DD","#7FC5D7",
     "#81C3D5","#75B6D6","#63A0CE","#62A1CD","#62A1CD"],
    # icon 行3 (中間やや薄)
    ["#5EAEDC","#60B0DE","#5FAFDE","#6EB9D6","#88C9D8",
     "#75C0D6","#55BDD5","#54BDD3","#6CC2D7","#47AFD2",
     "#45ACCE","#2E97C3","#2178B2","#207AB1","#227BB2"],
    # icon 行5 (中間やや濃)
    ["#467DB6","#477DB4","#477CB5","#4F8EC3","#59A3C8",
     "#4B95C6","#3781BB","#3585BE","#3992C0","#3381BA",
     "#307FB9","#295FA2","#274B9A","#254897","#264998"],
    # icon 行7 (濃い)
    ["#313C89","#313D8D","#2E3D8B","#3A589F","#4171B0",
     "#2B599C","#2A4781","#294781","#28528E","#2A4D8A",
     "#27437D","#1F356B","#1B2050","#1C2151","#1B2353"],
    # icon 行8 (最も濃い) - 下端カバー用
    ["#2F3174","#2E3176","#303078","#3B428B","#41589F",
     "#31458A","#26386A","#283A70","#2E437B","#2B4071",
     "#24346A","#1C245A","#141D4A","#151D4C","#161C49"],
]


def get_color(col, row):
    """col(0..COLS-1) を icon の 15列にマッピング"""
    icon_col = int(col * 14 / max(COLS - 1, 1))
    icon_col = min(icon_col, 14)
    return MOSAIC_COLORS[row][icon_col]

# viewBox: テキスト領域 + 少し余白
PADDING = 4
VB_W = COLS * CELL + PADDING * 2
VB_H = ROWS * CELL + PADDING * 2


def generate_svg():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {VB_W} {VB_H}" '
        f'width="{VB_W}" height="{VB_H}">'
    )
    parts.append('  <title>BLUE Mosaic Text</title>')

    # クリップパス: "BLUE" テキスト
    # テキストのベースラインを調整 (キャップハイトの上端がグリッド上端に近くなるように)
    text_x = PADDING
    text_baseline_y = PADDING + TEXT_H  # ベースライン = 上端 + キャップハイト

    parts.append('  <defs>')
    parts.append('    <clipPath id="blue-text-clip">')
    parts.append(
        f'      <text x="{text_x}" y="{text_baseline_y}" '
        f'font-family="{FONT_FAMILY}" font-weight="{FONT_WEIGHT}" '
        f'font-size="{FONT_SIZE}" '
        f'letter-spacing="0">BLUE</text>'
    )
    parts.append('    </clipPath>')
    parts.append('  </defs>')

    # モザイクセル (テキストでクリップ)
    parts.append('  <g id="blue-mosaic" clip-path="url(#blue-text-clip)">')

    for row in range(ROWS):
        for col in range(COLS):
            color = get_color(col, row)

            cx = PADDING + col * CELL
            cy = PADDING + row * CELL

            parts.append(
                f'    <rect x="{cx}" y="{cy}" '
                f'width="{CELL}" height="{CELL}" fill="{color}"/>'
            )

    parts.append('  </g>')
    parts.append('</svg>')
    return '\n'.join(parts)


if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'blue-mosaic.svg')
    output_path = os.path.normpath(output_path)

    svg = generate_svg()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"Generated: {output_path}")
    print(f"ViewBox: {VB_W} x {VB_H}")
    print(f"Grid: {COLS} x {ROWS} cells ({CELL}px)")
    print(f"Font: {FONT_FAMILY} {FONT_WEIGHT} {FONT_SIZE}px")
