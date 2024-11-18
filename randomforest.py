import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei黑体（或选择其他支持中文的字体）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号无法显示的问题

# 生成正弦波数据
def generate_sine_wave(frequency, sampling_rate=1000, duration=1):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    return t, np.sin(2 * np.pi * frequency * t)

# 提取特征：峰值数量和平均峰值间隔
def extract_features(signal, sampling_rate=1000):
    peaks, _ = find_peaks(signal)
    num_peaks = len(peaks)
    if num_peaks > 1:
        peak_intervals = np.diff(peaks) / sampling_rate
        avg_peak_interval = np.mean(peak_intervals)
    else:
        avg_peak_interval = 0
    return num_peaks, avg_peak_interval

# 生成训练数据
frequencies = np.linspace(1, 100, 500)  # 频率范围从1Hz到50Hz
features = []
labels = []

for freq in frequencies:
    _, sine_wave = generate_sine_wave(freq)
    num_peaks, avg_peak_interval = extract_features(sine_wave)
    features.append([num_peaks, avg_peak_interval])
    labels.append(freq)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# 训练随机森林回归模型
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = rf.predict(X_test)

# 评估模型性能
mse = mean_squared_error(y_test, y_pred)
print(f"均方误差: {mse:.2f}")

# 示例：预测新正弦波的频率
new_freq = 10  # 新的频率
t, new_sine_wave = generate_sine_wave(new_freq)
num_peaks, avg_peak_interval = extract_features(new_sine_wave)
predicted_freq = rf.predict([[num_peaks, avg_peak_interval]])[0]
print(f"真实频率: {new_freq} Hz, 预测频率: {predicted_freq:.2f} Hz")

# 根据预测频率生成正弦波
_, predicted_sine_wave = generate_sine_wave(predicted_freq)

# 绘制原始正弦波和预测正弦波
plt.figure(figsize=(10, 6))
plt.plot(t, new_sine_wave, label=f'原始正弦波 (频率: {new_freq} Hz)')
plt.plot(t, predicted_sine_wave, label=f'预测正弦波 (频率: {predicted_freq:.2f} Hz)', linestyle='--')
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.title('原始正弦波与预测正弦波对比')
plt.legend()
plt.grid(True)
plt.show()
