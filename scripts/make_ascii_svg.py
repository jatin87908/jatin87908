from PIL import Image
import html

INPUT = "source-prepped.png"
OUTPUT = "avi-ascii.svg"

# ASCII density ramp
RAMP = " .`:-=+*cs#%@"

# ASCII portrait width
WIDTH = 100

# Character aspect correction
CHAR_ASPECT = 0.5


def brightness_to_char(value):
    index = int((value / 255) * (len(RAMP) - 1))
    return RAMP[index]


def main():
    image = Image.open(INPUT).convert("L")

    original_width, original_height = image.size

    height = int(
        original_height
        / original_width
        * WIDTH
        * CHAR_ASPECT
    )

    image = image.resize((WIDTH, height))

    pixels = image.load()

    lines = []

    for y in range(height):
        line = ""

        for x in range(WIDTH):
            value = pixels[x, y]
            line += brightness_to_char(value)

        lines.append(line.rstrip())

    # SVG dimensions
    font_size = 7
    line_height = 7

    svg_width = WIDTH * 4.2
    svg_height = height * line_height + 20

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">'
    )

    svg.append("""
    <rect width="100%" height="100%" fill="white"/>
    """)

    # Definitions for row-by-row animation
    svg.append("<defs>")

    for y in range(height):
        svg.append(
            f"""
            <clipPath id="row-{y}">
                <rect x="0" y="{y * line_height}"
                      width="0" height="{line_height + 2}">
                    <animate
                        attributeName="width"
                        from="0"
                        to="{svg_width}"
                        dur="0.45s"
                        begin="{y * 0.025}s"
                        fill="freeze"/>
                </rect>
            </clipPath>
            """
        )

    svg.append("</defs>")

    # ASCII rows
    for y, line in enumerate(lines):

        escaped = html.escape(line)

        svg.append(
            f"""
            <text
                x="2"
                y="{(y + 1) * line_height}"
                font-family="monospace"
                font-size="{font_size}px"
                fill="#333333"
                clip-path="url(#row-{y})"
                xml:space="preserve">{escaped}</text>
            """
        )

    svg.append("</svg>")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Done! Created: {OUTPUT}")


if __name__ == "__main__":
    main()