9 Files  
-Main (start app)  
-PageLayouts (stores layouts for each page)  
-Algorithm (contains contains functions to calculate DCF and Trade Cmomps)   
-Database  
-Dashboard (Get input data and calls functions to get data for dashboard)  
-navbar (sets up moving between pages)  
-equations (stores equation function to be used in algorithm)  
-tickerData (stores ticker class which contains methods for geting and pulling data)  
-MonteCarlo.py (performs the monte carlo simulations)   


At least 3 layouts  
-Start  
-Prompt Kris    
-Dashboard  

Alogorithm (2 functinos)  
-trade comps (returns 3 calculated share prices)  
-DCF (returns an implied share price and a few data points)  


Database Polly  
-Create table with necessary variables  
-Check if ticker is in database  
-Check if date stored matches most recent date  
-Store data from ticker object  
-Create ticker object from stored data  


Main   
-start app with navbar  


Dashboard  
-gets input data   
-calls all necessary functions to get data for dashboard  
-create_dashboard function that returns dictionary of dashboard data  


navbar  
-calls page layouts  
-handles switching between pages  


equations  
-contains necessary equations for calling in algorithm and monte carlo simluaiton.  


tickerData  
-contains ticker class which stores all data needed for a ticker  
-can be initialized with just the ticker symbol or with necessary data.  
-contains pullData and getData method for retrieve data from the yfinance and returning data as dictionary  
-method for pefroming sentiment analysis  


Monte Carlo  
-runs monte carlo simulations of DCF  
-returns a distrubtion of valuations for displaying in graph  


Error Checking  
-check if tickers entered exist  
-check if data needed exists  
-check for outlier data  


Problems  
-unreliable data (ex. POWI)  
-negative numbers  
-dashboard loads slow  
-Dashboard formating for screen size  
-sensitive to wrong data  

