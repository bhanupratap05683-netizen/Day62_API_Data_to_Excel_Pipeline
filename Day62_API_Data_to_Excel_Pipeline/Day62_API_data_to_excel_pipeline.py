import datetime
import os
import pandas as pd
import requests


def fetch_financial_data():
    """Extract: Fetches real-time market data from a public API endpoint."""
    # Using a reliable public exchange rate API for currency or stock metrics
    url = "https://open.er-api.com/v6/latest/USD"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Extraction Error: Failed to fetch data. Details: {e}")
        return None


def transform_payload(raw_json):
    """Transform: Cleans, filters, and formats raw JSON data into a clean DataFrame."""
    if not raw_json or "rates" not in raw_json:
        return None

    # Extract the nested rates dictionary
    rates_dict = raw_json["rates"]

    # Convert dictionary to DataFrame
    df = pd.DataFrame(list(rates_dict.items()), columns=["Currency", "Rate"])

    # Financial data cleaning transformations
    # Filter for major global financial currencies
    major_currencies = ["INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"]
    df = df[df["Currency"].isin(major_currencies)].copy()

    # Add processing metadata tracking
    df["Base_Currency"] = raw_json.get("base_code", "USD")
    df["Last_Updated_UTC"] = raw_json.get("time_last_update_utc", "")
    df["Retrieved_At"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Reorder columns logically for financial analysis reporting
    df = df[
        [
            "Retrieved_At",
            "Base_Currency",
            "Currency",
            "Rate",
            "Last_Updated_UTC",
        ]
    ]

    return df


def load_to_excel(df, output_filename="FX_Market_Pipeline.xlsx"):
    """Load: Exports the processed DataFrame into a polished Excel file."""
    if df is None or df.empty:
        print("Load Error: No data available to write.")
        return

    try:
        # Use ExcelWriter for clean writing configurations
        with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Live_FX_Rates", index=False)

        print(
            f"Pipeline Execution Successful! Data loaded to '{output_filename}'."
        )
    except Exception as e:
        print(f"Load Error: Failed to write to Excel. Details: {e}")


if __name__ == "__main__":
    print("Starting Day 62 Automated API to Excel Pipeline...")

    # Run the full end-to-end pipeline
    raw_data = fetch_financial_data()
    processed_df = transform_payload(raw_data)
    load_to_excel(processed_df)