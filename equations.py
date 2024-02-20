'''
Enterprise value is a measure of the total value of a company
Necessary for calculating various ratios
'''
def enterprise_value(market_cap, debt, cash): 
    result = market_cap + debt - cash 
    if result != 0:
        return result
    else:
        return None

'''
The ratio of enterprise value to revenue
For the trading comps it is necessary to get an average of 
these next three ratios. This is done in order to compare and 
calculate with a target ticker.
'''
def revenue_multiple(enterprise_value, revenue):
    result = enterprise_value / revenue 
    if result != 0:
        return result
    else:
        return None 
'''
The ratio of enterprise value to ebitda
'''
def ebitda_multiple(enterprise_value, ebitda):
    result = enterprise_value / ebitda
    if result != 0:
        return result
    else:
        return None 
'''
Price to Earning (P/E) is the ratio of the total value of a company 
based on share price to it's net income. It's also commonly calculated
from it price per share to it's earnings per share.
'''     
def pe_ratio(market_cap, net_income):
    result = market_cap / net_income
    if result != 0:
        return result
    else:
        return None 

'''
This takes a revenue multiple and multiplies it by a given revenue
in order to get an implied enterprise value. This is necessary for 
calculating a implied equity value from revenue
'''
def implied_ev_from_revenue(revenue_multiple, revenue):
    result = revenue_multiple * revenue
    if result != 0:
        return result
    else:
        return None 
     
'''
This takes a ebitda multiple and multiplies it by a given ebitda
in order to get an implied enterprise value. This is necessary for 
calculating a implied equity value from ebitda
''' 
def implied_ev_from_ebitda(ebitda_multiple, ebitda):
    result = ebitda_multiple * ebitda
    if result != 0:
        return result
    else:
        return None

'''
This takes the implied enterprise value based of revenue along with
the cash and debt of the target ticker. It uses this to calculate 
and implied equity value. This can then directly be used to calculate 
the imlied share price based on revenue
'''   
def impliedValueRevenue(IEVR, Cash, Debt):
    result = (IEVR + Cash - Debt) 
    if result != 0:
        return result
    else:
        return None

'''
This takes the implied enterprise value based of ebitda along with
the cash and debt of the target ticker. It uses this to calculate 
and implied equity value. This can then directly be used to calculate 
the imlied share price based on ebitda
'''   
def impliedValueEBITDA(IEVE, Cash, Debt):
    result = (IEVE + Cash - Debt) 
    if result != 0:
        return result
    else:
        return None

'''
This takes the average P/E ratio of comparative companies, 
along with the earnings per share, and number of shares of the 
target ticker. This is used to calculate the equity value based on net
income.
'''
def impliedValueNetIncome(EPS, Shares, PtoE):
    result = (EPS * Shares * PtoE)
    if result != 0:
        return result
    else:
        return None

'''
The next three equations calculate an implied share price by
taking in an implied equity value and dividing by the number of
shares.
'''
def impliedSharePriceRevenue(IEQVR, Shares):
    result = IEQVR / Shares
    if result != 0:
        return result
    else:
        return None
def impliedSharePriceEBITDA(IEQVE, Shares):
    result = IEQVE / Shares
    if result != 0:
        return result
    else:
        return None
def impliedSharePriceNetIncome(IEQVN, Shares):
    result = IEQVN / Shares
    if result != 0:
        return result
    else:
        return None

def equityCost(Beta, ExpReturn, RiskFreeRate):
    result = RiskFreeRate + (Beta * (ExpReturn - RiskFreeRate))
    if result != 0:
        return result
    else:
        return None

def equityPercent(eVal, Debt):
    result =  eVal / (Debt+ eVal)
    if result != 0:
        return result
    else:
        return None

def debtPercent(Debt, eVal):
    result = Debt / (Debt + eVal)
    if result != 0:
        return result
    else:
        return None

def WACC(equityPercent, equityCost, debtPercent, debtCost, taxRate):
    result = ((equityPercent * equityCost) + (debtPercent * debtCost * (1 - taxRate)))
    if result != 0:
        return result
    else:
        return None

def tVal(LYCFO, TGR, WACC):
    result = ((LYCFO * (1 + TGR)) / (WACC - TGR))
    if result != 0:
        return result
    else:
        return None

def presentValue(CFO, WACC, Year):
    result = (CFO / ((1 + WACC)**Year))
    if result != 0:
        return result
    else:
        return None

def presentTerminalValue(tVal, WACC, lYear):
    result = (tVal / ((1 + WACC)**lYear))
    if result != 0:
        return result
    else:
        return None

def enVal(presentValueSum, presentTerminalValue):
    result = (presentValueSum + presentTerminalValue)
    if result != 0:
        return result
    else:
        return None

def eVal(enVal, Cash, Debt):
    result = (enVal + Cash - Debt)
    if result != 0:
        return result
    else:
        return None

def sharePriceImpl(eVal, shares):
    if shares != 0:
        return eVal / shares
    else:
        print("An exception has occurred.")
        return None