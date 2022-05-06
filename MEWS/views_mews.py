from django.shortcuts import render

def MEWS(request):
    au = request.session.get('au')
    return render(request, 'MEWS/views_mews.html',{'au':au})

##############################################################################################

# django
from django_plotly_dash import DjangoDash
from django.db import connections

# python
import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

def SQL(sql, colname):
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns = colname)
    return df

def connect():
    sql1 =  '''
            SELECT DISTINCT ChartNo, VisitNo, OccurDate, DivName, Ward, RRTWard, ICU, SPO2_V1, GCS_V
            FROM RRTFinish
            ORDER BY ChartNo, VisitNo, OccurDate
            '''
    colname1 = ['ChartNo', 'VisitNo', 'OccurDate', 'DivName', 'Ward', 'RRTWard', 'ICU', 'SPO2_V1', 'GCS_V']
    chdf = SQL(sql1, colname1)
    chdf.set_index('OccurDate', inplace=True)
    
    sql2 =  '''
            SELECT DISTINCT ChartNo, VisitNo, Ward, StartTime, EndTime
            FROM RRTICUTime
            ORDER BY ChartNo, VisitNo, StartTime
            '''
    colname2 = ['ChartNo', 'VisitNo', 'Ward', 'StartTime', 'EndTime']
    icudf = SQL(sql2, colname2)
    return chdf, icudf

chdf, icudf = connect()

##############################################################################################

app = DjangoDash('MEWS',
                 meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
                 external_stylesheets=[dbc.themes.QUARTZ]
                 )

app.title = 'AIC: MEWS'

##############################################################################################

sql = '''
        SELECT DISTINCT ChartNo, VisitNo, OccurDate,
                BP_V1, PULSE_V1, RESPIRATORY_V1,
                BT_V1, SPO2_V1,
                GCS_V, Score6_E, Score6_M, Score6_V, Score6, RRT
        FROM RRTFinish
        WHERE ChartNo=%s
        ORDER BY ChartNo, VisitNo, OccurDate
      '''
colname = ['ChartNo', 'VisitNo', 'OccurDate',
           'BP_V1', 'PULSE_V1', 'RESPIRATORY_V1', 'BT_V1', 'SPO2_V1',
           'GCS_V', 'Score6_E', 'Score6_M', 'Score6_V', 'Score6', 'RRT']

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

def DateRangeDf(df, start_date, end_date):
    if (start_date is None) and (end_date is None):
        dff = df
    elif (start_date is None) and (end_date is not None):
        end_date = DateRangeEnd(end_date)
        dff = df[df.index <= end_date]
    elif (start_date is not None) and (end_date is None):
        dff = df[start_date <= df.index]
    elif (start_date is not None) and (end_date is not None):
        end_date = DateRangeEnd(end_date)
        dff = df[(start_date <= df.index) & (df.index <= end_date)]
    else:
        pass
    return dff

##############################################################################################

def DateRangeEnd(end_date):
    end = dt.strptime(str(end_date), '%Y-%m-%d') + datetime.timedelta(days=1)
    return end

##############################################################################################

def Feature(df, SPO2, GCS):
    # 按鈕偵測: SPO2指標
    if SPO2:
        df1 = df[df['SPO2_V1'] != 0]
    else:
        df1 = df
    
    # 按鈕偵測: GCS指標
    if GCS:
        df2 = df1[df1['GCS_V'] != '']
    else:
        df2 = df1
    return df2

##############################################################################################

