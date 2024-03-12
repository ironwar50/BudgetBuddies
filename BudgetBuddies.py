import yfinance as yf
from fredapi import Fred
from dotenv import load_dotenv
import os

load_dotenv()

fred_api_key = os.getenv('FRED_API_KEY')

fred = Fred(api_key=fred_api_key)
ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100

def enterprise_value(market_cap, debt, cash):
    return market_cap + debt - cash

def revenue_multiple(enterprise_value, revenue):
    return enterprise_value / revenue

def ebitda_multiple(enterprise_value, ebitda):
    return enterprise_value / ebitda

def pe_ratio(market_cap, net_income):
    return market_cap / net_income

def implied_ev_from_revenue(revenue_multiple, revenue):
    return revenue_multiple * revenue

def implied_ev_from_ebitda(ebitda_multiple, ebitda):
    return ebitda_multiple * ebitda

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def impliedValueRevenue(IEVR, Cash, Debt):
    result = (IEVR + Cash - Debt) # are you sure its as simple as this?
    if result != 0:
        return result
    else:
        return None
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def impliedValueEBITDA(IEVE, Cash, Debt):
    result = (IEVE + Cash - Debt) # once again, are you sure its as simple as this?
    if result != 0:
        return result
    else:
        return None
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def impliedValueNetIncome(EPS, Shares, PtoE):
    result = (EPS * Shares * PtoE)
    if result != 0:
        return result
    else:
        return None
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def impliedSharePriceRevenue(IEQVR, Shares):
    result = IEQVR / Shares
    if result != 0:
        return result
    else:
        return None
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def impliedSharePriceEBITDA(IEQVE, Shares):
    result = IEQVE / Shares
    if result != 0:
        return result
    else:
        return None
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def impliedSharePriceNetIncome(IEQVN, Shares):
    result = IEQVN / Shares
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def equityCost(Beta, ExpReturn, RiskFreeRate):
    result = RiskFreeRate + (Beta * (ExpReturn - RiskFreeRate))
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def equityPercent(eVal, Debt):
    result =  eVal / (Debt+ eVal)
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def debtPercent(Debt, eVal):
    result = Debt / (Debt + eVal)
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def WACC(equityPercent, equityCost, debtPercent, debtCost, taxRate):
    result = ((equityPercent * equityCost) + (debtPercent * debtCost * (1 - taxRate)))
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def tVal(LYCFO, TGR, WACC):
    result = ((LYCFO * (1 + TGR)) / (WACC - TGR))
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def presentValue(CFO, WACC, Year):
    result = (CFO / ((1 + WACC)**Year))
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def presentTerminalValue(tVal, WACC, lYear):
    result = (tVal / ((1 + WACC)**lYear))
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def enVal(presentValueSum, presentTerminalValue):
    result = (presentValueSum + presentTerminalValue)
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def eVal(enVal, Cash, Debt):
    result = (enVal + Cash - Debt)
    if result != 0:
        return result
    else:
        return None

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def sharePriceImpl(eVal, shares):
    if shares != 0:
        return eVal / shares
    else:
        print("An exception has occurred.")
        return None

def pullTickerData(ticker):
    tickerIncome = ticker.quarterly_income_stmt.transpose() 
    tickerBalance = ticker.quarterly_balance_sheet.transpose()
    tickerCashFlow = ticker.quarterly_cash_flow.transpose()
    marketCap = ticker.info['regularMarketPreviousClose'] * tickerIncome['Diluted Average Shares'].iloc[0]
    revenue = 0
    ebitda = 0
    netIncome = 0
    eps = 0
    cash = tickerBalance['Cash Cash Equivalents And Short Term Investments'].iloc[0]
    debt = tickerBalance['Total Debt'].iloc[0]
    shares = tickerIncome['Diluted Average Shares'].iloc[0]
    for i in range(4):
        eps += tickerIncome['Diluted EPS'].iloc[i]
        revenue += tickerIncome['Total Revenue'].iloc[i]
        ebitda += tickerIncome['Total Revenue'].iloc[i]
        netIncome += tickerIncome['Net Income'].iloc[i]
    return {"tickerCashFlow" : tickerCashFlow, "marketCap" : marketCap, "revenue" : revenue, "ebitda" : ebitda, 
            "netIncome" : netIncome, "eps" : eps, "cash" : cash, "debt" : debt, "shares" : shares}
   
