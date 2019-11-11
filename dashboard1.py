import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from datetime import date,timedelta
from datetime import datetime as dt
import plotly.express as px
import pyodbc
import flask
import time
import numpy as np
import pandas.io.sql as psql
from dash.dependencies import Output,Input
suppress_callback_exceptions=True

dashboard = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css",dbc.themes.BOOTSTRAP,'https://stackpath.bootstrapcdn.com/bootswatch/4.3.1/darkly/bootstrap.min.css'])
dashboard.css.config.serve_locally = True
navbar= dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="assets/sales-icon-15.png", height="50px")),
                    dbc.Col(dbc.NavbarBrand("Dashboard", className="navbar-brand",style={'font-size':'40px'})),
                ],

                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        html.Div(dcc.Link('Offline',className='nav-link',style={'font-size':'18px','hover':dict(color='white')},href='/offline'),className='nav-item active'),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],

    color="#214161",
    dark=True,
    sticky='top',
)
navbar_offline= dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="assets/sales-icon-15.png", height="50px")),
                    dbc.Col(dbc.NavbarBrand("Dashboard", className="navbar-brand",style={'font-size':'40px'})),
                ],

                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        html.Div(dcc.Link('Live',className='nav-link',style={'font-size':'18px'},href='/'),className='nav-item active'),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="#214161",
    dark=True,
    sticky='top',
)


index=html.Div([
    html.Div([navbar]),
        html.Div([
        html.Div([
        html.Div([
            dcc.Graph(
                id="graph1",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True
                    },
                    "easing": "elastic"
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                }

            ),
            dcc.Interval(id='update1',
                         interval=1 * 10000,
                         n_intervals=0
                         )
        ], className='jumbotron'),
        ], className="six columns"),

        html.Div([
        html.Div([
                    dcc.Graph(
                        id="graph2",
                        animate=True,
                        animation_options={
                            "frame":{
                                "redraw":True
                            },
                            "easing":"elastic"
                        },

                        config={
                            "editable":True,
                            "edits":{
                                "shapePosition":True
                            }
                         },


                    ),
            dcc.Interval(id='update2',
                         interval=1*100000,
                         n_intervals=0
                         )
        ],className='jumbotron'),
        ], className="six columns"),


    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                        dcc.Graph(
                            id="graph4",
                            animate=True,
                            animation_options={
                                "frame":{
                                    "redraw":True,

                                },
                            },

                            config={
                                "editable":True,
                                "edits":{
                                    "shapePosition":True
                                }
                             },


                        ),
                dcc.Interval(id='map-update',
                             interval=1*100000,
                             n_intervals=0
                             ),
                html.P(id='rider_amount'),
                ],className='jumbotron'),

            ], className="twelve columns"),
    ],className='row'),

    html.Div([
        html.Div([
            html.Div([
            dcc.Graph(
                id="graph3",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True,

                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            ),
            dcc.Interval(id='update3',
                         interval=1 * 100000,
                         n_intervals=0
                         )
                ],className='jumbotron'),

        ], className="six columns"),
        html.Div([
            html.Div([

                dcc.Graph(
                    id="graph5",
                    animate=True,
                    animation_options={
                        "frame": {
                            "redraw": True
                        },
                        "easing": "elastic"
                    },

                    config={
                        "editable": True,
                        "edits": {
                            "shapePosition": True
                        }
                    },

                ),
                dcc.Interval(id='update4',
                             interval=1 * 100000,
                             n_intervals=0
                             )
            ], className='jumbotron'),
        ], className="six columns"),
    ], className='row'),

html.Div([
        html.Div([
            html.Div([
            dcc.Graph(
                id="graph6",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True,

                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            ),
            dcc.Interval(id='update_order',
                         interval=1 * 100000,
                         n_intervals=0
                         )
                ],className='jumbotron'),

        ], className="six columns"),

    html.Div([
        html.Div([
            dcc.Graph(
                id="graph7",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True,

                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            ),
            dcc.Interval(id='update_rider_number',
                         interval=1 * 100000,
                         n_intervals=0
                         )
        ], className='jumbotron'),

    ],className="six columns"),

    ], className='row'),


],style={"backgroundColor":"#222"})

url_bar_and_content_div=html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

offline_page = html.Div([
    html.Div([navbar_offline]),
    html.Div([
        html.Div([
            html.Div([
                dcc.Loading(id="loading-icon",
                            children=[   dcc.Graph(
                id="graph-off1",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True
                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                }

            )], type="default"),
            dcc.DatePickerRange(id='date-picker1',minimum_nights=0,start_date=date.today()-timedelta(days=1),end_date=date.today()-timedelta(days=1),
                                clearable=True,style={"background-color":"#333"}),



            html.Div(id='output-date1')
                ],className='jumbotron'),
        ],className="six columns"),
        html.Div([
            html.Div([
                dcc.Loading(id="loading-icon",
                            children=[     dcc.Graph(
                id="graph-off2",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True,
                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            )], type="default"),

dcc.DatePickerRange(id='date-picker2',minimum_nights=0,start_date=date.today()-timedelta(days=1),end_date=date.today()-timedelta(days=1),
                    clearable=True),
            html.Div(id='output-date2')
            ],className='jumbotron'),
        ], className="six columns"),
    ], className="row"),
    html.Div([

        html.Div([
            html.Div([
            dcc.DatePickerSingle(id='date-picker4',date=date.today()-timedelta(days=1),clearable=True),
            html.Div(id='output-date4'),
                dcc.Loading(id="loading-icon",
                            children=[  dcc.Graph(
                id="graph-off4",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True
                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            )], type="default"),

                ],className='jumbotron'),

        ], style={"backgroundColor": "black"}, className="twelve columns"),
    ], className='row'),
    html.Div([
        html.Div([
        html.Div([
            dcc.Loading(id="loading-icon",
                        children=[dcc.Graph(
                            id="graph-off3",
                            animate=True,
                            animation_options={
                                "frame": {
                                    "redraw": True
                                },
                            },

                            config={
                                "editable": True,
                                "edits": {
                                    "shapePosition": True
                                }
                            }

                        )], type="default"),
            dcc.DatePickerRange(id='date-picker3', minimum_nights=0, start_date=date.today() - timedelta(days=1),
                                end_date=date.today() - timedelta(days=1),
                                clearable=True, style={"background-color": "#333"}),

            html.Div(id='output-date3')
            ], className='jumbotron'),
        ], className='six columns'),

        html.Div([
            html.Div([
                dcc.Loading(id="loading-icon",
                            children=[dcc.Graph(
                                id="graph-off5",
                                animate=True,
                                animation_options={
                                    "frame": {
                                        "redraw": True
                                    },
                                },

                                config={
                                    "editable": True,
                                    "edits": {
                                        "shapePosition": True
                                    }
                                },

                            )], type="default"),
                dcc.Interval(id='update5',
                             interval=1 * 100000,
                             n_intervals=0
                             )

            ], className='jumbotron'),
        ], className="six columns"),
    ], className="row"),
    html.Div([
  html.Div([
            html.Div([
                dcc.Loading(id="loading-icon",
                            children=[     dcc.Graph(
                id="graph-number-order-hour",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True,
                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            )], type="default"),

dcc.DatePickerRange(id='date-picker-number-order-hour',minimum_nights=0,start_date=date.today()-timedelta(days=1),end_date=date.today()-timedelta(days=1),
                    clearable=True),
            html.Div(id='output-number-order-hour')
            ],className='jumbotron'),
        ], className="six columns"),

html.Div([
            html.Div([
                dcc.Loading(id="loading-icon",
                            children=[dcc.Graph(
                id="graph-number-rider-hour",
                animate=True,
                animation_options={
                    "frame": {
                        "redraw": True,
                    },
                },

                config={
                    "editable": True,
                    "edits": {
                        "shapePosition": True
                    }
                },

            )], type="default"),

dcc.DatePickerSingle(id='date-picker-number-rider-hour',date=date.today()-timedelta(days=1),clearable=True),
            html.Div(id='output-number-rider-hour')
            ],className='jumbotron'),
        ], className="six columns"),



    ],className='row')
],style={'backgroundColor':'#222'})

