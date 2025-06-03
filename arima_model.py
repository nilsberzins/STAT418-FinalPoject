from ctypes import memmove

import pandas as pd

from pmdarima import auto_arima

# CSV saved from data collection notebook
forex_df  = pd.read_csv("ex_rate_all.csv")
forex_df["Date"] = pd.to_datetime(forex_df["Date"])

# # testing on just Great British Pound, short term window since working with daily data
# temp = forex_df[forex_df['Currency'] == "GBP"]
# temp.sort_values('Date', inplace=True)
# y = temp['ExRate'].values
#
# # Using auto.arima to find best configuration for ARIMA models
#     # splitting data up:
# train_size = int(len(y) * 0.8)
# train, test = y[:train_size], y[train_size:]
#
#     #fitting auto_arima()
# model = auto_arima(train,
#                    seasonal=True,
#                    trace=True,
#                    suppress_warnings=True,
#                    stepwise=False)
#
# # Forecasting for length of test set
# n_periods = len(test)
# forecast = model.predict(n_periods=n_periods)

# plt.figure(figsize=(12, 6))
# plt.plot(range(len(train)), train, label='Training')
# plt.plot(range(len(train), len(train) + len(test)), test, label='Test')
# plt.plot(range(len(train), len(train) + len(forecast)), forecast, label='Forecast')
# plt.legend()
# plt.title('USD/GBP Exchange Rate Forecast')
# plt.xlabel('Time Index')
# plt.ylabel('Exchange Rate')
# plt.grid(True)
# plt.show()


def forecast(base_code = 'USD', quote_code = 'EUR', start_date = forex_df["Date"].min(), end_date = forex_df["Date"].max(), n_periods = 7):
    temp_df = forex_df[
        (forex_df["Currency"] == base_code) | (forex_df["Currency"] == quote_code)
    ]

    temp_df = temp_df[
        (temp_df["Date"] >= start_date) & (temp_df["Date"] <= end_date)
    ]

    temp_df = temp_df.pivot(index="Date", columns="Currency", values="ExRate")

    #B/c all exchange rates are USD-to rates, dividing quote by base will create the correct Country X to Country Y exchange rate.
    temp_df["Correct_Rate"] = temp_df[quote_code] / temp_df[base_code]

    y = temp_df["Correct_Rate"].values

    model = auto_arima(y,
                       seasonal=True,
                       trace=True,
                       suppress_warnings=True,
                       stepwise=False)

    forecast_values = model.predict(n_periods=n_periods)

    return forecast_values
