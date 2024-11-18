import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# 生成正弦数据
X = np.linspace(0, 2*np.pi, 100).reshape(-1, 1)  # 输入特征 x
y = np.sin(X).ravel()  # 目标输出 y = sin(x)

# 创建并训练随机森林回归模型
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 预测
y_pred = model.predict(X)

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(X, y, label="True sin(x)", color='blue')
plt.plot(X, y_pred, label="Random Forest Prediction", color='red', linestyle='--')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Random Forest Fitting Sin Function")
plt.show()
