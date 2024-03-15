import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd 

def create_dashboard(dashboard_data):
     return html.Div([
    html.Div([
        html.Div(
            html.H1(str(dashboard_data['FullName']) + " (" + 
                    str(dashboard_data['tickerSymbol']) + ")", 
                    style={'text-align' : 'right', 'margin-right' : '15px'}), 
        ),
        html.Div([
                html.P("Last Close",style={'display' : 'inline-block',
                                           'margin-left' : '150px'}),
                html.P(dashboard_data['LastClose'],
                       style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("P/E",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(dashboard_data['TrailingPE'],
                       style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("Forward P/E",
                       style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(dashboard_data['ForwardPE'],
                       style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("EPS",style={'display' : 'inline-block',
                                    'margin-left' : '150px'}),
                html.P(dashboard_data['eps'],
                       style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
                html.P("Analyst Target",
                       style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(dashboard_data['avgAnalystTarget'],
                       style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Thirty Day Exponential Moving Average",
                   style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P("%0.2f"%dashboard_data['movingAVG'],
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Annualized Log Rerturn",
                   style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P(str("%0.2f"%dashboard_data['aLogReturn'])+"%",
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("News Sentiment Analysis",
                   style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P(dashboard_data['sentimentAnalysis'],
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Br(),
        html.H2("Discounted Cash Flow",
                style={'display' : 'inline-block','margin-left' : '150px'}),
        html.Div([
            html.P("Current Cash Flow",
                   style={'display' : 'inline-block','margin-left' : '150px'}),
            html.P(f"{dashboard_data['DCF_ImpliedPrice']['FreeCashFlow']:,}",
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Average Yearly Growth",
                   style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P(dashboard_data['PerYGrowth'],
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Year Five Cash Flow",
                   style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P(f"{dashboard_data['DCF_ImpliedPrice']['LastYearCashFlow']:,}",
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Div([
            html.P("Implied Share Price",
                   style={'display' : 'inline-block', 'margin-left' : '150px'}),
            html.P("%0.2f" %dashboard_data['DCF_ImpliedPrice']['ImpliedSharePrice'],
                   style={'float' : 'right','display' : 'inline-block'})
        ]),
        html.Br(),
        html.H2("Trading Comps",style={'margin-left' : '150px'}),
        html.Div([
            html.Div(dashboard_data['toCompDiv']),
            html.P("Revenue Share Price: "+
                   str("%0.2f" %dashboard_data['TradeComps_ImpliedPrices']['revenue_SharePrice']),
                   style={'display' : 'inline-block'}),
            html.P("EBITDA Share Price: "+
                   str("%0.2f" %dashboard_data['TradeComps_ImpliedPrices']['ebitda_SharePrice']),
                   style={'display' : 'inline-block', 'margin-left' : '50px'}),
            html.P("P/E Share Price: "+
                   str("%0.2f" %dashboard_data['TradeComps_ImpliedPrices']['netIncome_SharePrice']),
                   style={'display' : 'inline-block', 'margin-left' : '50px'}),
        ],style={'textAlign' : 'center'})
        

    ],style={'textAlign' : 'top' ,'width' : '45%', 
             'display' : 'inline-block', 'margin-left' : '50px'}),
    html.Div([
        dcc.Graph(figure=dashboard_data['fig']),
        dcc.Graph(figure=dashboard_data['monteCarloFig']),
         html.P("Mean: "+str("%0.2f" %dashboard_data['monteCarloMean']),
                style={'textAlign' : 'center'})
    ],style={ 'width' : '45%', 'display' : 'inline-block', 
             'float' : 'right', 'margin-right' : '50px'}),
])


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
                          min=0, max=1, step=0.01),
            ]),
            html.Div(className='menu-item', children=[
                html.Label(className='menu-title', 
                children="Enter Additional Stock Ticker Symbols to Compare Against (Seperate By Comma):"),
                dcc.Input(id="compare-tickers-input", 
                          type="text", placeholder="MSFT,AAPL,NVDA" ,
                          className='space-between'),
            ]),
            html.Button('Analyze', id='analyze-button', className='analyze-button'),
            html.Div(id='hidden-div', style={'display': 'none'})
        ])
    ])


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
