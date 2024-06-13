import geopandas as gpd
import plotly.graph_objs as go
import pandas as pd
import requests

# URL
url = 'https://canada_gdp_by_province.csv'  # 例CSV文件URL

try:
    # 从URL获取数据并保存到CSV文件
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功

    with open('canada_gdp_by_province.csv', 'wb') as file:
        file.write(response.content)

    print("CSV file successfully download and saved")

except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

# 取地理数据
canada_geo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
canada_geo = canada_geo[canada_geo.name == "Canada"]

# 取GDP数据
gdp_data = pd.read_csv('canada_gdp_by_province.csv')

# 加经纬度数据
coordinates = {
    'Newfoundland and Labrador': (53.1355, -57.6604),
    'Prince Edward Island': (46.5107, -63.4168),
    'Nova Scotia': (44.6820, -63.7443),
    'New Brunswick': (46.5653, -66.4619),
    'Quebec': (52.9399, -73.5491),
    'Ontario': (51.2538, -85.3232),
    'Manitoba': (49.8951, -97.1384),
    'Saskatchewan': (52.9399, -106.4509),
    'Alberta': (53.9333, -116.5765),
    'British Columbia': (53.7267, -127.6476),
    'Yukon': (64.2823, -135.0000),
    'Northwest Territories': (64.8255, -124.8457),
    'Nunavut': (70.2998, -83.1076)
}

gdp_data['Latitude'] = gdp_data['Geography'].map(lambda x: coordinates[x][0] if x in coordinates else None)
gdp_data['Longitude'] = gdp_data['Geography'].map(lambda x: coordinates[x][1] if x in coordinates else None)

# 3D地图模型
fig = go.Figure()

# 地理边界
for feature in canada_geo.geometry:
    if feature.geom_type == 'Polygon':
        lon, lat = feature.exterior.xy
        fig.add_trace(go.Scatter3d(x=list(lon), y=list(lat), z=[0] * len(lon),
                                   mode='lines', line=dict(color='blue', width=2)))
    elif feature.geom_type == 'MultiPolygon':
        for poly in feature.geoms:
            lon, lat = poly.exterior.xy
            fig.add_trace(go.Scatter3d(x=list(lon), y=list(lat), z=[0] * len(lon),
                                       mode='lines', line=dict(color='blue', width=2)))

# 经济数据（2023年的GDP数据）
for i, row in gdp_data.iterrows():
    province = row['Geography']
    gdp_2023 = row['2023']
    lon = row['Longitude']
    lat = row['Latitude']

    fig.add_trace(go.Scatter3d(x=[lon], y=[lat], z=[gdp_2023],
                               mode='markers+text',
                               marker=dict(size=3, color=gdp_2023, colorscale='Viridis', showscale=True),
                               text=province, textposition='top center'))

# 布局
fig.update_layout(scene=dict(
    xaxis=dict(title='Longitude'),
    yaxis=dict(title='Latitude'),
    zaxis=dict(title='GDP (Index 2019=100)'),
), title='3D Canada Map with GDP Data by Province')

# 显示
fig.show()
