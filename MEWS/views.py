from django.shortcuts import render

def MEWS(request):
    au = request.session.get('au')
    return render(request, 'MEWS/MEWS.html',{'au':au})

##############################################################################################

# django
from django_plotly_dash import DjangoDash
from django.db import connections

# python
import pymssql
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
from plotly.subplots import make_subplots

def SQL(sql, colname):
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns = colname)
    return df

def connect():
    sql1 =  '''
                SELECT DISTINCT Year
                FROM HealthData.dbo.InPatientlenYear
                ORDER BY Year
            '''
    colname1 = ['Year']
    ydf = SQL(sql1, colname1)
    
    sql2 =  '''
                SELECT DISTINCT YEAR(OccurDate) AS Year, Ward
                FROM RRTFinish_1321
                WHERE RRTWard=0
                ORDER BY Year, Ward
            '''
    colname2 = ['Year', 'Ward']
    wdf = SQL(sql2, colname2)
    
    sql3 =  '''
                SELECT YEAR(StartTime) AS Year
                FROM Web_RRTRecord
                GROUP BY YEAR(StartTime)
                ORDER BY Year
            '''
    colname3 = ['Year']
    mydf = SQL(sql3, colname3)
    
    sql4 =   '''
                SELECT DISTINCT YEAR(StartTime) AS Year
                FROM ProgressTransfer_ICURRTNormal
                WHERE (YEAR(StartTime) between 2019 and 2021)
                    and StartTime >= '2019-04-16'
                ORDER BY Year
            '''
    colname4 = ['Year']
    unydf = SQL(sql4, colname4)
    
    return ydf, wdf, mydf, unydf

ydf, wdf, mydf, unydf = connect()

##############################################################################################

app = DjangoDash('MEWSData',
                 meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
                 external_stylesheets=[dbc.themes.QUARTZ]
                 )

app.title = 'AIC: MEWS'

##############################################################################################

def YearNum(year, on):
    if on:
        sql = '''
              EXEC HealthData.InPatientYearVis @Year=%s
              '''
        colname = [str(year)+'年: 患者總住院天數', '總就醫人次 (Number of VisitNo)', '總就醫人數']
    else:
        sql = '''
              EXEC HealthData.InPatientYearCh @Year=%s
              '''
        colname = [str(year)+'年: 患者總住院天數', '總就醫人數 (Number of ChartNo)', '總就醫人次']
    ID = [year]   
    cursor = connections['HealthData'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2]

##############################################################################################

def RRTNum(year1, year2, ward):
    sql = f'''
          EXEC MEWS.RRTData @Date1={year1}, @Date2={year2}, @Ward="{ward}"
          '''
    colname = ['RRT', 'num']
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1]

##############################################################################################

def RRTWardNum(year, avg):
    if avg:
        sql = '''
              EXEC MEWS.RRTWardAvgData @Date=%s
              '''
    else:
        sql = '''
              EXEC MEWS.RRTWardData @Date=%s
              '''
    colname = ['Ward', '安全', '達三項', '可啟動', '系統啟動']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3], colname[4]

##############################################################################################

def RRTDivNum(year, avg):
    if avg:
        sql = '''
              EXEC MEWS.RRTDivAvgData @Date=%s
              '''
    else:
        sql = '''
              EXEC MEWS.RRTDivData @Date=%s
              '''
    colname = ['DivName', '安全', '達三項', '可啟動', '系統啟動']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3], colname[4]

##############################################################################################

def MatchNum(year):
    sql = '''
          EXEC MEWS.RRTMatchPercentage @Date=%s
          '''
    colname = ['State', 'num']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1]

##############################################################################################

def MatchDiffNum(year):
    sql = '''
          EXEC MEWS.RRTMatch @Date=%s
          '''
    colname = ['diff', '安全', '達三項', '可啟動', '系統啟動']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3], colname[4]

##############################################################################################

def RRTTransferType(year, on):
    if on:
        age = 2
        txt = '小兒'
    else:
        age = 1
        txt = '成人'
    
    sql = '''
            EXEC MEWS.RRTTransferTypeNormal_EXEC @Date=%(Year)s, @Age=%(Age)s
          '''
    colname = [str(year)+'年: '+txt+'之病程轉入原因', '就醫人數', '就醫人次', 'RRT偵測筆數']
    ID = {'Year': year, 'Age': age}
    conn = pymssql.connect(
        server='172.31.6.157',
        user='TEST',
        password='81218',
        database='MEWS'
    )
    cursor = conn.cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    conn.close()
    return df, colname[1], colname[2], colname[3]

