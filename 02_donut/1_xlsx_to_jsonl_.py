import pandas as pd
import json
import math
import os

# Load the Excel file
df = pd.read_excel('excels/final_1077inv_v03.xlsx')  # Include the 'excels' folder in the file path
print("Excel file loaded.")

# Convert date fields to datetime
date_fields = ['invoice_date', 'charge_period_start_date', 'charge_period_end_date']
for field in date_fields:
    df[field] = pd.to_datetime(df[field], errors='coerce', dayfirst=True)

# Define the directory where you want to save the file
dir_name = './metadata/'

# Create 'metadata' directory if it does not exist
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Open the metadata.jsonl file in write mode
with open(os.path.join(dir_name, 'metadata.jsonl'), 'w') as f:
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Create the ground truth JSON object
        gt = {
            "vendor_name": row['vendor_name'].lower() if pd.notnull(row['vendor_name']) else None,  # Convert to lowercase
            "invoice_date": row['invoice_date'].strftime('%d/%m/%Y') if pd.notnull(row['invoice_date']) else None,  # Check for NaT
            "invoice_number": str(row['invoice_number']) if pd.notnull(row['invoice_number']) else None,  # Convert to string
            "total_amount": "{:.2f}".format(row['total_amount']) if pd.notnull(row['total_amount']) and isinstance(row['total_amount'], (int, float)) else str(row['total_amount']) if pd.notnull(row['total_amount']) else None,
            "charge_period_start_date": row['charge_period_start_date'].strftime('%d/%m/%Y') if pd.notnull(row['charge_period_start_date']) else None,  # Check for NaT
            "charge_period_end_date": row['charge_period_end_date'].strftime('%d/%m/%Y') if pd.notnull(row['charge_period_end_date']) else None,  # Check for NaT
            "mpan": str(int(row['mpan'])) if not math.isnan(row['mpan']) else None,  # Set to None if NaN
            "account_number": str(row['account_number']) if pd.notnull(row['account_number']) else None  # Convert to string
        }
        # Remove keys with None values
        gt = {k: v for k, v in gt.items() if v is not None}
        # Create the metadata JSON object
        metadata = {
            "file_name": str(row['file_name']) + '.jpg',  # Convert to string before appending the file extension
            "ground_truth": json.dumps({"gt_parse": gt})  # Wrap the ground truth JSON object in another JSON object with the key "gt_parse"
        }
        # Write the metadata JSON object to the file
        f.write(json.dumps(metadata) + '\n')
