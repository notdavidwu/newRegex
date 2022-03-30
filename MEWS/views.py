from django.shortcuts import render

def MEWS(request):
    au = request.session.get('au')
    return render(request, 'MEWS/MEWS.html',{'au':au})

##############################################################################################

# django
from django_plotly_dash import DjangoDash
from django.db import connections

# python
import pandas as pd
import numpy as np
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Input, Output

def SQL(sql, colname):
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns = colname)
    return df

def connect():
    sql = '''
            SELECT DISTINCT ChartNo, VisitNo, OccurDate, DivName, Ward, RRTWard
            FROM RRTFinish
            ORDER BY ChartNo, VisitNo, OccurDate
        '''
    colname = ['ChartNo', 'VisitNo', 'OccurDate', 'DivName', 'Ward', 'RRTWard']
    chdf = SQL(sql, colname)
    chdf.set_index('OccurDate', inplace=True)
    return chdf

chdf = connect()

##############################################################################################

app = DjangoDash('MEWS',
                 meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
                 external_stylesheets=[dbc.themes.CYBORG]
                 )

app.title = 'AIC: MEWS'

##############################################################################################

sql = '''
        SELECT DISTINCT ChartNo, VisitNo, OccurDate,
                BP_V1, Score1, PULSE_V1, Score2, RESPIRATORY_V1, Score3,
                BT_V1, Score4, SPO2_V1, Score5,
                GCS_V, Score6, Score, RRT
        FROM RRTFinish
        WHERE ChartNo=%s
        ORDER BY ChartNo, VisitNo, OccurDate
      '''
colname = ['ChartNo', 'VisitNo', 'OccurDate',
           'BP_V1', 'Score1', 'PULSE_V1', 'Score2', 'RESPIRATORY_V1', 'Score3',
           'BT_V1', 'Score4', 'SPO2_V1', 'Score5','GCS_V', 'Score6', 'Score', 'RRT']

def HisData(chartno):
    cursor = connections['MEWS'].cursor()
    ID = [str(chartno)]
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns = colname)
    df.set_index('OccurDate', inplace=True)
    return df

##############################################################################################

def DateRange(df, start_date, end_date):
    if (start_date is None) and (end_date is None):
        start = str(df.index.min())
        end = str(df.index.max())
    elif (start_date is None) and (end_date is not None):
        start = str(df.index.min())
        end = str(end_date)
    elif (start_date is not None) and (end_date is None):
        start = str(start_date)
        end = str(df.index.max())
    elif (start_date is not None) and (end_date is not None):
        start = str(start_date)
        end = str(end_date)
    else:
        pass
    return start, end

##############################################################################################

def img(df):
    fig = px.line()
    df1 = df[df['BP_V1'] > 0]
    fig.add_scatter(x=df1.index.astype(str), y=df1['BP_V1'], name='BP', mode='lines+markers')
    df2 = df[df['PULSE_V1'] > 0]
    fig.add_scatter(x=df2.index.astype(str), y=df2['PULSE_V1'], name='PULSE', mode='lines+markers')
    df3 = df[df['RESPIRATORY_V1'] > 0]
    fig.add_scatter(x=df3.index.astype(str), y=df3['RESPIRATORY_V1'], name= 'RESPIRATORY', mode='lines+markers')
    df4 = df[df['BT_V1'] > 0]
    fig.add_scatter(x=df4.index.astype(str), y=df4['BT_V1'], name='BT', mode='lines+markers')
    df5 = df[df['SPO2_V1'] > 0]
    fig.add_scatter(x=df5.index.astype(str), y=df5['SPO2_V1'], name='SPO2', mode='lines+markers')
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