##############################################################################################

def RRTTransferNum(year):
    if year is None:
        year = '%'
        yeartxt = 'All'
    else:
        yeartxt = year
    
    sql = '''
          EXEC MEWS.RRTTransferYearNormal @Date=%s, @Yeartxt=%s
          '''
    colname = ['Year', '就醫人數', '就醫人次', '筆數']
    ID = [year, yeartxt]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3]

##############################################################################################

def RRTTransferNullNum(year):
    if year is None:
        year = '%'
    else:
        pass

    sql = '''
           EXEC MEWS.RRTTransferYearNullNormal @Date=%s
          '''
    colname = ['Match', '就醫人數', '就醫人次', '筆數']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3]

##############################################################################################

def RRTTransferEndMiss(year):
    sql = '''
          EXEC MEWS.RRTTransferEndMissNormal @Date=%s
          '''
    colname = ['RRTType', '就醫人數', '就醫人次', '筆數']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3]

##############################################################################################

def RRTTransferEndType(year):
    sql = '''
          EXEC MEWS.RRTTransferEndTypeNormal @Date=%s
          '''
    colname = ['EndType', '就醫人數', '就醫人次', '筆數']
    ID = [year]
    cursor = connections['MEWS'].cursor()
    cursor.execute(sql, ID)
    row = cursor.fetchall()
    df = pd.DataFrame(row, columns=colname)
    df.set_index(colname[0], inplace=True)
    return df, colname[1], colname[2], colname[3]

##############################################################################################

# Web: 標題
def logo(app):
    title = html.H5(
        'AIC: Test Web',
        style={'marginTop': 5,
               'marginLeft': '10px',
               'width': '300px',
              },
    )

    info_about_app = html.H6(
        'Modified Early Warning Score(MEWS): '
        'User interface.',
        style={'marginLeft': '10px',
               'width': '500px',
              },
    )

    return dbc.Row([dbc.Col([dbc.Row([title]), dbc.Row([info_about_app])])])

##############################################################################################

# 住院資訊
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
                                            id='graph',
                                            config={'displayModeBar': True},
                                             style={'height': '436px',
                                                   }
                                        ),
                                    ],
                                    style={'marginBottom': '1%',
                                    },
                                )
                            ],
                            type='circle',
                        ),
                        html.Div(
                            [
                                dcc.Slider(id='year-dropdown',
                                           min=ydf['Year'].min(),
                                           max=ydf['Year'].max(),
                                           step=None,
                                           value=ydf['Year'].max(),
                                           marks={str(i): {'label' : str(i),
                                                           'style':{'color': '#ffffff',
                                                                    'font-size': '18px',
                                                                   }
                                                          }
                                                  for i in ydf['Year'].unique()
                                                 },
                                           included=False
                                )
                            ],
                        )
                    ],
                    style={'marginBottom': '2%',
                                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'ChartNo',
                                daq.BooleanSwitch(id='chvis-boolean-switch', on=True),
                                'VisitNo',
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '190px',
                            },
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'marginBottom': '1%'
                    }
                ),
            ],
            style={'text-align': 'center',
                   'border-radius': '1px',
                   'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
)

##############################################################################################

# RRT分布
graphs_RRT = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Loading(
                            id='loading-2',
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='RRT-graph',
                                        ),
                                    ],
                                    style={'marginBottom': '2%',
                                    },
                                ),
                            ],
                            type='circle',
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'Select Year:',
                                 dcc.Dropdown(id='RRT-year-dropdown',
                                              multi=False,
                                              searchable=True,
                                              style={'width': '90px',
                                                     'color': '#1a1f61',
                                                    }
                                ),
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '200px',
                            }
                        ),
                        html.Div(
                            [
                                'Select Ward:',
                                 dcc.Dropdown(id='RRT-ward-dropdown',
                                              multi=False,
                                              searchable=True,
                                              style={'width': '90px',
                                                     'color': '#1a1f61',
                                                    }
                                ),
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '200px',
                            }
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'width': '430px',
                           'marginBottom': '1%',
                    }
                ),
            ],
            style={'text-align': 'flex-start',
                   'border-radius': '1px',
                   'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
)

