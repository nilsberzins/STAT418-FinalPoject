from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "ex_rate_all.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df = df[df["Currency"] != "SLE"]