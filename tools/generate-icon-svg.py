"""
BLUE APP WORKS アイコン SVG ジェネレーター
仕様書 (docs/icon-specification.md) に基づいて icon.svg を生成する
"""

# 寸法定義（正規化値: 基本単位 10px）
CELL = 20        # セル 1マス
RECT_W = 100     # 長方形幅 (5セル)
RECT_H = 40      # 長方形高 (2セル)
GAP = 10         # 列間・行間
RADIUS = 10      # 角丸半径

# 全体サイズ
CONTENT_W = RECT_W * 3 + GAP * 2  # 320
CONTENT_H = RECT_H * 4 + GAP * 3  # 190

# 全120セル カラーコード定義 (15列 x 8行)
# 画像からピクセルサンプリングで取得した実測値
COLORS = [
    # 行1: 長方形1段目・上セル
    ["#99D1E9", "#97D0E9", "#98D0E7", "#AADAEB", "#C0E3F0",
     "#ADDFEA", "#9AD4DD", "#99D2DC", "#9BD5DD", "#7FC5D7",
     "#81C3D5", "#75B6D6", "#63A0CE", "#62A1CD", "#62A1CD"],
    # 行2: 長方形1段目・下セル
    ["#7FC0E4", "#83C2E4", "#81C2E5", "#92CEE6", "#A8D8E7",
     "#95D1E4", "#7ACCDB", "#78CADB", "#82CDD9", "#65BFD8",
     "#65BBD5", "#64A9D2", "#4F9BCF", "#4F9BCF", "#4E9ACF"],
    # 行3: 長方形2段目・上セル
    ["#5EAEDC", "#60B0DE", "#5FAFDE", "#6EB9D6", "#88C9D8",
     "#75C0D6", "#55BDD5", "#54BDD3", "#6CC2D7", "#47AFD2",
     "#45ACCE", "#2E97C3", "#2178B2", "#207AB1", "#227BB2"],
    # 行4: 長方形2段目・下セル
    ["#4A8DC1", "#4B8EC3", "#4E8FC3", "#5E9FCC", "#74B3D5",
     "#58A6D3", "#38A5D3", "#3CA6D4", "#45AFDC", "#419BCD",
     "#399ACA", "#377BB4", "#2C6BAB", "#2C6AAA", "#2C6CA9"],
    # 行5: 長方形3段目・上セル
    ["#467DB6", "#477DB4", "#477CB5", "#4F8EC3", "#59A3C8",
     "#4B95C6", "#3781BB", "#3585BE", "#3992C0", "#3381BA",
     "#307FB9", "#295FA2", "#274B9A", "#254897", "#264998"],
    # 行6: 長方形3段目・下セル
    ["#3A5CA1", "#3A5DA5", "#3B5DA4", "#4572B5", "#4F8BC2",
     "#4275B2", "#2567A7", "#276CAA", "#3278B2", "#356CAF",
     "#2F69A9", "#2F529A", "#2B4282", "#2B4283", "#2C4586"],
    # 行7: 長方形4段目・上セル
    ["#313C89", "#313D8D", "#2E3D8B", "#3A589F", "#4171B0",
     "#2B599C", "#2A4781", "#294781", "#28528E", "#2A4D8A",
     "#27437D", "#1F356B", "#1B2050", "#1C2151", "#1B2353"],
    # 行8: 長方形4段目・下セル
    ["#2F3174", "#2E3176", "#303078", "#3B428B", "#41589F",
     "#31458A", "#26386A", "#283A70", "#2E437B", "#2B4071",
     "#24346A", "#1C245A", "#141D4A", "#151D4C", "#161C49"],
]


def generate_svg():
    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {CONTENT_W} {CONTENT_H}" '
        f'width="{CONTENT_W}" height="{CONTENT_H}">'
    )
    svg_parts.append(f'  <title>Blue App Works Icon</title>')

    # 角丸クリップパスを12個の長方形分定義
    svg_parts.append('  <defs>')
    for rect_row in range(4):
        for rect_col in range(3):
            clip_id = f"clip-r{rect_row}-c{rect_col}"
            rx = rect_col * (RECT_W + GAP)
            ry = rect_row * (RECT_H + GAP)
            svg_parts.append(
                f'    <clipPath id="{clip_id}">'
                f'<rect x="{rx}" y="{ry}" '
                f'width="{RECT_W}" height="{RECT_H}" '
                f'rx="{RADIUS}" ry="{RADIUS}"/>'
                f'</clipPath>'
            )
    svg_parts.append('  </defs>')

    # 12個の長方形グループ
    for rect_row in range(4):
        for rect_col in range(3):
            clip_id = f"clip-r{rect_row}-c{rect_col}"
            group_id = f"rect-r{rect_row}-c{rect_col}"
            svg_parts.append(f'  <g id="{group_id}" clip-path="url(#{clip_id})">')

            # 各長方形内の 5x2 セル
            for cell_row in range(2):
                for cell_col in range(5):
                    # グローバルな列・行番号 (0-indexed)
                    global_col = rect_col * 5 + cell_col
                    global_row = rect_row * 2 + cell_row

                    color = COLORS[global_row][global_col]

                    # セルの座標
                    cx = rect_col * (RECT_W + GAP) + cell_col * CELL
                    cy = rect_row * (RECT_H + GAP) + cell_row * CELL

                    svg_parts.append(
                        f'    <rect x="{cx}" y="{cy}" '
                        f'width="{CELL}" height="{CELL}" '
                        f'fill="{color}"/>'
                    )

            svg_parts.append('  </g>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


if __name__ == '__main__':
    import os
    output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'icon.svg')
    output_path = os.path.normpath(output_path)
    svg = generate_svg()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {output_path}")
    print(f"Size: {CONTENT_W} x {CONTENT_H} px")
    print(f"Cells: {15 * 8} = 120")
