import pandas as pd
import json
import re

# 读取日志文件路径
file_path = 'C:/Users/203/Desktop/data/FP_NULL.log'
with open(file_path, 'r') as file:
    file_content = file.readlines()

# 提取 scannum、CHA 和 CHB 的数据
data = []
for line in file_content:
    # 使用正则表达式提取 scannum
    scannum_match = re.search(r'\[scannum:(\d+)\]', line)
    if scannum_match:
        scannum = int(scannum_match.group(1))
        # 提取行中的 JSON 部分
        json_part = line.split(']')[-1].strip()
        try:
            json_data = json.loads(json_part)
            if 'CHA' in json_data and 'CHB' in json_data:
                cha = json_data['CHA']
                chb = json_data['CHB']
                data.append((scannum, max(cha, chb)))
        except json.JSONDecodeError:
            continue

# 将数据转换为 DataFrame
df = pd.DataFrame(data, columns=['scannum', 'max_value'])

# 透视数据，使每个 scannum 成为一列
pivot_df = df.pivot_table(index=df.index, columns='scannum', values='max_value', aggfunc='first')

# 保存为 Excel 文件
output_file_path = 'C:/Users/203/Desktop/data/scannum_max_values.xlsx'
pivot_df.to_excel(output_file_path, index=False)

print("数据已保存为 Excel 文件：", output_file_path)
