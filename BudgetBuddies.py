import yfinance as yf
from fredapi import Fred
import equations as eq
fred = Fred(api_key='a02d5cbed56418e2d72837659e22b8ca')
ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100

'''
Checks for occurences of missing data and sets it to zero
'''
def checkData(tickerData):
    for data in tickerData:
        if not data < 0 or not data > 0:
            return 0
    return tickerData

'''
This function pulls all necessary data that is needed for calculations with a given ticker.
Returns a dictionary of with the data. 
'''
def pullTickerData(ticker):
    tickerIncome = ticker.quarterly_income_stmt.transpose() 
    tickerBalance = ticker.quarterly_balance_sheet.transpose()                                                              
    tickerCashFlow = ticker.quarterly_cash_flow.transpose()
    tickerData = {}
    tickerData['makerCap'] = ticker.info['regularMarketPreviousClose'] * tickerIncome['Diluted Average Shares'].iloc[0]     
    tickerData['revenue'] = 0
    tickerData['ebitda'] = 0
    tickerData['netIncome'] = 0                                                                                                 
    tickerData['eps'] = 0
    tickerData['cash'] = tickerBalance['Cash Cash Equivalents And Short Term Investments'].iloc[0]
    tickerData['debt'] = tickerBalance['Cash Cash Equivalents And Short Term Investments'].iloc[0]
    tickerData['shares'] = tickerIncome['Diluted Average Shares'].iloc[0]
    for i in range(4):                                                                                                      
        tickerData['revenue'] += tickerIncome['Total Revenue'].iloc[i]
        tickerData['ebitda'] += tickerIncome['Total Revenue'].iloc[i]
        tickerData['netIncome'] += tickerIncome['Net Income'].iloc[i]
    tickerData = checkData(tickerData)                                                                                      
    return {"tickerCashFlow" : tickerCashFlow, "marketCap" :  tickerData['makerCap'], "revenue" : tickerData['revenue'], "ebitda" : tickerData['ebitda'], 
            "netIncome" : tickerData['netIncome'], "eps" : tickerData['eps'], "cash" : tickerData['cash'], "debt" : tickerData['debt'], "shares" : tickerData['shares']} 
   
'''
Performs the Trade Comps calculation. 
Takes in the tickers being compared to along with the cash, debt, number of shares, and EPS of the target ticker.
Returns a dictionary with the three calculated shares prices on revenue, EBITDA, and net income/Price to Earnings
'''
def TradeComps(toComp, cash, debt, shares, eps):
    AVG_rev_multi = 0 
    AVG_EBITDA_multi = 0
    AVG_PE_ratio = 0
    for tick in toComp: 
        tickIncome = tick.quarterly_income_stmt.transpose()
        tickBalance = tick.quarterly_balance_sheet.transpose()
        tickData = {}
        tickData['marketCap'] = tick.info['regularMarketPreviousClose']* tickIncome['Diluted Average Shares'].iloc[0]
        tickData['revenue'] = 0
        tickData['ebitda'] = 0
        tickData['netIncome'] = 0
        for i in range(4):                                              
            tickData['revenue'] += tickIncome['Total Revenue'].iloc[i]
            tickData['ebitda']  += tickIncome['EBITDA'].iloc[i]
            tickData['netIncome'] += tickIncome['Net Income'].iloc[i]
        if 'Total Debt' in tickBalance.keys():
            debt = tickBalance['Total Debt'].iloc[0]
        else:
            debt = 0
        tickData['cash'] = tickBalance['Cash Cash Equivalents And Short Term Investments'].iloc[0]
        tickerData = checkData(tickerData)
        EV = eq.enterprise_value(tickData['marketCap'],debt,tickData['cash'])
        AVG_rev_multi += eq.revenue_multiple(EV, tickData['revenue'])
        AVG_EBITDA_multi += eq.ebitda_multiple(EV, tickData['ebitda'])
        AVG_PE_ratio += eq.pe_ratio(tickData['marketCap'], tickData['netIncome'])
    AVG_rev_multi /= 5
    AVG_EBITDA_multi /= 5
    AVG_PE_ratio /= 5
    revenue_SharePrice = eq.impliedSharePriceRevenue(eq.impliedValueRevenue(eq.implied_ev_from_revenue(AVG_rev_multi,tickData['revenue']),cash,debt),shares)
    ebitda_SharePrice = eq.impliedSharePriceEBITDA(eq.impliedValueEBITDA(eq.implied_ev_from_ebitda(AVG_EBITDA_multi,tickData['ebitda']),cash,debt),shares)
    NetIncome_SharePrice = eq.impliedSharePriceNetIncome(eq.impliedValueNetIncome(eps, shares, AVG_PE_ratio),shares)
    
    return {"revenue_SharePrice" : revenue_SharePrice, "ebitda_SharePrice" : ebitda_SharePrice, "netIncome_SharePrice" : NetIncome_SharePrice}

