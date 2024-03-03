import scipy.stats
import yfinance as yf
from fredapi import Fred
import openturns as ot
import equations as eq
from tickerData import Ticker
import pandas as pd
import plotly.express as px
fred = Fred(api_key='a02d5cbed56418e2d72837659e22b8ca')
ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100

def MonteCarloSimluation(variable_dist, variable_names):
    R = ot.CorrelationMatrix(len(variable_dist))
    copula = ot.NormalCopula(R)
    BuiltComposedDistribution = ot.ComposedDistribution(variable_dist, copula)

    generated_sample = BuiltComposedDistribution.getSample(10000)
    df_generated_sample = pd.DataFrame.from_records(generated_sample, columns=variable_names)
    return df_generated_sample


def EquityCost(beta, ExpectedReturn, risk_free_rate):
    beta = ot.Triangular(beta * .9, beta, beta * 1.1)
    ExpectedReturn = ot.Normal(ExpectedReturn, ExpectedReturn * .2)
    risk_free_rate = ot.Normal(risk_free_rate, risk_free_rate * .2)

    variable_dist = [beta, ExpectedReturn, risk_free_rate]
    variable_names = ['beta', 'ExpectedReturn', 'risk_free_rate']

    df_generated_sample = MonteCarloSimluation(variable_dist, variable_names)

    df_generated_sample['EquityCost'] = df_generated_sample.apply(
        lambda row: eq.equityCost(Beta=row.iloc[0], ExpReturn=row.iloc[1], RiskFreeRate=row.iloc[2]), axis=1)
    return df_generated_sample['EquityCost']

def EquityPercent(marketCap, debt):
    debt = ot.Normal(debt, debt * .2)
    marketCap = ot.Normal(marketCap, marketCap * .2)

    variable_dist = [marketCap, debt]
    variable_names = ['marketCap', 'debt']

    df_generated_sample = MonteCarloSimluation(variable_dist, variable_names)

    df_generated_sample['EquityPercent'] = df_generated_sample.apply(
        lambda row: eq.equityPercent(eVal=row.iloc[0]+row.iloc[1], Debt=row.iloc[1]), axis=1)

    df_generated_sample['DebtPercent'] = df_generated_sample.apply(
        lambda row: eq.debtPercent(Debt=row.iloc[1], eVal=row.iloc[0] + row.iloc[1]), axis=1)

    return df_generated_sample

def meanSTD(list):
    mean = sum(list) / len(list)
    variance = sum([((x - mean) ** 2) for x in list]) / len(list)
    res = variance ** 0.5
    return [mean, res]

def WACC(EquityPercent,EquityCost,DebtPercent,CostofDebt,TaxRate):
    TaxRate = ot.Normal(TaxRate, TaxRate*.2)
    CostofDebt = ot.Normal(CostofDebt, CostofDebt*.2)

    variable_dist = [CostofDebt,TaxRate]
    variable_names = ['CostofDebt','TaxRate']

    df_generated_sample = MonteCarloSimluation(variable_dist, variable_names)

    df_generated_sample['EquityPercent'] = EquityPercent
    df_generated_sample['EquityCost'] = EquityCost
    df_generated_sample['DebtPercent'] = DebtPercent

    df_generated_sample['WACC'] = df_generated_sample.apply(
        lambda row: eq.WACC(equityPercent=row.iloc[2], equityCost=row.iloc[3], debtPercent=row.iloc[4], debtCost=row.iloc[0],taxRate=row.iloc[1]), axis=1)

    return df_generated_sample

def presentValueSum(presentValue, PerYGrowth, WCD):
    #presentValue = ot.Normal(presentValue, presentValue*.2)
    PerYGrowth = ot.Distribution(ot.SciPyDistribution(scipy.stats.skewnorm(.99, loc=PerYGrowth, scale=PerYGrowth*.2)))
    #PerYGrowth = ot.Normal(PerYGrowth, PerYGrowth*.2)
    variable_dist = [PerYGrowth]
    variable_names = ['PerYGrowth']

    df_generated_sample = MonteCarloSimluation(variable_dist, variable_names)
    df_generated_sample['PresentValue0'] = presentValue

    for i in range(4):
        df_generated_sample['PresentValue{}'.format(i+1)] = df_generated_sample.apply(
            lambda row: row.iloc[i+1]*(1+row.iloc[0]), axis=1)
    df_generated_sample['WACC'] = WCD[:]['WACC']
    df_generated_sample['PresentValueSum'] = df_generated_sample.apply(
        lambda row: eq.presentValue(CFO=row['PresentValue0'], WACC=row['WACC'], Year=1)
        + eq.presentValue(CFO=row['PresentValue1'], WACC=row['WACC'], Year=2)
        + eq.presentValue(CFO=row['PresentValue2'], WACC=row['WACC'], Year=3)
        + eq.presentValue(CFO=row['PresentValue3'], WACC=row['WACC'], Year=4)
        + eq.presentValue(CFO=row['PresentValue4'], WACC=row['WACC'], Year=5), axis=1)

    return df_generated_sample

