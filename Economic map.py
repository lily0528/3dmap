import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Load data
population_data = pd.DataFrame({
    'Province': ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Nova Scotia',
                 'Newfoundland and Labrador', 'Prince Edward Island', 'New Brunswick', 'Yukon',
                 'Northwest Territories'],
    'Population': [14734014, 8589494, 5147712, 4413146, 1379263, 1178681, 979351,
                   520998, 156947, 781315, 41078, 45061],
    'Latitude': [51.2538, 52.9399, 53.7267, 53.9333, 49.8951, 52.9399, 44.6819866,
                 53.1355, 46.5107, 46.5653, 64.2823, 64.8255],
    'Longitude': [-85.3232, -73.5491, -127.6476, -116.5765, -97.1384, -106.4509, -63.744311,
                  -57.6604, -63.4168, -66.4619, -135.0, -124.8457]
})

economic_data = pd.DataFrame({
    "Province": ["Ontario", "Quebec", "Alberta", "British Columbia", "Manitoba", "Saskatchewan", "Nova Scotia", "New Brunswick", "Newfoundland and Labrador", "Prince Edward Island"],
    "2020": [854.3, 429.5, 318.5, 291.6, 78.9, 79.3, 45.9, 35.4, 31.0, 6.8],
    "2021": [882.0, 447.8, 330.4, 305.1, 81.7, 82.1, 47.5, 36.6, 32.0, 7.0],
    "2022": [909.6, 466.0, 342.3, 318.6, 84.5, 84.8, 49.1, 37.8, 33.0, 7.2],
    "2023": [927.4, 474.2, 355.0, 327.1, 86.3, 86.3, 50.0, 38.5, 33.5, 7.5]
})

economic_data = pd.melt(economic_data, id_vars=["Province"], var_name="Year", value_name="GDP")
economic_data["Year"] = economic_data["Year"].astype(int)

# Function to create the main population density map
def create_population_density_map():
    fig = go.Figure(data=[go.Scattergeo(
        lon=population_data['Longitude'],
        lat=population_data['Latitude'],
        text=population_data['Province'],
        mode='markers',
        marker=dict(
            size=population_data['Population'] / 1000000,  # Scale down for better visualization
            color='purple',
            opacity=0.6
        )
    )])

    fig.update_layout(
        title='Population Density Map of Canada',
        geo_scope='north america'
    )
    return fig

# Function to create 3D economic data plots
def create_3d_economic_plot(province):
    province_data = economic_data[economic_data['Province'] == province]
    fig = go.Figure(data=[go.Scatter3d(
        x=province_data['Year'],
        y=['GDP'] * len(province_data),
        z=province_data['GDP'],
        mode='lines+markers',
        marker=dict(size=5, color='purple'),
        line=dict(color='purple')
    )])
    fig.update_layout(
        title=f'Economic Data for {province}',
        scene=dict(
            zaxis_title='GDP',
            xaxis_title='Year',
            yaxis_title='Metric'
        )
    )
    return fig

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='map', figure=create_population_density_map()),
    html.Div(id='province-data'),
    html.Button('Compare', id='compare-button', n_clicks=0),
    dcc.Graph(id='comparison-chart')
])

# Callback to update economic data based on clicked province
@app.callback(
    Output('province-data', 'children'),
    Input('map', 'clickData')
)
def display_province_data(clickData):
    if clickData is None:
        return 'Click on a province to see its economic data.'
    province = clickData['points'][0]['text']
    fig = create_3d_economic_plot(province)
    return dcc.Graph(figure=fig)

# Callback to show comparison chart
@app.callback(
    Output('comparison-chart', 'figure'),
    Input('compare-button', 'n_clicks')
)
def compare_gdp(n_clicks):
    if n_clicks == 0:
        return go.Figure()
    fig = go.Figure()
    for province in economic_data['Province'].unique():
        province_data = economic_data[(economic_data['Province'] == province)]
        fig.add_trace(go.Scatter(
            x=province_data['Year'],
            y=province_data['GDP'],
            fill='tozeroy',
            name=province
        ))
    fig.update_layout(title='GDP Comparison across Provinces')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
