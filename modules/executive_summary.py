import pandas as pd


def generate_executive_summary(df):

    total_revenue = (
        df["ticket_revenue"].sum() +
        df["ancillary_revenue"].sum()
    )

    total_profit = df["profit"].sum()

    avg_load_factor = (
        df["load_factor"].mean()
    )

    otp = (
        (df["delay_minutes"] <= 15)
        .mean() * 100
    )

    top_route = (
        df.groupby("route")["profit"]
        .sum()
        .idxmax()
    )

    narrative = f"""
Revenue reached ${total_revenue/1e6:.1f}M across the reporting period.

Profit generated was ${total_profit/1e6:.1f}M.

Average load factor remained strong at {avg_load_factor:.1f}%.

OTP performance is currently {otp:.1f}%.

The most profitable route is {top_route}.
"""

    return narrative