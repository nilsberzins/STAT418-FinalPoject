## Shiny Foreign Exchange Dashboard Backend 

This project is a shiny dashboard that allows the user access to all foreign exchange rates between January 1st, 2021 and May 20th 2025 (final day of my free premium access to the forex api). This directory holds all necessary files and scripts for the backend ARIMA model. The python script server.py provides the flask architecture necessary to deploy (and make accessable through curl commands) the arima_model.py script. Within this script holds the forecast() function with the fie parameters (From country, To country, start date, end date, and number of days to forecast) to create a quality short-term forecast on the given exchange rate.

Also within this file (and deployed with the flask API) is the full .csv file containing all daily USD to [All other traded currencies] from January 1st, 2021 to May 20th, 2025.