def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        index,
        offline_page,
    ],style={'backgroundColor':'black'})

dashboard.layout = serve_layout
@dashboard.callback(dash.dependencies.Output('graph-off1','figure'),
                    [dash.dependencies.Input('date-picker1','start_date'),
                     dash.dependencies.Input('date-picker1','end_date')])
def select_date_order(start_date,end_date):
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
    set nocount on;
     USE [db_delivereat_G2]
    

    DECLARE	@return_value int
    DECLARE	@current_date date = convert(date,SYSDATETIME())
    create table #tmp(
    year int,
    month varchar(100),
    state varchar(100),
    area_id int,
    zone varchar(100),
    sales float,
    commision float,
    GMV float,
    revenue float,
    number_of_order int,
    late_order int,
    late_order_percentage varchar(100)
    
    )
    
    insert into #tmp
    
    EXEC	@return_value = [dbo].[sp_report]
    		@action =?,
    		@restaurant_id = ?,
    		@date_from =?,
    		@date_to =?,
    		@zone_id = ?,
    		@state = ?
    select * from #tmp
    '''
    cursor=conn.cursor()
    values=('k',0,start_date,end_date,0,'- All States -')
    cursor.execute(sql,values)
    df = pd.DataFrame.from_records(cursor.fetchall(),columns=[desc[0] for desc in cursor.description])
    trace_bar = go.Bar(x=list(df.zone), y=list(df.number_of_order), name='order_id', marker_color=list(df.number_of_order))
    layout = go.Layout(

        title="Number of order ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='Number of Order',range=[min(df.number_of_order),max(df.number_of_order)]),
        xaxis=dict(title='Zone',tickmode='linear'),
        font={
            "color": "#7FDBFF"
        },
        autosize=True
    )
    data.append(trace_bar)
    return {"data": data, "layout": layout}


@dashboard.callback(dash.dependencies.Output('graph-off2', 'figure'),
                    [dash.dependencies.Input('date-picker2', 'start_date'),
                     dash.dependencies.Input('date-picker2', 'end_date')])
def select_date_GMV(start_date, end_date):
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
    set nocount on;
     USE [db_delivereat_G2]


    DECLARE	@return_value int
    DECLARE	@current_date date = convert(date,SYSDATETIME())
    create table #tmp(
    year int,
    month varchar(100),
    state varchar(100),
    area_id int,
    zone varchar(100),
    sales float,
    commision float,
    GMV float,
    revenue float,
    number_of_order int,
    late_order int,
    late_order_percentage varchar(100)

    )

    insert into #tmp

    EXEC	@return_value = [dbo].[sp_report]
    		@action =?,
    		@restaurant_id = ?,
    		@date_from =?,
    		@date_to =?,
    		@zone_id = ?,
    		@state = ?
    select * from #tmp
    '''
    cursor = conn.cursor()
    values = ('k', 0, start_date, end_date, 0, '- All States -')
    cursor.execute(sql, values)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    trace_bar = go.Bar(x=list(df.zone), y=list(df.GMV), name='order_id',
                       marker_color=list(df.number_of_order))
    layout = go.Layout(

        title="GMV ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='GMV(RM)',range=[min(df.GMV),max(df.GMV)]),
        xaxis=dict(title='Zone',tickmode='linear'),
        font={
            "color": "#7FDBFF"
        },
        autosize=True
    )
    data.append(trace_bar)
    return {"data": data, "layout": layout}


@dashboard.callback(dash.dependencies.Output('graph-off3', 'figure'),
                    [dash.dependencies.Input('date-picker3', 'start_date'),
                     dash.dependencies.Input('date-picker3', 'end_date')])
def select_date_late(start_date, end_date):
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
    set nocount on;
     USE [db_delivereat_G2]


    DECLARE	@return_value int
    DECLARE	@current_date date = convert(date,SYSDATETIME())
    create table #tmp(
    year int,
    month varchar(100),
    state varchar(100),
    area_id int,
    zone varchar(100),
    sales float,
    commission float,
    GMV float,
    revenue float,
    number_of_order int,
    late_order int,
    late_order_percentage varchar(100)

    )

    insert into #tmp

    EXEC	@return_value = [dbo].[sp_report]
    		@action =?,
    		@restaurant_id = ?,
    		@date_from =?,
    		@date_to =?,
    		@zone_id = ?,
    		@state = ?
    select * from #tmp
    '''
    cursor = conn.cursor()
    values = ('k', 0, start_date, end_date, 0, '- All States -')
    cursor.execute(sql, values)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    scatterpie = go.Pie(labels=list(df.zone), values=list(df.late_order))
    # trace_bar = go.Bar(x=list(df.zone), y=list(df.number_of_order), name='order_id',
    #                    marker_color=list(df.number_of_order))
    layout = go.Layout(

        title="Late Order",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
         # yaxis=dict(title='late order'),
         # xaxis=dict(title='Zone',tickmode='linear'),
        font={
            "color": "#7FDBFF"
        }
    )
    data.append(scatterpie)
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output('graph-off4', 'figure'),
                    [dash.dependencies.Input('date-picker4','date')])
def select_date_map(date):
    if date is not None:
        start_date = dt.strptime(date, '%Y-%m-%d')
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )


    query = '''
 set nocount on
 
