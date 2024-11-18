import numpy as np
import matplotlib.pyplot as plt

# 给定的数据点
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# 使用最小二乘法计算拟合直线的参数
# 计算斜率a和截距b
A = np.vstack([x, np.ones_like(x)]).T
a, b = np.linalg.lstsq(A, y, rcond=None)[0]

# 拟合直线方程 y = ax + b
y_fit = a * x + b

# 绘制数据点和拟合直线
plt.scatter(x, y, color='red', label='数据点')  # 绘制原始数据点
plt.plot(x, y_fit, label=f'拟合直线: y = {a:.2f}x + {b:.2f}', color='blue')  # 绘制拟合直线

# 添加图形标签
plt.xlabel('x')
plt.ylabel('y')
plt.title('最小二乘法拟合')
plt.legend()

# 显示图形
plt.grid(True)
plt.show()
