import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei黑体（或选择其他支持中文的字体）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号无法显示的问题

# 用于存储每个 DK 值的数据的字典
dk_data = {}
current_dk = None

# 加载数据文件
file_path = 'C:/Users/203/Desktop/111.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        # 检测描述行中的 DK 值
        if "DK=" in line:
            dk_match = re.search(r"DK=(\d+\.?\d*)", line)
            if dk_match:
                current_dk = float(dk_match.group(1))
                dk_data[current_dk] = []  # 为当前 DK 初始化一个新的列表
            continue

        # 检查行是否包含实际数据（非说明行，且非空行）
        if current_dk is not None and line[0].isdigit():
            try:
                values = line.strip().split('\t')
                frequency = float(values[0])  # 频率 (GHz)
                real_part = float(values[1])   # S21 实部
                imag_part = float(values[2])   # S21 虚部
                dk_data[current_dk].append([frequency, real_part, imag_part])
            except ValueError:
                # 跳过不符合预期格式的行
                continue

# 绘制每个 DK 值的 S21 幅度和相位
plt.figure(figsize=(12, 10))

train = []
target = []
predicted = []

for dk, data in dk_data.items():
    df = pd.DataFrame(data, columns=["Frequency (GHz)", "S21 Real", "S21 Imaginary"])
    # 计算 S21 的幅度
    df['S21 Magnitude'] = np.sqrt(df['S21 Real']**2 + df['S21 Imaginary']**2)
    df['S21 Phase'] = np.arctan2(df['S21 Imaginary'], df['S21 Real']) * (180 / np.pi)  # 转换为角度制
    
    train.append(df['S21 Magnitude'].tolist()+df['S21 Phase'].tolist())
    target.append(dk)
    if dk == 2.2:
        predicted = df['S21 Magnitude'].tolist()+df['S21 Phase'].tolist()


X_train, X_test, y_train, y_test = train_test_split(train, target, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=10000, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"均方误差: {mse:.2f}")

predicted_dk = rf.predict([predicted])[0]

print(f"预测的 DK 值为: {predicted_dk:.2f}")