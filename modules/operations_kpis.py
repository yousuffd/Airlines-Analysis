def calculate_operations_kpis(df):

    otp = (
        df["otp_flag"].mean()
        * 100
    )

    delay_rate = (
        (df["delay_minutes"] > 15)
        .mean()
        * 100
    )

    completion_rate = (
        df["completed_flag"].mean()
        * 100
    )

    cancellation_rate = (
        df["cancelled_flag"].mean()
        * 100
    )

    return {

        "OTP": otp,

        "Delay Rate":
            delay_rate,

        "Completion Rate":
            completion_rate,

        "Cancellation Rate":
            cancellation_rate
    }