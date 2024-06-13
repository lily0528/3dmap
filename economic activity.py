import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 经济活动指数
economic_activity = {
    'Alberta': {'agriculture': 0.2, 'industry': 0.4, 'services': 0.6},
    'British Columbia': {'agriculture': 0.3, 'industry': 0.5, 'services': 0.7},
    'Manitoba': {'agriculture': 0.4, 'industry': 0.6, 'services': 0.8},
    'New Brunswick': {'agriculture': 0.2, 'industry': 0.3, 'services': 0.5},
    'Newfoundland and Labrador': {'agriculture': 0.1, 'industry': 0.2, 'services': 0.4},
    'Nova Scotia': {'agriculture': 0.2, 'industry': 0.3, 'services': 0.6},
    'Ontario': {'agriculture': 0.3, 'industry': 0.7, 'services': 0.9},
    'Prince Edward Island': {'agriculture': 0.3, 'industry': 0.4, 'services': 0.6},
    'Quebec': {'agriculture': 0.3, 'industry': 0.6, 'services': 0.8},
    'Saskatchewan': {'agriculture': 0.4, 'industry': 0.5, 'services': 0.7}
}

# 加载加拿大地图数据（省份边界）
province_boundaries = {
    'Alberta': (49, 60, -120, -110),
    'British Columbia': (48, 60, -140, -115),
    'Manitoba': (49, 60, -102, -88),
    'New Brunswick': (45, 48, -67, -64),
    'Newfoundland and Labrador': (46, 52, -60, -53),
    'Nova Scotia': (43, 47, -67, -60),
    'Ontario': (42, 50, -95, -74),
    'Prince Edward Island': (45, 47, -64, -62),
    'Quebec': (45, 52, -79, -57),
    'Saskatchewan': (49, 60, -110, -101)
}

# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制省份边界
for province, bounds in province_boundaries.items():
    x = [bounds[2], bounds[3], bounds[3], bounds[2], bounds[2]]
    y = [bounds[0], bounds[0], bounds[1], bounds[1], bounds[0]]
    z = [0, 0, 0, 0, 0]
    ax.plot(x, y, z, color='black')

# 标记经济活动
for province, activity in economic_activity.items():
    for sector, value in activity.items():
        color = (np.random.rand(), np.random.rand(), np.random.rand())  # 随机颜色
        bounds = province_boundaries[province]
        x = np.random.uniform(bounds[2], bounds[3], size=100)
        y = np.random.uniform(bounds[0], bounds[1], size=100)
        z = np.ones_like(x) * value * 10  # 根据经济活动指数设置高度
        ax.scatter(x, y, z, color=color, alpha=0.5)

# 设置图形属性
ax.set_xlim(-140, -50)
ax.set_ylim(40, 80)
ax.set_zlim(0, 10)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Economic Activity')

# 显示图形
plt.title('Economic Activity in Canada')
plt.show()