def img(df, chartno):
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
    df6 = df[df['GCS_V'] != '']
    fig.add_scatter(x=df6.index, y=df6['Score6'], name='GCS', mode='lines+markers')
    
    # 背景填色
    if len(icudf[icudf['ChartNo'] == chartno]) == 0:
        pass
    else:
        # 日期範圍
        min_date = df.index.min()
        max_date = df.index.max()
        # 搜尋: ICU區間
        icudff = icudf[icudf['ChartNo'] == chartno]
        for i in range(len(icudff)):
            start = icudff.iloc[i]['StartTime']
            end = icudff.iloc[i]['EndTime']
            ward = icudff.iloc[i]['Ward']
            if (end < min_date) or (max_date < start):
                pass
            else:
                if (min_date < start) and (end < max_date):
                    fig.add_vrect(x0=start, x1=end, fillcolor='LightSalmon', opacity=0.5, \
                                  layer='below', line_width=0, annotation_text=ward)
                elif (start < min_date) and (end < max_date):
                    start = min_date
                    fig.add_vrect(x0=start, x1=end, fillcolor='LightSalmon', opacity=0.5, \
                                  layer='below', line_width=0, annotation_text=ward)
                elif (min_date < start) and (max_date < end):
                    end = max_date
                    fig.add_vrect(x0=start, x1=end, fillcolor='LightSalmon', opacity=0.5, \
                                  layer='below', line_width=0, annotation_text=ward)
                elif (start < min_date) and (max_date < end):
                    start = min_date
                    end = max_date
                    fig.add_vrect(x0=start, x1=end, fillcolor='LightSalmon', opacity=0.5, \
                                  layer='below', line_width=0, annotation_text=ward)
                else:
                    pass
    
    fig.update_layout(
        updatemenus=[
            dict(
                direction='right',
                active=0,
                x=0.1068,
                y=1.21,
                buttons=list([
                    dict(label='All',
                         method='update',
                         args=[ {'visible': [True, True, True, True, True, True]},
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='BP', 
                         method='update', 
                         args=[ {'visible': [True, False, False, False, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='PULSE', 
                         method='update', 
                         args=[ {'visible': [False, True, False, False, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='RESPIRATORY', 
                         method='update', 
                         args=[ {'visible': [False, False, True, False, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='BT', 
                         method='update', 
                         args=[ {'visible': [False, False, False, True, False, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='SPO2', 
                         method='update', 
                         args=[ {'visible': [False, False, False, False, True, False]}, 
                                {'showlegend' : True}
                              ]
                        ),
                    dict(label='GCS', 
                         method='update', 
                         args=[ {'visible': [False, False, False, False, False, True]}, 
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
                         '#deed07':[89.5, 94.5],
                         '#23b000':[94.5, Max[i]]
                        }
            elif 89.5<Max[i]<94.5:
                value = {'red':[0, 84.5],
                         '#ff7300':[84.5, 89.5],
                         '#deed07':[89.5, Max[i]]
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
        'Modified Early Warning Score(MEWS): '
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
                'border-radius': '1px',
                'border-width': '5px',
            },
        ),
        dbc.CardBody(
            [
                daq.LEDDisplay(
                    id='chartno-led',
                    size=28,
                    color='#fec036',
                    backgroundColor='#2b2b2b'
                )
            ],
            style={
                'display': 'flex',
                'justify-content': 'space-around',
                'align-items': 'center',
                'height': '80px',
                'text-align': 'center',
                'border-radius': '1px',
                'border-width': '5px',
            },
        ),
    ],
    style={'marginBottom': '3%'},
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
                            clearable=True,
                            calendar_orientation='vertical',
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-around',
                           'align-items': 'center',
                           'height': '75px',
                          }
                    
                )
            ],
            style={
                'text-align': 'center',
                'border-radius': '1px',
                'border-width': '5px',
            },
        )
    ],
    style={'marginBottom': '3%'},
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
                                   'width': '150px',
                            }
                        ),
                        html.Div(
                            [
                                'ICU:',
                                daq.BooleanSwitch(id='ward-boolean-switch', on=False),
                            ],
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'height': '30px',
                          }
                )
            ],
            style={
                'text-align': 'center',
                'border-radius': '1px',
                'border-width': '5px',
            },
        )
    ],
    style={'marginBottom': '3%'},
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
                                   'width': '175px',
                            }
                         ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'height': '10px',
                    }
                )
            ],
            style={
                'text-align': 'center',
                'border-radius': '1px',
                'border-width': '5px',
            },
        )
    ],
    style={'marginBottom': '3%'},
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
                                   'width': '145px',
                            }
                         )

                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'height': '10px',
                    }
                )
            ],
            style={
                'text-align': 'center',
                'border-radius': '1px',
                'border-width': '5px',
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
                        dcc.Loading(
                            id='loading-1',
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='mews-graph',
                                            config={'displayModeBar': True},
                                        ),
                                    ],
                                    style={
                                        'marginBottom': '0.6%',
                                    },
                                )
                            ],
                            type='circle',
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'SPO2:',
                                daq.BooleanSwitch(id='SPO2-boolean-switch', on=False),
                            ],
                            style={
                                'display': 'flex',
                                'justify-content': 'space-around',
                                'width': '105px',
                            },
                        ),
                        html.Div(
                            [
                                'GCS:',
                                daq.BooleanSwitch(id='GCS-boolean-switch', on=False),
                            ],
                            style={
                                'display': 'flex',
                                'justify-content': 'space-around',
                                'width': '95px',
                            },
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                        'marginBottom': '-1.45%',
                    },
                ),
            ],
            style={
                'border-radius': '1px',
                'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
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
                'border-radius': '1px',
                'border-width': '5px',
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
                            'marginTop': '8%',
                            'marginBottom': '-25%',

                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'border-radius': '1px',
                'justify-content': 'center',
            },
        ),
    ],
    style={'width': '95%',
           'height': '370px',
          },
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
                'border-radius': '1px',
                'border-width': '5px',
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
                            'marginTop': '8%',
                            'marginBottom': '-25%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'border-radius': '1px',
                'justify-content': 'center',
            },
        ),
    ],
    style={'width': '95%',
           'height': '370px',
          },
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
                'border-radius': '1px',
                'border-width': '5px',
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
                            'marginTop': '8%',
                            'marginBottom': '-25%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'border-radius': '1px',
                'justify-content': 'center',
            },
        ),
    ],
    style={'width': '95%',
           'height': '370px',
          },
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
                'border-radius': '1px',
                'border-width': '5px',
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
                            'marginTop': '8%',
                            'marginBottom': '-25%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'border-radius': '1px',
                'justify-content': 'center',
            },
        ),
    ],
    style={'width': '95%',
           'height': '370px',
          },
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
                'border-radius': '1px',
                'border-width': '5px',
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
                            'marginTop': '8%',
                            'marginBottom': '-25%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                )
            ],
            className='d-flex',
            style={
                'border-radius': '1px',
                'justify-content': 'center',
            },
        ),
    ],
    style={'width': '95%',
           'height': '370px',
          },
)