def Color(RRT, Max):
    color = []
    for i in range(len(Max)):
        if RRT[i]=='BP_V1':
            if 199.5<Max[i]:
                value = {'red':[0, 70.5],
                         '#ff7300':[70.5, 80.5],
                         'yellow':[80.5, 100.5],
                         'green':[100.5, 199.5],
                         '#ff7700':[199.5, Max[i]]
                        }
            elif 100.5<Max[i]<199.5:
                value = {'red':[0, 70.5],
                         '#ff7300':[70.5, 80.5],
                         'yellow':[80.5, 100.5],
                         'green':[100.5, Max[i]]
                        }
            elif 80.5<Max[i]<100.5:
                value = {'red':[0, 70.5],
                         '#ff7300':[70.5, 80.5],
                         'yellow':[80.5, Max[i]]
                        }
            elif 70.5<Max[i]<80.5:
                value = {'red':[0, 70.5],
                         '#ff7300':[70.5, Max[i]]
                        }
            else:
                value = {'red':[0, Max[i]]
                        }
                
        elif RRT[i]=='PULSE_V1':
            if 129.5<Max[i]:
                value = {'#ff7300':[0, 40.5],
                         'yellow':[40.5, 50.5],
                         'green':[50.5, 100.5],
                         'rgb(255, 255, 51)':[100.5, 110.5],
                         '#ff7700':[110.5, 129.5],
                         'red':[129.5, Max[i]]
                        }
            elif 110.5<Max[i]<129.5:
                value = {'#ff7300':[0, 40.5],
                         'yellow':[40.5, 50.5],
                         'green':[50.5, 100.5],
                         'rgb(255, 255, 51)':[100.5, 110.5],
                         '#ff7700':[110.5, Max[i]]
                        }
            elif 100.5<Max[i]<110.5:
                value = {'#ff7300':[0, 40.5],
                         'yellow':[40.5, 50.5],
                         'green':[50.5, 100.5],
                         'rgb(255, 255, 51)':[100.5, Max[i]]
                        }
            elif 50.5<Max[i]<100.5:
                value = {'#ff7300':[0, 40.5],
                         'yellow':[40.5, 50.5],
                         'green':[50.5, Max[i]]
                        }
            elif 40.5<Max[i]<50.5:
                value = {'#ff7300':[0, 40.5],
                         'yellow':[40.5, Max[i]]
                        }
            else:
                value = {'#ff7300':[0, Max[i]]
                        }
                
        elif RRT[i]=='RESPIRATORY_V1':
            if 29.5<Max[i]:
                value = {'#ff7300':[0, 8.5],
                         'green':[8.5, 20.5],
                         '#ff7700':[20.5, 29.5],
                         'red':[29.5, Max[i]]
                        }
            elif 20.5<Max[i]<29.5:
                value = {'#ff7300':[0, 8.5],
                         'green':[8.5, 20.5],
                         '#ff7700':[20.5, Max[i]]
                        }
            elif 8.5<Max[i]<20.5:
                value = {'#ff7300':[0, 8.5],
                         'green':[8.5, Max[i]]
                        }
            else:
                value = {'#ff7300':[0, Max[i]]
                        }
        
        elif RRT[i]=='BT_V1':
            if 38.45<Max[i]:
                value = {'#ff7300':[0, 35.05],
                         'green':[35.05, 38.45],
                         '#ff7700':[38.45, Max[i]]
                        }
            elif 35.05<Max[i]<38.45:
                value = {'#ff7300':[0, 35.05],
                         'green':[35.05, Max[i]]
                        }
            else:
                value = {'#ff7300':[0, Max[i]]
                        }
        
        if RRT[i]=='SPO2_V1':
            if 94.5<Max[i]:
                value = {'red':[0, 84.5],
                         '#ff7300':[84.5, 89.5],
                         'yellow':[89.5, 94.5],
                         'green':[94.5, Max[i]]
                        }
            elif 89.5<Max[i]<94.5:
                value = {'red':[0, 84.5],
                         '#ff7300':[84.5, 89.5],
                         'yellow':[89.5, Max[i]]
                        }
            elif 84.5<Max[i]<89.5:
                value = {'red':[0, 84.5],
                         '#ff7300':[84.5, Max[i]]
                        }
            else:
                value = {'red':[0, Max[i]]
                        }
        cvalue = {'gradient':True, 'ranges': value}
        color.append(cvalue)
    return color