select a.order_id,b.customer_id,b.longitude as long,b.latitude as lat,d.name as zone,e.order_no as no_order from tbl_order a with (nolock) inner join 
        tbl_customer b with (nolock) on a.customer_id = b.customer_id inner join 
        tbl_area_location c with (nolock) on b.postal_code =c.postal_code inner join 
        tbl_area d with (nolock) on c.area_id = d.area_id 
        inner join (select c.name as name ,count(c.name) as order_no from tbl_order a with (nolock) inner join 
        tbl_restaurant b with (nolock) on a.restaurant_id = b.restaurant_id inner join 
        tbl_area c with (nolock) on b.area_id = c.area_id where convert(date,(case when a.time_pickup='1753-01-01 00:00:00' then dateadd(hour,1, a.time_in) else a.time_pickup end)) = ?
        group by c.name) e on d.name = e.name 
		where  convert(date,(case when a.time_pickup='1753-01-01 00:00:00' then dateadd(hour,1, a.time_in) else a.time_pickup end))=? and a.status='C'

        
        '''
    mapbox_access_token = "pk.eyJ1IjoiamVmZnJleS1sZWFuIiwiYSI6ImNrMjV6NG5hYTAwZzYzZnJwbmY1OGQwd2kifQ.3MpZyi6tyV1pPSOJB8fpxQ"
    cursor = conn.cursor()
    cursor.execute(query, start_date,start_date)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    scattermapbox= go.Scattermapbox(lat=list(df.lat), lon=list(df.long), mode="markers", text=list(df.order_id),
                                      marker={'opacity': 0.5, 'size': 15, 'color': df['no_order'],
                                              'colorbar': dict(title='Number of Customer'),
                                              'colorscale': 'plasma'})
    layout = go.Layout(
        title='Order Location',
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=800,
        font={
            "color": "#7FDBFF"
        },
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            uirevision=True,
            # center={"lat":5.4164,"lon":100.3327
            #
            # },
            pitch=0,
            # zoom=10,
            style='dark'

        )
    )

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'mapbox.zoom': 11,
                           'mapbox.center.lon': '100.3327',
                           'mapbox.center.lat': '5.4164'}],
                    label='zoom',
                    method='relayout'
                )
            ]),
            direction='left',
            pad={'r': 10, 't': 10},
            showactive=True,
            type='buttons',
            x=0.1,
            xanchor='left',
            y=1,
            yanchor='top',
            bordercolor='#00FFFF'
        ),
    ])

    layout['updatemenus'] = updatemenus
    data.append(scattermapbox)
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output('graph-number-order-hour', 'figure'),
                    [dash.dependencies.Input('date-picker-number-order-hour', 'start_date'),
                     dash.dependencies.Input('date-picker-number-order-hour', 'end_date')])
def select_date_order_hour(start_date, end_date):
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
     set nocount on
     DECLARE @start date=?
     DECLARE @end date=?
	SELECT d.name as zone ,
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 10 THEN 1 ELSE 0 END) AS '10am',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 11 THEN 1 ELSE 0 END) AS '11am',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 12 THEN 1 ELSE 0 END) AS '12pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 13 THEN 1 ELSE 0 END) AS '1pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 14 THEN 1 ELSE 0 END) AS '2pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 15 THEN 1 ELSE 0 END) AS '3pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 16 THEN 1 ELSE 0 END) AS '4pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 17 THEN 1 ELSE 0 END) AS '5pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 18 THEN 1 ELSE 0 END) AS '6pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 19 THEN 1 ELSE 0 END) AS '7pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 20 THEN 1 ELSE 0 END) AS '8pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 21 THEN 1 ELSE 0 END) AS '9pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 22 THEN 1 ELSE 0 END) AS '10pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 23 THEN 1 ELSE 0 END) AS '11pm'
FROM  tbl_order a with (nolock)
inner join tbl_restaurant b with (nolock) on a.restaurant_id=b.restaurant_id 
inner join tbl_area c with (nolock) on b.area_id=c.area_id 
inner join tbl_area_zonegroup d on c.zonegroup=d.zone_id
where (((convert(date,time_pickup) between @start and @end )  OR (((convert(date,time_in) between @start and @end))
AND time_pickup='1753-01-01 00:00:00'))and a.status<>'X' and a.status<>'1')
GROUP BY d.name
ORDER BY d.name
    '''
    cursor = conn.cursor()
    values = (start_date, end_date)
    cursor.execute(sql, values)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    hour = ('10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm')
    for x in range(len(df.zone)):
        line = go.Scatter(x=hour, y=list(df.iloc[x, 1:15]), mode='lines', name=df['zone'].apply(str)[x])
        data.append(line)

    layout = go.Layout(

        title="Number of order each hour ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='Number of Order', autorange=True),
        xaxis=dict(title='time', autorange=True, tickmode='linear'),
        autosize=True,
        font={
            "color": "#7FDBFF"
        },
    )
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output('graph-number-rider-hour', 'figure'),
                    [dash.dependencies.Input('date-picker-number-rider-hour', 'date')])
def select_date_rider_hour(date):
    if date is not None:
        start_date = dt.strptime(date, '%Y-%m-%d')
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_on2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
      set nocount on
      declare @select_date date=?
	 create table #s
 (
 crew_id int, 
	updated_datetime datetime

 )
    insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=10) group by crew_id)
	 

 insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=11) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=12) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=13) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=14) group by crew_id)


	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=15) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=16) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=17) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=18) group by crew_id)
	
	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) =@select_date and (datepart(hour,updated_datetime)=19) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) = @select_date and (datepart(hour,updated_datetime)=20) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) =@select_date and (datepart(hour,updated_datetime)=21) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) =@select_date and (datepart(hour,updated_datetime)=22) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location
	 where convert(date,updated_datetime) =@select_date and (datepart(hour,updated_datetime)=23) group by crew_id)

	 SELECT c.name as zone ,
       SUM(case when datepart(hour,updated_datetime)= 10 THEN 1 ELSE 0 END) AS '10am',
	   SUM(case when datepart(hour,updated_datetime)= 11 THEN 1 ELSE 0 END) AS '11am',
	   SUM(case when datepart(hour,updated_datetime)= 12 THEN 1 ELSE 0 END) AS '12pm',
	   SUM(case when datepart(hour,updated_datetime)= 13 THEN 1 ELSE 0 END) AS '1pm',
	   SUM(case when datepart(hour,updated_datetime)= 14 THEN 1 ELSE 0 END) AS '2pm',
	   SUM(case when datepart(hour,updated_datetime)= 15 THEN 1 ELSE 0 END) AS '3pm',
	   SUM(case when datepart(hour,updated_datetime)= 16 THEN 1 ELSE 0 END) AS '4pm',
	   SUM(case when datepart(hour,updated_datetime)= 17 THEN 1 ELSE 0 END) AS '5pm',
	   SUM(case when datepart(hour,updated_datetime)= 18 THEN 1 ELSE 0 END) AS '6pm',
	   SUM(case when datepart(hour,updated_datetime)= 19 THEN 1 ELSE 0 END) AS '7pm',
	   SUM(case when datepart(hour,updated_datetime)= 20 THEN 1 ELSE 0 END) AS '8pm',
	   SUM(case when datepart(hour,updated_datetime)= 21 THEN 1 ELSE 0 END) AS '9pm',
	   SUM(case when datepart(hour,updated_datetime)= 22 THEN 1 ELSE 0 END) AS '10pm',
	   SUM(case when datepart(hour,updated_datetime)= 23 THEN 1 ELSE 0 END) AS '11pm'
      