##############################################################################################

# 護理站資訊
graphs_ward = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Loading(
                            id='loading-3',
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='ward-graph',
                                            config={'displayModeBar': True},
                                             style={'height': '436px',
                                                   }
                                        ),
                                    ],
                                    style={'marginBottom': '1%',
                                    },
                                )
                            ],
                            type='circle',
                        ),
                        html.Div(
                            [
                                dcc.Slider(id='ward-year-dropdown',
                                           min=ydf['Year'].min(),
                                           max=ydf['Year'].max(),
                                           step=None,
                                           value=ydf['Year'].max(),
                                           marks={str(i): {'label' : str(i),
                                                           'style':{'color': '#ffffff',
                                                                    'font-size': '18px',
                                                                   }
                                                          }
                                                  for i in ydf['Year'].unique()
                                                 },
                                           included=False
                                )
                            ],
                        )
                    ],
                    style={'marginBottom': '2%',
                                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'Ward',
                                daq.BooleanSwitch(id='Ward-boolean-switch', on=False),
                                'DivName',
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '170px',
                            },
                        ),
                        html.Div(
                            [
                                'Aggregate',
                                daq.BooleanSwitch(id='avg-boolean-switch', on=True),
                                'Mean',
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '190px',
                            },
                        ),
                        html.Div(
                            [
                                'Stack',
                                daq.BooleanSwitch(id='draw-boolean-switch', on=False),
                                'Group',
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '150px',
                            },
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'width': '600px',
                           'marginBottom': '1%'
                    }
                ),
            ],
            style={'text-align': 'center',
                   'border-radius': '1px',
                   'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
)

##############################################################################################

# RRT 匹配分布
graph_match = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Loading(
                            id='loading-4',
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                 dcc.Graph(
                                                    id='Match-graph',
                                                ),
                                            ],
                                            style={'width': '480px',
                                                  }
                                        ),
                                        html.Div(
                                            [
                                                 dcc.Graph(
                                                    id='Match-bar-graph',
                                                ),
                                            ],
                                            style={'width': '1200px',
                                                  }
                                        ),
                                    ],
                                    style={'marginBottom': '2%',
                                           'display': 'flex',
                                           'justify-content': 'space-between',
                                    },
                                ),
                            ],
                            type='circle',
                        ),
                        
                    ],
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'Select Year:',
                                dcc.Dropdown(id='Match-year-dropdown',
                                             options=[{'label': i, 'value': i} for i in mydf['Year'].unique()],
                                             multi=False,
                                             searchable=True,
                                             style={'width': '90px',
                                                    'color': '#1a1f61',
                                                   }
                                ),
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '200px',
                            }
                        ),
                        html.Div(
                            [
                                'Stack',
                                daq.BooleanSwitch(id='Match-draw-boolean-switch', on=False),
                                'Group',
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '150px',
                            },
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'width': '400px',
                           'marginBottom': '1%',
                    }
                ),
            ],
            style={'text-align': 'flex-start',
                   'border-radius': '1px',
                   'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
)

##############################################################################################

# HIS RRT病程分布
graphs_RRTType = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Loading(
                            id='loading-5',
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='RRTType-graph',
                                            config={'displayModeBar': True},
                                             style={'height': '436px',
                                                   }
                                        ),
                                    ],
                                    style={'marginBottom': '1%',
                                    },
                                )
                            ],
                            type='circle',
                        ),
                        html.Div(
                            [
                                dcc.Slider(id='RRTType-year-dropdown',
                                           min=unydf['Year'].min(),
                                           max=unydf['Year'].max(),
                                           step=None,
                                           value=unydf['Year'].max(),
                                           marks={str(i): {'label' : str(i),
                                                           'style':{'color': '#ffffff',
                                                                    'font-size': '18px',
                                                                   }
                                                          }
                                                  for i in unydf['Year'].unique()
                                                 },
                                           included=False
                                )
                            ],
                        )
                    ],
                    style={'marginBottom': '2%',
                                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'Aldult',
                                daq.BooleanSwitch(id='RRTType-age-boolean-switch', on=False),
                                'Children',
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '190px',
                            },
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'marginBottom': '1%'
                    }
                ),
            ],
            style={'text-align': 'center',
                   'border-radius': '1px',
                   'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
)

