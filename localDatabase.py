import MySQLdb as sql
import MySQLdb.cursors as cursors
import os
from tickerData import Ticker
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    connection = sql.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USERNAME"),
            passwd=os.getenv("DATABASE_PASSWORD"),
            db=os.getenv("DATABASE"),
            cursorclass=cursors.DictCursor,
            autocommit=True,
            ssl_mode="VERIFY_IDENTITY",
            ssl={
                "ca": "/etc/ssl/certs/ca-certificates.crt"
            }
        )
    return connection


def create_ticker_data_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TickerData (
            id int(11) NOT NULL AUTO_INCREMENT,PRIMARY KEY (id),
            CurrentReportDate FLOAT(11),
            Ticker VARCHAR(255),
            Revenue FLOAT(15,2),
            NetIncome FLOAT(15,2),
            EBITDA FLOAT(15,2),
            Debt FLOAT(15,2),
            Cash FLOAT(15,2),
            Shares FLOAT(15,2),
            CFO FLOAT(15,2),
            TaxRate FLOAT(5,2)
        );
    ''')

#insert into table if ticker doesn't already exits, update if it does
def insertFromTicker(ticker: Ticker,conn):
    tickerData = ticker.getData()
    cursor = conn.cursor()
    cursor.execute("""select Ticker from TickerData""")
    tickers = cursor.fetchall()
    if not tickerData['tickerSymbol'] in tickers:
        cursor.execute("""Insert Into TickerData (CurrentReportDate,Ticker,
                    Revenue,NetIncome,EBITDA,Debt,Cash,Shares,CFO,TaxRate)
                Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(tickerData['reportDate'], tickerData['tickerSymbol'],
                                                tickerData['revenue'], tickerData['netIncome'], 
                                                tickerData['ebitda'],tickerData['debt'],
                                                tickerData['cash'], tickerData['shares'], 
                                                tickerData['CFO'], tickerData['TaxRate']))
    else:
        sql_update_query = ("""UPDATE TickerData
                            SET CurrentReportDate=%s, Revenue=%s, NetIncome=%s, EBITDA=%s,
                            Debt=%s, Cash=%s, Shares=%s, CFO=%s, TaxRate=%s
                            WHERE Ticker=%s""")
        cursor.execute(sql_update_query, [tickerData['reportDate'], tickerData['revenue'],
                                            tickerData['netIncome'],tickerData['ebitda'], 
                                            tickerData['debt'],tickerData['cash'],
                                            tickerData['shares'],tickerData['CFO'],
                                            tickerData['TaxRate'],tickerData['tickerSymbol']])
#check if date newly pulled matches stored data
def checkDate(newDate, tickerSymbol,conn)->bool:
    cursor = conn.cursor()
    sql_select_query = "select CurrentReportDate from TickerData where Ticker = %s"
    cursor.execute(sql_select_query, [tickerSymbol])
    oldDate = cursor.fetchone()
    print(oldDate, newDate)
    if oldDate:
        if oldDate['CurrentReportDate']==newDate:
            print("Hello")
            return True
    return False

#create new ticker from database or by pulling data based on the checkdate function
#if date doesn't match or ticker not in database add data to database. 
#Return -1 if ticker not found
def createTicker(tickerSymbol):
    with connect_to_database() as conn:
        create_ticker_data_table(conn)
        ticker = Ticker(tickerSymbol)

        tickerData = ticker.getData()
        if tickerData['tickerSymbol'] == -1: return -1

        if checkDate(tickerData['reportDate'], tickerSymbol, conn):
            cursor = conn.cursor()
            sql_select_query = """select * from TickerData where Ticker = %s"""
            cursor.execute(sql_select_query, [tickerSymbol])
            tickerDB = cursor.fetchone()
            ticker.updateFromDatabase(tickerDB['Revenue'], tickerDB['EBITDA'],
                                        tickerDB['NetIncome'], tickerDB['Debt'], 
                                        tickerDB['Cash'], tickerDB['Shares'],
                                        tickerDB['CFO'],  tickerDB['TaxRate'])
        else:
            ticker.pullData()
            insertFromTicker(ticker, conn)
    
    return ticker

    