##############################################################################################

# 測量計: GCS
GCS_Gauge = dbc.Card(
    children=[
        dbc.CardHeader(
            'MEWS: GCS ( E / M / V )',
            style={
                'display': 'inline-block',
                'text-align': 'center',
                'color': 'white',
                'border-radius': '1px',
                'border-width': '5px',
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Thermometer(
                        id='GCS-E-thermometer',
                        units='分',
                        min=-1,
                        max=4,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '-10%',
                            'marginBottom': '-95%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                ),
                html.Div(
                    daq.Thermometer(
                        id='GCS-M-thermometer',
                        units='分',
                        min=-1,
                        max=4,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '-10%',
                            'marginBottom': '-95%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '5px',
                    },
                ),
                html.Div(
                    daq.Thermometer(
                        id='GCS-V-thermometer',
                        units='分',
                        min=-1,
                        max=4,
                        showCurrentValue=True,
                        style={
                            'align': 'center',
                            'display': 'flex',
                            'marginTop': '-10%',
                            'marginBottom': '-95%',
                        },
                    ),
                    className='m-auto',
                    style={
                        'display': 'flex',
                        'border-radius': '1px',
                        'border-width': '1px',
                    },
                )
            ],
            className='d-flex',
            style={
                'border-radius': '1px',
                'align-items': 'center',
                'justify-content': 'space-around',
            },
        ),
    ],
    style={'width': '95%',
           'height': '370px',
          },
)

##############################################################################################

# UI主題
theme = {
    'dark': True,
    'detail': '#06FF00',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}
graphs = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=graphs)]
)
button_ward = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=button_ward)]
)
BP_Gauge = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=BP_Gauge)]
)
PULSE_Gauge = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=PULSE_Gauge)]
)
RESPIRATORY_Gauge = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=RESPIRATORY_Gauge)]
)
BT_Gauge = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=BT_Gauge)]
)
SPO2_Gauge = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=SPO2_Gauge)]
)
GCS_Gauge = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=GCS_Gauge)]
)

