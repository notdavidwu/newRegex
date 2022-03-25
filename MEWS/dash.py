# 計時


# 陣列
import pandas as pd
import numpy as np

# 格式轉換
import decimal

# 視覺化
import matplotlib.pyplot as plt
import plotly.express as px
import dash_daq as daq
import plotly.figure_factory as ff
import dash
from dash.dependencies import Input
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from .views import connect

# 開始連結SQL
chdf ,mews = connect()
app = DjangoDash('MEWS')
app.layout = html.Div([
    # 標題
    html.H1('MEWS介面'),
    html.Br(),
    html.Hr(),
    
    # 月歷
    html.H3('查詢日期:'),
    dcc.DatePickerRange(
        min_date_allowed=chdf.index.min(),
        max_date_allowed=chdf.index.max(),
        initial_visible_month=chdf.index[0],
        calendar_orientation='vertical',
        id='date-picker'
    ),
    html.Br(),
    
    # 護理站選單
    html.H3('護理站:'),
    dcc.Dropdown(id='ward-dropdown'),
    html.Br(),
    
    # 科別選單
    html.H3('科別:'),
    dcc.Dropdown(id='div-dropdown'),
    html.Br(),

    # 病歷號選單
    html.H3('病歷號:'),
    dcc.Dropdown(id='chartno-dropdown'),
    html.Br(),
    
    html.Hr(),
    html.Br(),
    
    # LED: 病歷號
    daq.LEDDisplay(
        label='ChartNo',
        labelPosition='bottom',
        backgroundColor='#2b2b2b',
        size=24,
        color='#fec036',
        id='chartno-led'
    ),
    html.Br(),
    
    # 折線圖
    dcc.Graph(id='mews-graph'),
    html.Br(),
    
    # Table
    dcc.Graph(id='mews-table')
])
@app.callback(
    dash.dependencies.Output('ward-dropdown', 'options'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('div-dropdown', 'value')
)
def update_ward(start_date, end_date, div):
    if (start_date is None) and (end_date is None):
        start_date = str(chdf.index.min())
        end_date = str(chdf.index.max())
    elif start_date is None:
        start_date = str(chdf.index.min())
        end_date = str(end_date)
    elif end_date is None:
        start_date = str(start_date)
        end_date = str(chdf.index.max())
    else:
        pass

    if div is None:
        df = chdf[(start_date <= chdf.index) & (chdf.index <= end_date)]
        return [{'label': i, 'value': i} for i in np.sort(df['Ward'].unique(), axis=-1)]
    else:
        df = chdf[(start_date <= chdf.index) & (chdf.index <= end_date) & (chdf['DivName'] == div)]
        return [{'label': i, 'value': i} for i in np.sort(df['Ward'].unique(), axis=-1)]

##############################################################################################

# 篩選器: 科別選單
@app.callback(
    dash.dependencies.Output('div-dropdown', 'options'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('ward-dropdown', 'value')
)
def update_div(start_date, end_date, ward):
    if (start_date is None) and (end_date is None):
        start_date = str(chdf.index.min())
        end_date = str(chdf.index.max())
    elif start_date is None:
        start_date = str(chdf.index.min())
        end_date = str(end_date)
    elif end_date is None:
        start_date = str(start_date)
        end_date = str(chdf.index.max())
    else:
        pass

    if ward is None:
        df = chdf[(start_date <= chdf.index) & (chdf.index <= end_date)]
        return [{'label': i, 'value': i} for i in np.sort(df['DivName'].unique(), axis=-1)]
    else:
        df = chdf[(start_date <= chdf.index) & (chdf.index <= end_date) & (chdf['Ward'] == ward)]
        return [{'label': i, 'value': i} for i in np.sort(df['DivName'].unique(), axis=-1)]

##############################################################################################

# 篩選器: 病歷號選單
@app.callback(
    dash.dependencies.Output('chartno-dropdown', 'options'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_chartno(start_date, end_date):
    if (start_date is None) and (end_date is None):
        start_date = str(chdf.index.min())
        end_date = str(chdf.index.max())
    elif start_date is None:
        start_date = str(chdf.index.min())
        end_date = str(end_date)
    elif end_date is None:
        start_date = str(start_date)
        end_date = str(chdf.index.max())
    else:
        pass
    df = chdf[(start_date <= chdf.index) & (chdf.index <= end_date)]
    return [{'label': i, 'value': i} for i in df['ChartNo'].unique()]

##############################################################################################

# 篩選器: LED
@app.callback(
    dash.dependencies.Output('chartno-led', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_chartno(chartno):
    if chartno is None:
        chartno=chartno=chdf['ChartNo'][0]
    else:
        pass
    return chartno

##############################################################################################

# 篩選器: 圖表
@app.callback(
    dash.dependencies.Output('mews-graph', 'figure'),
    Input('chartno-dropdown', 'value')
)
def update_graph(chartno):
    if chartno is None:
        chartno=chdf['ChartNo'][0]
    else:
        pass
    df = mews[chartno == mews['ChartNo']]
    fig = px.line()
    df1 = df[df['BP_V1'] > 0]
    fig.add_scatter(x=df1.index, y=df1['BP_V1'], name='BP', mode='lines+markers')
    df2 = df[df['PULSE_V1'] > 0]
    fig.add_scatter(x=df2.index, y=df2['PULSE_V1'], name='PULSE', mode='lines+markers')
    df3 = df[df['RESPIRATORY_V1'] > 0]
    fig.add_scatter(x=df3.index, y=df3['RESPIRATORY_V1'], name= 'RESPIRATORY', mode='lines+markers')
    df4 = df[df['BT_V1'] > 0]
    fig.add_scatter(x=df4.index, y=df4['BT_V1'], name='BT', mode='lines+markers')
    df5 = df[df['SPO2_V1'] > 0]
    fig.add_scatter(x=df5.index, y=df5['SPO2_V1'], name='SPO2', mode='lines+markers')
    fig.update_layout(
        updatemenus=[
            dict(
                direction='right',
                active=0,
                x=0.08,
                y=1.2,
                buttons=list([
                    dict(label='All',
                         method='update',
                         args=[ {'visible': [True, True, True, True, True]},
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='BP', 
                         method='update', 
                         args=[ {'visible': [True, False, False, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='PULSE', 
                         method='update', 
                         args=[ {'visible': [False, True, False, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='RESPIRATORY', 
                         method='update', 
                         args=[ {'visible': [False, False, True, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='BT', 
                         method='update', 
                         args=[ {'visible': [False, False, False, True, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='SPO2', 
                         method='update', 
                         args=[ {'visible': [False, False, False, False, True]}, 
                                {'showlegend' : True}
                              ]
                        ),
                ]), 
            ) 
        ]
    )
    fig.update_xaxes(rangeslider_visible=True)
    return fig

##############################################################################################

# 篩選器: 表單
@app.callback(
    dash.dependencies.Output('mews-table', 'figure'),
    Input('chartno-dropdown', 'value')
)
def update_table(chartno):
    if chartno is None:
        chartno=chdf['ChartNo'][0]
    else:
        pass
    df = mews[chartno == mews['ChartNo']]
    fig = ff.create_table(df)
    return fig
