import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px

# Sample data for demonstration purposes
provinces = ["British Columbia", "Alberta", "Saskatchewan", "Manitoba", "Ontario", "Quebec",
             "Newfoundland and Labrador", "New Brunswick", "Nova Scotia", "Prince Edward Island"]

# GDP data for each province over the years
years = np.linspace(2005, 2022, 18).astype(int)
data = {
    "British Columbia": [631.35, 754.62, 721.12, 498.42, 741.41, 116.37, 196.99, 83.92, 294.00, 341.51, 253.51, 671.55, 317.56, 260.70, 457.02, 155.69, 651.65, 105.91],
    "Alberta": [580.14, 596.76, 628.45, 105.53, 318.85, 136.90, 697.33, 517.47, 298.17, 97.67, 283.24, 293.89, 597.20, 528.17, 715.41, 404.16, 139.70, 584.93],
    "Saskatchewan": [655.58, 722.07, 288.50, 132.54, 220.95, 370.33, 663.51, 695.55, 55.21, 433.06, 363.06, 216.58, 139.90, 303.21, 757.18, 292.40, 439.09, 577.26],
    "Manitoba": [370.66, 69.06, 130.92, 73.57, 527.31, 285.77, 431.43, 730.67, 236.97, 357.79, 616.66, 221.60, 107.73, 267.31, 170.92, 747.27, 656.09, 525.05],
    "Ontario": [166.99, 93.56, 699.63, 500.84, 581.05, 65.44, 777.43, 674.33, 209.25, 186.37, 187.55, 278.18, 443.57, 373.96, 268.42, 508.89, 154.62, 269.11],
    "Quebec": [494.31, 84.84, 505.66, 177.89, 98.79, 761.66, 774.22, 656.30, 278.46, 123.25, 563.17, 380.11, 141.53, 421.38, 75.79, 731.99, 244.08, 546.89],
    "Newfoundland and Labrador": [231.39, 119.83, 722.91, 725.31, 524.83, 304.27, 311.91, 594.47, 722.83, 715.31, 634.91, 531.52, 113.10, 171.22, 723.92, 504.82, 56.90, 126.10],
    "New Brunswick": [290.59, 189.89, 80.58, 493.17, 558.17, 62.44, 434.07, 219.87, 533.88, 180.77, 568.20, 340.05, 752.55, 153.14, 305.80, 135.11, 743.52, 708.00],
    "Nova Scotia": [275.66, 263.63, 77.67, 507.17, 427.01, 88.61, 258.98, 731.20, 229.67, 158.67, 417.09, 789.24, 231.54, 554.10, 621.21, 228.23, 596.16, 325.84],
    "Prince Edward Island": [538.97, 218.20, 584.13, 227.94, 294.05, 609.87, 537.22, 686.92, 543.21, 476.23, 120.26, 325.79, 248.90, 232.99, 779.76, 344.82, 719.03, 523.35]
}

# Introductions for each province
introductions = {
    "British Columbia": "British Columbia is Canada's westernmost province, known for its natural beauty.",
    "Alberta": "The Athabasca Oil Sands are in Alberta, but the processed bitumen and other petroleum products are often shipped to export markets via ports like the Port of Vancouver in British Columbia. As Canada's largest port, the Port of Vancouver is a gateway for Canadian exports, including oil and gas products. The port's location on the Pacific coast makes it good at handling shipments to lots of different international markets, which shows how Canada's resources and global trade networks are connected.",
    "Saskatchewan": "Saskatchewan is known for its vast prairies and agriculture.",
    "Manitoba": "Manitoba is home to diverse cultures and beautiful landscapes.",
    "Ontario": "Toronto's growth as Canada's financial and cultural hub attracts immigrants and internal migrants, leading to significant population increases and urban sprawl. This rapid growth causes problems like crowded public transit and high housing prices. To help, the city is building new transit lines like the Eglinton Crosstown LRT and creating more affordable housing. Toronto is also working to protect the environment with initiatives like the Green Roof Bylaw and the TransformTO climate action plan.",
    "Quebec": "Quebec is known for its French heritage and vibrant culture.",
    "Newfoundland and Labrador": "Newfoundland and Labrador is known for its rugged coastline and maritime history.",
    "New Brunswick": "New Brunswick features beautiful rivers and forests.",
    "Nova Scotia": "Nova Scotia is famous for its coastal beauty and seafood.",
    "Prince Edward Island": "Prince Edward Island practises sustainability by investing in wind energy, which reduces the use of fossil fuels and promotes clean energy. This helps the local economy by creating jobs and attracting eco-friendly consumers. It also helps the environment by cutting down on pollution and conserving resources. Socially, it ensures everyone has access to clean energy and makes the community feel responsible for protecting the environment."

}

