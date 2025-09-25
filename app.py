import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import os

file_path = os.path.join(os.path.dirname(__file__), "Weather_Data_IIT_Jodhpur.csv")
df = pd.read_csv(file_path)

df['time'] = pd.to_datetime(df['time'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Weather Dashboard - IIT Jodhpur"

app.layout = html.Div([
    # Fixed header section
    html.Div([
        dbc.Container([
            html.Div(style={
                'backgroundColor': '#f8f9fa',
                'padding': '8px',
                'padding-bottom': '0px',
                'borderRadius': '10px',
                'position': 'relative',
                'zIndex': 1000   # ensures date picker calendar is on top
            }, children=[
                html.H2("IIT Jodhpur Weather Dashboard | Created by Aatif Ahmad",
                        className='text-center mb-1',
                        style={'font-family': 'Arial, sans-serif', 'fontSize': '1.3rem'}),
                
                html.P([
                    "26.4710° N, 73.1134° E | Data: ",
                    html.A("Open-Meteo", href="https://open-meteo.com/", target="_blank", className='text-primary'),
                    " | March 2024 - March 2025"
                ], className='text-center text-muted mb-2',
                   style={'fontSize': '0.75rem', 'margin': '0'}),
                
                html.Div([
                    html.Label("Select Date Range:", className='fw-bold',
                               style={'fontSize': '0.85rem', 'marginRight': '10px'}),
                    dcc.DatePickerRange(
                        id='date-picker',
                        start_date=df['time'].min(),
                        end_date=df['time'].max(),
                        min_date_allowed=df['time'].min(),
                        max_date_allowed=df['time'].max(),
                        display_format='YYYY-MM-DD',
                        style={'display': 'inline-block', 'fontSize': '0.85rem'},
                    ),
                ], className='text-center mb-1'),
            ]),
        ], fluid=True, style={'padding': '10px', 'padding-bottom': '0px'})
    ], style={'height': '120px', 'overflow': 'visible'}), 
    
    # Dynamic graphs section - takes remaining height
    html.Div([
        dbc.Container([
            html.Div([
                html.H6("Temperature Trends", className='text-center mb-1'), 
                dcc.Graph(id='temp-trends', style={'height': 'calc((100vh - 120px) / 3 - 60px)'})
            ], className='mb-1 p-2 border rounded shadow-sm bg-white',
               style={'height': 'calc((100vh - 120px) / 3)'}),
            
            html.Div([
                html.H6("Daily Rainfall", className='text-center mb-1'), 
                dcc.Graph(id='rainfall-trends', style={'height': 'calc((100vh - 120px) / 3 - 60px)'})
            ], className='mb-1 p-2 border rounded shadow-sm bg-white',
               style={'height': 'calc((100vh - 120px) / 3)'}),
            
            html.Div([
                html.H6("Wind Speed Trends", className='text-center mb-1'), 
                dcc.Graph(id='wind-trends', style={'height': 'calc((100vh - 120px) / 3 - 60px)'})
            ], className='p-2 border rounded shadow-sm bg-white',
               style={'height': 'calc((100vh - 120px) / 3)'}),
        ], fluid=True, style={'padding': '0 10px 10px 10px'})
    ], style={'height': 'calc(100vh - 120px)', 'overflow': 'hidden'})
], style={'height': '100vh', 'overflow': 'hidden'})

@app.callback(
    [dash.dependencies.Output('temp-trends', 'figure'),
     dash.dependencies.Output('rainfall-trends', 'figure'),
     dash.dependencies.Output('wind-trends', 'figure')],
    [dash.dependencies.Input('date-picker', 'start_date'),
     dash.dependencies.Input('date-picker', 'end_date')]
)
def update_graphs(start_date, end_date):
    filtered_df = df[(df['time'] >= start_date) & (df['time'] <= end_date)]
    
    # Common legend configuration for all graphs
    legend_config = dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.8)"
    )
    
    temp_fig = px.line(
        filtered_df, x='time',
        y=['temperature_2m_mean (°C)', 'temperature_2m_max (°C)', 'temperature_2m_min (°C)'],
        labels={'value': 'Temp(°C)', 'time': 'Date'}, title=''
    )
    temp_fig.update_layout(margin=dict(l=40, r=40, t=30, b=30), legend=legend_config)
    
    rain_fig = px.bar(
        filtered_df, x='time', y='rain_sum (mm)',
        labels={'rain_sum (mm)': 'Rainfall(mm)', 'time': 'Date'},
        title='', barmode='group'
    )
    rain_fig.update_traces(name='Daily Rainfall', showlegend=True)
    rain_fig.update_layout(margin=dict(l=40, r=40, t=30, b=30), legend=legend_config)
    
    wind_fig = px.line(
        filtered_df, x='time',
        y=['wind_speed_10m_max (km/h)', 'wind_gusts_10m_max (km/h)'],
        labels={'value': 'Speed(km/h)', 'time': 'Date'}, title=''
    )
    wind_fig.update_layout(margin=dict(l=40, r=40, t=30, b=30), legend=legend_config)
    
    return temp_fig, rain_fig, wind_fig

server = app.server

if __name__ == '__main__':
    app.run(debug=False)
