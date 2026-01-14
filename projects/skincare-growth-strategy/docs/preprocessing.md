# Data Preprocessing Pipeline

## 1. Objective

The raw data from the clinic's website is stored in a MySQL database and exported as CSV. However, the critical lead information (Age, Service Interest, Customer Type) is encapsulated within a nested JSON string in the `form_data` column.

This script extracts that unstructured data and transforms it into a clean, tabular format suitable for Looker Studio visualization.

## 2. Key Transformations

### A. JSON Parsing

- **Input:** `[{"field_name": "age", "field_value": "34"}, ...]`
- **Output:** Column `age` with value `34`.
- **Technique:** Used Python's `json` library to parse strings and `pandas.json_normalize` to flatten the structure.

### B. Feature Engineering

- **Time-of-Day Analysis:** Extracted `hour` (0-23) from the timestamp to identify peak traffic times (specifically checking for the 9 PM "Golden Time").
- **Service Mapping:** Mapped numerical Service IDs (e.g., '3') to business-readable names (e.g., 'Dark Spot / Melasma').
- **Customer Segmentation:** Standardized various input values (e.g., 'I am New', 'new_treatment') into binary categories: `New` vs. `Returning`.

## 3. How to Run

Required libraries: `pandas`

    cd scripts
    python 01_data_preprocessing.py

## 4. Output

- **File:** `data/processed/cleaned_skincare_data.csv`
- **Usage:** This file serves as the primary data source for the Looker Studio Dashboard.
