from dash import html
import pandas as pd
from PageLayouts import Dashboard 
import datetime as dt
import BudgetBuddies as eq
import plotly.graph_objects as go
from tickerData import Ticker


def get_start_end_dates():
    """Get the start and end dates for a date range.

    Returns:
        tuple: A tuple containing the start and end dates.
    """
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365 * 3)
    return start, end

def get_ticker_data(symbol):
    """Retrieve data for a given stock ticker symbol.

    Args:
        symbol (str): The stock ticker symbol.

    Returns:
        Object: Data associated with the stock ticker.
    """
    ticker = Ticker(symbol)
    ticker.pullData()
    return ticker.getData()

def get_comparison_data(toComp):
    """Retrieve comparison data for a list of stock tickers.

    Args:
        toComp (list): A list of stock ticker objects for comparison.

    Returns:
        list: A list of tuples containing comparison data.
    """
    toCompData = []
    for comp in toComp:
        compData = comp.getData()
        tick = compData['ticker']
        temp = (tick.info['symbol'], tick.info['previousClose'])
        toCompData.append(temp)
    return toCompData

def get_dataframe(ticker_data, start, end):
    """Get a DataFrame for a given date range.

    Args:
        ticker_data (DataFrame): Data for a stock ticker.
        start (datetime): Start date of the date range.
        end (datetime): End date of the date range.

    Returns:
        DataFrame: DataFrame containing the stock data for the specified date range.
    """
    return ticker_data['ticker'].history(start=start, end=end)

def create_candlestick_figure(df):
    """Create a candlestick chart from a DataFrame.

    Args:
        df (DataFrame): DataFrame containing stock data.

    Returns:
        Figure: Candlestick chart figure.
    """
    fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                )])
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
    return fig

def get_ticker_info(ticker_data):
    """Retrieve characteristics for a stock ticker.

    Args:
        ticker_data (Object): Data for a stock ticker.

    Returns:
        tuple: Tuple containing various characteristics of the stock ticker.
    """
    tickerInfo = ticker_data['ticker'].info
    FullName = tickerInfo['longName']
    LastClose = tickerInfo['previousClose']
    TrailingPE = tickerInfo['trailingPE']
    ForwardPE = tickerInfo['forwardPE']
    avgAnalystTarget = tickerInfo['targetMeanPrice']
    return FullName, LastClose, TrailingPE, ForwardPE, avgAnalystTarget

def get_comps_implied_prices(toComp, ticker_data):
    return eq.TradeComps(toComp, ticker_data)

def get_dcf_implied_price(ticker_data, PerYGrowth):
    return eq.DiscountedCashFlow(ticker_data, PerYGrowth)

def generate_comparison_div(toCompData):
    """Generate HTML comparison div for comparison data.

    Args:
        toCompData (list): List of tuples containing comparison data.

    Returns:
        list: List of HTML elements representing the comparison data.
    """
    toCompDiv = []
    x = 0
    for data in toCompData:
        if x > 0:
            toCompDiv.append(html.P(str(data[0]) + ":   " + str(data[1]), style={'display': 'inline-block', 'margin-left': '50px'}))
        else:
            toCompDiv.append(html.P(str(data[0]) + ":   " + str(data[1]), style={'display': 'inline-block'}))
            x += 1
    return toCompDiv

def create_dashboard():
    start, end = get_start_end_dates()
    tickerSymbol = 'LSCC'
    tickerData = get_ticker_data(tickerSymbol)
    toComp = [Ticker('MTSI'), Ticker('POWI'),
              Ticker('QRVO'), Ticker('RMBS'), Ticker('SLAB')]
    toCompData = get_comparison_data(toComp)
    df = get_dataframe(tickerData, start, end)
    fig = create_candlestick_figure(df)
    FullName, LastClose, TrailingPE, ForwardPE, avgAnalystTarget = get_ticker_info(tickerData)
    TradeComps_ImpliedPrices = get_comps_implied_prices(toComp, tickerData)
    DCF_ImpliedPrice = get_dcf_implied_price(tickerData, 0.25)
    toCompDiv = generate_comparison_div(toCompData)

    return Dashboard(FullName, tickerSymbol, LastClose, TrailingPE, ForwardPE, avgAnalystTarget, DCF_ImpliedPrice, 0.25,
                     fig, toCompDiv, TradeComps_ImpliedPrices)