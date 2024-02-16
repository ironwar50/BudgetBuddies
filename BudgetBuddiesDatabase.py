import sqlite3

conn = sqlite3.connect('budgetbuddies.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS TickerData''')
cursor.execute('''CREATE TABLE TickerData (
                    PrimaryKey INTEGER PRIMARY KEY,
                    CurrentReportDate TEXT,
                    Ticker TEXT,
                    Revenue REAL,
                    EBITDA REAL,
                    Debt REAL,
                    Cash TEXT,
                    Shares REAL,
                    CFO REAL,
                    TaxRate REAL
                )''')