##############################################################################################

# Web: 標題
def logo(app):
    title = html.H5(
        'AIC: Test Web',
        style={'marginTop': 5, 'marginLeft': '10px'},
    )

    info_about_app = html.H6(
        'Modified Early Warning Score(MEWS):'
        'User interface.',
        style={'marginLeft': '10px'},
    )
    
    return dbc.Row([dbc.Col([dbc.Row([title]), dbc.Row([info_about_app])])])

##############################################################################################

# LED: 病歷號
chartno_led = dbc.Card(
    children=[
        dbc.CardHeader(
            'ChartNo',
            style={
                'text-align': 'center',
                'color': 'white',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
        dbc.CardBody(
            [
                daq.LEDDisplay(
                    id='chartno-led',
                    size=24,
                    color='#fec036',
                    style={'color': '#black'},
                    backgroundColor='#2b2b2b'
                )
            ],
            style={
                'text-align': 'center',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
    ]
)

##############################################################################################

# button: date
button_date = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.DatePickerRange(
                            id='date-picker',
                            calendar_orientation='vertical',
                        ),
                    ]
                )
            ],
            style={
                'text-align': 'center',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
                'border-left': '1px solid rgb(216, 216, 216)',
                'border-right': '1px solid rgb(216, 216, 216)',
                'border-bottom': '1px solid rgb(216, 216, 216)',
            },
        )
    ],
)

##############################################################################################

# button: ward
button_ward = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                '護理站:',
                                dcc.Dropdown(
                                    id='ward-dropdown',
                                    multi=False,
                                    searchable=True,
                                    style={'color': '#1a1f61'},
                                ),
                            ],
                            style={'display': 'inline-block',
                                   'width': '160px',
                            }
                        ),
                        html.Div(
                            [
                                'ICU:',
                                daq.BooleanSwitch(id='boolean-switch', on=False),
                            ],
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-around',
                           'align-items': 'center',
                    }
                )
            ],
            style={
                'text-align': 'center',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
                'border-left': '1px solid rgb(216, 216, 216)',
                'border-right': '1px solid rgb(216, 216, 216)',
                'border-bottom': '1px solid rgb(216, 216, 216)',
            },
        )
    ],
)

##############################################################################################

# button: div
button_div = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        '科別:',
                         html.Div(
                            [
                                dcc.Dropdown(
                                    id='div-dropdown',
                                    multi=False,
                                    searchable=True,
                                    style={'color': '#1a1f61'},
                                ),
                            ],
                            style={'display': 'inline-block',
                                   'width': '190px',
                                  }
                         ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-around',
                           'align-items': 'center',
                          }
                )
            ],
            style={
                'text-align': 'center',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
                'border-left': '1px solid rgb(216, 216, 216)',
                'border-right': '1px solid rgb(216, 216, 216)',
                'border-bottom': '1px solid rgb(216, 216, 216)',
            },
        )
    ],
)

##############################################################################################

# button: chartno
button_chartno = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        '病歷號:',
                         html.Div(
                            [
                                dcc.Dropdown(
                                    id='chartno-dropdown',
                                    multi=False,
                                    searchable=True,
                                    style={'color': '#1a1f61'},
                                )
                            ],
                            style={'display': 'inline-block',
                                   'width': '170px',
                                  }
                         )

                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-around',
                           'align-items': 'center'
                          }
                )
            ],
            style={
                'text-align': 'center',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
                'border-left': '1px solid rgb(216, 216, 216)',
                'border-right': '1px solid rgb(216, 216, 216)',
                'border-bottom': '1px solid rgb(216, 216, 216)',
            },
        )
    ],
)

##############################################################################################

