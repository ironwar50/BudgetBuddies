import dash
from dash import html
from PageLayouts import Dashboard 
import datetime as dt
import yfinance as yf
import BudgetBuddies as eq
import plotly.graph_objects as go
from tickerData import Ticker


def create_dashboard():
    end = dt.datetime.now()
    start = end - dt.timedelta(days = 365*3)
    tickerSymbol = 'LSCC'
    ticker = Ticker(tickerSymbol)
    ticker.pullData()
    tickerData = ticker.getData()
    toComp = [Ticker('MTSI'),Ticker('POWI'),
              Ticker('QRVO'),Ticker('RMBS'),Ticker('SLAB')]
    PerYGrowth = .25
    toCompData = []
    for comp in toComp:
        compData = comp.getData()
        tick = compData['ticker']
        temp = (tick.info['symbol'], tick.info['previousClose'])
        toCompData.append(temp)
    df = tickerData['ticker'].history(start = start, end = end)
    #df = df['Close']
    #fig = px.line(df, " "," ", title="LSCC")
    fig = go.Figure(data=[go.Candlestick(
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = "LSCC")])
    tickerInfo = tickerData['ticker'].info
    FullName = tickerInfo['longName']
    LastClose = tickerInfo['previousClose']
    TrailingPE = tickerInfo['trailingPE']
    ForwardPE = tickerInfo['forwardPE']
    avgAnalystTarget = tickerInfo['targetMeanPrice']
    TradeComps_ImpliedPrices = eq.TradeComps(toComp, tickerData)
    DCF_ImpliedPrice = eq.DiscountedCashFlow(tickerData,PerYGrowth)
    toCompDiv = []
    x = 0
    for data in toCompData:
        if x > 0: 
            toCompDiv.append(html.P(str(data[0])+":   "+str(data[1]),style={'display' : 'inline-block', 'margin-left' : '50px'}))
        else:
            toCompDiv.append(html.P(str(data[0])+":   "+str(data[1]),style={'display' : 'inline-block'}))
            x+=1
            
    return Dashboard(FullName, tickerSymbol, LastClose, TrailingPE, ForwardPE, avgAnalystTarget,DCF_ImpliedPrice,PerYGrowth,
                fig, toCompDiv, TradeComps_ImpliedPrices)