# Create a mock population density map data
pop_density = {
    'province': provinces,
    'lat': [53.7267, 53.9333, 52.9399, 49.8951, 51.2538, 52.9399, 53.1355, 46.5653, 44.6820, 46.5107],
    'lon': [-127.6476, -116.5765, -106.4509, -97.1384, -85.3232, -73.5491, -57.6604, -66.4619, -63.7443, -63.2008],
    'population_density': [5.4, 6.4, 1.8, 2.3, 14.1, 6.0, 1.4, 10.5, 17.4, 24.7]  # Mock data
}

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Population Density Map - CANADA", style={'textAlign': 'center', 'fontFamily': 'Times New Roman', 'fontSize': '36px', 'color': '#333'}),
    dcc.Graph(id='pop-density-map', config={'displayModeBar': False}, style={'height': '90vh'}),
    html.Div(id='province-data', style={'display': 'none'}),
    html.Button('Compare', id='compare-button', n_clicks=0, style={'marginTop': '10px', 'fontFamily': 'Times New Roman', 'fontSize': '18px'}),
    dcc.Graph(id='comparison-chart', style={'display': 'none', 'marginTop': '10px'})
], style={'padding': '20px', 'height': '100vh', 'display': 'flex', 'flexDirection': 'column', 'backgroundColor': '#f9f9f9'})


@app.callback(
    Output('pop-density-map', 'figure'),
    [Input('pop-density-map', 'clickData')]
)
def update_map(click_data):
    df = pd.DataFrame(pop_density)
    fig = px.scatter_geo(df, lat='lat', lon='lon', text='province',
                         size='population_density', size_max=30,
                         hover_name='province', template='plotly_white',
                         title='Population Density Map - CANADA')

    fig.update_geos(
        projection_type="natural earth",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Black",
        lataxis_range=[41, 83], lonaxis_range=[-141, -52],  # Focus on Canada
        showland=True, landcolor="white",
        showocean=True, oceancolor="lightblue",
        showrivers=True, rivercolor="blue",
        showlakes=True, lakecolor="lightblue"
    )

    fig.update_layout(
        title_x=0.5,  # Center the title
        clickmode='event+select',
        margin={'l': 0, 'r': 0, 't': 50, 'b': 0},  # Fullscreen map
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)')  # Transparent background
    )

    fig.update_traces(marker=dict(color='rgba(153, 0, 153, 0.6)', line=dict(width=0)))

    if click_data:
        province = click_data['points'][0]['text']
        fig.update_traces(marker=dict(color='rgba(153, 0, 153, 0.6)'), selector=dict(mode='markers+text'))
        fig.add_trace(go.Scattergeo(
            lat=[df[df['province'] == province]['lat'].values[0]],
            lon=[df[df['province'] == province]['lon'].values[0]],
            text=[province],
            marker=dict(size=15, color='rgba(255, 0, 0, 0.8)', symbol='star'),
            hoverinfo='text'
        ))

    return fig


@app.callback(
    Output('province-data', 'style'),
    Output('province-data', 'children'),
    [Input('pop-density-map', 'clickData')]
)
def display_province_data(click_data):
    if click_data:
        province = click_data['points'][0]['text']
        intro_text = introductions.get(province, "")
        year_data = data[province]
        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            z=year_data, x=years, y=[province] * len(years),
            mode='lines+markers',
            line=dict(color='blue'),
            marker=dict(size=4)
        ))

        fig.update_layout(
            title=f'Economic Data for {province}',
            scene=dict(
                xaxis_title='Year',
                yaxis_title='Province',
                zaxis_title='GDP'
            ),
            autosize=False,
            width=1000,
            height=800,
            margin=dict(l=65, r=50, b=65, t=90)
        )

        return {'display': 'block'}, [
            html.H2(f'Economic Data for {province}', style={'fontFamily': 'Times New Roman'}),
            dcc.Graph(figure=fig),
            html.H4('Introduction', style={'fontFamily': 'Times New Roman'}),
            html.P(intro_text, style={'fontFamily': 'Times New Roman'})
        ]
    return {'display': 'none'}, ''


@app.callback(
    Output('comparison-chart', 'style'),
    Output('comparison-chart', 'figure'),
    [Input('compare-button', 'n_clicks')]
)
def show_comparison_chart(n_clicks):
    if n_clicks > 0:
        df = pd.DataFrame(data, index=years)
        fig = px.line(df, labels={"value": "GDP", "variable": "Province"})
        fig.update_layout(title='GDP Comparison Across Provinces', title_x=0.5)
        return {'display': 'block'}, fig
    return {'display': 'none'}, {}


if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.0.146', port=8050)
