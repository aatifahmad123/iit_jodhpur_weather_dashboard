import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

file_path = "Weather_Data_IIT_Jodhpur.csv"
df = pd.read_csv(file_path)

df['time'] = pd.to_datetime(df['time'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Weather Dashboard - IIT Jodhpur"

app.layout = dbc.Container([
    html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px'}, children=[
        html.H1("IIT Jodhpur Weather Dashboard", className='text-center mb-2', style={'font-family': 'Arial, sans-serif'}),
        html.H5("Created by Aatif Ahmad", className='text-center text-secondary mb-2', style={'font-family': 'Arial, sans-serif'}),
        html.P("Latitude: 26.4710° N, Longitude: 73.1134° E", className='text-center fw-bold'),
        html.P(["Data Source: ", html.A("Open-Meteo", href="https://open-meteo.com/", target="_blank", className='text-primary')], className='text-center text-muted'),
        html.P("Note: We are using data only from 1st March 2024 to 1st March 2025.", className='text-center text-primary fw-bold'),
        
        html.Div([
            html.Label("Select Date Range:", className='fw-bold'),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df['time'].min(),
                end_date=df['time'].max(),
                min_date_allowed=df['time'].min(),
                max_date_allowed=df['time'].max(),
                display_format='YYYY-MM-DD',
                className='mb-3 d-block'
            ),
        ], className='mb-4 text-center'),
        
        html.Div([html.H4("Temperature Trends", className='text-center'), dcc.Graph(id='temp-trends')], className='mb-4 p-3 border rounded shadow-sm bg-white'),
        html.Div([html.H4("Daily Rainfall", className='text-center'), dcc.Graph(id='rainfall-trends')], className='mb-4 p-3 border rounded shadow-sm bg-white'),
        html.Div([html.H4("Wind Speed Trends", className='text-center'), dcc.Graph(id='wind-trends')], className='mb-4 p-3 border rounded shadow-sm bg-white'),
    ])
])

@app.callback(
    [dash.dependencies.Output('temp-trends', 'figure'),
     dash.dependencies.Output('rainfall-trends', 'figure'),
     dash.dependencies.Output('wind-trends', 'figure')],
    [dash.dependencies.Input('date-picker', 'start_date'),
     dash.dependencies.Input('date-picker', 'end_date')]
)
def update_graphs(start_date, end_date):
    filtered_df = df[(df['time'] >= start_date) & (df['time'] <= end_date)]
    
    temp_fig = px.line(filtered_df, x='time', y=['temperature_2m_mean (°C)', 'temperature_2m_max (°C)', 'temperature_2m_min (°C)'],
                        labels={'value': 'Temperature (°C)', 'time': 'Date'},
                        title='Temperature Trends')
    
    rain_fig = px.bar(filtered_df, x='time', y='rain_sum (mm)',
                       labels={'rain_sum (mm)': 'Rainfall (mm)', 'time': 'Date'},
                       title='Daily Rainfall',
                       barmode='group')
    
    wind_fig = px.line(filtered_df, x='time', y=['wind_speed_10m_max (km/h)', 'wind_gusts_10m_max (km/h)'],
                        labels={'value': 'Wind Speed (km/h)', 'time': 'Date'},
                        title='Wind Speed Trends')
    
    return temp_fig, rain_fig, wind_fig

if __name__ == '__main__':
    app.run(debug=False)
