import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load SpaceX data
spacex_df = pd.read_csv('spacex_launch_geo.csv')  # Replace with your dataset
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    
    # TASK 1: Add a Launch Site Dropdown Input Component
    html.Div([
        html.Label('Launch Site:'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
            ],
            value='ALL',
            placeholder='Select a Launch Site',
            searchable=True
        )
    ]),
    
    # TASK 2: Add a Pie Chart for Success Rates
    html.Div(dcc.Graph(id='success-pie-chart')),

    # TASK 3: Add a Range Slider for Payload Mass
    html.Div([
        html.Label('Payload Range (kg):'),
        dcc.RangeSlider(
            id='payload-slider',
            min=min_payload,
            max=max_payload,
            step=1000,
            marks={i: f'{i} kg' for i in range(int(min_payload), int(max_payload) + 1, 1000)},
            value=[min_payload, max_payload]
        )
    ]),
    
    # TASK 4: Add a Scatter Plot for Success Rates vs Payload
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback for the success-pie-chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success Launches for site {selected_site}')
    return fig

# TASK 4: Add a callback for the success-payload-scatter-chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Correlation Between Payload and Success')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
