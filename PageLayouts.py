import os
import sqlite3 as sql
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import MySQLdb
import remoteDatabase as rd
import localDatabase as ld

image_path1 = 'assets/monte_carlo.png'
image_path2 = 'assets/sentiment_analysis.png'

def create_homepage():
    return html.Div([
       html.H1("Automatic Valuation Calculation"),
       html.H3("Speeds up the process of financial modeling"),
       html.Br(),
       html.H5("""Intrinsic value will be calculated from the 
               input of a ticker with an estimated yearly growth"""),
       html.H5("Enter tickers of competitors for Trade Comps"),
       html.Br(),
       html.Div([
              html.H5("Easy construction \nof the Monte Carlo Model",
                     style={'margin-right' : '50px', 'display' : 'inline-block'}),
              html.Img(src=image_path1,style={'display' : 'inline-block'})
       ]),
       html.Br(),
       html.Div([
              html.H5("Sentiment analysis from the current news",
                      style={'margin-right' : '50px', 'display' : 'inline-block'}),
              html.Img(src=image_path2,style={'display' : 'inline-block'})
       ]),
    ],style={'float' : 'center', 'text-align' : 'center'})


def create_dashboard(dashboard_data):
    """
    Fill out and display dashboard data based on the values 
    from the passed in dashboard_data key:value pairs.
    """
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H1(
                                        f"{dashboard_data['FullName']} ({dashboard_data['tickerSymbol']})",
                                        style={'text-align': 'left'}
                                    ),
                                    html.Div([
                                        html.P("Last Close", style={'display': 'inline-block'}),
                                        html.P(
                                            dashboard_data['LastClose'],
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("P/E", style={'display': 'inline-block'}),
                                        html.P(
                                            dashboard_data['TrailingPE'],
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Forward P/E", style={'display': 'inline-block'}),
                                        html.P(
                                            dashboard_data['ForwardPE'],
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("EPS", style={'display': 'inline-block'}),
                                        html.P(
                                            dashboard_data['eps'],
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Analyst Target", style={'display': 'inline-block'}),
                                        html.P(
                                            dashboard_data['avgAnalystTarget'],
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Thirty Day Exponential Moving Average", style={'display': 'inline-block'}),
                                        html.P(
                                            "{:0.2f}".format(dashboard_data['movingAVG']),
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Annualized Log Return", style={'display': 'inline-block'}),
                                        html.P(
                                            "{:0.2f}%".format(dashboard_data['aLogReturn']),
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.P("News Sentiment Analysis"),
                                    dcc.Graph(
                                        figure=dashboard_data['sentimentAnalysis'],
                                        style={'width': '100%'}
                                    ),
                                    html.Br(),
                                    html.H2("Discounted Cash Flow"),
                                    html.Div([
                                        html.P("Current Cash Flow", style={'display': 'inline-block'}),
                                        html.P(
                                            f"{dashboard_data['DCF_ImpliedPrice']['FreeCashFlow']:,}",
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Average Yearly Growth", style={'display': 'inline-block'}),
                                        html.P(
                                            dashboard_data['PerYGrowth'],
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Year Five Cash Flow", style={'display': 'inline-block'}),
                                        html.P(
                                            f"{dashboard_data['DCF_ImpliedPrice']['LastYearCashFlow']:,.2f}",
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Div([
                                        html.P("Implied Share Price", style={'display': 'inline-block'}),
                                        html.P(
                                            "{:0.2f}".format(dashboard_data['DCF_ImpliedPrice']['ImpliedSharePrice']),
                                            style={'float': 'right', 'display': 'inline-block'}
                                        )
                                    ]),
                                    html.Br(),
                                    html.H2("Trading Comps"),
                                    html.Div([
                                        html.Div(dashboard_data['toCompDiv']),
                                        html.P(
                                            "Revenue Share Price: {:0.2f}".format(dashboard_data['TradeComps_ImpliedPrices']['revenue_SharePrice']),
                                            style={'display': 'inline-block'}
                                        ),
                                        html.P(
                                            "EBITDA Share Price: {:0.2f}".format(dashboard_data['TradeComps_ImpliedPrices']['ebitda_SharePrice']),
                                            style={'display': 'inline-block', 'margin-left': '3%'}
                                        ),
                                        html.P(
                                            "P/E Share Price: {:0.2f}".format(dashboard_data['TradeComps_ImpliedPrices']['netIncome_SharePrice']),
                                            style={'display': 'inline-block', 'margin-left': '3%'}
                                        ),
                                    ], style={'text-align': 'center'}),
                                ]
                            )
                        ],
                        width=12, lg=6
                    ),
                    
                    dbc.Col(
                        [
                            dcc.Graph(
                                figure=dashboard_data['fig'],
                                style={'width': '100%'}
                            ),
                            html.Br(),
                            dcc.Graph(
                                figure=dashboard_data['monteCarloFig'],
                                style={'width': '100%'}
                            ),
                            html.Div([
                                html.P(
                                    "Lower Quantile: {:0.2f}".format(dashboard_data['monteCarloLower']),
                                    style={'display': 'inline-block'}
                                ),
                                html.P(
                                    "Mean: {:0.2f}".format(dashboard_data['monteCarloMean']),
                                    style={'display': 'inline-block', 'margin-left': '3%'}
                                ),
                                html.P(
                                    "Upper Quantile: {:0.2f}".format(dashboard_data['monteCarloUpper']),
                                    style={'display': 'inline-block', 'margin-left': '3%'}
                                ),
                            ], style={'text-align': 'center'}),
                            
                        ],
                        width=12, lg=6
                    )
                ]
            )
        ],
        style={
            # Change this if you want to adjust 
            # spacing around the edges of the screen
            'margin': '20px',
        }
    )



def upload_data_layout():
    """
    This creates a page layout allowing users to enter their specific stock ticker,
    5 additional stock tickers to compare against and an "Analyze" button which will
    send the user to the dashboard to visualize the data.
    """
    return html.Div([
        html.Div(className='header', children=[
            html.H1(className='header-title', 
                    children="BudgetBuddies Market Analysis Tool"),
            html.P(className='header-description', 
                   children="Welcome to the BudgetBuddies Market Analysis Tool. Analyze historical stock data and trends."),
        ]),
        html.Div(className='wrapper', children=[
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', 
                           children="Enter Stock Ticker Symbol:"),
                dcc.Input(id="ticker-input", type="text", 
                          placeholder="Ticker Symbol", className='ticker-input'),
            ]),
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', children="Enter Per Year Growth:"),
                dcc.Input(id="per-year-growth-input", type="number", 
                          placeholder=0.25, className='ticker-input', 
                          min=-1, max=2, step=0.01),
            ]),
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', 
                children="Enter Additional Stock Ticker Symbols to Compare Against (Separated By Comma):"),
                dcc.Input(id="compare-tickers-input", 
                          type="text", placeholder="MSFT,AAPL,NVDA" ,
                          className='space-between'),
            ]),
            html.Button('Analyze', id='analyze-button', className='analyze-button'),
            html.Div(id='hidden-div', style={'display': 'none'})
        ])
    ])


