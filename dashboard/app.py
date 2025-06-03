import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df

from shiny import App, reactive, render, ui

# curr_list = df["Currency"].unique().tolist()

curr_list = df[["Currency", "Currency Name"]].agg(' - '.join, axis=1).unique().tolist()

app_ui = ui.page_fluid(
ui.input_select(
        "From",
        "From:",
        choices=curr_list,
        selected="USD - United States Dollar"
    ),
    ui.input_numeric(
        "From_Amount",
        "Amount:",
        value=1,
        min=0
    ),
    ui.input_select(
        "To",
        "To:",
        choices=curr_list,
        selected="GBP - British Pound Sterling"
    ),
    ui.input_numeric(
        "To_Amount",
        "Amount:",
        value=1,
        min=0
    ),
    # ui.input_action_button("swap", "Swap Currencies"),
    ui.input_slider(
        "Date_Range",
        "Date Range:",
        min=df["Date"].min(),
        max=df["Date"].max(),
        time_format="%Y-%m-%d",
        value=[df["Date"].min(), df["Date"].max()]
    ),
    ui.output_plot("forex_plot"),
    ui.input_switch("forecast", "Forecast", value=False),
    ui.panel_conditional("input.forecast == true",
                         ui.input_slider(
                             "forecast_days",
                             "Forecast how many days ahead?",
                             min=1,
                             max=30,
                             value=7
                            )
                         ),
    ui.output_text("forecast_val")
    # ui.output_data_frame("filtered_table")
)


def server(input, output, session):
    updating = {"from": False, "to":False, "swap": False}
    
    @reactive.Calc 
    def filtered_df():
        base = input.From()[:3]
        quote = input.To()[:3]
        start_date, end_date = input.Date_Range()
        temp_df = df[
            (df["Currency"] == base) | (df["Currency"] == quote)
        ]
        temp_df = temp_df[
            (temp_df["Date"] >= start_date) & (temp_df["Date"] <= end_date)
        ]
        temp_df = temp_df.pivot(index="Date", columns="Currency", values="ExRate")

        #Now normalizing the forex conversion so that the quote rate is always
        #amount of country 1 currency per one country 2 currency
        temp_df[quote] = temp_df[quote] / temp_df[base]
        temp_df[base] = temp_df[base] / temp_df[base]
        return temp_df

    @reactive.Effect
    def sync_to_amount():
        if updating["swap"]:
            return
        if updating["to"]:
            updating["to"] = False
            return
        
        data = filtered_df()
        base = input.From()[:3]
        quote = input.To()[:3]
        from_amount = input.From_Amount()
        
        if base in data.columns and quote in data.columns:
            # Calculate exhange rate (latest date)
            rate = data[quote].iloc[-1] / data[base].iloc[-1]
            new_to_amount = from_amount * rate
            if abs(input.To_Amount() - new_to_amount) > 1e-8:
                updating["from"] = True
                session.send_input_message("To_Amount", {"value": new_to_amount})


    @reactive.Effect
    def sync_from_amount():
        if updating["swap"]:
            return
        if updating["from"]:
            updating["from"] = False
            return

        data = filtered_df()
        base = input.From()[:3]
        quote = input.To()[:3]
        to_amount = input.To_Amount()
        
        if base in data.columns and quote in data.columns:
            rate = data[quote].iloc[-1] / data[base].iloc[-1]
            new_from_amount = to_amount / rate
            if abs(input.From_Amount() - new_from_amount) > 1e-8:
                updating["to"] = True
                session.send_input_message("From_Amount", {"value": new_from_amount})

    # @reactive.Effect
    # def swap_currencies():
    #     if input.swap() > 0:
    #         from_currency = input.From()
    #         to_currency = input.To()
    #         from_amount = input.From_Amount()
    #         to_amount = input.To_Amount()
    #         updating["swap"] = True

    #         #Swap the currencies
    #         session.send_input_message("From", {"value": to_currency})
    #         session.send_input_message("To", {"value": from_currency})
            
    #         import threading
    #         def finish_swap():
    #             import time
    #             time.sleep(2)

    #             data = filtered_df()
    #             base = to_currency
    #             quote = from_currency
    #             if base in data.columns and quote in data.columns:
    #                 rate = data[quote].iloc[-1] / data[base].iloc[-1]
    #                 new_to_amount = from_amount * rate
    #                 session.send_input_message("To_Amount", {"value": new_to_amount})
    #             updating["swap"] = False
    #         threading.Thread(target=finish_swap).start()
    
    @output 
    @render.plot
    def forex_plot():
        data = filtered_df()
        base = input.From()[:3]
        quote = input.To()[:3]

        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.lineplot(x = data.index, y = data[quote], ax=ax)

        if input.forecast():
            base_code = input.From()[:3]
            quote_code = input.To()[:3]
            start_date, end_date = input.Date_Range()
            n_periods = input.forecast_days()

            payload = {
                "base_code": base_code,
                "quote_code": quote_code,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "n_periods": n_periods
            }

            url = "https://forex-forecast-173754053169.us-west1.run.app/forecast"
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                forecast_result = response.json()["forecast"]

                # Generate future dates starting from last date in date range
                future_dates = pd.date_range(start=pd.to_datetime(end_date), periods = n_periods+1, freq ='D')[1:]

                sns.lineplot(x=future_dates, y=forecast_result, ax=ax, label="Forecast", color = "orange", linestyle="--")
            except Exception as e:
                ax.text(0.5, 0.5, f"Forecast error: {e}", ha = 'center', transform=ax.transAxes, color = 'red')

        ax.set_title(f"Exchange Rate: {base} to {quote}")
        ax.set_ylabel("Exchange Rate")
        ax.set_xlabel("Date")
        return fig

    @output
    @render.text
    def forecast_val():
        return

    # @output 
    # @render.data_frame
    # def filtered_table():
    #     return filtered_df().head(10)

app = App(app_ui, server)