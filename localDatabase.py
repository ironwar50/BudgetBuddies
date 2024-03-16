import sqlite3 as sql
from tickerData import Ticker

def create_ticker_data_table():
    with sql.connect('budgetbuddies.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "TickerData" (
                PrimaryKey INTEGER PRIMARY KEY,
                CurrentReportDate REAL,
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

#insert into table if ticker doesn't already exits, update if it does
def insertFromTicker(ticker: Ticker):
    tickerData = ticker.getData()
    with sql.connect('budgetbuddies.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""select Ticker from TickerData""")
        tickers = cursor.fetchall()
        if not tickerData['tickerSymbol'] in tickers:
            cursor.execute("""Insert Into TickerData (CurrentReportDate,Ticker,
                        Revenue,NetIncome,EBITDA,Debt,Cash,Shares,CFO,TaxRate)"""
                    "Values (?,?,?,?,?,?,?,?,?,?)",(tickerData['reportDate'], tickerData['tickerSymbol'],
                                                    tickerData['revenue'], tickerData['netIncome'], 
                                                    tickerData['ebitda'],tickerData['debt'],
                                                    tickerData['cash'], tickerData['shares'], 
                                                    tickerData['CFO'], tickerData['TaxRate']))
        else:
            sql_update_query = ("""UPDATE TickerData
                                SET CurrentReportDate=?, Revenue=?, NetIncome=?, EBITDA=?,
                                Debt=?, Cash=?, Shares=?, CFO=?, TaxRate=? 
                                WHERE Ticker=?""")
            cursor.execute(sql_update_query, [tickerData['reportDate'], tickerData['revenue'],
                                              tickerData['netIncome'],tickerData['ebitda'], 
                                              tickerData['debt'],tickerData['cash'],
                                              tickerData['shares'],tickerData['CFO'],
                                              tickerData['TaxRate'],tickerData['tickerSymbol']])
#check if date newly pulled matches stored data
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

#create new ticker from database or by pulling data based on the checkdate function
#if date doesn't match or ticker not in database add data to database. 
#Return -1 if ticker not found
def createTicker(tickerSymbol):
    create_ticker_data_table()
    ticker = Ticker(tickerSymbol)

    tickerData = ticker.getData()
    if tickerData['tickerSymbol'] == -1: return -1

    if checkDate(tickerData['reportDate'], tickerSymbol):
        print("Database")
        with sql.connect('budgetbuddies.db') as conn:
            conn.row_factory = sql.Row
            cursor = conn.cursor()
            sql_select_query = """select * from TickerData where Ticker = ?"""
            cursor.execute(sql_select_query, [tickerSymbol])
            tickerDB = cursor.fetchone()
            ticker.updateFromDatabase(tickerDB['Revenue'], tickerDB['EBITDA'],
                                      tickerDB['NetIncome'], tickerDB['Debt'], 
                                      tickerDB['Cash'], tickerDB['Shares'],
                                      tickerDB['CFO'],  tickerDB['TaxRate'])
    else:
        print("Pulling Data")
        ticker.pullData()
        insertFromTicker(ticker)
    
    return ticker

#for testing
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
