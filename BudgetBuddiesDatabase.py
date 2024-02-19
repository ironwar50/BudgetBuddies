import sqlite3

# Function to create the TickerData table
def create_ticker_data_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "TickerData" (
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
        );
    ''')

# Function to create the temporary TickerData table
def create_temp_ticker_data_table(cursor):
    cursor.execute('''
        DROP TABLE IF EXISTS "TickerData_temp";
        CREATE TABLE "TickerData_temp" (
            SpacerColumn INT
        );
    ''')

# Function to add columns to the temporary TickerData table
def add_columns_to_temp_table(cursor):
    cursor.execute('''
        ALTER TABLE "TickerData_temp"
        ADD COLUMN CurrentReportDate VARCHAR(255);
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN Ticker VARCHAR(255);
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN Revenue INT;
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN EBITDA INT;
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN Debt INT;
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN Cash INT;
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN Shares INT;
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN CFO INT;
        
        ALTER TABLE "TickerData_temp"
        ADD COLUMN TaxRate INT;
        
        ALTER TABLE "TickerData_temp"
        DROP COLUMN SpacerColumn;
    ''')

# Function to copy data from the original table to the temporary table
def copy_data_to_temp_table(cursor):
    cursor.execute('''
        INSERT INTO "TickerData_temp" (
            CurrentReportDate,
            Ticker,
            Revenue,
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
            EBITDA,
            Debt,
            Cash,
            Shares,
            CFO,
            TaxRate
        FROM
            "TickerData";
    ''')

# Function to replace placeholder values and insert data into the TickerData table
def insert_data_into_ticker_data_table(cursor, values):
    cursor.execute('''
        INSERT INTO TickerData (
            CurrentReportDate,
            Ticker,
            Revenue,
            EBITDA,
            Debt,
            Cash,
            Shares,
            CFO,
            TaxRate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)

# Function to drop the original TickerData table
def drop_original_ticker_data_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS "TickerData";')

# Function to rename the temporary table to the original table name
def rename_temp_table(cursor):
    cursor.execute('ALTER TABLE "TickerData_temp" RENAME TO "TickerData";')


# Example usage:

# Connect to the SQLite database
conn = sqlite3.connect('budgetbuddies.db')
cursor = conn.cursor()

# Create the TickerData table
create_ticker_data_table(cursor)

# Create the temporary TickerData table
create_temp_ticker_data_table(cursor)

# Add columns to the temporary table
add_columns_to_temp_table(cursor)

# Copy data from the original table to the temporary table
copy_data_to_temp_table(cursor)

# Drop the original table
drop_original_ticker_data_table(cursor)

# Rename the temporary table to the original table name
rename_temp_table(cursor)

# Replace placeholder values and insert data into the TickerData table
user_input_values = (2, 2, 2, 2, 2, 2, 2, 2, 2)  # Example values
insert_data_into_ticker_data_table(cursor, user_input_values)

# Commit changes and close connection
conn.commit()
conn.close()
