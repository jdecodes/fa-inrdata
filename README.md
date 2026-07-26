# fa-inrdata

Generate historical stock prices in INR with **SBI TT Buying Rates** for Indian Income Tax **Schedule FA (Foreign Assets)** reporting.


---

## Why this project?

If you own foreign stocks (RSUs, ESPPs), filing **Schedule FA** in the Indian Income Tax Return (ITR) can be surprisingly tedious.

For every foreign holding, you may need values such as:

* Initial value of investment
* Peak value during the year
* Closing balance
* Gross proceeds
* Gross income/dividends

These values are required **in INR**, not in the foreign currency.

The challenge is that historical INR values depend on the **SBI TT Buying Rate** applicable on the respective dates.

Finding those rates manually for every trading day is extremely time-consuming, especially when your portfolio contains hundreds of transactions.

This project automates that process by generating historical datasets where every trading day's market price is enriched with the corresponding SBI TT Buying Rate and its INR equivalent.

---

## How it works

For every supported ticker and year, the project:

1. Downloads historical daily prices from Yahoo Finance.
2. Fetches the corresponding historical SBI TT Buying Rate.
3. Computes the INR price for each trading day.
4. Stores the results as CSV files.

Example:

```text
data/
├── AAPL/
│   ├── 2024.csv
│   └── 2025.csv
├── MSFT/
│   └── 2025.csv
└── NVDA/
    └── 2025.csv
```

These generated files can later be used to determine:

* Initial investment value (INR)
* Peak value during the reporting period
* Closing balance
* Other Schedule FA computations

---

## Why generate data only after year-end?

Schedule FA is filed for a completed financial year.

Since historical prices and SBI TT rates are finalized after the year ends, there is generally **no need to regenerate historical datasets repeatedly**.

A typical workflow is:

* Wait until the relevant calendar year has ended.
* Generate that year's dataset once.
* Reuse the generated CSVs while preparing Schedule FA.

This keeps the dataset stable and avoids unnecessary overwrites.

---

## Dependencies

Historical exchange conversion uses the **sbi-tt-rates** project.

Install it using:

```bash
pip install sbi-tt-rates
```

GitHub:

https://github.com/jdecodes/sbi-tt-rates

The package itself builds upon: https://github.com/sahilgupta/sbi-fx-ratekeeper

---

## Installation

Clone the repository:

```bash
git clone https://github.com/jdecodes/fa-inrdata.git
cd fa-inrdata
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Generate data for a specific year:

```bash
python main.py --year 2025
```

The generated CSV files will be stored under the `data/` directory.

---

## Supported Companies

Supported companies are listed in:

```text
tickers.csv
```

Each row contains:

* Ticker
* Company Name
* Address
* ZIP Code
* Country

---

## Missing a Company?

If a company is not currently supported:

* Open an Issue
* Or submit a Pull Request updating `tickers.csv`

Please include:

* Yahoo Finance ticker
* Company name
* Registered address
* ZIP / Postal code
* Country

Note : as ticker file in csv, don't include extra commas, or "" while adding new tickers.
This helps improve Schedule FA reporting for everyone.

---

## Data Sources

* Yahoo Finance — Historical daily stock prices
* SBI TT Buying Rates — Historical TT buying rates used for INR conversion

---

## Disclaimer

This project is **unofficial** and is provided for educational and tax-assistance purposes only.

Although reasonable efforts have been made to generate accurate historical datasets, the generated values **may contain errors**.

Always verify the final numbers before filing your Income Tax Return.

The authors accept **no responsibility or liability** for tax filings, financial decisions, or losses arising from the use of this project.

---

## License

This project is licensed under the **MIT License**.