FROM  #s a with (nolock)
inner join tbl_delivery_crew b with (nolock) on a.crew_id=b.crew_id
inner join db_delivereat_G2.dbo.tbl_area_zonegroup c with (nolock) on b.delivery_team_id=c.zone_id
GROUP BY c.name
ORDER BY c.name
    '''
    cursor = conn.cursor()
    values = (start_date)
    cursor.execute(sql, values)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    hour = ('10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm')
    for x in range(len(df.zone)):
        line = go.Scatter(x=hour, y=list(df.iloc[x, 1:15]), mode='lines', name=df['zone'].apply(str)[x])
        data.append(line)

    layout = go.Layout(

        title="Number of rider each hour ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='Number of rider', autorange=True),
        xaxis=dict(title='time', autorange=True, tickmode='linear'),
        autosize=True,
        font={
            "color": "#7FDBFF"
        },
    )
    return {"data": data, "layout": layout}


@dashboard.callback(dash.dependencies.Output('page-content','children'),
                    [dash.dependencies.Input('url','pathname')])
def display_page(pathname):
    if pathname == '/offline':
        return offline_page
    else:
        return index


@dashboard.callback(dash.dependencies.Output("graph1","figure"),
                    [dash.dependencies.Input("update1","n_intervals")])
def update_bar_order(self):
    data=[]
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1533;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    conn2 = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1533;'
                          'Database=db_delivereat_on2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    query=pd.read_sql_query('''
    select d.name,count(order_id) as number_of_order from tbl_order a with (nolock) inner join tbl_restaurant b with (nolock) on a.restaurant_id=b.restaurant_id
