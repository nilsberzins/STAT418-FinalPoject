## Shiny Foregin Exchange Rate Dashboard Frontend

This directory holds the python scripts necessary to create a functioning, interactive Shiny dashboard to display the foreign exchange rate data and forecasts. 

- app.py: Holds all UI and Server code to make a deployable foreign exchange dashboard onto shinappys.io, including a function to request to the Flask API endpoint to get the forecasted forex rates 
- shared.py: Grabs the exchange rate data from ex_rate_all.csv (not present in repository due to file size), makes two small data cleaning adjustments before making the dataframe sendable to the shiny app script

Shiny app link: https://rw1djq-nils-berzins.shinyapps.io/forex-dashboard-stat418-final/
