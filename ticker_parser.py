"""
loader.py

Loads and validates the master ticker list.
"""

from __future__ import annotations

import csv
from pathlib import Path

EXPECTED_COLUMNS = [
    "ticker",
    "name",
    "address",
    "zip",
    "country",
]


TICKERS_FILE = "tickers.csv"

def _ticker_csv_path() -> Path:
    """Returns the path to tickers.csv."""
    return Path(__file__).resolve().parent / TICKERS_FILE


def load_tickers() -> list[dict[str, str]]:
    """
    Loads and validates tickers.csv.

    Returns
    -------
    list[dict]
        One dictionary per ticker.
    """

    csv_path = _ticker_csv_path()

    if not csv_path.exists():
        raise FileNotFoundError(f"Ticker file not found: {csv_path}")

    # ---------- Raw validation ----------
    with csv_path.open("r", encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split(",")

        if header != EXPECTED_COLUMNS:
            raise ValueError(
                f"Invalid header.\n"
                f"Expected: {EXPECTED_COLUMNS}\n"
                f"Found: {header}"
            )

        for line_no, line in enumerate(f, start=2):
            line = line.rstrip("\n")

            if not line:
                raise ValueError(f"Row {line_no}: Empty line")

            if '"' in line:
                raise ValueError(f"Row {line_no}: Quotes are not allowed")

            fields = line.split(",")

            if len(fields) != len(EXPECTED_COLUMNS):
                print(f" found {fields}")
                raise ValueError(
                    f"Row {line_no}: Expected {len(EXPECTED_COLUMNS)} fields, "
                    f"found {len(fields)}"
                )

            if any(not field.strip() for field in fields):
                raise ValueError(f"Row {line_no}: Empty field found")

    # ---------- Parse ----------
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)