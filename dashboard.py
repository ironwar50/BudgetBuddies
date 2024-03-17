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
from concurrent.futures import ThreadPoolExecutor 
import time

executor = ThreadPoolExecutor(max_workers=5)

def create_ticker(tickerSymbol):
    return ld.createTicker(tickerSymbol)

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
        try: #if tick.info is empty it will throw KeyError
            temp = (compData['tickerSymbol'], compData['previousClose'])
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
    fig.update_layout(title='Candlestick Chart', xaxis_title=None, yaxis_title='Price',margin=dict(t=85,r=30,b=30,l=20), 
                      plot_bgcolor="#F7F7F7", paper_bgcolor="#343A40", font=dict(color="#F7F7F7"))
    return fig

def get_ticker_info(ticker_data):
    """Retrieve characteristics for a stock ticker.

    Args:
        ticker_data (Object): Data for a stock ticker.

    Returns:
        tuple: Tuple containing various characteristics of the stock ticker.
    """
    FullName = ticker_data['lName']
    LastClose = ticker_data['previousClose']
    TrailingPE = str("%0.2f" %ticker_data['PE'])
    ForwardPE = str("%0.2f" %ticker_data['fPE'])
    avgAnalystTarget = ticker_data['targetMeanPrice']
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
    #df = pd.DataFrame([{'Bearish' : 3, 'Somewhat Bearish': 7,'Somewhat Bullish' : 25, 'Bullish' : 20}])
    df = pd.DataFrame([ticker.sentimentAnalysis()]) 
    fig = px.bar(df,orientation='h', height=125, width=600, color_discrete_sequence = ['maroon', 'lightcoral', 'mediumseagreen', 'forestgreen'])
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
    fig = px.histogram(distribution, nbins=35, title='Monte Carlo Simulation of DCF', 
                       color_discrete_sequence = ['maroon'])
    fig.update_layout(legend_title=None, plot_bgcolor="#F7F7F7", paper_bgcolor="#343A40",
                      margin=dict(t=75,b=20,l=20),font=dict(color="#F7F7F7"))
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
    '''tickerSymbol = 'NVDA'
    perYearGrowth = .65
    compareTickers = 'TSM,INTC,QCOM,AMD,MU'''

    tickerSymbol = str(df['Ticker'].iloc[0])
    perYearGrowth = df['PerYearGrowth'].iloc[0]
    compareTickers = str(df['CompareTickers'].iloc[0])
    if tickerSymbol == '' or np.isnan(perYearGrowth)  or compareTickers == 'nan': return{'error': True}

    start_total_time = time.time()
   
    f_compareTickersList = executor.submit(create_comp_tickers,compareTickers.split(','))
    f_Ticker = executor.submit(create_ticker, tickerSymbol)
    compareTickersList = f_compareTickersList.result()
    ticker = f_Ticker.result()
   
    #check if there's been an error with finding ticker
    if ticker == -1: return{'error': True}
    if compareTickersList == -1: return{'error': True}
    start, end = get_start_end_dates()
    tickerData = ticker.getData()  
    toCompData = get_comparison_data(compareTickersList)
    if toCompData == -1: return{'error': True}
    df = get_dataframe(tickerData, start, end)
    fig = create_candlestick_figure(df)
    FullName, LastClose, TrailingPE, ForwardPE, avgAnalystTarget = get_ticker_info(tickerData)
    
    #monteCarlo = getMonteCarlo(tickerData, perYearGrowth)
    
    f_monteCarlo = executor.submit(getMonteCarlo, tickerData, perYearGrowth)
    f_TradeComps_ImpliedPrices = executor.submit(get_comps_implied_prices, compareTickersList, tickerData)
    f_DCF_ImpliedPrice = executor.submit(get_dcf_implied_price, tickerData, perYearGrowth)
    f_toCompDiv = executor.submit(generate_comparison_div,toCompData)
    f_sentimentAnalysis = executor.submit(getSentimentAnalysis,ticker)
    f_aLogReturn = executor.submit(annualLogReturn,df)
    f_movingAVG = executor.submit(ThirtyDayEMA,df)
    
    TradeComps_ImpliedPrices = f_TradeComps_ImpliedPrices.result()
    DCF_ImpliedPrice = f_DCF_ImpliedPrice.result()
    toCompDiv = f_toCompDiv.result()
    sentimentAnalysis = f_sentimentAnalysis.result()
    aLogReturn = f_aLogReturn.result()
    movingAVG = f_movingAVG.result()
    monteCarlo = f_monteCarlo.result()
  
    print("Total Time:", time.time()-start_total_time)
    
    return {
        'FullName': FullName,
        'tickerSymbol': tickerData['tickerSymbol'],
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

