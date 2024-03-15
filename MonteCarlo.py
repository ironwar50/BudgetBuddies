import scipy.stats
import yfinance as yf
from fredapi import Fred
import openturns as ot
import equations as eq
from tickerData import Ticker
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()

fred_api_key = os.getenv('FRED_API_KEY')
fred = Fred(api_key=fred_api_key)
ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100

def meanSTD(list):
    mean = sum(list) / len(list)
    variance = sum([((x - mean) ** 2) for x in list]) / len(list)
    res = variance ** 0.5
    return [mean, res]

'''
Performs Monte Carlo simulation on DCF model. Takes in input variables
required to perform DCF, then creates distributions based on them.
The distrubtions are combined and a dataframe with 100,000 simulations is generated. 
New distributions are added by making calculations on the 
existing columns and storing the data in a new column. 
This is done same as previous in the DCF, just for 100,000 data points. This creates 
a distributions of valuations which can be used to create a graph.
'''
def MonteCarloSimulation(beta, ExpectedReturn, risk_free_rate, debt, 
                         marketCap, TaxRate, CostofDebt, PerYGrowth, 
                         TargetGrowthRate, cash, presentValue, shares):
    beta = ot.Triangular(beta * .9, beta, beta * 1.1)
    ExpectedReturn = ot.Normal(ExpectedReturn, ExpectedReturn * .1)
    risk_free_rate = ot.Normal(risk_free_rate, risk_free_rate * .1)
    debt = ot.Normal(debt, debt * .1)
    marketCap = ot.Normal(marketCap, marketCap * .1)
    TaxRate = ot.Normal(TaxRate, TaxRate*.1)
    CostofDebt = ot.Normal(CostofDebt, CostofDebt*.1)
    PerYGrowth = ot.Normal(PerYGrowth, PerYGrowth*.1)
    TargetGrowthRate = ot.Normal(TargetGrowthRate, TargetGrowthRate*.1)
    cash = ot.Normal(cash, cash*.1)
    presentValue = ot.Normal(presentValue, presentValue*.1)
    shares = ot.Normal(shares, shares*.1)

    variable_dist = [beta, ExpectedReturn, risk_free_rate, debt, marketCap, 
                     TaxRate, CostofDebt, PerYGrowth, TargetGrowthRate, cash, 
                     presentValue, shares]
    variable_names = ['beta', 'ExpectedReturn', 'risk_free_rate', 'debt', 
                      'marketCap', 'TaxRate', 'CostofDebt', 'PerYGrowth', 
                      'TargetGrowthRate', 'cash', 'presentValue', 'shares']

    R = ot.CorrelationMatrix(len(variable_dist))
    copula = ot.NormalCopula(R)
    BuiltComposedDistribution = ot.ComposedDistribution(variable_dist, copula)
    generated_sample = BuiltComposedDistribution.getSample(100000)
    df_generated_sample = pd.DataFrame.from_records(generated_sample, 
                                                    columns=variable_names)

    df_generated_sample['EquityCost'] = df_generated_sample.apply(
        lambda row: eq.equityCost(Beta=row.iloc[0], ExpReturn=row.iloc[1], 
                                  RiskFreeRate=row.iloc[2]), axis=1)
    
    
    df_generated_sample['EquityPercent'] = df_generated_sample.apply(
        lambda row: eq.equityPercent(eVal=row.iloc[3]+row.iloc[4], 
                                     Debt=row.iloc[3]), axis=1)

    df_generated_sample['DebtPercent'] = df_generated_sample.apply(
        lambda row: eq.debtPercent(Debt=row.iloc[3], 
                                   eVal=row.iloc[4] + row.iloc[3]), axis=1)
    
    df_generated_sample['WACC'] = df_generated_sample.apply(
        lambda row: eq.WACC(equityPercent=row['EquityPercent'], 
                            equityCost=row['EquityCost'], debtPercent=row['DebtPercent'], 
                            debtCost=row.iloc[6],taxRate=row.iloc[5]), axis=1)
    
    df_generated_sample['PresentValue0'] = df_generated_sample['presentValue']

    for i in range(4):
        df_generated_sample['PresentValue{}'.format(i+1)] = df_generated_sample.apply(
            lambda row: row['PresentValue{}'.format(i)]*(1+row.iloc[7]), axis=1)

    df_generated_sample['PresentValueSum'] = df_generated_sample.apply(
        lambda row: eq.presentValue(CFO=row.iloc[10], WACC=row['WACC'], Year=1)
        + eq.presentValue(CFO=row['PresentValue1'], WACC=row['WACC'], Year=2)
        + eq.presentValue(CFO=row['PresentValue2'], WACC=row['WACC'], Year=3)
        + eq.presentValue(CFO=row['PresentValue3'], WACC=row['WACC'], Year=4)
        + eq.presentValue(CFO=row['PresentValue4'], WACC=row['WACC'], Year=5), axis=1)
    
    df_generated_sample['TerminalValue'] = df_generated_sample.apply(
        lambda row: eq.tVal(LYCFO=row['PresentValue4'], TGR=row.iloc[8], 
                            WACC=row['WACC']), axis=1)
    
    df_generated_sample['PresentOfTerminal'] = df_generated_sample.apply(
        lambda row: eq.presentTerminalValue(tVal=row['TerminalValue'], 
                                            WACC=row['WACC'], lYear=5), axis=1)
    
    df_generated_sample['EnterpriseValue'] = df_generated_sample.apply(
        lambda row: eq.enVal(presentValueSum=row['PresentValueSum'], 
                             presentTerminalValue=row['PresentOfTerminal']), axis=1)
    
    df_generated_sample['EquityValue'] = df_generated_sample.apply(
        lambda row: eq.eVal(enVal=row['EnterpriseValue'], Cash=row.iloc[9], 
                            Debt=row.iloc[3]), axis=1)
    
    df_generated_sample['ImpliedSharePrice'] = df_generated_sample.apply(
        lambda row: eq.sharePriceImpl(eVal=row['EquityValue'], 
                                      shares=row.iloc[11]), axis=1)
    
    return df_generated_sample['ImpliedSharePrice']

def MonteCarlo(tickerData,PerYGrowth):
    """Gets necessesary data to perfrom DCF, calls the MonteCarloSimulation, 
    then removes outlier from distribution

    Args:
        tickerData (Dict): Dictionary of ticker data.
        PerYGrowth (Float): User inputed average per year growth rate  

    Returns:
        df_filter: List containing distribution of valuations
    """
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
   
    ISPD = MonteCarloSimulation(beta, ExpectedReturn, risk_free_rate, debt, 
                                marketCap, TaxRate, CostofDebt, PerYGrowth, 
                                TargetGrowthRate, cash, CFO, shares)

    q_low = ISPD.quantile(0.005)
    q_hi = ISPD.quantile(0.99)

    df_filtered = ISPD[(ISPD < q_hi) & (ISPD > q_low)]

    return df_filtered

#for testing
def main():
    tickerSymbol = 'NVDA'
    ticker = Ticker(tickerSymbol)
    ticker.pullData()
    tickerData = ticker.getData()
    PerYGrowth = .65
    monteCarlo = MonteCarlo(tickerData, PerYGrowth)
    fig = px.histogram(monteCarlo, nbins=65)
    fig.show()

if __name__ == "__main__":
    main()
