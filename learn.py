import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Step 1: 生成或加载曲线特征数据（假设特征已经提取）
# 这里使用示例数据，假设有十个特征代表曲线信息
# 实际情况下，你需要从每条曲线中提取统计特征（例如最大值、最小值、平均值等）
np.random.seed(42)
num_samples = 1000
num_features = 10  # 假设每条曲线提取10个特征
X = np.random.rand(num_samples, num_features)  # 1000条曲线，每条曲线提取10个特征
y = 10 * X[:, 0] + 5 * X[:, 1] + 3 * X[:, 2] + np.random.rand(num_samples)  # 水分值（模拟真实关系）

# Step 2: 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: 初始化随机森林回归模型
rf = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=10)

# Step 4: 训练模型
rf.fit(X_train, y_train)

# Step 5: 进行预测
y_pred = rf.predict(X_test)

# Step 6: 评估模型性能
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R^2 Score: {r2:.4f}")

# 可视化预测值与实际值的对比
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='b')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Actual Water Content')
plt.ylabel('Predicted Water Content')
plt.title('Actual vs Predicted Water Content')
plt.grid(True)
plt.show()