def TerminalValue(finalCFO,TargetGrowthRate,WCD):
    TargetGrowthRate = ot.Normal(TargetGrowthRate, TargetGrowthRate*.15)

    variable_dist = [TargetGrowthRate]
    variable_names = ['TargetGrowthRate']

    df_generated_sample = MonteCarloSimluation(variable_dist, variable_names)

    df_generated_sample['FinalCFO'] = finalCFO
    df_generated_sample['WACC'] = WCD[:]['WACC']

    df_generated_sample['TerminalValue'] = df_generated_sample.apply(
        lambda row: eq.tVal(LYCFO=row['FinalCFO'], TGR=row.iloc[0], WACC=row['WACC']), axis=1)

    return df_generated_sample[:]['TerminalValue']

def PresentOfTerminal(TVD, WCD, FinalYear):
    WCD['TerminalValue'] = TVD
    WCD['PresentOfTerminal'] = WCD.apply(
        lambda row: eq.presentTerminalValue(tVal=row['TerminalValue'], WACC=row['WACC'], lYear=FinalYear), axis=1)
    return WCD[:]['PresentOfTerminal']

def EquityValue(EVD,cash,debt):
    cash = ot.Normal(cash, cash*.15)
    debt = ot.Normal(debt, debt*.15)
    variable_dist = [cash, debt]
    variable_names = ['cash', 'debt']

    df_generated_sample = MonteCarloSimluation(variable_dist, variable_names)
    df_generated_sample['EnterpriseValue'] = EVD

    df_generated_sample['EquityValue'] = df_generated_sample.apply(
        lambda row: eq.eVal(enVal=row['EnterpriseValue'], Cash=row.iloc[0], Debt=row.iloc[1]), axis=1)
    return df_generated_sample['EquityValue']

def MonteCarlo(tickerData,PerYGrowth):
    cash = tickerData['cash']
    debt = tickerData['debt']
    shares = tickerData['shares']
    marketCap = tickerData['marketCap']
    risk_free_rate = ten_year_treasury_rate.iloc[-1]
    TargetGrowthRate = .03
    ExpectedReturn = .08
    CostofDebt = .03
    beta = tickerData['beta']
    CFO = tickerData['CFO']
    TaxRate = tickerData['TaxRate']
   
    EC = eq.equityCost(tickerData['beta'], ExpectedReturn, risk_free_rate)
   
    ECD = EquityCost(beta, ExpectedReturn, risk_free_rate)
    
    EP = eq.equityPercent(marketCap + debt, debt)
   
    EPD = EquityPercent(marketCap, debt)['EquityPercent']
    
    DP = eq.debtPercent(debt,marketCap+debt)
    
    DPD = EquityPercent(marketCap, debt)['DebtPercent']
   
    WC = eq.WACC(EP,EC,DP,CostofDebt,TaxRate)
   
    WCD = WACC(EPD,ECD,DPD,CostofDebt,TaxRate)
 
    PVS = eq.presentValue(CFO, WC, 1)
   
    futureCFO = []
    temp = CFO
    year = 2
    for i in range(4):
        temp *= (1 + PerYGrowth)
        futureCFO.append(temp)
        PVS += eq.presentValue(temp, WC, year)
        year += 1
   
    PVSD = presentValueSum(CFO, PerYGrowth,WCD)
    
    TV = eq.tVal(futureCFO[3], TargetGrowthRate, WC)
    
    TVD = TerminalValue(PVSD[:]['PresentValue4'], TargetGrowthRate, WCD)
    
    PoT = eq.presentTerminalValue(TV, WC, 5)
    
    PoTD = PresentOfTerminal(TVD, WCD, 5)
    
    EV = eq.enVal(PVS, PoT)
    
    PVSD['PresentOfTernimal'] = PoTD
    PVSD['EnterpriseValue'] = PVSD.apply(
        lambda row: eq.enVal(presentValueSum=row['PresentValueSum'], presentTerminalValue=row['PresentOfTernimal']), axis=1)
    EVD =  PVSD[:]['EnterpriseValue']

    EQV = eq.eVal(EV,cash,debt)
    
    EQVD = EquityValue(EVD, cash, debt)
    

    ISP = eq.sharePriceImpl(EQV, shares)
    
    WCD['EquityValue'] = EQVD
    WCD['ImpliedSharePrice'] = WCD.apply(
        lambda row: eq.sharePriceImpl(eVal=row['EquityValue'], shares=shares), axis=1)
    ISPD = WCD['ImpliedSharePrice']

    q_low = ISPD.quantile(0.01)
    q_hi = ISPD.quantile(0.935)

    df_filtered = ISPD[(ISPD < q_hi) & (ISPD > q_low)]

    return df_filtered

def main():
    tickerSymbol = 'LSCC'
    ticker = Ticker(tickerSymbol)
    ticker.pullData()
    tickerData = ticker.getData()
    PerYGrowth = .25
    monteCarlo = MonteCarlo(tickerData, PerYGrowth)
    fig = px.histogram(monteCarlo, nbins=65)
    fig.show()

if __name__ == "__main__":
    main()