##############################################################################################

# 不可預期: RRT分布
graphs_ICURRT = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Loading(
                            id='loading-6',
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='ICURRT-graph',
                                        ),
                                    ],
                                    style={'marginBottom': '2%',
                                    },
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='ICURRT2-graph',
                                        ),
                                    ],
                                    style={'marginBottom': '2%',
                                    },
                                ),
                            ],
                            type='circle',
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                'Select Year:',
                                 dcc.Dropdown(id='ICURRT-year-dropdown',
                                              options=[{'label': i, 'value': i} for i in unydf['Year'].unique()],
                                              multi=False,
                                              searchable=True,
                                              style={'width': '90px',
                                                     'color': '#1a1f61',
                                                    }
                                ),
                            ],
                            style={'display': 'flex',
                                   'justify-content': 'space-around',
                                   'align-items': 'center',
                                   'width': '200px',
                            }
                        ),
                    ],
                    style={'display': 'flex',
                           'justify-content': 'space-between',
                           'align-items': 'center',
                           'width': '430px',
                           'marginBottom': '1%',
                    }
                ),
            ],
            style={'text-align': 'flex-start',
                   'border-radius': '1px',
                   'border-width': '5px',
            },
        )
    ],
    style={'width': '99%'},
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

graphs_ward = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=graphs_ward)]
)

graph_match = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=graph_match)]
)

graphs_RRTType = html.Div(
    children=[daq.DarkThemeProvider(theme=theme, children=graphs_RRTType)]
)


##############################################################################################

# Web介面
graph_size = 12
app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),
        dbc.Row(
            [
                dbc.Col(graphs,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size,
                       )
            ],
            style={'display': 'flex',
                   'marginBottom': '1%',
                   }
        ),
        dbc.Row(
            [
                dbc.Col(graphs_RRT,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size,
                        style={'z-index': '99'},
                       )
            ],
            style={'display': 'flex',
                   'marginBottom': '1%',
                   }
        ),
        dbc.Row(
            [
                dbc.Col(graphs_ward,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size,
                        style={'z-index': '98'},
                       )
            ],
            style={'display': 'flex',
                   'marginBottom': '1%',
                   }
        ),
        dbc.Row(
            [
                dbc.Col(graph_match,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size,
                        style={'z-index': '97'},
                       )
            ],
            style={'display': 'flex',
                   'marginBottom': '1%',
                   }
        ),
        dbc.Row(
            [
                dbc.Col(graphs_RRTType,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size,
                        style={'z-index': '96'},
                       )
            ],
            style={'display': 'flex',
                   'marginBottom': '1%',
                   }
        ),
        dbc.Row(
            [
                dbc.Col(graphs_ICURRT,
                        xs=graph_size,
                        sm=graph_size,
                        md=graph_size,
                        lg=graph_size,
                        width=graph_size,
                        style={'z-index': '95'},
                       )
            ],
            style={'display': 'flex',
                   'marginBottom': '1%',
                   }
        ),
    ],
    style={#'overflow-x': 'hidden',
           #'overflow-y': 'hidden',
    }
)

##############################################################################################

# 篩選器: 住院
@app.callback(
    Output('graph', 'figure'), 
    Input('year-dropdown', 'value'),
    Input('chvis-boolean-switch', 'on'),
)
def update_graph(year, on):
    if year is None:
        year = ydf['Year'].max()
        df, col1, col2 = YearNum(year, on)
    else:
        df, col1, col2 = YearNum(year, on)

    fig = px.bar(df, x=df.index, y=col1, hover_data=[col1, col2])
    fig.update_traces(text=df[col1],
                      textposition='auto',
                      textfont_size=15,
                      selector=dict(type='bar'),
                     )
    fig.update_layout(hovermode='x unified',
                      hoverlabel=dict(font_size=15),
                      modebar_remove=['resetscale', 'lasso'],
                     )
    fig.update_xaxes(rangeslider_visible=True)
    return fig

##############################################################################################

# 篩選器: 年份選單
@app.callback(
    Output('RRT-year-dropdown', 'options'),
    Input('RRT-ward-dropdown', 'value'),
)
def update_graph(ward):
    if ward is None:
        df = wdf
    else:
        df = wdf[wdf['Ward']==ward]

    return [{'label': i, 'value': i} for i in df['Year'].unique()]

