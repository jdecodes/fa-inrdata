import argparse

from pricehistory import build_year_file
from ticker_parser import load_tickers
from dividends import build_dividend_history
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
    failed_dividends = []
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

        start_div_time = time.time()
        try:
            build_dividend_history(ticker=symbol, year=args.year)
            end_div_time = time.time()
            print(f"[generated] dividend of {symbol} in {end_div_time - start_div_time} seconds")
        except Exception as ex:
            print(f"[DIVIDEND FAILED] for {symbol}: {ex}")
            failed_dividends.append(symbol)

    print("\nGeneration completed.")
    if failed_tickers:
        print(f"Price history Skipped tickers: {len(failed_tickers) / {len(tickers)}}")
        print(f"{failed_tickers}")
    if failed_dividends:
        print(f"Dividend Skipped tickers: {len(failed_tickers) / {len(tickers)}}")
        print(f"{failed_dividends}")

if __name__ == "__main__":
    main()