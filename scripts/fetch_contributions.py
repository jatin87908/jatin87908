import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "jatin87908"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def main():
    print(f"Fetching contributions for @{USERNAME}...")

    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    days = []

    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")
        level = cell.get("data-level")

        if not date or level is None:
            continue

        label = cell.get("aria-label", "")

        match = re.search(r"(\d[\d,]*) contribution", label)

        count = 0

        if match:
            count = int(match.group(1).replace(",", ""))

        days.append(
            {
                "date": date,
                "count": count,
                "level": int(level),
            }
        )

    if not days:
        raise RuntimeError(
            "No contribution cells found. GitHub may have changed its HTML."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "username": USERNAME,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "days": days,
    }

    OUTPUT.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    print(f"Saved {len(days)} contribution days.")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()