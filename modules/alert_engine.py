def generate_alerts(kpis):

    alerts = []

    if kpis["OTP"] < 80:

        alerts.append(
            (
                "danger",
                "OTP below target."
            )
        )

    if kpis["Load Factor"] < 75:

        alerts.append(
            (
                "warning",
                "Load factor below target."
            )
        )

    if kpis["Profit"] > 0:

        alerts.append(
            (
                "success",
                "Profitability healthy."
            )
        )

    return alerts