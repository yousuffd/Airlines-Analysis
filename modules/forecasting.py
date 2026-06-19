import pandas as pd
from sklearn.linear_model import LinearRegression


def generate_forecast(df, metric, periods=4):

    monthly = (
        df.groupby(df["date"].dt.to_period("Q"))[metric]
        .sum()
        .reset_index()
    )

    monthly["quarter_period"] = monthly["date"]
    monthly["date"] = monthly["date"].astype(str)
    monthly["month_idx"] = range(len(monthly))

    monthly["quarter"] = (monthly["quarter_period"].dt.quarter)

    X = monthly[["month_idx", "quarter"]]

    y = monthly[metric]

    model = LinearRegression()

    model.fit(X, y)

    future = pd.DataFrame({
        "month_idx": range(
            len(monthly),
            len(monthly) + periods
        )
    })

    future["quarter"] = [
        ((i - len(monthly)) % 4) + 1
        for i in future["month_idx"]
    ]

    future[metric] = model.predict(future)
    last_period = pd.Period(
        monthly["date"].iloc[-1],
        freq="Q"
    )

    future["date"] = [
        str(last_period + i + 1)
        for i in range(periods)
    ]

    return monthly, future