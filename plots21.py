import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 文件路径
file_path = 'C:/Users/203/Desktop/111.txt'

# 读取文件，跳过注释行并设置列名
data = pd.read_csv(file_path, sep='\t', comment='#', skiprows=3, header=None, names=["Frequency (GHz)", "Re_S21", "Im_S21"])

# 计算 S21 的幅度
data['Magnitude_S21'] = np.sqrt(data['Re_S21']**2 + data['Im_S21']**2)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(data['Frequency (GHz)'], data['Magnitude_S21'], label="DK=2")
plt.xlabel("Frequency (GHz)")
plt.ylabel("Magnitude of S21")
plt.title("Magnitude of S21 vs Frequency for DK=2")
plt.legend()
plt.grid(True)
plt.show()