inner join tbl_area c with (nolock) on b.area_id=c.area_id
inner join tbl_area_zonegroup d with (nolock) on c.zonegroup=d.zone_id where
((convert(date, time_pickup) BETWEEN convert(date,SYSDATETIME()) AND convert(date,sysdatetime())) 
OR ((convert(date,time_in) BETWEEN convert(date,SYSDATETIME()) AND convert(date,SYSDATETIME())) AND time_pickup='1753-01-01 00:00:00'))
and a.status not in ('c','x','1')
group by d.name
    ''',conn)
    query2=pd.read_sql_query('''
    set nocount on
	create table #S
		(
			crew_id int,
			crew_name varchar(200),
			isLogin bit,
			updated_datetime datetime,
			jobStatus varchar(2),
			jobStatusSeq int,
			zone_id int,
			state varchar(20),
			is_break bit,
			is_block bit,
			isHalal bit,
			is_working bit
		)
	
		--get current job status
		create table #tempS
		(
			crew_id int,
			status varchar(2),
			statusSeq int
		)

		insert into #tempS 
		select distinct crew_id, a.status, 6 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'N'

		insert into #tempS 
		select distinct crew_id, a.status, 5 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'P' and crew_id not in (select crew_id from #tempS)
		
		insert into #tempS 
		select distinct crew_id, a.status, 4 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'R' and crew_id not in (select crew_id from #tempS)

		insert into #tempS 
		select distinct crew_id, a.status, 3 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D1' and crew_id not in (select crew_id from #tempS)

		insert into #tempS 
		select distinct crew_id, a.status, 2 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D2' and crew_id not in (select crew_id from #tempS)
		
		insert into #tempS 
		select distinct crew_id, a.status, 1 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D3' and crew_id not in (select crew_id from #tempS)

		INSERT INTO #S	
		SELECT a.crew_id, first_name + ', ' + last_name as crew_name,
		(select case when count(*) >= 1 then 1 else 0 end from tbl_token_d with (nolock) where crew_id = a.crew_id 
		and created_datetime < GETDATE() and (closed_datetime > GETDATE() or closed_datetime is null)) as isLogin,
		IsNUll(b.LatestTime, '1900-01-01 00:00:00.000') as updated_datetime, IsNull(c.status, '') as jobStatus, IsNull(c.statusSeq, 0) as jobStatusSeq,
		a.delivery_team_id as zone_id, area.state, 
		(SELECT CASE WHEN count(*) > 0  THEN 1 ELSE 0 END FROM tbl_delivery_crew_break with (nolock) WHERE crew_id = a.crew_id
		AND datetime_break BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) AND is_break = 1) as is_break,
		(SELECT CASE WHEN count(*) > 0  THEN 1 ELSE 0 END FROM tbl_delivery_crew_block_order with (nolock) WHERE crew_id = a.crew_id
		AND time_block BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) AND is_block = 1 ) as is_block,
		a.is_halal as isHalal, a.is_working
		FROM tbl_delivery_crew a with (nolock)
		left join (select MAX(updated_datetime) as LatestTime, crew_id from tbl_delivery_crew_location with (nolock)
		group by crew_id) b on  a.crew_id = b.crew_id 
		left join db_delivereat_G2.dbo.tbl_area area with (nolock) on a.delivery_team_id = area.zonegroup
		left join (select * from #tempS ) c on a.crew_id = c.crew_id
		WHERE a.status = 'A'
		
		SELECT #S.*, a.latitude as lat, a.longitude as lng INTO #S1 from #S with (nolock) left join tbl_delivery_crew_location a with (nolock) on #S.crew_id = a.crew_id and #S.updated_datetime = a.updated_datetime
				
		SELECT c.name,count(distinct a.crew_id) as number_of_rider FROM #S1 a with (nolock) inner join tbl_delivery_crew b with (nolock) on a.crew_id=b.crew_id
		inner join db_delivereat_G2.dbo.tbl_area_zonegroup c with (nolock) on b.delivery_team_id=c.zone_id
		WHERE (a.is_working = 1) and (isLogin=1) OR (a.is_working = CASE WHEN jobStatusSeq <> 0 THEN 0 END)
		group by (c.name)
    ''',conn2)

    df = pd.DataFrame(query)
    df2=pd.DataFrame(query2)
    trace_bar = go.Bar(x=list(df.name), y=list(df.number_of_order), name='number_of_order', marker_color='#007bff')
    trace_bar2 = go.Bar(x=list(df2.name), y=list(df2.number_of_rider), name='number_of_rider', marker_color='yellow')
    layout = go.Layout(

                title="Number of order ",
                plot_bgcolor= "#111111",
                paper_bgcolor= "#111111",
                yaxis=dict(title='Number of Order/Riders',autorange=True),
                xaxis=dict(title='Zone',autorange=True,tickmode='linear'),
                autosize=True,
                font= {
                    "color": "#7FDBFF"
                },
        barmode='group'
    )
    data.append(trace_bar)
    data.append(trace_bar2)
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output("graph2","figure"),
                    [dash.dependencies.Input("update2","n_intervals")])
def update_bar_GMV(self):
    data=[]
    conn = pyodbc.connect('Driver={SQL Server};'
                           'Server=43.252.214.228,1533;'
                           'Database=db_delivereat_G2;'
                           'UID=weifong;'
                           'PWD=123.123;'
                           )
    cursor=conn.cursor()
    query=pd.read_sql_query('set nocount on '
                            ' DECLARE @return_value int '
                            ' DECLARE @current_date date = convert(date,SYSDATETIME()) '
                            'create table #tmp( year int,month varchar(100),state varchar(100),area_id int,zone varchar(100),sales float,commission float, '
                            'GMV float,revenue float,number_of_order int,late_order int,late_order_percentage varchar(100)) '
                            'insert into #tmp EXEC	@return_value = [dbo].[sp_report] @action = N\'k\',@restaurant_id = 0,@date_from = @current_date, '
                            '@date_to = @current_date,@zone_id = 0,@state =\'- All States -\''
                            ''
                            ' SELECT * from #tmp',conn)
    df = pd.DataFrame(query)


    scatterbar= go.Bar(x=list(df.zone), y=list(df.GMV),name='GMV',marker_color=list(df.GMV))

    layout = go.Layout(

        title="GMV ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='GMV(RM)',autorange=True),
        xaxis=dict(title='Zone',autorange=True,tickmode='linear'),
        autosize=True,
        font={
            "color": "#7FDBFF"
        }
    )


    data.append(scatterbar)
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output("graph3","figure"),
                    [dash.dependencies.Input("update3","n_intervals")])
def update_late(self):
    data=[]
    conn = pyodbc.connect('Driver={SQL Server};'
                           'Server=43.252.214.228,1533;'
                           'Database=db_delivereat_G2;'
                           'UID=weifong;'
                           'PWD=123.123;'
                           )

    query=pd.read_sql_query('set nocount on '
                            ' DECLARE @return_value int '
                            ' DECLARE @current_date date = convert(date,SYSDATETIME()) '
                            'create table #tmp( year int,month varchar(100),state varchar(100),area_id int,zone varchar(100),sales float,commission float,'
                            'GMV float,revenue float,number_of_order int,late_order int,late_order_percentage varchar(100)) '
                            'insert into #tmp EXEC	@return_value = [dbo].[sp_report] @action = N\'k\',@restaurant_id = 0,@date_from = @current_date, '
                            '@date_to = @current_date,@zone_id = 0,@state =\'- All States -\''
                            ''
                            ' SELECT * from #tmp',conn)
    # values=('k',0,date.today(),date.today(),0,'- All States -')
    # cursor.execute(sql,values)
    # val=cursor.fetchval()
    # print(val)
    df = pd.DataFrame(query)


    scatterpie= go.Pie(labels=list(df.zone),values=list(df.late_order))
    #scatterbar = go.Bar(x=list(df2.zone), y=list(df2.late_order), name='late_order', marker_color=list(df2.late_order))

    layout = go.Layout(

        title="Later Order",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        # yaxis=dict(title='late order', autorange=True),
        # xaxis=dict(title='Zone', autorange=True,tickmode='linear'),
        autosize=True,
        font={
            "color": "#7FDBFF"
        }
    )


    data.append(scatterpie)
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output("graph4","figure"),
                    [dash.dependencies.Input("map-update","n_intervals")])

def update_map(self):
    conn = pyodbc.connect('Driver={SQL Server};'
                           'Server=43.252.214.228,1533;'
                           'Database=db_delivereat_on2;'
                           'UID=weifong;'
                           'PWD=123.123;'
                           )
    query_map = pd.read_sql_query('''
    set nocount on
    create table #S
		(
			crew_id int,
			crew_name varchar(200),
			isLogin bit,
			updated_datetime datetime,
			jobStatus varchar(2),
			jobStatusSeq int,
			zone_id int,
			state varchar(20),
			is_break bit,
			is_block bit,
			isHalal bit,
			is_working bit
		)
	
		--get current job status
		create table #tempS
		(
			crew_id int,
			status varchar(2),
			statusSeq int
		)

		insert into #tempS 
		select distinct crew_id, a.status, 6 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'N'

		insert into #tempS 
		select distinct crew_id, a.status, 5 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'P' and crew_id not in (select crew_id from #tempS)
		
		insert into #tempS 
		select distinct crew_id, a.status, 4 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'R' and crew_id not in (select crew_id from #tempS)

		insert into #tempS 
		select distinct crew_id, a.status, 3 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D1' and crew_id not in (select crew_id from #tempS)

		insert into #tempS 
		select distinct crew_id, a.status, 2 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D2' and crew_id not in (select crew_id from #tempS)
		
		insert into #tempS 
		select distinct crew_id, a.status, 1 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D3' and crew_id not in (select crew_id from #tempS)

		INSERT INTO #S	
		SELECT a.crew_id, first_name + ', ' + last_name as crew_name,
		(select case when count(*) >= 1 then 1 else 0 end from tbl_token_d with (nolock) where crew_id = a.crew_id 
		and created_datetime < GETDATE() and (closed_datetime > GETDATE() or closed_datetime is null)) as isLogin,
		IsNUll(b.LatestTime, '1900-01-01 00:00:00.000') as updated_datetime, IsNull(c.status, '') as jobStatus, IsNull(c.statusSeq, 0) as jobStatusSeq,
		a.delivery_team_id as zone_id, area.state, 
		(SELECT CASE WHEN count(*) > 0  THEN 1 ELSE 0 END FROM tbl_delivery_crew_break with (nolock) WHERE crew_id = a.crew_id
		AND datetime_break BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) AND is_break = 1) as is_break,
		(SELECT CASE WHEN count(*) > 0  THEN 1 ELSE 0 END FROM tbl_delivery_crew_block_order with (nolock) WHERE crew_id = a.crew_id
		AND time_block BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) AND is_block = 1 ) as is_block,
		a.is_halal as isHalal, a.is_working
		FROM tbl_delivery_crew a with (nolock)
		left join (select MAX(updated_datetime) as LatestTime, crew_id from tbl_delivery_crew_location with (nolock)
		group by crew_id) b on  a.crew_id = b.crew_id 
		left join db_delivereat_G2.dbo.tbl_area area with (nolock) on a.delivery_team_id = area.zonegroup
		left join (select * from #tempS ) c on a.crew_id = c.crew_id
		WHERE a.status = 'A'
		
		SELECT #S.*, a.latitude as lat, a.longitude as lng INTO #S1 from #S with (nolock) left join tbl_delivery_crew_location a with (nolock) on #S.crew_id = a.crew_id and #S.updated_datetime = a.updated_datetime
				
		SELECT DISTINCT crew_id, crew_name,isLogin,updated_datetime, jobStatus, jobStatusSeq, zone_id, state, lat, lng, is_break, is_block, isHalal, is_working FROM #S1 with (nolock)
		WHERE (isLogin = 1) and (is_working=1) OR (is_working = CASE WHEN jobStatusSeq <> 0 THEN 0 END)  ORDER BY isLogin desc, jobStatusSeq, crew_name, is_break, is_block ;
    
    ''',conn)
    df = pd.DataFrame(query_map)
    df_gotjob=df[~df['jobStatus'].isin([''])]
    df_nojob=df[df['jobStatus'].isin([''])]
    mapbox_access_token = "pk.eyJ1IjoiamVmZnJleS1sZWFuIiwiYSI6ImNrMjJxcXFkYzF4ODUzY3BpbXY2MjR5aTYifQ.dbh14TzvagiNsksJobeK1Q"
    rider_gotjob = go.Scattermapbox(lat=list(df_gotjob.lat), lon=list(df_gotjob.lng), mode="markers", text=list(df_gotjob.crew_name),marker={'size':8,'color':'red'},legendgroup='active rider',
                                    name='active rider',showlegend=True)
    rider_nojob= go.Scattermapbox(lat=list(df_nojob.lat), lon=list(df_nojob.lng), mode="markers",
                                     text=list(df_nojob.crew_name), marker={'size': 8, 'color': 'green'},legendgroup='free rider',name='free rider',
                                  showlegend=True)

    data=[]
    query=pd.read_sql_query('''
select a.order_id,b.customer_id,b.longitude as long,b.latitude as lat,d.name as zone,e.order_no as no_order,b.longitude as rest_long,b.latitude as rest_lat,a.is_retrieved from tbl_order a with (nolock) inner join 
        db_delivereat_G2.dbo.tbl_customer b with (nolock) on a.customer_id = b.customer_id inner join 
        db_delivereat_G2.dbo.tbl_area_location c with (nolock) on b.postal_code =c.postal_code inner join 
        db_delivereat_G2.dbo.tbl_area d with (nolock) on c.area_id = d.area_id 
        inner join (select c.name as name ,count(c.name) as order_no from tbl_order a with (nolock) inner join 
        db_delivereat_G2.dbo.tbl_restaurant b with (nolock) on a.restaurant_id = b.restaurant_id inner join 
        db_delivereat_G2.dbo.tbl_area c with (nolock) on b.area_id = c.area_id where convert(date,(case when a.time_pickup='1753-01-01 00:00:00' then dateadd(hour,1, a.time_in) else a.time_pickup end)) = convert(date,SYSDATETIME())
        group by c.name) e on d.name = e.name 
		where  convert(date,(case when a.time_pickup='1753-01-01 00:00:00' then dateadd(hour,1, a.time_in) else a.time_pickup end))=convert(date,SYSDATETIME()) and a.is_retrieved not in ('C','X','1') or 
		(a.is_retrieved='R' and SYSDATETIME() between a.time_in and (case when a.time_pickup='1753-01-01 00:00:00' then dateadd(hour,1, a.time_in) else a.time_pickup end)) 

    ''',conn)
    df2=pd.DataFrame(query)
    df3=pd.DataFrame(columns=('rest_long','rest_lat','is_retrieved'))
    df3['rest_long']=df2['rest_long']
    df3['rest_lat']=df2['rest_lat']
    df3['is_retrieved']=df2['is_retrieved']
    # df4 = df4[~df4['is_retrieved'].isin(['R','N'])]

    customer = go.Scattermapbox(lat=list(df2.lat), lon=list(df2.long), mode="markers", text=list(df2.customer_id),marker={'opacity':0.5,'size':15,'color':'#007bff'}
                                ,legendgroup='customer',name='customer',showlegend=True)
    restaurant = go.Scattermapbox(lat=list(df3.rest_lat), lon=list(df3.rest_long), mode="markers", text=list(df3.is_retrieved),
                                      marker={'opacity': 0.5, 'size': 15, 'color': 'yellow'},legendgroup='restaurant',name='restaurant',showlegend=True)

    layout = go.Layout(
        title='Rider Active Location',
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=800,
        font={
            "color": "#7FDBFF"
        },
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            uirevision=True,
            # center={"lat":5.4164,"lon":100.3327
            #
            # },
            pitch=0,
            # zoom=10,
            style='dark'
        )
    )

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'mapbox.zoom': 11,
                           'mapbox.center.lon': '100.3327',
                           'mapbox.center.lat': '5.4164'}],
                    label='zoom',
                    method='relayout',
                )
            ]),
            direction='left',
            pad={'r': 10, 't': 10},
            showactive=True,
            type='buttons',
            x=0.1,
            xanchor='left',
            y=1,
            yanchor='top',
            bordercolor='#00FFFF',


        ),
    ])

    layout['updatemenus'] = updatemenus

    data.append(rider_gotjob)
    data.append(rider_nojob)
    data.append(customer)
    data.append(restaurant)
    return{"data":data,"layout": layout}
@dashboard.callback(dash.dependencies.Output("rider_amount","children"),
                    [dash.dependencies.Input("update4","n_intervals")])
def rider_amount(self):
    conn2 = pyodbc.connect('Driver={SQL Server};'
                           'Server=43.252.214.228,1533;'
                           'Database=db_delivereat_on2;'
                           'UID=weifong;'
                           'PWD=123.123;'
                           )
    value = pd.read_sql_query('''
    set nocount on
   	create table #S
		(
			crew_id int,
			crew_name varchar(200),
			isLogin bit,
			updated_datetime datetime,
			jobStatus varchar(2),
			jobStatusSeq int,
			zone_id int,
			state varchar(20),
			is_break bit,
			is_block bit,
			isHalal bit,
			is_working bit
		)
	
		--get current job status
		create table #tempS
		(
			crew_id int,
			status varchar(2),
			statusSeq int
		)

		insert into #tempS 
		select distinct crew_id, a.status, 6 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'N'

		insert into #tempS 
		select distinct crew_id, a.status, 5 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'P' and crew_id not in (select crew_id from #tempS)
		
		insert into #tempS 
		select distinct crew_id, a.status, 4 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'R' and crew_id not in (select crew_id from #tempS)

		insert into #tempS 
		select distinct crew_id, a.status, 3 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D1' and crew_id not in (select crew_id from #tempS)

		insert into #tempS 
		select distinct crew_id, a.status, 2 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D2' and crew_id not in (select crew_id from #tempS)
		
		insert into #tempS 
		select distinct crew_id, a.status, 1 as statusSeq from tbl_order a with (nolock)
		inner join tbl_job b with (nolock) on a.order_id = b.order_id where a.status = 'D3' and crew_id not in (select crew_id from #tempS)

		INSERT INTO #S	
		SELECT a.crew_id, first_name + ', ' + last_name as crew_name,
		(select case when count(*) >= 1 then 1 else 0 end from tbl_token_d with (nolock) where crew_id = a.crew_id 
		and created_datetime < GETDATE() and (closed_datetime > GETDATE() or closed_datetime is null)) as isLogin,
		IsNUll(b.LatestTime, '1900-01-01 00:00:00.000') as updated_datetime, IsNull(c.status, '') as jobStatus, IsNull(c.statusSeq, 0) as jobStatusSeq,
		a.delivery_team_id as zone_id, area.state, 
		(SELECT CASE WHEN count(*) > 0  THEN 1 ELSE 0 END FROM tbl_delivery_crew_break with (nolock) WHERE crew_id = a.crew_id
		AND datetime_break BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) AND is_break = 1) as is_break,
		(SELECT CASE WHEN count(*) > 0  THEN 1 ELSE 0 END FROM tbl_delivery_crew_block_order with (nolock) WHERE crew_id = a.crew_id
		AND time_block BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(DAY, 1, CAST(GETDATE() AS DATE)) AND is_block = 1 ) as is_block,
		a.is_halal as isHalal, a.is_working
		FROM tbl_delivery_crew a with (nolock)
		left join (select MAX(updated_datetime) as LatestTime, crew_id from tbl_delivery_crew_location with (nolock)
		group by crew_id) b on  a.crew_id = b.crew_id 
		left join db_delivereat_G2.dbo.tbl_area area with (nolock) on a.delivery_team_id = area.zonegroup
		left join (select * from #tempS ) c on a.crew_id = c.crew_id
		WHERE a.status = 'A'
		
		SELECT #S.*, a.latitude as lat, a.longitude as lng INTO #S1 from #S with (nolock) left join tbl_delivery_crew_location a with (nolock) on #S.crew_id = a.crew_id and #S.updated_datetime = a.updated_datetime
				
	

		select state,count(distinct crew_id)as inactive from #S1 with (nolock)
		where (is_working = 1) and (jobStatus='') and (isLogin=1) OR (is_working = CASE WHEN jobStatusSeq <> 0 THEN 0 END)
		group by state
    ''',conn2)
    df=pd.DataFrame(value)
    return html.Div("Total Number of free riders Penang: {:,d}".format(
       df.at[1,'inactive'])),html.Div('Total Number of free riders KL: {:,d}'.format(df.at[0,'inactive']))

@dashboard.callback(dash.dependencies.Output("graph5","figure"),
                    [dash.dependencies.Input("update4","n_intervals")])
def update_bar_return(self):
    data=[]
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1533;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
    set nocount on
    SELECT
        b.signup_date,c.member_id, COUNT(*) as counts into #a
    FROM
        tbl_order a with (nolock) ,tbl_customerDB b with (nolock),tbl_customer c with (nolock) where a.customer_id = b.customer_id and b.customer_id=c.member_id and CONVERT(date,b.signup_date) between ? and ?
    GROUP BY
       c.member_id, order_id,signup_date
    HAVING 
        COUNT(*) >= 1
    	select convert(date,a.signup_date) as date,count(member_id) as number,cast(count(member_id) as float)*100/(select cast(count(customer_id) as float)
    	from tbl_customerDB with (nolock) where CONVERT(date,signup_date)=CONVERT(date,a.signup_date)) as percentage from #a a with (nolock)
    	group by convert(date,a.signup_date)

    '''
    cursor = conn.cursor()
    start = date.today() - timedelta(days=4)
    start = start.strftime('%Y/%m/%d')
    end = date.today()
    end = end.strftime('%Y/%m/%d')
    cursor.execute(sql, start, end)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    trace_bar = go.Bar(x=list(df.date), y=list(df.percentage), name='return customer', marker_color=list(df.percentage))
    layout = go.Layout(

                title="Return customer percentage ",
                plot_bgcolor= "#111111",
                paper_bgcolor= "#111111",
                yaxis=dict(title='Percentage(%)',autorange=True),
                xaxis=dict(title='Date',autorange=True,tickmode='linear'),
                autosize=True,
                font= {
                    "color": "#7FDBFF"
                }
    )
    data.append(trace_bar)
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output("graph-off5","figure"),
                    [dash.dependencies.Input("update5","n_intervals")])
def update_bar_return_off(self):
    data=[]
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1535;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    sql = '''
    set nocount on
    SELECT
    b.signup_date,c.member_id, COUNT(*) as counts into #a
FROM
    tbl_order a with (nolock) ,tbl_customerDB b with (nolock),tbl_customer c with (nolock) where a.customer_id = b.customer_id and b.customer_id=c.member_id and CONVERT(date,b.signup_date) between '2019-01-01' and convert(date,sysdatetime())
GROUP BY
   c.member_id, order_id,signup_date
HAVING 
    COUNT(*) >= 1
	select month(a.signup_date) as month,count(member_id)as number,cast(count(member_id) as float)*100/(select cast(count(customer_id) as float)
	from tbl_customerDB with (nolock) where month(a.signup_date)=month(signup_date) and year(signup_date)='2019') as percentage from #a a
	group by month(a.signup_date)
	order by month

    '''
    sql2=pd.read_sql_query('''
    	select month(signup_date) as month,count(customer_id) as number from tbl_customerDB with (nolock) where month(signup_date) between '1' and month(sysdatetime()) 
	and year(signup_date)=2019
	group by month(signup_date)
	
    ''',conn)
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    df2=pd.DataFrame(sql2)
    percentage = go.Bar(x=list(df.month), y=list(df.number), name='return customer', marker_color='yellow')
    number = go.Bar(x=list(df2.month), y=list(df2.number), name='New customer',
                       marker_color='#007bff')
    layout = go.Layout(

                title="Number of new customer/Return customer  ",
                plot_bgcolor= "#111111",
                paper_bgcolor= "#111111",
                yaxis=dict(title='Number of Customer',autorange=True),
                xaxis=dict(title='Month',autorange=True,tickmode='linear'),
                autosize=True,
                font= {
                    "color": "#7FDBFF"
                },
                barmode='group'

    )
    data.append(percentage)
    data.append(number)

    return {"data": data, "layout": layout}


@dashboard.callback(dash.dependencies.Output("graph6", "figure"),
                    [dash.dependencies.Input("update_order", "n_intervals")])
def update_number_order(self):
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1533;'
                          'Database=db_delivereat_G2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    query = pd.read_sql_query('''
       set nocount on
	SELECT d.name as zone ,
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 10 THEN 1 ELSE 0 END) AS '10am',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 11 THEN 1 ELSE 0 END) AS '11am',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 12 THEN 1 ELSE 0 END) AS '12pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 13 THEN 1 ELSE 0 END) AS '1pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 14 THEN 1 ELSE 0 END) AS '2pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 15 THEN 1 ELSE 0 END) AS '3pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 16 THEN 1 ELSE 0 END) AS '4pm',
       SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 17 THEN 1 ELSE 0 END) AS '5pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 18 THEN 1 ELSE 0 END) AS '6pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 19 THEN 1 ELSE 0 END) AS '7pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 20 THEN 1 ELSE 0 END) AS '8pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 21 THEN 1 ELSE 0 END) AS '9pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 22 THEN 1 ELSE 0 END) AS '10pm',
	   SUM(CASE WHEN DATEPART(hour,(case when time_pickup = '1753-01-01 00:00:00' then dateadd(hour,1,time_in) else time_pickup end)) = 23 THEN 1 ELSE 0 END) AS '11pm'
