"""
builder.py

Builds yearly price history files enriched with SBI TT buying rates.
"""

from __future__ import annotations

import os

import pandas as pd
import yfinance as yf
from sbi_tt_rates import get_rate


def fetch_yahoo_prices(ticker: str, year: int) -> pd.DataFrame:
    """
    Fetch daily close prices for the given ticker/year.
    """

    start = f"{year}-01-01"
    end = f"{year + 1}-01-01"

    raw = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
    )

    if raw.empty:
        raise ValueError(
            f"No price data returned for ticker='{ticker}', year={year}"
        )

    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = raw[["Close"]].reset_index()
    df.columns = ["date", "close"]

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["close"] = df["close"].astype(float)

    return df.sort_values("date").reset_index(drop=True)


def enrich_with_sbi_tt(
    df: pd.DataFrame,
    currency: str = "USD",
) -> pd.DataFrame:
    """
    Adds SBI TT buying rate and INR close price.
    """

    df = df.copy()

    df["sbi_tt"] = df["date"].apply(
        lambda d: float(
            get_rate(
                d.isoformat(),
                currency=currency,
                rate_type="tt_buy",
            ).rate
        )
    )

    df["close_inr"] = (df["close"] * df["sbi_tt"]).round(4)

    return df


def build_year_file(
    ticker: str,
    year: int,
    out_dir: str = "data",
    overwrite: bool = False,
) -> str:
    """
    Builds data/<ticker>/<year>.csv
    """

    ticker = ticker.upper().strip()

    ticker_dir = os.path.join(out_dir, ticker)
    out_path = os.path.join(ticker_dir, f"{year}.csv")

    if os.path.exists(out_path) and not overwrite:
        print(f"[skip] {out_path}")
        return out_path

    prices = fetch_yahoo_prices(ticker, year)
    prices = enrich_with_sbi_tt(prices)

    os.makedirs(ticker_dir, exist_ok=True)

    prices.to_csv(out_path, index=False)

    print(f"[wrote] {out_path} ({len(prices)} rows)")

    return out_path