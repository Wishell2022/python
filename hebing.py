
##合并文件夹内提取的cha_chb

import os
import pandas as pd

# 设置文件夹路径和输出文件名
folder_path = r"C:\Users\203\Desktop\hebing"
output_file = "merged_output.xlsx"  # 合并后的文件名

# 获取文件夹内所有的Excel文件
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 创建一个空的DataFrame用于合并所有的Excel文件
merged_df = pd.DataFrame()

# 逐个读取文件并合并
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    # 读取Excel文件到DataFrame
    df = pd.read_excel(file_path)
    # 将数据添加到合并的DataFrame中
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# 将合并后的数据保存为新的Excel文件
merged_df.to_excel(output_file, index=False)

print(f"合并完成，结果已保存为 {output_file}")