# 互動式圖表
graphs = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='mews-graph',
                            figure={
                                'layout': {
                                    'margin': {'t': 30, 'r': 35, 'b': 40, 'l': 50},
                                    'xaxis': {
                                        'dtick': 5,
                                        'gridcolor': '#636363',
                                        'showline': False,
                                    },
                                    'yaxis': {'showgrid': False, 'showline': False},
                                    'plot_bgcolor': 'black',
                                    'paper_bgcolor': 'black',
                                    'font': {'color': 'gray'},
                                },
                            },
                            config={'displayModeBar': False},
                        ),
                        html.Pre(id='update-on-click-data'),
                    ],
                ),
            ],
            style={
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        )
    ]
)

##############################################################################################

# 儀錶板: BP
BP_Gauge = dbc.Card(
    children=[
        dbc.CardHeader(
            'MEWS: BP',
            style={
                'display': 'inline-block',
                'text-align': 'center',
                'color': 'white',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id='BP-gauge',
                        units='mmHg',
                        min=0,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '5%',
                            'marginBottom': '-10%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'backgroundColor': 'black',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
    ],
    style={'height': '95%'},
)

##############################################################################################

# 儀錶板: PULSE
PULSE_Gauge = dbc.Card(
    children=[
        dbc.CardHeader(
            'MEWS: PULSE',
            style={
                'display': 'inline-block',
                'text-align': 'center',
                'color': 'white',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id='PULSE-gauge',
                        units='次',
                        min=0,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '5%',
                            'marginBottom': '-10%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'backgroundColor': 'black',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
    ],
    style={'height': '95%'},
)

##############################################################################################

# 儀錶板: RESPIRATORY
RESPIRATORY_Gauge = dbc.Card(
    children=[
        dbc.CardHeader(
            'MEWS: RESPIRATORY',
            style={
                'display': 'inline-block',
                'text-align': 'center',
                'color': 'white',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id='RESPIRATORY-gauge',
                        units='次',
                        min=0,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '5%',
                            'marginBottom': '-10%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'backgroundColor': 'black',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
    ],
    style={'height': '95%'},
)

##############################################################################################

# 儀錶板: BT
BT_Gauge = dbc.Card(
    children=[
        dbc.CardHeader(
            'MEWS: BT',
            style={
                'display': 'inline-block',
                'text-align': 'center',
                'color': 'white',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id='BT-gauge',
                        units='℃',
                        min=0,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '5%',
                            'marginBottom': '-10%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'backgroundColor': 'black',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
    ],
    style={'height': '95%'},
)

##############################################################################################

# 儀錶板: SPO2
SPO2_Gauge = dbc.Card(
    children=[
        dbc.CardHeader(
            'MEWS: SPO2',
            style={
                'display': 'inline-block',
                'text-align': 'center',
                'color': 'white',
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id='SPO2-gauge',
                        units='%',
                        min=0,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '5%',
                            'marginBottom': '-10%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'backgroundColor': 'black',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'backgroundColor': 'black',
                'border-radius': '1px',
                'border-width': '5px',
                'border-top': '1px solid rgb(216, 216, 216)',
            },
        ),
    ],
    style={'height': '95%'},
)

##############################################################################################

# Web介面
sidebar_size = 12
graph_size = 10
gauge_size = 'auto'
app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(dbc.Col(chartno_led,
                                        xs=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size)
                        ),
                        dbc.Row(dbc.Col(button_date,
                                        xs=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size)
                        ),
                        dbc.Row(
                                dbc.Col(button_ward,
                                        xs=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size)
                        ),
                        dbc.Row(dbc.Col(button_div,
                                        xs=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size)
                        ),
                        dbc.Row(dbc.Col(button_chartno,
                                        xs=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size)
                        ),
                    ]
                ),
                dbc.Col(graphs,
                        xs=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size)
            ],
            style={
                'display': 'flex',
                'marginBottom': '1%'
                   }
        ),
        dbc.Row(
            [
                dbc.Col(BP_Gauge,
                        xs=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(PULSE_Gauge,
                        xs=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(RESPIRATORY_Gauge,
                        xs=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(BT_Gauge,
                        xs=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(SPO2_Gauge,
                        xs=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
            ],
            justify='end',
            style={
                'marginTop': '1%',
            },
        ),
    ],
)

##############################################################################################

# 篩選器: 月曆
@app.callback(
    Output('date-picker', 'min_date_allowed'),
    Output('date-picker', 'max_date_allowed'),
    Output('date-picker', 'initial_visible_month'),
    Input('boolean-switch', 'on'),
    Input('ward-dropdown', 'value'),
    Input('div-dropdown', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_chartno(on, ward, div, chartno):
    # 按鈕偵測: ICU
    if on:
        df = chdf[chdf['RRTWard'] == 1]
    else:
        df = chdf[chdf['RRTWard'] == 0]
    
    # 按鈕偵測: 護理站
    if ward is None:
        dff = df
    else:
        dff = df[df['Ward'] == ward]
    
    # 按鈕偵測: 科別
    if div is None:
        dfff = dff
    else:
        dfff = dff[dff['DivName'] == div]
    
    # 按鈕偵測: 病歷號
    if chartno is None:
        dffff = dfff
    else:
        dffff = dfff[dfff['ChartNo'] == chartno]
    
    # 日期範圍
    min_date = dffff.index.min().date()
    max_date = dffff.index.max().date()
    start_date = min_date
    
    return min_date, max_date, start_date

##############################################################################################

# 篩選器: 護理站選單
@app.callback(
    Output('ward-dropdown', 'options'),
    Input('boolean-switch', 'on'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('div-dropdown', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_ward(on, start_date, end_date, div, chartno):
    # 按鈕偵測: ICU
    if on:
        df = chdf[chdf['RRTWard'] == 1]
    else:
        df = chdf[chdf['RRTWard'] == 0]
    
    # 按鈕偵測: 日期, 科別
    start_date, end_date = DateRange(df, start_date, end_date)
    if div is None:
        dff = df[(start_date <= df.index) & (df.index <= end_date)]
    else:
        dff = df[(start_date <= df.index) & (df.index <= end_date) & (df['DivName'] == div)]
    
    # 按鈕偵測: 病歷號
    if chartno is None:
        dfff = dff
    else:
        dfff = dff[dff['ChartNo'] == chartno]
        
    return [{'label': i, 'value': i} for i in np.sort(dfff['Ward'].unique(), axis=-1)]

##############################################################################################

# 篩選器: 科別選單
@app.callback(
    Output('div-dropdown', 'options'),
    Input('boolean-switch', 'on'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('ward-dropdown', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_div(on, start_date, end_date, ward, chartno):
    # 按鈕偵測: ICU
    if on:
        df = chdf[chdf['RRTWard'] == 1]
    else:
        df = chdf[chdf['RRTWard'] == 0]
        
    # 按鈕偵測: 日期, 護理站
    start_date, end_date = DateRange(df, start_date, end_date)
    if ward is None:
        dff = df[(start_date <= df.index) & (df.index <= end_date)]
    else:
        dff = df[(start_date <= df.index) & (df.index <= end_date) & (df['Ward'] == ward)]
    
    # 按鈕偵測: 病歷號
    if chartno is None:
        dfff = dff
    else:
        dfff = dff[dff['ChartNo'] == chartno]
    
    return [{'label': i, 'value': i} for i in np.sort(dfff['DivName'].unique(), axis=-1)]

##############################################################################################

# 篩選器: 病歷號選單
@app.callback(
    Output('chartno-dropdown', 'options'),
    Input('boolean-switch', 'on'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('ward-dropdown', 'value'),
    Input('div-dropdown', 'value')
)
def update_chartno(on, start_date, end_date, ward, div):
    # 按鈕偵測: ICU
    if on:
        df = chdf[chdf['RRTWard'] == 1]
    else:
        df = chdf[chdf['RRTWard'] == 0]
    
    # 按鈕偵測: 護理站, 科別
    if (ward is None) and (div is None):
        dff = df
    elif (ward is None) and (div is not None):
        dff = df[df['DivName'] == div]
    elif (ward is not None) and (div is None):
        dff = df[df['Ward'] == ward]
    elif (ward is not None) and (div is not None):
        dff = df[(df['Ward'] == ward) & (df['DivName'] == div)]
    else:
        pass
    
    # 按鈕偵測: 日期
    if (start_date is None) and (end_date is None):
        dfff = dff
    elif (start_date is None) and (end_date is not None):
        dfff = dff[dff.index <= end_date]
    elif (start_date is not None) and (end_date is None):
        dfff = dff[start_date <= dff.index]
    elif (start_date is not None) and (end_date is not None):
        dfff = dff[(start_date <= dff.index) & (dff.index <= end_date)]
    else:
        pass
    
    return [{'label': i, 'value': i} for i in dfff['ChartNo'].unique()]

##############################################################################################

# 篩選器: LED
@app.callback(
    Output('chartno-led', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_chartno(chartno):
    if chartno is None:
        chartno = chdf['ChartNo'][0]
    else:
        pass
    return chartno

##############################################################################################

# 篩選器: 圖表
@app.callback(
    Output('mews-graph', 'figure'),
    Input('chartno-dropdown', 'value')
)
def update_graph(chartno):
    if chartno is None:
        chartno=chdf['ChartNo'][0]
        df = HisData(chartno)
        fig = img(df)
    else:
        df = HisData(chartno)
        fig = img(df)
    return fig

##############################################################################################

# 篩選器: 儀錶板
@app.callback(
    Output('BP-gauge', 'value'),
    Output('BP-gauge', 'max'),
    Output('BP-gauge', 'color'),
    Output('PULSE-gauge', 'value'),
    Output('PULSE-gauge', 'max'),
    Output('PULSE-gauge', 'color'),
    Output('RESPIRATORY-gauge', 'value'),
    Output('RESPIRATORY-gauge', 'max'),
    Output('RESPIRATORY-gauge', 'color'),
    Output('BT-gauge', 'value'),
    Output('BT-gauge', 'max'),
    Output('BT-gauge', 'color'),
    Output('SPO2-gauge', 'value'),
    Output('SPO2-gauge', 'max'),
    Output('SPO2-gauge', 'color'),
    Input('mews-graph', 'clickData'),
    Input('chartno-dropdown', 'value')
)
def display_click_data(clickData, chartno):
    
    # 按鈕偵測: 病歷號
    if chartno is None:
        chartno = chdf['ChartNo'][0]
        df = HisData(chartno)
    else:
        df = HisData(chartno)
    
    # 錶面樣式: 儀錶板
    RRT = ['BP_V1', 'PULSE_V1', 'RESPIRATORY_V1', 'BT_V1', 'SPO2_V1']
    Max = []
    for i in range(len(RRT)):
        k = df[RRT[i]].max()
        if k%1 == 0:
            if k == 0:
                k = 100
                Max.append(k)
            else:
                Max.append(int(k))
        else:
            Max.append(float(k))
    color = Color(RRT, Max)

    # 按鈕偵測: 圖表
    if clickData is None:
        key = [0] * len(RRT)
    else:
        data_time = clickData['points'][0]['x']
        
        # 補值: 秒
        if len(data_time) == 16:
            data_time = data_time + ':00'
            data_time = pd.Timestamp(data_time)
        elif len(data_time) == 19:
            data_time = pd.Timestamp(data_time)
        else:
            pass
        
        # 刷新: 儀錶板重置
        if len(df[(chartno == df['ChartNo']) & (data_time == df.index)]) == 0:
            key = [0] * len(RRT)
        else:
            # 數值抓取
            dff = df[data_time == df.index]
            key = []
            for i in range(len(RRT)):
                v = dff[RRT[i]][0]
                if v%1 == 0:
                    key.append(int(v))
                else:
                    key.append(float(v))

    return (key[0], Max[0], color[0],
            key[1], Max[1], color[1],
            key[2], Max[2], color[2],
            key[3], Max[3], color[3],
            key[4], Max[4], color[4]
           )