##############################################################################################

# Web介面
sidebar_size = 12
graph_size = 10
gauge_size = 2
GCS_size = 2
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
                                        sm=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size,
                                        style={'z-index': '99999'}
                                       )
                        ),
                        dbc.Row(dbc.Col(button_date,
                                        xs=sidebar_size,
                                        sm=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size,
                                        style={'z-index': '99998'}
                                       )
                        ),
                        dbc.Row(
                                dbc.Col(button_ward,
                                        xs=sidebar_size,
                                        sm=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size,
                                        style={'z-index': '99997'}
                                       )
                        ),
                        dbc.Row(dbc.Col(button_div,
                                        xs=sidebar_size,
                                        sm=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size,
                                        style={'z-index': '99996'}
                                       )
                        ),
                        dbc.Row(dbc.Col(button_chartno,
                                        xs=sidebar_size,
                                        sm=sidebar_size,
                                        md=sidebar_size,
                                        lg=sidebar_size,
                                        width=sidebar_size,
                                        style={'z-index': '99995'}
                                       )
                        ),
                    ],
                    #width=2
                ),
                dbc.Col(graphs,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size)
            ],
            style={
                'display': 'flex',
                'marginBottom': '1%',
                   }
        ),
        dbc.Row(
            [
                dbc.Col(BP_Gauge,
                        xs=gauge_size,
                        sm=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(PULSE_Gauge,
                        xs=gauge_size,
                        sm=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(RESPIRATORY_Gauge,
                        xs=gauge_size,
                        sm=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(BT_Gauge,
                        xs=gauge_size,
                        sm=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(SPO2_Gauge,
                        xs=gauge_size,
                        sm=gauge_size,
                        md=gauge_size,
                        lg=gauge_size,
                        width=gauge_size),
                dbc.Col(GCS_Gauge,
                        xs=GCS_size,
                        sm=GCS_size,
                        md=GCS_size,
                        lg=GCS_size,
                        width=GCS_size),
            ],
            justify='center',
            style={
                'marginTop': '1%',
            },
        ),
        dbc.Row(html.Pre(id='space')),
    ],
    style={
        'overflow-x': 'hidden',
        'overflow-y': 'hidden',
    }
)

##############################################################################################

# 篩選器: 月曆
@app.callback(
    Output('date-picker', 'min_date_allowed'),
    Output('date-picker', 'max_date_allowed'),
    Output('date-picker', 'initial_visible_month'),
    Input('ward-boolean-switch', 'on'),
    Input('SPO2-boolean-switch', 'on'),
    Input('GCS-boolean-switch', 'on'),
    Input('ward-dropdown', 'value'),
    Input('div-dropdown', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_chartno(on, SPO2, GCS, ward, div, chartno):
    # 按鈕偵測: ICU
    if on:
        icudf = chdf[chdf['RRTWard'] == 1]
        df = Feature(icudf, SPO2, GCS)
    else:
        icudf = chdf[chdf['RRTWard'] == 0]
        df = Feature(icudf, SPO2, GCS)
    
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
    Input('ward-boolean-switch', 'on'),
    Input('SPO2-boolean-switch', 'on'),
    Input('GCS-boolean-switch', 'on'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('div-dropdown', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_ward(on, SPO2, GCS, start_date, end_date, div, chartno):
    # 按鈕偵測: ICU
    if on:
        icudf = chdf[chdf['RRTWard'] == 1]
        df = Feature(icudf, SPO2, GCS)
    else:
        icudf = chdf[chdf['RRTWard'] == 0]
        df = Feature(icudf, SPO2, GCS)
    
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
    Input('ward-boolean-switch', 'on'),
    Input('SPO2-boolean-switch', 'on'),
    Input('GCS-boolean-switch', 'on'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('ward-dropdown', 'value'),
    Input('chartno-dropdown', 'value')
)
def update_div(on, SPO2, GCS, start_date, end_date, ward, chartno):
    # 按鈕偵測: ICU
    if on:
        icudf = chdf[chdf['RRTWard'] == 1]
        df = Feature(icudf, SPO2, GCS)
    else:
        icudf = chdf[chdf['RRTWard'] == 0]
        df = Feature(icudf, SPO2, GCS)
        
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
    Input('ward-boolean-switch', 'on'),
    Input('SPO2-boolean-switch', 'on'),
    Input('GCS-boolean-switch', 'on'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('ward-dropdown', 'value'),
    Input('div-dropdown', 'value')
)
def update_chartno(on, SPO2, GCS, start_date, end_date, ward, div):
    # 按鈕偵測: ICU
    if on:
        icudf = chdf[chdf['RRTWard'] == 1]
        df = Feature(icudf, SPO2, GCS)
    else:
        icudf = chdf[chdf['RRTWard'] == 0]
        df = Feature(icudf, SPO2, GCS)
    
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
    dfff = DateRangeDf(dff, start_date, end_date)
    
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
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('chartno-dropdown', 'value')
)
def update_graph(start_date, end_date, chartno):
    # 按鈕偵測: 病歷號
    if chartno is None:
        chartno=chdf['ChartNo'][0]
        df = HisData(chartno)
        #dff = DateRangeDf(df, None, None)
        dff = DateRangeDf(df, start_date, end_date)
        fig = img(dff, chartno)
    else:
        df = HisData(chartno)
        dff = DateRangeDf(df, start_date, end_date)
        fig = img(dff, chartno)
    
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
    Output('GCS-E-thermometer', 'value'),
    Output('GCS-E-thermometer', 'color'),
    Output('GCS-M-thermometer', 'value'),
    Output('GCS-M-thermometer', 'color'),
    Output('GCS-V-thermometer', 'value'),
    Output('GCS-V-thermometer', 'color'),
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
        key_E = 0
        key_M = 0
        key_V = 0
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
            key_E = 0
            key_M = 0
            key_V = 0
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
            key_E = dff['Score6_E'][0]
            key_M = dff['Score6_M'][0]
            key_V = dff['Score6_V'][0]
            
    # 量計樣式
    key_GCS = [key_E, key_M, key_V]
    color_GCS = []
    for i in range(len(key_GCS)):
        if key_GCS[i] == 0:
            c = theme['primary']
            color_GCS.append(c)
        elif key_GCS[i] == 1:
            c = 'yellow'
            color_GCS.append(c)
        elif key_GCS[i] == 2:
            c = 'orange'
            color_GCS.append(c)
        elif key_GCS[i] == 3:
            c = 'red'
            color_GCS.append(c)
        else:
            pass

    return (key[0], Max[0], color[0],
            key[1], Max[1], color[1],
            key[2], Max[2], color[2],
            key[3], Max[3], color[3],
            key[4], Max[4], color[4],
            key_E, color_GCS[0],
            key_M, color_GCS[1],
            key_V, color_GCS[2],
           )