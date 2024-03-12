import yfinance as yf
import pandas as pd
import requests
from dotenv import load_dotenv
import os

def checkData(tickerData):
    for key in tickerData.keys():
        if (not key == 'tickerSymbol' and not key == 'ticker' 
        and not key == 'reportDate' and str(tickerData[key])[0] < 'z' 
        and str(tickerData[key])[0] > 'A'):
            tickerData[key] = 0

class Ticker:
    def __init__(self, tickerSymbol, revenue=0, ebitda=0, netIncome = 0, 
                 debt=0, cash=0, shares=0, CFO=0, TaxRate=0, PE = 0, 
                 marketCap = 0, enterpriseValue = 0, enterpriseToRevenue = 0, 
                 enterpriseToEbitda = 0, eps = 0, beta = 0):
        self.tickerSymbol = tickerSymbol.upper()
        self.ticker = yf.Ticker(self.tickerSymbol) 
        tickerInfo = self.ticker.info
        try:
            self.reportDate = self.ticker.earnings_dates.index[4]
        except:
            print("KEY ERROR")
            self.reportDate = ''
            self.tickerSymbol = -1
        self.revenue = revenue
        self.ebitda = ebitda
        self.netIncome = netIncome
        self.debt = debt
        self.cash = cash
        self.shares = shares
        self.CFO = CFO
        self.TaxRate = TaxRate
        if 'trailingPE' in tickerInfo.keys():
            self.PE = tickerInfo['trailingPE']
        elif 'forwardPE' in tickerInfo.keys():
            self.PE = tickerInfo['forwardPE']
        else: 
            self.PE = PE 
        if 'marketCap' in tickerInfo.keys():
            self.marketCap = tickerInfo['marketCap']
        else:
            self.marketCap = marketCap
        if 'enterpriseValue' in tickerInfo.keys():
            self.enterpriseValue = tickerInfo['enterpriseValue']
        else: 
            self.enterpriseValue = enterpriseValue
        if 'enterpriseToRevenue' in tickerInfo.keys():
            self.enterpriseToRevenue = tickerInfo['enterpriseToRevenue']
        else: 
            self.enterpriseToRevenue = enterpriseToRevenue
        if 'enterpriseToEbitda' in tickerInfo.keys():
            self.enterpriseToEbitda = tickerInfo['enterpriseToEbitda']
        else: 
            self.enterpriseToEbitda = enterpriseToEbitda
        if 'trailingEps' in tickerInfo.keys():
            self.eps = tickerInfo['trailingEps']
        elif 'forwardEps' in tickerInfo.keys(): 
            self.eps = tickerInfo['forwardEps']
        else:
            self.eps = eps
        if 'beta' in tickerInfo.keys():
            self.beta = tickerInfo['beta']
        else:
            self.beta = beta
        
        
    def updateFromDatabase(self, revenue, ebitda, netIncome, debt, cash, shares, 
                 CFO, TaxRate):
        self.revenue = revenue
        self.ebitda = ebitda
        self.netIncome = netIncome
        self.debt = debt
        self.cash = cash
        self.shares = shares
        self.CFO = CFO
        self.TaxRate = TaxRate

    def sentimentAnalysis(self):
        load_dotenv()
        alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')
        symbol = self.ticker.info['symbol'].upper().strip()
        url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={}&apikey={}".format(symbol, alpha_vantage_key)
        r = requests.get(url)
        data = r.json()
        sentimentTotal = 0
        for feed in data['feed']:
            for sentiment in feed['ticker_sentiment']:
                if sentiment['ticker'] == symbol:
                    if sentiment['ticker_sentiment_label'] == "Bearish":
                        sentimentTotal -= 2
                    elif sentiment['ticker_sentiment_label'] == 'Somewhat-Bearish':
                        sentimentTotal -= 1
                    elif sentiment['ticker_sentiment_label'] == 'Somewhat-Bullish':
                        sentimentTotal += 1
                    elif sentiment['ticker_sentiment_label'] == 'Bullish':
                        sentimentTotal += 2
        if(sentimentTotal > 5):
            return 'Bullish'
        elif(sentimentTotal < -5):
            return 'Bearish'
        return 'Neutral'
        
    def pullData(self):
        ticker = self.ticker
        tickerIncome = ticker.quarterly_income_stmt 
        tickerIncome = tickerIncome.transpose()
        tickerBalance = ticker.quarterly_balance_sheet.transpose()                                                              
        tickerCashFlow = ticker.quarterly_cash_flow.transpose()
        tickerInfo = ticker.info
        self.marketCap = ticker.info['marketCap']
        revenue = 0
        ebitda = 0
        netIncome = 0 
        cfo = 0
        for i in range(4):                                                                                                      
            revenue += tickerIncome['Total Revenue'].iloc[i]
            ebitda += tickerIncome['EBITDA'].iloc[i]
            netIncome += tickerIncome['Net Income'].iloc[i] 
            cfo += tickerCashFlow['Cash Flow From Continuing Operating Activities'].iloc[i]
        self.revenue = revenue
        self.ebitda = ebitda
        self.netIncome = netIncome                                                                                                
        if 'totalCash' in tickerInfo.keys():
            self.cash = tickerInfo['totalCash']
        elif "Total Debt" in tickerBalance.keys():
            self.cash = tickerBalance['Cash Cash Equivalents And Short Term Investments'].iloc[0]
        else: 
            self.cash = 0
        if 'totalDebt' in tickerInfo.keys():
            self.debt = tickerInfo['totalDebt']
        elif "Total Debt" in tickerBalance.keys():
            self.debt = tickerBalance['Total Debt'].iloc[0]
        else: 
            self.debt = 0
        self.shares = tickerInfo['sharesOutstanding'] 
        self.CFO = cfo
        self.TaxRate = tickerIncome['Tax Rate For Calcs'].iloc[0]
    
    def getData(self):
        tickerData =  {'tickerSymbol': self.tickerSymbol, 'ticker' : self.ticker,
                       'revenue': self.revenue,'ebitda' : self.ebitda, 
                'netIncome' : self.netIncome,'debt' : self.debt,'cash' : self.cash,
                'shares' : self.shares,'CFO' : self.CFO,'TaxRate' : self.TaxRate,
                'PE' : self.PE, 'marketCap' : self.marketCap,
                'enterpriseValue' : self.enterpriseValue, 
                'enterpriseToRevenue' : self.enterpriseToRevenue, 
                'enterpriseToEbitda' : self.enterpriseToEbitda,'eps' : self.eps, 
                'beta' : self.beta, 'reportDate': str(self.reportDate)}
        checkData(tickerData)
        return tickerData
                                       

        

        
