def calculate_core_kpis(df):

    revenue = (
        df["ticket_revenue"].sum() +
        df["ancillary_revenue"].sum()
    )

    profit = (
        df["profit"].sum()
    )

    passengers = (
        df["passengers"].sum()
    )

    load_factor = (
        df["load_factor"].mean()
    )

    otp = (
        df["otp_flag"].mean()
        * 100
    )

    return {

        "Revenue": revenue,
        "Profit": profit,
        "Passengers": passengers,
        "Load Factor": load_factor,
        "OTP": otp

    }


