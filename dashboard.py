from dash import html
import datetime as dt
import BudgetBuddies as eq
import plotly.graph_objects as go
from tickerData import Ticker
import numpy as np
import MonteCarlo as mc
import plotly.express as px
import localDatabase as ld
import pandas as pd

def get_start_end_dates():
    """Get the start and end dates for a date range.

    Returns:
        tuple: A tuple containing the start and end dates.
    """
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365 * 3)
    return start, end

def get_ticker_data(ticker):
    """Retrieve data for a given stock ticker symbol.

    Args:
        symbol (str): The stock ticker symbol.

    Returns:
        Object: Data associated with the stock ticker.
    """
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
        try: #if tick.info is empty it will throw KeyError
            temp = (tick.info['symbol'], tick.info['previousClose'])
        except KeyError: #if KeyError thrown return -1 to alert of error
            return -1
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
            ]), font=dict(color="#343A40")
        )
    )
    fig.update_layout(title='Candlestick Chart', xaxis_title=None, yaxis_title='Price', 
                      plot_bgcolor="#F7F7F7", paper_bgcolor="#343A40", font=dict(color="#F7F7F7"))
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
    if 'trailingPE' in tickerInfo.keys():
        TrailingPE = str("%0.2f" %tickerInfo['trailingPE'])
    else:
        TrailingPE = ""
    if 'forwardPE' in tickerInfo.keys():
        ForwardPE = str("%0.2f" %tickerInfo['forwardPE'])
    else:
        ForwardPE = ""
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
            toCompDiv.append(html.P(str(data[0]) + ":   " + 
                                str(data[1]), 
                                style={'display': 'inline-block', 'margin-left': '50px'}))
        else:
            toCompDiv.append(html.P(
                str(data[0]) + ":   " + str(data[1]), 
                style={'display': 'inline-block'}))
            x += 1
    return toCompDiv

def getSentimentAnalysis(ticker: Ticker):
    """Generate output from sentiment analysis on ticker.

    Args:
        tickerData (Object): Data for a stock ticker

    Returns:
        string: Bullish, Neutral, Bearish.
    """
    #df = pd.DataFrame([ticker.sentimentAnalysis()]) 
    sentiment = {'Bearish' : 3, 'Somewhat Bearish' : 7, 'Somewhat Bullish' : 25, 'Bullish' : 20}
    df = pd.DataFrame([sentiment])
    fig = px.bar(df,orientation='h', height=125, width=800, color_discrete_sequence = ['maroon', 'lightcoral', 'mediumseagreen', 'forestgreen'])
    fig.update_layout(legend_title=None, yaxis = dict(visible=False), xaxis_title = None, 
                      margin=dict(l=0,t=0,b=10), paper_bgcolor="#F7F7F7", plot_bgcolor="#F7F7F7")
    return fig

def annualLogReturn(df):
    """Calculate log rate of return over three years

    Args:
        df (DataFrame): DataFrame containing stock data.

    Returns:
        float: three year log return average
    """
    log_returns = np.log(df['Close'] / df['Close'].shift(1)).dropna().sum()*100
    return log_returns/3

def ThirtyDayEMA(df):
    """Calculate thirty day exponential moving average

    Args:
        df (DataFrame): DataFrame containing stock data.

    Returns:
        float: EMA
    """
    thirtyDay = df['Close'].tail(30)
    thirtyDay = thirtyDay.iloc[::-1]
    thirtyDayAVG = thirtyDay.ewm(span=30, adjust=False).mean().sum()/30
    return thirtyDayAVG

def getMonteCarlo(tickerData, PerYearGrowth):
    """Generate histogram based on Monte Carlo simulations

    Args:
        tickerData (Dict): Dictionary of ticker data.
        PerYearGrowth (Float): User inputed average per year growth rate 

    Returns:
        figure: histogram
        mean: float
    """
    distribution =  mc.MonteCarlo(tickerData, PerYearGrowth)
    fig = px.histogram(distribution, nbins=75, title='Monte Carlo Simulation of DCF', color_discrete_sequence = ['maroon'])
    fig.update_layout(legend_title=None, plot_bgcolor="#F7F7F7", paper_bgcolor="#343A40",font=dict(color="#F7F7F7"))
    mean = distribution.mean()
    return {'fig': fig, 'mean': mean}

def create_comp_tickers(tickerSymbols):
    compTickers = []
    for ticker in tickerSymbols:
        temp = ld.createTicker(ticker)
        if temp == -1: 
            return -1
        compTickers.append(temp)
    return compTickers

def create_dashboard_data(df):
    tickerSymbol = df['Ticker'].iloc[0]
    perYearGrowth = df['PerYearGrowth'].iloc[0]
    compareTickers = df['CompareTickers'].iloc[0]
    
    ticker = ld.createTicker(tickerSymbol)
    #check if there's been an error with finding ticker
    if ticker == -1: return{'error': True}
    start, end = get_start_end_dates()
    tickerData = get_ticker_data(ticker)   
    compareTickersList = create_comp_tickers(compareTickers.split(','))
    if compareTickersList == -1: return{'error': True}
    toCompData = get_comparison_data(compareTickersList)
    if toCompData == -1: return{'error': True}
    df = get_dataframe(tickerData, start, end)
    fig = create_candlestick_figure(df)
    FullName, LastClose, TrailingPE, ForwardPE, avgAnalystTarget = get_ticker_info(tickerData)
    TradeComps_ImpliedPrices = get_comps_implied_prices(compareTickersList, tickerData)
    DCF_ImpliedPrice = get_dcf_implied_price(tickerData, perYearGrowth)
    toCompDiv = generate_comparison_div(toCompData)
    sentimentAnalysis = getSentimentAnalysis(ticker)
    aLogReturn = annualLogReturn(df)
    movingAVG = ThirtyDayEMA(df)
    monteCarlo = getMonteCarlo(tickerData, perYearGrowth)

    return {
        'FullName': FullName,
        'tickerSymbol': tickerSymbol,
        'LastClose': LastClose,
        'TrailingPE': TrailingPE,
        'ForwardPE': ForwardPE,
        'avgAnalystTarget': avgAnalystTarget,
        'DCF_ImpliedPrice': DCF_ImpliedPrice,
        'PerYGrowth': perYearGrowth,
        'fig': fig,
        'toCompDiv': toCompDiv,
        'TradeComps_ImpliedPrices': TradeComps_ImpliedPrices,
        'sentimentAnalysis': sentimentAnalysis,
        'aLogReturn': aLogReturn,
        'movingAVG': movingAVG,
        'monteCarloFig': monteCarlo['fig'],
        'monteCarloMean': monteCarlo['mean'],
        'eps' : tickerData['eps'],
        'error' : False
    }

