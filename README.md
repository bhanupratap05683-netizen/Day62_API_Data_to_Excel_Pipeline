# Automated API to Excel Financial Data Pipeline

## Overview
An automated Python ETL pipeline that interfaces with an external web API, extracts live market payloads, normalizes nested JSON data structures, and writes polished data exports directly to Excel spreadsheets.

## Architecture & Workflow
1. **Extract (`fetch_financial_data`):** Issues resilient HTTP GET requests with custom timeout configurations to safely extract currency market benchmarks.
2. **Transform (`transform_payload`):** Parses raw JSON payloads into high-performance pandas DataFrames, isolates critical currencies, and appends execution audit timestamps.
3. **Load (`load_to_excel`):** Uses an explicit context manager engine to securely package data structures directly into target spreadsheets without file corruption risk.

## Tech Stack
* Python 3.x
* pandas (Data Processing)
* requests (HTTP Client Engine)
* openpyxl (Excel Optimization)

## How to Run
Ensure dependencies are satisfied:
```bash
pip install pandas requests openpyxl