def TradeComps(toComp, cash, debt, shares, eps):
    AVG_rev_multi = 0 
    AVG_EBITDA_multi = 0
    AVG_PE_ratio = 0
    for tick in toComp: 
        tickIncome = tick.quarterly_income_stmt.transpose()
        tickBalance = tick.quarterly_balance_sheet.transpose()
        marketCap = tick.info['regularMarketPreviousClose']* tickIncome['Diluted Average Shares'].iloc[0]
        revenue = 0
        ebitda = 0
        netIncome = 0
        for i in range(4):
            revenue += tickIncome['Total Revenue'].iloc[i]
            ebitda += tickIncome['EBITDA'].iloc[i]
            netIncome += tickIncome['Net Income'].iloc[i]
        if 'Total Debt' in tickBalance.keys():
            debt = tickBalance['Total Debt'].iloc[0]
        else:
            debt = 0
        EV = enterprise_value(marketCap,debt,tickBalance['Cash Cash Equivalents And Short Term Investments'].iloc[0])
        AVG_rev_multi += revenue_multiple(EV, revenue)
        AVG_EBITDA_multi += ebitda_multiple(EV, ebitda)
        AVG_PE_ratio += pe_ratio(marketCap, netIncome)
    AVG_rev_multi /= 5
    AVG_EBITDA_multi /= 5
    AVG_PE_ratio /= 5
    revenue_SharePrice = impliedSharePriceRevenue(impliedValueRevenue(implied_ev_from_revenue(AVG_rev_multi,revenue),cash,debt),shares)
    ebitda_SharePrice = impliedSharePriceEBITDA(impliedValueEBITDA(implied_ev_from_ebitda(AVG_EBITDA_multi,ebitda),cash,debt),shares)
    NetIncome_SharePrice = impliedSharePriceNetIncome(impliedValueNetIncome(eps, shares, AVG_PE_ratio),shares)
    ImpliedSharePrices = {"revenue_SharePrice" : revenue_SharePrice, "ebitda_SharePrice" : ebitda_SharePrice, "netIncome_SharePrice" : NetIncome_SharePrice}
    return ImpliedSharePrices

def DiscountedCashFlow(ticker,PerYGrowth,tickerCashFlow,cash,debt,marketCap,shares):
    CFO = 0
    for i in range(4):
        CFO += tickerCashFlow['Cash Flow From Continuing Operating Activities'].iloc[i]
    risk_free_rate = ten_year_treasury_rate.iloc[-1]
    taxRate = ticker.income_stmt.transpose()['Tax Rate For Calcs'].iloc[0]
    beta = ticker.info['beta']
    TargetGrowthRate = .03
    ExpectedReturn = .08
    CostofDebt = .03
    EquityCost = equityCost(beta, .08, risk_free_rate)
    EquityPercent = equityPercent(marketCap + debt, debt)
    DebtPercent = debtPercent(debt,marketCap+debt)
    wacc = WACC(EquityPercent,EquityCost,DebtPercent,CostofDebt,taxRate)
    presentValueSum = presentValue(CFO,wacc,1)
    futureCFO = []
    temp = CFO
    for i in range(4):
        temp *= (1 + PerYGrowth)
        futureCFO.append(temp)
        presentValueSum += presentValue(temp,wacc,i+2)
    terminalValue = tVal(futureCFO[3],TargetGrowthRate,wacc)
    PresentOfTerminal = presentTerminalValue(terminalValue,wacc,5)
    EnterpriseValue = enVal(presentValueSum,PresentOfTerminal)
    EquityValue = eVal(EnterpriseValue,cash,debt)
    ImpliedSharePrice = sharePriceImpl(EquityValue, shares)
    return {"ImpliedSharePrice" : ImpliedSharePrice, "FreeCashFlow" : CFO, "LastYearCashFlow" : futureCFO[3]}

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
