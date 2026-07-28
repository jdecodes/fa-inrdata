from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from sbi_tt_rates import get_rate

import requests

DIVIDEND_DIR = Path("dividends")

URL = "https://api.nasdaq.com/api/quote/{ticker}/dividends"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def _parse_date(date_str: str) -> datetime | None:
    if not date_str or date_str == "N/A":
        return None

    return datetime.strptime(date_str, "%m/%d/%Y")


def _parse_amount(amount: str) -> float:
    return float(amount.replace("$", "").replace(",", "").strip())


def _download_dividends(ticker: str) -> list[dict]:
    response = requests.get(
        URL.format(ticker=ticker),
        params={
            "assetclass": "stocks",
            "lang": "en",
        },
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()

    status = payload.get("status", {})
    if status.get("rCode") != 200:
        raise RuntimeError(
            status.get("developerMessage")
            or status.get("bCodeMessage")
            or str(status)
        )

    data = payload.get("data")
    if not data:
        return []

    dividends = data.get("dividends")
    if not dividends:
        return []

    rows = dividends.get("rows")
    return rows or []


def build_dividend_history(
    ticker: str,
    year: int,
) -> None:
    """
    Update dividend history for a single calendar year.

    Existing years are preserved.
    The requested year is replaced.
    """

    rows = _download_dividends(ticker)

    dividends = []

    for row in rows:
        payment = _parse_date(row["paymentDate"])

        if payment is None:
            continue

        if payment.year != year:
            continue

        record = _parse_date(row["recordDate"])

        sbi_rate = get_rate(
            payment.strftime("%Y-%m-%d"),
            currency="USD",
            rate_type="tt_buy",
        )

        dividend_per_share = _parse_amount(row["amount"])
        dividend_per_share_inr = dividend_per_share * sbi_rate.rate

        dividends.append(
            {
                "record_date": record.strftime("%Y-%m-%d"),
                "payment_date": payment.strftime("%Y-%m-%d"),
                "dividend_per_share": dividend_per_share,
                "dividend_per_share_inr": round(dividend_per_share_inr, 2),
            }
        )

    dividends.sort(key=lambda x: x["payment_date"])

    DIVIDEND_DIR.mkdir(parents=True, exist_ok=True)

    outfile = DIVIDEND_DIR / f"{ticker.upper()}.json"

    if outfile.exists():
        with outfile.open("r", encoding="utf-8") as fp:
            existing = json.load(fp)
    else:
        existing = {}

    # Replace this year (idempotent)
    existing[str(year)] = dividends

    # Keep years sorted
    existing = dict(sorted(existing.items()))

    with outfile.open("w", encoding="utf-8") as fp:
        json.dump(existing, fp, indent=2)
        fp.write("\n")