'''
Performs the Discounted Cash Flow calculation.
Takes in the ticker, an averages estimated per year growth, the cashflow sheet, cash, debt, market cap, and number of shares of a given ticker.
It returns a dictionary with the calculated shares price with the first and last year cash flow.
'''

def DiscountedCashFlow(ticker,PerYGrowth,tickerCashFlow,cash,debt,marketCap,shares):
    tickerData = {}
    tickerData['CFO'] = 0
    for i in range(4):
        tickerData['CFO'] += tickerCashFlow['Cash Flow From Continuing Operating Activities'].iloc[i]
    risk_free_rate = ten_year_treasury_rate.iloc[-1]
    tickerData['taxRate'] = ticker.income_stmt.transpose()['Tax Rate For Calcs'].iloc[0]
    tickerData['beta'] = ticker.info['beta']
    tickerData = checkData(tickerData)
    TargetGrowthRate = .03
    ExpectedReturn = .08
    CostofDebt = .03
    EquityCost = eq.equityCost(tickerData['beta'], ExpectedReturn, risk_free_rate)
    EquityPercent = eq.equityPercent(marketCap + debt, debt)
    DebtPercent = eq.debtPercent(debt,marketCap+debt)
    wacc = eq.WACC(EquityPercent,EquityCost,DebtPercent,CostofDebt,tickerData['taxRate'])
    presentValueSum = eq.presentValue(tickerData['CFO'],wacc,1)
    futureCFO = []
    temp = tickerData['CFO']
    for i in range(4):
        temp *= (1 + PerYGrowth)
        futureCFO.append(temp)
        presentValueSum += eq.presentValue(temp,wacc,i+2)
    terminalValue = eq.tVal(futureCFO[3],TargetGrowthRate,wacc)
    PresentOfTerminal = eq.presentTerminalValue(terminalValue,wacc,5)
    EnterpriseValue = eq.enVal(presentValueSum,PresentOfTerminal)
    EquityValue = eq.eVal(EnterpriseValue,cash,debt)
    ImpliedSharePrice = eq.sharePriceImpl(EquityValue, shares)
    return {"ImpliedSharePrice" : ImpliedSharePrice, "FreeCashFlow" : tickerData['CFO'], "LastYearCashFlow" : futureCFO[3]}

def main():
    print("Enter the ticker you would like to evaluate: ")
    ticker = 'LSCC'
    ticker = yf.Ticker(ticker.upper())
    print("Enter five similiar companies to compare to:")
    '''for i in range(5):
        temp = input()
        toComp.append(yf.Ticker(temp.upper()))'''
    toComp = [yf.Ticker('MTSI'),yf.Ticker('POWI'),yf.Ticker('QRVO'),yf.Ticker('RMBS'),yf.Ticker('SLAB')]
    PerYGrowth = .25
    tickerData = pullTickerData(ticker)
    TradeCompPrices = TradeComps(toComp, tickerData['cash'], tickerData['debt'], tickerData['shares'], tickerData['eps'])
    print("--Trading Comps--")
    print("Implied Share Price from Revenue: ", TradeCompPrices['revenue_SharePrice'])
    print("Implied Share Price from EBITDA: ", TradeCompPrices['ebitda_SharePrice'])
    print("Implied Share Price from P/E: ", TradeCompPrices['netIncome_SharePrice'])
    print()
    '''variables = [CFO,ExpectedReturn,risk_free_rate,beta,taxRate,CostofDebt,cash,debt,marketCap,EquityCost,debt+marketCap,EquityPercent, DebtPercent,wacc,terminalValue,presentValueSum,PresentOfTerminal,EnterpriseValue,EquityValue,shares,ImpliedSharePrice]
    for x in variables:
        print(x)'''
    print("--Discounted Cash Flow--")
    print("Discounted Cash Flow Implied Share Price: ", DiscountedCashFlow(ticker,PerYGrowth,tickerData['tickerCashFlow'],tickerData['cash'],tickerData['debt'],tickerData['marketCap'],tickerData['shares']))
    print()
    print("Real Share Price:", ticker.info['regularMarketPreviousClose'])

if __name__ == "__main__":
    main()