from dash import dcc, html
import pandas as pd 

def Dashboard(FullName, symbol, LastClose, TrailingPE, ForwardPE, avgAnalystTarget,DCF_ImpliedPrice,PerYGrowth,
              fig, toCompDiv, TradeComps_ImpliedPrices):
    return html.Div([
    html.Div([
        html.Div(
            html.H1(str(FullName) + " (" + str(symbol) + ")", style={'text-align' : 'right', 'margin-right' : '15px'}), 
        ),
        html.Div([
                html.P("Last Close",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(LastClose,style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("P/E",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P("%0.2f" %TrailingPE,style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("Forward P/E",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P("%0.2f" %ForwardPE,style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("Analyst Target",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(avgAnalystTarget,style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Br(),
        html.H2("Discounted Cash Flow",style={'display' : 'inline-block','margin-left' : '150px'}),
        html.Div([
            html.P("Current Cash Flow",style={'display' : 'inline-block','margin-left' : '150px'}),
            html.P(DCF_ImpliedPrice['FreeCashFlow'],style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Average Yearly Growth",style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P(PerYGrowth,style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Year Five Cash Flow",style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P("%0.2f" %DCF_ImpliedPrice['LastYearCashFlow'],style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Implied Share Price",style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P("%0.2f" %DCF_ImpliedPrice['ImpliedSharePrice'],style={'float' : 'right','display' : 'inline-block'})
        ])

    ],style={'textAlign' : 'top' ,'width' : '45%', 'display' : 'inline-block', 'margin-left' : '50px'}),
    html.Div([
        dcc.Graph(figure=fig),
        html.Div([
            html.Div(toCompDiv),
            html.P("Revenue Share Price: "+str("%0.2f" %TradeComps_ImpliedPrices['revenue_SharePrice']),style={'display' : 'inline-block'}),
            html.P("EBITDA Share Price: "+str("%0.2f" %TradeComps_ImpliedPrices['ebitda_SharePrice']),style={'display' : 'inline-block', 'margin-left' : '50px'}),
            html.P("P/E Share Price: "+str("%0.2f" %TradeComps_ImpliedPrices['netIncome_SharePrice']),style={'display' : 'inline-block', 'margin-left' : '50px'}),
        ],style={'textAlign' : 'center'})
    ],style={ 'width' : '45%', 'display' : 'inline-block', 'float' : 'right', 'margin-right' : '50px'}),
])

def upload_data_layout():
    """
    This creates a page layout allowing users to enter their specific stock ticker,
    5 addtional stock tickers to compare against and an "Analyze" button which will
    send the user to the dashboard to visualize the data.
    """
    return html.Div([
        html.Div(className='header', children=[
            html.H1(className='header-title', children="BudgetBuddies Market Analysis Tool"),
            html.P(className='header-description', children="Welcome to the BudgetBuddies Market Analysis Tool. Analyze historical stock data and trends."),
        ]),
        html.Div(className='wrapper', children=[
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', children="Enter Stock Ticker Symbol:"),
                dcc.Input(id="ticker", type="text", value="LSCC", className='ticker-input'),
            ]),
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', children="Enter 5 Additional Stock Ticker Symbols to Compare Against:"),
                dcc.Input(id="ticker", type="text", className='space-between'),
            ]),
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', children="Select Start Date:"),
                html.Br(),
                dcc.DatePickerSingle(
                    id='start-date-picker',
                    date=pd.Timestamp.now() - pd.DateOffset(months=1),  # Default value (1 month ago)
                    display_format='YYYY-MM-DD'
                ),
            ]),
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', children="Select End Date:"),
                html.Br(),
                dcc.DatePickerSingle(
                    id='end-date-picker',
                    date=pd.Timestamp.now(),  # Default value (today)
                    display_format='YYYY-MM-DD'
                ),
            ]),
            dcc.Link(html.Button('Analyze', id='analyze-button', className='analyze-button'), href='/dashboard_layout', refresh=True),
            ]),
        ])


# @callback(
#     [Input('analyze-button', 'n_clicks')],
#     [State('ticker-input', 'value'),
#      State('start-date-picker', 'date'),
#      State('end-date-picker', 'date')]
# )
# def process_input(n_clicks, ticker, start_date, end_date):
    
#     start_date = pd.to_datetime(start_date)
#     end_date = pd.to_datetime(end_date)

#     data = bb.pullTickerData(ticker=ticker)

