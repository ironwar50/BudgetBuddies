import dash
from dash import html
from PageLayouts import Dashboard 
import datetime as dt
import yfinance as yf
import BudgetBuddies as eq
import plotly.graph_objects as go


def create_dashboard():
    end = dt.datetime.now()
    start = end - dt.timedelta(days = 365*3)
    ticker = 'LSCC'
    symbol = ticker.upper()
    ticker = ticker = yf.Ticker(symbol)
    toComp = [yf.Ticker('MTSI'),yf.Ticker('MPWR'),yf.Ticker('QRVO'),yf.Ticker('RMBS'),yf.Ticker('SLAB')]
    PerYGrowth = .25
    toCompData = []
    for comp in toComp:
        temp = (comp.info['symbol'], comp.info['previousClose'])
        toCompData.append(temp)
    df = ticker.history(start = start, end = end)
    #df = df['Close']
    #fig = px.line(df, " "," ", title="LSCC")
    fig = go.Figure(data=[go.Candlestick(
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = "LSCC")])
    tickerInfo = ticker.info
    FullName = tickerInfo['longName']
    LastClose = tickerInfo['previousClose']
    TrailingPE = tickerInfo['trailingPE']
    ForwardPE = tickerInfo['forwardPE']
    avgAnalystTarget = tickerInfo['targetMeanPrice']
    tickerData = eq.pullTickerData(ticker)
    TradeComps_ImpliedPrices = eq.TradeComps(toComp, tickerData['cash'], tickerData['debt'], tickerData['shares'], tickerData['eps'], tickerData['ebitda'], tickerData['revenue'])
    DCF_ImpliedPrice = eq.DiscountedCashFlow(ticker, PerYGrowth,  tickerData['tickerCashFlow'], tickerData['cash'], tickerData['debt'], tickerData['marketCap'], tickerData['shares'])
    toCompDiv = []
    x = 0
    for data in toCompData:
        if x > 0: 
            toCompDiv.append(html.P(str(data[0])+":   "+str(data[1]),style={'display' : 'inline-block', 'margin-left' : '50px'}))
        else:
            toCompDiv.append(html.P(str(data[0])+":   "+str(data[1]),style={'display' : 'inline-block'}))
            x+=1
            
    return Dashboard(FullName, symbol, LastClose, TrailingPE, ForwardPE, avgAnalystTarget,DCF_ImpliedPrice,PerYGrowth,
                fig, toCompDiv, TradeComps_ImpliedPrices)