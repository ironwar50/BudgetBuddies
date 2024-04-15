
import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    connection = MySQLdb.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USERNAME"),
        passwd=os.getenv("DATABASE_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={"ca": "C:\\Users\\17278\\Documents\\MyCourses\\CEN4090L\\cacert-2024-03-11.pem"}
    )
    return connection



def add_data_to_database(new_data):
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Insert new data into the TickerData table
        cursor.execute(
            "INSERT INTO TickerData (CurrentReportDate, Ticker, Revenue, NetIncome, EBITDA, Debt, Cash, Shares, CFO, TaxRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_data['CurrentReportDate'], new_data['Ticker'], new_data['Revenue'], new_data['NetIncome'], new_data['EBITDA'], new_data['Debt'], new_data['Cash'],
             new_data['Shares'], new_data['CFO'], new_data['TaxRate']))

        print("Data added successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def edit_data_in_database(ticker, updated_data):
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Update the data in the TickerData table
        cursor.execute(
            "UPDATE TickerData SET CurrentReportDate = %s, Revenue = %s, NetIncome = %s, EBITDA = %s, Debt = %s, Cash = %s, Shares = %s, CFO = %s, TaxRate = %s WHERE Ticker = %s",
            (updated_data['CurrentReportDate'], updated_data['Revenue'], updated_data['NetIncome'], updated_data['EBITDA'], updated_data['Debt'], updated_data['Cash'],
             updated_data['Shares'], updated_data['CFO'], updated_data['TaxRate'], ticker))

        print("Data updated successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def remove_data_from_database(ticker):
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Delete the data from the TickerData table
        cursor.execute("DELETE FROM TickerData WHERE Ticker = %s", (ticker,))

        print("Data removed successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# Sample data to be added to the database
sample_data = [
    {
        "CurrentReportDate": "2024-01-31 00:00:00",
        "Ticker": "NVDA",
        "Revenue": 60922000000,
        "NetIncome" : 29760000000,
        "EBITDA": 35583000000,
        "Debt": 11056000000,
        "Cash": 25984000000,
        "Shares": 2489750000,
        "CFO": 28090000000,
        "TaxRate": 0.129094
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "INTC",
        "Revenue": 54228000000,
        "NetIncome" : 1690000000,
        "EBITDA": 11242000000,
        "Debt": 49278000000,
        "Cash": 25034000000,
        "Shares": 4165750000,
        "CFO": 11471000000,
        "TaxRate": 0.045911
    },
    {
        "CurrentReportDate": "2023-11-30 00:00:00",
        "Ticker": "MU",
        "Revenue": 16181000000,
        "NetIncome" : -3770000000,
        "EBITDA": 1582000000.0,
        "Debt": 14168000512,
        "Cash": 9048000512,
        "Shares": 1103910016,
        "CFO": 2017000000.0,
        "TaxRate": 0.045911
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "AMD",
        "Revenue": 22680000000.0,
        "NetIncome" : 854000000,
        "EBITDA": 4149000000.0,
        "Debt": 3108999936,
        "Cash": 5773000192,
        "Shares": 1615789952,
        "CFO": 1667000000.0,
        "TaxRate": 0.21
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "MSFT",
        "Revenue": 227583000000.0,
        "NetIncome" : 82540000000,
        "EBITDA": 120925000000.0,
        "Debt": 111358001152,
        "Cash": 80981999616,
        "Shares": 7430439936,
        "CFO": 102647000000.0,
        "TaxRate": 0.21
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "GOOG",
        "Revenue": 307394000000.0,
        "NetIncome" : 73800000000,
        "EBITDA": 97971000000.0,
        "Debt": 29866999808,
        "Cash": 110916001792,
        "Shares": 5671000064,
        "CFO": 101746000000.0,
        "TaxRate": 0.152589
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "AMZN",
        "Revenue": 574785000000.0,
        "NetIncome" : 30420000000,
        "EBITDA": 89402000000.0,
        "Debt": 161573994496,
        "Cash": 86780002304,
        "Shares": 10387399680,
        "CFO": 84946000000.0,
        "TaxRate": 0.223732
    },
    {
        "CurrentReportDate": "2023-10-31 00:00:00",
        "Ticker": "AVGO",
        "Revenue": 35819000000.0,
        "NetIncome" : 11580000000,
        "EBITDA": 20554000000.0,
        "Debt": 40456998912,
        "Cash": 11105000448,
        "Shares": 463420992,
        "CFO": 18085000000.0,
        "TaxRate": 0.111671
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "META",
        "Revenue": 134901000000.0,
        "NetIncome" : 39100000000,
        "EBITDA": 59051000000.0,
        "Debt": 37923999744,
        "Cash": 65402998784,
        "Shares": 2200049920,
        "CFO": 71113000000.0,
        "TaxRate": 0.166002
    },
    {
        "CurrentReportDate": "2023-12-31 00:00:00",
        "Ticker": "AAPL",
        "Revenue": 385706000000.0,
        "NetIncome" : 100910000000,
        "EBITDA": 132867000000.0,
        "Debt": 108040003584,
        "Cash": 73100001280,
        "Shares": 15441899520,
        "CFO": 116433000000.0,
        "TaxRate": 0.159
    }
]


def insert_sample_data():
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()
        #create_ticker_data_table(cursor)

        # Insert each sample data into the database
        for data in sample_data:
            cursor.execute(
                "INSERT INTO TickerData (CurrentReportDate, Ticker, Revenue, NetIncome, EBITDA, Debt, Cash, Shares, CFO, TaxRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (data['CurrentReportDate'], data['Ticker'], data['Revenue'], data['NetIncome'], data['EBITDA'], data['Debt'], data['Cash'],
                 data['Shares'], data['CFO'], data['TaxRate']))

        print("Sample data inserted successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Function to create the TickerData table
def create_ticker_data_table(cursor):
    cursor.execute('''
        CREATE TABLE TickerData (
            PrimaryKey INTEGER PRIMARY KEY,
            CurrentReportDate REAL,
            Ticker TEXT,
            Revenue REAL,
            NetIncome REAL,
            EBITDA REAL,
            Debt REAL,
            Cash TEXT,
            Shares REAL,
            CFO REAL,
            TaxRate REAL
        );
    ''')


# Function to create the temporary TickerData table
def create_temp_ticker_data_table(cursor):
    cursor.execute('''
        DROP TABLE IF EXISTS TickerData_temp;
        CREATE TABLE TickerData_temp (
            SpacerColumn INT
        );
    ''')


# Function to add columns to the temporary TickerData table
def add_columns_to_temp_table(cursor):
    cursor.execute('''
        ALTER TABLE TickerData_temp
        ADD COLUMN CurrentReportDate VARCHAR(255);

        ALTER TABLE TickerData_temp
        ADD COLUMN Ticker VARCHAR(255);

        ALTER TABLE TickerData_temp
        ADD COLUMN Revenue INT;
                   
        ALTER TABLE TickerData_temp
        ADD COLUMN NetIncome INT;

        ALTER TABLE TickerData_temp
        ADD COLUMN EBITDA INT;

        ALTER TABLE TickerData_temp
        ADD COLUMN Debt INT;

        ALTER TABLE TickerData_temp
        ADD COLUMN Cash INT;

        ALTER TABLE TickerData_temp
        ADD COLUMN Shares INT;

        ALTER TABLE TickerData_temp
        ADD COLUMN CFO INT;

        ALTER TABLE TickerData_temp
        ADD COLUMN TaxRate INT;

        ALTER TABLE TickerData_temp
        DROP COLUMN SpacerColumn;
    ''')


# Function to copy data from the original table to the temporary table
def copy_data_to_temp_table(cursor):
    cursor.execute('''
        INSERT INTO TickerData_temp (
            CurrentReportDate,
            Ticker,
            Revenue,
            NetIncome,
            EBITDA,
            Debt,
            Cash,
            Shares,
            CFO,
            TaxRate
        )
        SELECT
            CurrentReportDate,
            Ticker,
            Revenue,
            NetIncome,
            EBITDA,
            Debt,
            Cash,
            Shares,
            CFO,
            TaxRate
        FROM
            TickerData;
    ''')


# Function to replace placeholder values and insert data into the TickerData table
def insert_data_into_ticker_data_table(cursor, values):
    cursor.execute('''
        INSERT INTO TickerData (
            CurrentReportDate,
            Ticker,
            Revenue,
            NetIncome,
            EBITDA,
            Debt,
            Cash,
            Shares,
            CFO,
            TaxRate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)


# Function to drop the original TickerData table
def drop_original_ticker_data_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS TickerData;')


# Function to rename the temporary table to the original table name
def rename_temp_table(cursor):
    cursor.execute('ALTER TABLE TickerData_temp RENAME TO TickerData;')

connection = connect_to_database()
cursor = connection.cursor()

drop_original_ticker_data_table(cursor)