FROM  tbl_order a with (nolock)
inner join tbl_restaurant b with (nolock) on a.restaurant_id=b.restaurant_id 
inner join tbl_area c with (nolock) on b.area_id=c.area_id 
inner join tbl_area_zonegroup d with (nolock) on c.zonegroup=d.zone_id
where((convert(date,time_pickup) =convert(date,sysdatetime()) OR ((convert(date,time_in)=convert(date,sysdatetime()) ) 
AND time_pickup='1753-01-01 00:00:00'))and a.status<>'X' and a.status<>'1')
GROUP BY d.name
ORDER BY d.name
    ''', conn)

    df = pd.DataFrame(query)
    hour = ('10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm')
    for x in range(len(df.zone)):
        line=go.Scatter(x=hour, y=list(df.iloc[x, 1:15]), mode='lines',name=df['zone'].apply(str)[x])
        data.append(line)

    layout = go.Layout(

        title="Number of order each hour ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='Number of Order', autorange=True),
        xaxis=dict(title='time', autorange=True, tickmode='linear'),
        autosize=True,
        font={
            "color": "#7FDBFF"
        },
    )
    return {"data": data, "layout": layout}

@dashboard.callback(dash.dependencies.Output("graph7", "figure"),
                    [dash.dependencies.Input("update_rider_number", "n_intervals")])
def update_rider_number(self):
    data = []
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=43.252.214.228,1533;'
                          'Database=db_delivereat_on2;'
                          'UID=weifong;'
                          'PWD=123.123;'
                          )
    query = pd.read_sql_query('''
       set nocount on
	 create table #s
 (
 crew_id int, 
	updated_datetime datetime

 )
    insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=10) group by crew_id)
	 

 insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=11) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=12) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=13) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=14) group by crew_id)


	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=15) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=16) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) = convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=17) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=18) group by crew_id)
	
	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=19) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=20) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location  with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=21) group by crew_id)
	 

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=22) group by crew_id)
	

	  insert into #s
     select crew_id,updated_datetime
     from 
	 tbl_delivery_crew_location with (nolock) where updated_datetime in (select max(updated_datetime) from tbl_delivery_crew_location with (nolock)
	 where convert(date,updated_datetime) =convert(date,sysdatetime()) and (datepart(hour,updated_datetime)=23) group by crew_id)

	 SELECT c.name as zone ,
       SUM(case when datepart(hour,updated_datetime)= 10 THEN 1 ELSE 0 END) AS '10am',
	   SUM(case when datepart(hour,updated_datetime)= 11 THEN 1 ELSE 0 END) AS '11am',
	   SUM(case when datepart(hour,updated_datetime)= 12 THEN 1 ELSE 0 END) AS '12pm',
	   SUM(case when datepart(hour,updated_datetime)= 13 THEN 1 ELSE 0 END) AS '1pm',
	   SUM(case when datepart(hour,updated_datetime)= 14 THEN 1 ELSE 0 END) AS '2pm',
	   SUM(case when datepart(hour,updated_datetime)= 15 THEN 1 ELSE 0 END) AS '3pm',
	   SUM(case when datepart(hour,updated_datetime)= 16 THEN 1 ELSE 0 END) AS '4pm',
	   SUM(case when datepart(hour,updated_datetime)= 17 THEN 1 ELSE 0 END) AS '5pm',
	   SUM(case when datepart(hour,updated_datetime)= 18 THEN 1 ELSE 0 END) AS '6pm',
	   SUM(case when datepart(hour,updated_datetime)= 19 THEN 1 ELSE 0 END) AS '7pm',
	   SUM(case when datepart(hour,updated_datetime)= 20 THEN 1 ELSE 0 END) AS '8pm',
	   SUM(case when datepart(hour,updated_datetime)= 21 THEN 1 ELSE 0 END) AS '9pm',
	   SUM(case when datepart(hour,updated_datetime)= 22 THEN 1 ELSE 0 END) AS '10pm',
	   SUM(case when datepart(hour,updated_datetime)= 23 THEN 1 ELSE 0 END) AS '11pm'
      
FROM  #s a with (nolock)
inner join tbl_delivery_crew b with (nolock) on a.crew_id=b.crew_id
inner join db_delivereat_G2.dbo.tbl_area_zonegroup c with (nolock) on b.delivery_team_id=c.zone_id
GROUP BY c.name
ORDER BY c.name
    ''', conn)

    df = pd.DataFrame(query)
    hour = ('10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm')
    for x in range(len(df.zone)):
        line=go.Scatter(x=hour, y=list(df.iloc[x, 1:15]), mode='lines',name=df['zone'].apply(str)[x])
        data.append(line)

    layout = go.Layout(

        title="Number of rider each hour ",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        yaxis=dict(title='Number of rider', autorange=True),
        xaxis=dict(title='time', autorange=True, tickmode='linear'),
        autosize=True,
        font={
            "color": "#7FDBFF"
        },
    )
    return {"data": data, "layout": layout}


dashboard.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})
if __name__ == "__main__":
    #dashboard.run_server(debug=True,dev_tools_hot_reload=True)
	server=dashboard.Dash(__name__,debug=True)





