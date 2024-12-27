#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1(
    "Automobile Sales Statistics Dashboard", 
    style={
        'textAlign': 'center',  # Center align the title
        'color': '#503D36',     # Set the color to #503D36
        'font-size': '24px'     # Set the font size to 24px
    }
    ),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:", style={'font-size': '18px'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value=None,  # Default value is None
            style={
                'width': '80%',
                'margin': 'auto',  # Center the dropdown
                'padding': '5px',
                'font-size': '16px',
                'text-align-last': 'center'
            }
        )
    ], style={'margin-bottom': '20px'}),  # Add spacing below the dropdown

    html.Div([
        html.Label("Select Year:", style={'font-size': '18px'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],  # Convert years to string for labels
            placeholder='Select a year',
            disabled=True,  # Initially disabled
            style={
                'width': '80%',
                'margin': 'auto',  # Center the dropdown
                'padding': '5px',
                'font-size': '16px',
                'text-align-last': 'center'
            }
        )
    ], style={'margin-bottom': '20px'}),  # Add spacing below the dropdown

#TASK 2.3: Add a division for output display
    html.Div(
        id='output-container', 
        className='chart-grid', 
        style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px'}
    )
])

#TASK 2.4: Creating Callbacks
# Callback to enable or disable the year selection dropdown
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    """
    Enables the 'Year' dropdown only when 'Yearly Statistics' is selected.
    """
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable the dropdown
    else:
        return True  # Disable the dropdown

# Callback to update the output container based on selected statistics and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    """
    Updates the output-container with relevant charts based on the selected statistics.
    """
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average automobile sales fluctuation over recession period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation Over Recession Period")
        )

        # Plot 2: Average number of vehicles sold by vehicle type during recession
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Number of Vehicles Sold by Vehicle Type During Recession")
        )

        
        
        # Return the charts for the Recession Period Statistics
        
        return [
            html.Div(children=[R_chart1, R_chart2], style={'display': 'flex', 'flex-wrap': 'wrap'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales',
                           title="Yearly Automobile Sales")
        )

        # Plot 2: Total monthly automobile sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales',
                           title="Total Monthly Automobile Sales")
        )

        # Return the charts for the Yearly Statistics
        return [
            html.Div(children=[Y_chart1, Y_chart2], style={'display': 'flex', 'flex-wrap': 'wrap'})
        ]

    # Default return (in case no selection is made)
    return html.Div("Please select a report type and year (if applicable).")


#TASK 2.5: Create and display graphs for Recession Report Statistics
    # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using line chart
    yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

    # Plotting the line graph
    R_chart1 = dcc.Graph(
        figure=px.line(yearly_rec,
                    x='Year', 
                    y='Automobile_Sales', 
                    title="Average Automobile Sales Fluctuation Over Recession Period")
    )

    # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
    average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

    R_chart2 = dcc.Graph(
        figure=px.bar(average_sales,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    title="Average Number of Vehicles Sold by Vehicle Type During Recession")
    )

    # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
    exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

    R_chart3 = dcc.Graph(
        figure=px.pie(exp_rec,
                    values='Advertising_Expenditure',
                    names='Vehicle_Type',
                    title="Total Expenditure Share by Vehicle Type During Recession")
    )

    # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
    unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()

    R_chart4 = dcc.Graph(
        figure=px.bar(unemp_data,
                    x='unemployment_rate',
                    y='Automobile_Sales',
                    color='Vehicle_Type',
                    labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                    title="Effect of Unemployment Rate on Vehicle Type and Sales")
    )

    # Returning the graphs
    return [
        html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
    ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics                                                        
# Yearly Statistic Report Plots
    if (input_year and selected_statistics == 'Yearly Statistics'):
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        # Grouping data for plotting
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                        x='Year',
                        y='Automobile_Sales',
                        title="Yearly Automobile Sales")
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        # Grouping data for plotting
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                        x='Month',
                        y='Automobile_Sales',
                        title='Total Monthly Automobile Sales')
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        # Grouping data for plotting
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                        x='Vehicle_Type',
                        y='Automobile_Sales',
                        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year))
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        # Grouping data for plotting
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                        values='Advertising_Expenditure',
                        names='Vehicle_Type',
                        title='Total Advertisement Expenditure for Each Vehicle')
        )
        
        # Returning the charts
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]
    
    # Default return (in case no selection is made)
    return html.Div("Please select a report type and year (if applicable).")

# Run the Dash app

if __name__ == '__main__':
    app.run_server(debug=True)
