#提取鞋底数据cha_chb

import pandas as pd
import json

# Load the Excel file
file_path = 'data.xlsx'  # Replace with your actual file path

# Load the data from the sheet
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Function to extract the "CHA" and "CHB" values from a JSON-like string
def extract_cha_chb(row):
    try:
        # Convert the string to a dictionary
        record = json.loads(row)
        # Return the values associated with the "CHA" and "CHB" keys
        cha_value = record.get("CHA", None)
        chb_value = record.get("CHB", None)
        return cha_value, chb_value
    except json.JSONDecodeError:
        return None, None

# Apply the extraction function to each row and store the results in new columns
data[['CHA_value', 'CHB_value']] = data.iloc[:, 0].apply(extract_cha_chb).apply(pd.Series)

# Get the non-null "CHA" and "CHB" values
cha_chb_values = data[['CHA_value', 'CHB_value']].dropna()

# Save the extracted "CHA" and "CHB" values to a new Excel file
output_file_path = 'extracted_values.xlsx'  # Replace with your desired output file path
cha_chb_values.to_excel(output_file_path, index=False)

print(f"CHA and CHB values have been saved to {output_file_path}")
