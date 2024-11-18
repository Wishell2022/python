import os
import re
import json
import pandas as pd
from collections import defaultdict

def process_log_files(folder_path, output_excel_path):
    # Prepare to extract scannum, CHA, and CHB for all files
    data = defaultdict(list)

    # Regular expression patterns to match scannum and JSON data
    scannum_pattern = re.compile(r'\[scannum:(\d+)\]')
    json_pattern = re.compile(r'\{.*\}')

    # Iterate through all log files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.log'):
            file_path = os.path.join(folder_path, file_name)
            # Read the file and extract scannum, CHA, and CHB
            with open(file_path, 'r') as file:
                for line in file:
                    # Extract scannum
                    scannum_match = scannum_pattern.search(line)
                    if scannum_match:
                        scannum = int(scannum_match.group(1))

                    # Extract JSON part
                    json_match = json_pattern.search(line)
                    if json_match:
                        json_data = json.loads(json_match.group())
                        # Only process lines with "message-type": "smd-scan"
                        if json_data.get("message-type") == "smd-scan":
                            cha = json_data.get("CHA")
                            chb = json_data.get("CHB")
                            if cha is not None and chb is not None:
                                # Save the larger value of CHA and CHB under the corresponding scannum
                                data[scannum].append(max(cha, chb))

    # Convert the data to a DataFrame
    # Each scannum becomes a column, and each value is added row-wise
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))

    # Save to an Excel file
    df.to_excel(output_excel_path, index=False)

# Define folder path containing log files and the output Excel file path
folder_path = 'C:/Users/203/Desktop/data'  # Replace with your folder path
output_excel_path = 'C:/Users/203/Desktop/data/all_logs_scannum_cha_chb_values.xlsx'

# Process all log files in the folder and save to an Excel file
process_log_files(folder_path, output_excel_path)

# Display the output path
print(output_excel_path)
