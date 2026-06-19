def calculate_health_score(kpis):

    score = 0

    revenue_score = min(
        kpis["Revenue"] / 100000000,
        1
    ) * 25

    profit_score = min(
        kpis["Profit"] / 20000000,
        1
    ) * 25

    otp_score = (
        kpis["OTP"] / 100
    ) * 20

    load_factor_score = (
        kpis["Load Factor"] / 100
    ) * 15

    score = (
        revenue_score +
        profit_score +
        otp_score +
        load_factor_score +
        15
    )

    return round(score, 1)