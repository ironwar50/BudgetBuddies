import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime as dt
import BuggetBuddies as eq
import PageLayouts as pl

app = dash.Dash(__name__)
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
TradeComps_ImpliedPrices = eq.TradeComps(toComp, tickerData['cash'], tickerData['debt'], tickerData['shares'], tickerData['eps'])
DCF_ImpliedPrice = eq.DiscountedCashFlow(ticker, PerYGrowth,  tickerData['tickerCashFlow'], tickerData['cash'], tickerData['debt'], tickerData['marketCap'], tickerData['shares'])
toCompDiv = []
for data in toCompData:
    toCompDiv.append(html.P(str(data[0])+":   "+str(data[1]),style={'display' : 'inline-block','margin-left' : '50px'}))
app.layout = pl.Dashboard(FullName, symbol, LastClose, TrailingPE, ForwardPE, avgAnalystTarget,DCF_ImpliedPrice,PerYGrowth,
              fig, toCompDiv, TradeComps_ImpliedPrices)

if __name__ == "__main__":
    app.run()