##############################################################################################

# 篩選器: 護理站選單
@app.callback(
    Output('RRT-ward-dropdown', 'options'), 
    Input('RRT-year-dropdown', 'value'),
)
def update_graph(year):
    if year is None:
        df = wdf
    else:
        df = wdf[wdf['Year']==year]

    return [{'label': i, 'value': i} for i in df['Ward'].unique()]

##############################################################################################

# 篩選器: RRT分布
@app.callback(
    Output('RRT-graph', 'figure'),
    Input('RRT-year-dropdown', 'value'),
    Input('RRT-ward-dropdown', 'value'),
)
def update_graph_RRT(year, ward):
    if year is None:
        year1 = wdf['Year'].min()
        year2 = wdf['Year'].max()
    else:
        year1 = year
        year2 = year
    
    if ward is None:
        ward = '%'
        wardname = 'all Ward'
        df, col1 = RRTNum(year1, year2, ward)
        dff = df[df.index!='0~4分: 安全']
    else:
        wardname = ward
        df, col1 = RRTNum(year1, year2, ward)
        dff = df[df.index!='0~4分: 安全']

    c1 = []
    for i in range(len(df)):
        if df.index[i]=='0~4分: 安全':
            c1.append('green')
        elif df.index[i]=='3~4分: 達三項':
            c1.append('#ede500')
        elif df.index[i]=='5~6分: 可啟動':
            c1.append('#ff9d00')
        elif df.index[i]=='7分以上: 系統啟動':
            c1.append('red')
        else:
            pass
        
    c2 = []
    for i in range(len(dff)):
        if dff.index[i]=='0~4分: 安全':
            c2.append('green')
        elif dff.index[i]=='3~4分: 達三項':
            c2.append('#ede500')
        elif dff.index[i]=='5~6分: 可啟動':
            c2.append('#ff9d00')
        elif dff.index[i]=='7分以上: 系統啟動':
            c2.append('red')
        else:
            pass
            
    col = df.index.unique()
    
    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                       )
    fig.add_trace(go.Pie(labels=df.index, values=df[col1],
                         name='全數據分布',
                         marker_colors=c1,
                         pull=[0, 0.1, 0.1, 0.1],
                        ),
                  1, 1)
    fig.add_trace(go.Pie(labels=dff.index, values=dff[col1],
                         name='偵測數據分布',
                         marker_colors=c2
                        ),
                  1, 2)
    fig.update_layout(uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      hoverlabel=dict(font_size=15),
                      title_text=(str(year1)+'/1/1~'+str(year2)+'/12/31: Data Distribution of '+str(wardname))
                     )
    return fig

##############################################################################################

# 篩選器: 護理站/科別分布
@app.callback(
    Output('ward-graph', 'figure'), 
    Input('ward-year-dropdown', 'value'),
    Input('Ward-boolean-switch', 'on'),
    Input('avg-boolean-switch', 'on'),
    Input('draw-boolean-switch', 'on'),
)
def update_graph(year, on, avg, draw):
    if year is None:
        year = ydf['Year'].max()
    else:
        pass
    
    if on:
        name = 'Division'
        df, col1, col2, col3, col4 = RRTDivNum(year, avg)
    else:
        name = 'Ward'
        df, col1, col2, col3, col4 = RRTWardNum(year, avg)

    if draw:
        bar = 'group'
    else:
        bar = 'stack'

    data = [go.Bar(name=col1, x=df.index, y=df[col1], marker_color='green'),
            go.Bar(name=col2, x=df.index, y=df[col2], marker_color='yellow'),
            go.Bar(name=col3, x=df.index, y=df[col3], marker_color='#ff9d00'),
            go.Bar(name=col4, x=df.index, y=df[col4], marker_color='red'),
           ]
    fig = go.Figure(data=data)
    fig.update_layout(title_text=(str(year)+': Data Distribution of '+str(name)),
                      barmode=bar,
                      hovermode='x unified',
                      hoverlabel=dict(font_size=15,
                                     ),
                      modebar_remove=['resetscale', 'lasso'],
                     )
    return fig

##############################################################################################

