def calculate_commercial_kpis(df):

    total_revenue = (
        df["ticket_revenue"].sum()
        + df["ancillary_revenue"].sum()
    )

    total_profit = df["profit"].sum()

    total_passengers = df["passengers"].sum()

    total_flights = len(df)

    revenue_per_passenger = (
        total_revenue / total_passengers
    )

    revenue_per_flight = (
        total_revenue / total_flights
    )

    profit_margin = (
        total_profit / total_revenue
    ) * 100

    passenger_yield = (
        total_revenue /
        df["distance_km"].sum()
    )

    top_route = (
        df.groupby("route")["profit"]
        .sum()
        .idxmax()
    )

    return {

        "Revenue": total_revenue,

        "Revenue Per Passenger":
            revenue_per_passenger,

        "Revenue Per Flight":
            revenue_per_flight,

        "Profit Margin":
            profit_margin,

        "Passenger Yield":
            passenger_yield,

        "Top Route":
            top_route
    }