def database_table_layout():
    """
        This function generates a layout to display database tables.
        :param tables: List of table names retrieved from the database
        :return: Dash HTML layout
    """
    # Establish connection to the MySQL database
    connection = MySQLdb.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USERNAME"),
        passwd=os.getenv("DATABASE_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={"ca": "C:\\Users\\17278\\Documents\\MyCourses\\CEN4090L\\cacert-2024-03-11.pem"}
    )
    
    # Create cursor
    cursor = connection.cursor()

    rd.create_ticker_data_table(connection)
    # Execute query to select all rows from TickerData table
    cursor.execute("SELECT * FROM TickerData")

    # Fetch all rows
    rows = cursor.fetchall()

    # Create table rows for each row in the TickerData table
    table_rows = [
        html.Tr([
            html.Td(column, className="table-cell") for column in row[1:]
        ]) for row in rows
    ]

    # Return the layout with CSS styling
    return html.Div([
        html.H1("TickerData Table", className="table-header", style={'text-align': 'center', 'padding': '10px'}),
        html.Div(className="table-container", style={"overflow": "auto", "height": "500px"}, children=[
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Current Report Date", className="table-header"),
                    html.Th("Ticker", className="table-header"),
                    html.Th("Revenue", className="table-header"),
                    html.Th("Net Income", className="table-header"),
                    html.Th("EBITDA", className="table-header"),
                    html.Th("Debt", className="table-header"),
                    html.Th("Cash", className="table-header"),
                    html.Th("Shares", className="table-header"),
                    html.Th("CFO", className="table-header"),
                    html.Th("Tax Rate", className="table-header")
                ])),
                html.Tbody(table_rows)
            ], className="table", style={'table-layout': 'auto', 'width': '100%', 'overflow-x': 'auto'})
        ])
    ], className="table-layout")



@callback(
    Output('hidden-div', 'children'),
    [Input('analyze-button', 'n_clicks')],
    [State('ticker-input', 'value'),
     State('per-year-growth-input', 'value'),
     State('compare-tickers-input', 'value')],
     prevent_initial_call=True,
)
def handle_analyze_button(n_clicks, ticker_input, per_year_growth_input, compare_tickers_input):
    if n_clicks is None:
        return dash.no_update

    df = pd.DataFrame({
        'Ticker': [ticker_input],
        'PerYearGrowth': [per_year_growth_input],
        'CompareTickers': [compare_tickers_input]
    })

    # Save DataFrame to a CSV file
    csv_filename = 'user_input.csv'
    df.to_csv(csv_filename, index=False)

    return dcc.Location('Go to Dashboard', href='/dashboard_layout', refresh=True)
