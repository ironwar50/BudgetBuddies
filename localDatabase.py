import sqlite3 as sql
from tickerData import Ticker
import pandas as pd

def create_ticker_data_table():
    with sql.connect('budgetbuddies.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "TickerData" (
                PrimaryKey INTEGER PRIMARY KEY,
                CurrentReportDate TEXT,
                Ticker TEXT,
                Revenue REAL,
                NetIncome REAL,
                EBITDA REAL,
                Debt REAL,
                Cash REAL,
                Shares REAL,
                CFO REAL,
                TaxRate REAL
            );
        ''')

def insertFromTicker(ticker: Ticker):
    tickerData = ticker.getData()
    with sql.connect('budgetbuddies.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""Insert Into TickerData (CurrentReportDate,Ticker,
                    Revenue,NetIncome,EBITDA,Debt,Cash,Shares,CFO,TaxRate)"""
                "Values (?,?,?,?,?,?,?,?,?,?)",(tickerData['reportDate'], tickerData['tickerSymbol'],
                                                tickerData['revenue'], tickerData['netIncome'], tickerData['ebitda'],
                                                tickerData['debt'],tickerData['cash'], tickerData['shares'], 
                                                tickerData['CFO'], tickerData['TaxRate']))

def checkDate(newDate, tickerSymbol)->bool:
    with sql.connect('budgetbuddies.db') as conn:
        cursor = conn.cursor()
        sql_select_query = "select CurrentReportDate from TickerData where Ticker = ?"
        cursor.execute(sql_select_query, [tickerSymbol])
        oldDate = cursor.fetchone()
        if oldDate:
            if oldDate[0]==newDate:
                return True
        return False

def createTicker(tickerSymbol: str) ->Ticker:
    create_ticker_data_table()
    ticker = Ticker(tickerSymbol)
    tickerData = ticker.getData()
    if checkDate(tickerData['reportDate'], tickerSymbol):
        with sql.connect('budgetbuddies.db') as conn:
            conn.row_factory = sql.Row
            cursor = conn.cursor()
            sql_select_query = """select * from TickerData where Ticker = ?"""
            cursor.execute(sql_select_query, [tickerSymbol])
            tickerDB = cursor.fetchone()
            ticker.updateFromDatabase(tickerDB['Revenue'], tickerDB['EBITDA'],tickerDB['NetIncome'], 
                                      tickerDB['Debt'], tickerDB['Cash'], tickerDB['Shares'],
                                      tickerDB['CFO'],  tickerDB['TaxRate'])
    else:
        ticker.pullData()
        insertFromTicker(ticker)
    
    return ticker

# Create the TickerData table
def main():
    with sql.connect('budgetbuddies.db') as conn:
        cursor = conn.cursor()
        create_ticker_data_table()
        tickerSymbol = 'NVDA'
        ticker = Ticker(tickerSymbol)
        ticker.pullData()
        insertFromTicker(ticker)
        cursor.execute("select * from TickerData")
        data = cursor.fetchall()
        print("TickerData Table")
        print(data)
        ticker2 = createTicker(tickerSymbol)
        tickerData = ticker2.getData()
        print("NVDA Ticker2 Data")
        print(tickerData)
        

if __name__ == "__main__":
    main()