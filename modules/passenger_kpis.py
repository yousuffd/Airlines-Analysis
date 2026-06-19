def calculate_passenger_kpis(df):

    passengers = (
        df["passengers"].sum()
    )

    occupancy = (
        df["occupancy"].mean()
    )

    load_factor = (
        df["load_factor"].mean()
    )

    passenger_yield = (
        (
            df["ticket_revenue"].sum()
            +
            df["ancillary_revenue"].sum()
        )
        /
        df["passengers"].sum()
    )

    top_route = (
        df.groupby("route")
        ["passengers"]
        .sum()
        .idxmax()
    )

    return {

        "Passengers":
            passengers,

        "Occupancy":
            occupancy,

        "Load Factor":
            load_factor,

        "Passenger Yield":
            passenger_yield,

        "Top Route":
            top_route
    }