# 篩選器: RRT匹配比例
@app.callback(
    Output('Match-graph', 'figure'),
    Input('Match-year-dropdown', 'value'),
)
def update_graph_RRT(year):
    if year is None:
        year = '%'
        year1 = mydf['Year'].min()
        year2 = mydf['Year'].max()
        df, col = MatchNum(year)
    else:
        year1 = year
        year2 = year
        df, col = MatchNum(year)

    c = []
    for i in range(len(df)):
        if df.index[i] == 'Match':
            c.append('green')
        elif df.index[i] == 'Discrepancy':
            c.append('red')
        else:
            pass
            
    data = [go.Pie(labels=df.index, values=df[col],
                   name='RRT匹配比例',
                   marker_colors=c,
                  ),
           ]
    fig = go.Figure(data=data)
    fig.update_layout(uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      hoverlabel=dict(font_size=15),
                      title_text=(str(year1)+'~'+str(year2)+': Percentage of RRTRecord')
                     )
    return fig

##############################################################################################

# 篩選器: RRT匹配分布
@app.callback(
    Output('Match-bar-graph', 'figure'),
    Input('Match-year-dropdown', 'value'),
    Input('Match-draw-boolean-switch', 'on'),
)
def update_graph_RRT(year, on):
    if year is None:
        year = '%'
        year1 = mydf['Year'].min()
        year2 = mydf['Year'].max()
        df, col1, col2, col3, col4 = MatchDiffNum(year)
    else:
        year1 = year
        year2 = year
        df, col1, col2, col3, col4 = MatchDiffNum(year)
        
    if on:
        bar = 'group'
    else:
        bar = 'stack'

    data = [go.Bar(name=col1, x=df.index, y=df[col1], marker_color='green'),
            go.Bar(name=col2, x=df.index, y=df[col2], marker_color='yellow'),
            go.Bar(name=col3, x=df.index, y=df[col3], marker_color='#ff9d00'),
            go.Bar(name=col4, x=df.index, y=df[col4], marker_color='red'),
           ]
    fig = go.Figure(data=data)
    fig.update_layout(title_text=(str(year1)+'~'+str(year2)+': Duration Between Nursing Date and RRT Date (Minute Unit)'),
                      hovermode='x unified',
                      barmode=bar,
                      hoverlabel=dict(font_size=15,
                                     ),
                      modebar_remove=['resetscale', 'lasso'],
                     )
    fig.update_xaxes(rangeslider_visible=True)
    return fig

##############################################################################################

# 篩選器: HIS RRT病程分布
@app.callback(
    Output('RRTType-graph', 'figure'), 
    Input('RRTType-year-dropdown', 'value'),
    Input('RRTType-age-boolean-switch', 'on'),
)
def update_graph(year, on):
    if year is None:
        year = unydf['Year'].max()
    else:
        pass
    
    df, col1, col2, col3 = RRTTransferType(year, on)

    fig = px.bar(df, x=df.index, y=col3, hover_data=[col1, col2])
    fig.update_traces(text=df[col3],
                      textposition='auto',
                      textfont_size=15,
                      selector=dict(type='bar'),
                     )
    fig.update_layout(hovermode='x unified',
                      hoverlabel=dict(font_size=15),
                      modebar_remove=['resetscale', 'lasso'],
                     )
    return fig

##############################################################################################

