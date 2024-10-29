import os
import re
import pandas as pd
import json
import matplotlib.pyplot as plt

# Folder containing the log files
folder_path = r'C:\Users\203\Desktop\data'

# Regular expression to extract scannum from the line
scannum_pattern = re.compile(r'\[scannum:(\d+)\]')

# Data structures to hold entries for files with and without "null"
scannum_data_with_null = {}
scannum_data_without_null = {}

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Ensure the file is a text file
    if os.path.isfile(file_path) and filename.endswith('.log'):
        # Determine if the file name contains "null"
        target_data = scannum_data_with_null if "null" in filename.lower() else scannum_data_without_null
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Extract scannum
                scannum_match = scannum_pattern.search(line)
                if scannum_match:
                    scannum = scannum_match.group(1)
                    
                    # Extract JSON part and parse it
                    json_part = line.split(']', 1)[-1].strip()
                    try:
                        log_entry = json.loads(json_part)
                        
                        # Check if CHA and CHB are present in the log entry
                        if 'CHA' in log_entry and 'CHB' in log_entry:
                            cha_value = log_entry['CHA']
                            chb_value = log_entry['CHB']
                            
                            # Initialize scannum entry if it doesn't exist
                            if scannum not in target_data:
                                target_data[scannum] = {'CHA': [], 'CHB': []}
                            
                            # Append CHA and CHB values for each scannum
                            target_data[scannum]['CHA'].append(cha_value)
                            target_data[scannum]['CHB'].append(chb_value)
                    except json.JSONDecodeError:
                        continue

# Function to calculate counts for each threshold for a given data set
def calculate_threshold_counts(scannum_data):
    threshold_counts = []
    for threshold in range(100, 401):
        count = 0
        for scannum, values in scannum_data.items():
            if any(cha > threshold for cha in values['CHA']) or any(chb > threshold for chb in values['CHB']):
                count += 1
        threshold_counts.append({'Threshold': threshold, 'Count': count})
    return pd.DataFrame(threshold_counts)

# Calculate threshold counts for both data sets
df_counts_with_null = calculate_threshold_counts(scannum_data_with_null)
df_counts_without_null = calculate_threshold_counts(scannum_data_without_null)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(df_counts_with_null['Threshold'], df_counts_with_null['Count'], marker='o', color='b', linestyle='-', label='null')
plt.plot(df_counts_without_null['Threshold'], df_counts_without_null['Count'], marker='o', color='r', linestyle='-', label='with object')
plt.title('Count of Scannum Entries with CHA or CHB Above Threshold')
plt.xlabel('Threshold Value')
plt.ylabel('Count')
plt.legend()
plt.grid()
plt.show()

# Optional: Save the DataFrames to Excel files
output_path_with_null = r'C:\Users\203\Desktop\data\threshold_counts_with_null.xlsx'
output_path_without_null = r'C:\Users\203\Desktop\data\threshold_counts_without_null.xlsx'
df_counts_with_null.to_excel(output_path_with_null, index=False)
df_counts_without_null.to_excel(output_path_without_null, index=False)

print(f"Threshold counts saved to {output_path_with_null} and {output_path_without_null}")
