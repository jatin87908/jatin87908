import json
from pathlib import Path
from datetime import datetime


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

CELL = 13
GAP = 4

LEFT = 35
TOP = 30

WIDTH = 860
HEIGHT = 150


def main():

    data = json.loads(INPUT.read_text(encoding="utf-8"))

    days = data["days"]

    # GitHub contribution levels are normally 0-4
    # Clamp just in case.
    for day in days:
        day["level"] = max(0, min(4, day["level"]))

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">
        '''
    )

    svg.append(
        '''
        <rect width="100%" height="100%" rx="12"
              fill="#0d1117"/>
        '''
    )

    # Title
    svg.append(
        '''
        <text x="20" y="20"
              font-family="monospace"
              font-size="11"
              fill="#8b949e">
            jatin@github:~$ contributions
        </text>
        '''
    )

    # Draw calendar
    for index, day in enumerate(days[-371:]):

        week = index // 7
        weekday = index % 7

        x = LEFT + week * (CELL + GAP)
        y = TOP + weekday * (CELL + GAP)

        level = day["level"]

        delay = index * 0.006

        svg.append(
            f'''
            <rect
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="3"
                fill="{PALETTE[level]}"
                opacity="0">

                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    dur="0.25s"
                    begin="{delay:.3f}s"
                    fill="freeze"/>
            </rect>
            '''
        )

    total = sum(day["count"] for day in days)

    svg.append(
        f'''
        <text x="20" y="132"
              font-family="monospace"
              font-size="11"
              fill="#8b949e">
            {total:,} contributions in the last year
        </text>
        '''
    )

    # Legend
    legend_x = 620

    svg.append(
        '''
        <text x="620" y="132"
              font-family="monospace"
              font-size="10"
              fill="#8b949e">
            Less
        </text>
        '''
    )

    for i, color in enumerate(PALETTE):

        x = legend_x + 32 + i * 17

        svg.append(
            f'''
            <rect x="{x}" y="123"
                  width="11"
                  height="11"
                  rx="2"
                  fill="{color}"/>
            '''
        )

    svg.append(
        '''
        <text x="755" y="132"
              font-family="monospace"
              font-size="10"
              fill="#8b949e">
            More
        </text>
        '''
    )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8",
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()