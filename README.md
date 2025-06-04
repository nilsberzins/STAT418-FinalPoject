## Shiny Foreign Exchange Dashboard Backend 

This project is a shiny dashboard that allows the user to access all foreign exchange rates between January 1st, 2021, and May 20th, 2025 (the final day of my free premium access to the forex API). This directory holds all necessary files and scripts for the backend ARIMA model and the preliminary data collection/EDA done in a Jupyter notebook. 
- server.py: Provides the Flask architecture necessary to deploy (and make accessible through curl commands)
- arima_model.py: Holds the forecast() function with the five parameters (From country, To country, start date, end date, and number of days to forecast) to create a quality short-term forecast on the given exchange rate. Forecasts calculated through pmdarima.auto_arima() function.
- Data Collection.ipnyb: Pulls the JSON data from ExchangeRate-API and converts it into a workable pandas data frame. It can also find EDA to find currencies that went defunct within that time frame. 

Also within this file (and deployed with the Flask API) is the ex_rate_full.csv file, which contains all daily USD to [All other traded currencies] from January 1st, 2021, to May 20th, 2025.

**How to access the Flask API**

Users can directly access the Flask API using the curl command structure below:


```curl -X POST https://forex-forecast-173754053169.us-west1.run.app/forecast -H "Content-Type: application/json" -d '{"base_code": "USD", "quote_code": "GBP", "start_date": "2023-01-01", "end_date": "2024-01-01", "n_periods": 10}' ```

See the "dashboard" directory for the frontend Shiny scripts. 

Shiny App Link:
https://rw1djq-nils-berzins.shinyapps.io/forex-dashboard-stat418-final/