# 篩選器: 不可預期ICURRT
@app.callback(
    Output('ICURRT-graph', 'figure'),
    Input('ICURRT-year-dropdown', 'value'),
)
def update_graph_RRT(year):
    if year is None:
        year1 = unydf['Year'].min()
        year2 = unydf['Year'].max()
        title = str(year1)+'~'+str(year2)
    else:
        year1 = year
        year2 = year
        title = str(year)
    
    df1, col11, col12, col13 = RRTTransferNum(year)
    df2, col21, col22, col23 = RRTTransferNullNum(year)

    c1 = []
    for i in range(len(df1)):
        if df1.index[i]=='other':
            c1.append('#adadad')
        else:
            c1.append('#05b511')
    
    c2 = []
    for i in range(len(df2)):
        if df2.index[i]=='Match':
            c2.append('green')
        elif df2.index[i]=='Miss':
            c2.append('red')
        else:
            pass
    
    if year is None:
        text = [col11+': '+str(df1[col11][0])+', '+col12+': '+str(df1[col12][0])
                ]
    else:
        text = [col11+': '+str(df1[col11][0])+', '+col12+': '+str(df1[col12][0]),
                col11+': '+str(df1[col11][1])+', '+col12+': '+str(df1[col12][1])
                ]
        
    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                       )
    fig.add_trace(go.Pie(labels=df1.index, values=df1[col13],
                         name='不可預期數據之分布',
                         marker_colors=c1,
                         hovertext=text,
                        ),
                  1, 1)
    fig.add_trace(go.Pie(labels=df2.index, values=df2[col23],
                         name='不可預期數據之偵測分布',
                         marker_colors=c2,
                         hovertext=[col21+': '+str(df2[col21][0])+', '+col22+': '+str(df2[col22][0]),
                                    col21+': '+str(df2[col21][1])+', '+col22+': '+str(df2[col22][1])
                                   ],
                        ),
                  1, 2)
    fig.update_layout(uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      hoverlabel=dict(font_size=15),
                      title_text=(title+': 不可預期進ICU患者之RRT偵測數據分布')
                     )
    return fig

##############################################################################################

# 篩選器: 不可預期ICURRT 判斷Error
@app.callback(
    Output('ICURRT2-graph', 'figure'),
    Input('ICURRT-year-dropdown', 'value'),
)
def update_graph_RRT(year):
    if year is None:
        year = '%'
        year1 = unydf['Year'].min()
        year2 = unydf['Year'].max()
        title = str(year1)+'~'+str(year2)
    else:
        year1 = year
        year2 = year
        title = str(year)
    
    df1, col11, col12, col13 = RRTTransferEndMiss(year)
    df2, col21, col22, col23 = RRTTransferEndType(year)

    c1 = []
    for i in range(len(df1)):
        if df1.index[i]=='Fail':
            c1.append('#ff2626')
        elif df1.index[i]=='Success':
            c1.append('#05b511')
        else:
            pass
    
    c2 = []
    for i in range(len(df2)):
        if df2.index[i]=='RRT到場處理':
            c2.append('green')
        elif df2.index[i]=='MEWS警示但未呼叫RRT':
            c2.append('#ffdd00')
        elif df2.index[i]=='未啟動':
            c2.append('red')
        elif df2.index[i]=='空值':
            c2.append('#adadad')
        else:
            pass
    
    if len(df2.index)==2:
        text = [col21+': '+str(df2[col21][0])+', '+col22+': '+str(df2[col22][0]),
                col21+': '+str(df2[col21][1])+', '+col22+': '+str(df2[col22][1])
                ]
    elif len(df2.index)==3:
        text = [col21+': '+str(df2[col21][0])+', '+col22+': '+str(df2[col22][0]),
                col21+': '+str(df2[col21][1])+', '+col22+': '+str(df2[col22][1]),
                col21+': '+str(df2[col21][2])+', '+col22+': '+str(df2[col22][2])
                ]
    elif len(df2.index)==4:
        text = [col21+': '+str(df2[col21][0])+', '+col22+': '+str(df2[col22][0]),
                col21+': '+str(df2[col21][1])+', '+col22+': '+str(df2[col22][1]),
                col21+': '+str(df2[col21][2])+', '+col22+': '+str(df2[col22][2]),
                col21+': '+str(df2[col21][3])+', '+col22+': '+str(df2[col22][3])
                ]
    else:
        pass
        
    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                       )
    fig.add_trace(go.Pie(labels=df1.index, values=df1[col13],
                         name='RRT偵測成功率分布',
                         marker_colors=c1,
                         hovertext=[col11+': '+str(df1[col11][0])+', '+col12+': '+str(df1[col12][0]),
                                    col11+': '+str(df1[col11][1])+', '+col12+': '+str(df1[col12][1]),
                                   ],
                        ),
                  1, 1)
    fig.add_trace(go.Pie(labels=df2.index, values=df2[col23],
                         name='RRT處理結果',
                         marker_colors=c2,
                         hovertext=text,
                        ),
                  1, 2)
    fig.update_layout(uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      hoverlabel=dict(font_size=15),
                      title_text=(title+': 不可預期進ICU患者之HisRRT偵測失誤比例 (Conditional Exclusion: DNR)')
                     )
    return fig
