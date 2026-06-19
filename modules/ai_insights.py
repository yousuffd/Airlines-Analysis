def generate_ai_insights(df):

    revenue = (
        df["ticket_revenue"].sum() +
        df["ancillary_revenue"].sum()
    )

    profit = df["profit"].sum()

    otp = (
        df["otp_flag"].mean() * 100
    )

    load_factor = (
        df["load_factor"].mean()
    )

    route = (
        df.groupby("route")["profit"]
        .sum()
        .idxmax()
    )

    return [
        f"Revenue reached ${revenue/1e6:.1f}M.",
        f"Profit generated ${profit/1e6:.1f}M.",
        f"Load factor averaged {load_factor:.1f}%.",
        f"OTP performance is {otp:.1f}%.",
        f"{route} remains the most profitable route."
    ]