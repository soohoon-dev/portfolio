import pandas as pd
import json
import os

# ==========================================
# CONFIGURATION
# ==========================================
INPUT_PATH = '../data/raw/wp_wap_nex_forms_entries-edit.csv'
OUTPUT_PATH = '../data/processed/cleaned_skincare_data.csv'

# Service ID to Name Mapping (Based on client website)
SERVICE_MAP = {
    '1': 'Skin Lifting / Tightening',
    '2': 'Rejuvenation / Injectables',
    '3': 'Dark Spot / Melasma',
    '4': 'Pore / Acne',
    '5': 'Body Treatments',
    '6': 'Facials',
    '7': 'General Consultation'
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def parse_form_data(json_str):
    """
    Parses the JSON string from the 'form_data' column.
    Transforms list of dicts [{'field_name': 'age', 'field_value': '30'}]
    into a flat dictionary {'age': '30'}.
    """
    try:
        if pd.isna(json_str):
            return {}
        data_list = json.loads(json_str)
        return {item['field_name']: item['field_value'] for item in data_list}
    except (json.JSONDecodeError, TypeError):
        return {}

def main():
    print(f"Status: Loading data from {INPUT_PATH}...")
    
    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_PATH)
    except FileNotFoundError:
        print("Error: Input file not found. Please check the file path.")
        return

    # 2. Parse JSON 'form_data'
    print("Status: Parsing unstructured JSON fields...")
    df['parsed'] = df['form_data'].apply(parse_form_data)
    
    # Normalize the dictionary into separate columns
    df_parsed = pd.json_normalize(df['parsed'])
    
    # Combine original metadata with parsed data
    df_clean = pd.concat([df[['Id', 'date_time', 'city']], df_parsed], axis=1)

    # 3. Data Cleaning & Feature Engineering
    print("Status: Cleaning and transforming features...")

    # A. Time Features (For 'Golden Time' Analysis)
    df_clean['submission_time'] = pd.to_datetime(df_clean['date_time'], errors='coerce')
    df_clean['hour'] = df_clean['submission_time'].dt.hour
    df_clean['day_of_week'] = df_clean['submission_time'].dt.day_name()

    # B. Customer Type Standardization
    # Logic: Merge 'question_1' and 'question_2' to handle schema variations
    df_clean['customer_type_raw'] = df_clean['question_1'].fillna(df_clean.get('question_2', ''))
    
    df_clean['customer_type'] = df_clean['customer_type_raw'].replace({
        'I am New': 'New', 
        'Welcome Back!': 'Returning',
        'BACK': 'Returning',
        'new_treatment': 'New'
    })
    # Assumption: Unknown types are treated as 'New' if they selected a service
    df_clean['customer_type'] = df_clean['customer_type'].fillna('Unknown')
    df_clean.loc[df_clean['customer_type'] == 'Unknown', 'customer_type'] = 'New'

    # C. Service Mapping
    df_clean['service_id'] = df_clean['service'].astype(str)
    df_clean['service_name'] = df_clean['service_id'].map(SERVICE_MAP).fillna('Other')

    # D. Lead Conversion Status (Is the form complete?)
    # Logic: A valid lead must have 'Age' and 'Service' filled out
    df_clean['age'] = pd.to_numeric(df_clean['age'], errors='coerce')
    df_clean['is_complete'] = df_clean.apply(
        lambda x: 1 if (pd.notnull(x['age']) and x['service_name'] != 'Other') else 0, axis=1
    )

    # 4. Filter & Select Final Columns
    final_cols = [
        'Id', 'submission_time', 'day_of_week', 'hour', 
        'city', 'customer_type', 'service_name', 'age', 'is_complete'
    ]
    # Ensure all columns exist before selecting
    available_cols = [c for c in final_cols if c in df_clean.columns]
    df_final = df_clean[available_cols]

    # 5. Export
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_final.to_csv(OUTPUT_PATH, index=False)
    print(f"Success! Processed data saved to: {OUTPUT_PATH}")
    print(f"Total Records Processed: {len(df_final)}")

if __name__ == "__main__":
    main()