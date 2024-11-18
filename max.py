import json
import pandas as pd
import os

# Step 1: 定义文件夹路径
folder_path = 'C:/Users/203/Desktop/data/'

# Step 2: 初始化数据字典以存储每个文件的结果
data_dict = {}

# Step 3: 遍历文件夹中的所有 .log 文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.log'):
        file_path = os.path.join(folder_path, file_name)
        max_values = []

        # 逐行读取文件并提取 CHA 和 CHB
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    # 提取日志中包含 JSON 数据的部分
                    json_start = line.find('{')
                    json_data = line[json_start:]

                    # 将 JSON 数据加载为字典
                    log_entry = json.loads(json_data)

                    # 检查是否有 "CHA" 和 "CHB" 字段
                    if "CHA" in log_entry and "CHB" in log_entry:
                        cha_value = log_entry["CHA"]
                        chb_value = log_entry["CHB"]

                        # 选择较大的值
                        max_value = max(cha_value, chb_value)

                        # 添加到最大值列表中
                        max_values.append(max_value)
                except (ValueError, KeyError):
                    # 跳过无法解析的行或缺少字段的行
                    continue

        # 将每个文件的最大值保存到字典中
        if max_values:
            data_dict[file_name] = pd.DataFrame(max_values, columns=["Max_Value"])

# Step 4: 将每个文件的数据保存为对应的 Excel 文件
for file_name, df in data_dict.items():
    output_file_name = file_name.replace('.log', '.xlsx')
    output_file_path = os.path.join(folder_path, output_file_name)
    df.to_excel(output_file_path, index=False)
    print(f"Excel 文件已保存到: {output_file_path}")
