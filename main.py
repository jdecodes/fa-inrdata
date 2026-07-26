import argparse

from pricehistory import build_year_file
from ticker_parser import load_tickers
import time

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fa-inrdata",
        description="Build historical INR-enriched stock data.",
    )

    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Calendar year to build.",
    )

    args = parser.parse_args()

    tickers = load_tickers()
    failed_tickers = []
    for ticker in tickers:
        symbol = ticker["ticker"]
        start_time = time.time()
        try:
            build_year_file(ticker=symbol, year=args.year)
            end_time = time.time()
            print(f"[generated] {symbol} in {end_time - start_time} seconds")

        except Exception as ex:
            print(f"[SKIPPED] {symbol}: {ex}")
            failed_tickers.append(symbol)
            continue

    print("\nGeneration completed.")
    if failed_tickers:
        print("\nSkipped tickers:")
        for symbol in failed_tickers:
            print(f"  - {symbol}")


if __name__ == "__main__":
    main()