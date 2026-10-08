OUTPUT = "info-card.svg"

lines = [
    ("Now", "BCA 3rd Year Student"),
    ("Focus", "Full Stack Development"),
    ("Stack", "Python • JavaScript • React • Node"),
    ("Learning", "DSA • System Design • AI/LLM"),
    ("Project", "CodeSync"),
    ("Goal", "SDE / Software Engineering"),
]

WIDTH = 490
HEIGHT = 300


def main():

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

    <rect
        width="100%"
        height="100%"
        rx="12"
        fill="#0d1117"
        stroke="#30363d"
        stroke-width="2"
    />

    <!-- Header -->
    <rect
        x="0"
        y="0"
        width="{WIDTH}"
        height="42"
        rx="12"
        fill="#161b22"
    />

    <text
        x="20"
        y="27"
        font-family="monospace"
        font-size="16"
        font-weight="bold"
        fill="#58a6ff">
        jatin@github:~
    </text>

    <text
        x="20"
        y="72"
        font-family="monospace"
        font-size="13"
        fill="#8b949e">
        ─────────────────────────────────
    </text>
'''

    y = 105

    for index, (key, value) in enumerate(lines):

        delay = index * 0.12

        svg += f'''
        <g opacity="0">
            <animate
                attributeName="opacity"
                from="0"
                to="1"
                dur="0.4s"
                begin="{delay}s"
                fill="freeze"
            />

            <text
                x="25"
                y="{y}"
                font-family="monospace"
                font-size="13"
                font-weight="bold"
                fill="#7ee787">
                {key}
            </text>

            <text
                x="125"
                y="{y}"
                font-family="monospace"
                font-size="13"
                fill="#c9d1d9">
                {value}
            </text>
        </g>
        '''

        y += 34

    svg += '''
    <text
        x="25"
        y="282"
        font-family="monospace"
        font-size="11"
        fill="#6e7681">
        $ whoami → building things, learning every day
    </text>

    </svg>
    '''

    with open(OUTPUT, "w", encoding="utf-8") as file:
        file.write(svg)

    print(f"Done! Created: {OUTPUT}")


if __name__ == "__main__":
    main()