import os
import re
import pandas as pd
import json

# Folder containing the log files
folder_path = r'C:\Users\203\Desktop\data'

# List to store the extracted data from all files
data = []

# Regular expression to extract scannum from the line
scannum_pattern = re.compile(r'\[scannum:(\d+)\]')

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Ensure the file is a text file (you can adjust this if needed)
    if os.path.isfile(file_path) and filename.endswith('.log'):
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
                            # Append scannum, CHA, and CHB to data list
                            data.append({
                                'filename': filename,  # add filename for reference
                                'scannum': scannum,
                                'CHA': log_entry['CHA'],
                                'CHB': log_entry['CHB']
                            })
                    except json.JSONDecodeError:
                        continue

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_path = r'C:\Users\203\Desktop\data\scannum_cha_chb_data.xlsx'
df.to_excel(output_path, index=False)

print(f"Data saved to {output_path}")
