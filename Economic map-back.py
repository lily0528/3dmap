import geopandas as gpd
import plotly.graph_objs as go
import pandas as pd

# 创建数据
data = {
    "Geography": [
        "Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia", "New Brunswick",
        "Quebec", "Ontario", "Manitoba", "Saskatchewan", "Alberta", "British Columbia",
        "Yukon", "Northwest Territories", "Nunavut", "Canada"
    ],
    "2019": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    "2020": [95.3, 97.1, 95.5, 96.4, 95.2, 95.4, 95.9, 95.8, 92.2, 96.9, 101.8, 91.3, 102.1, 95.1],
    "2023": [92.5, 110.8, 105.7, 104.3, 104.5, 105.6, 101.9, 102.5, 103.1, 109.5, 118.6, 97.8, 115.6, 105.4]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为CSV文件
df.to_csv('canada_gdp_by_province.csv', index=False)