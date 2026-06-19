def calculate_fleet_kpis(df):

    avg_utilization = (
        df["utilization_hours"]
        .mean()
    )

    fuel_efficiency = (
        df["distance_km"].sum()
        /
        df["fuel_burn_liters"].sum()
    )

    avg_casm = (
        df["casm"].mean()
    )

    avg_rask = (
        df["rask"].mean()
    )

    fleet_profit = (
        df["profit"].sum()
    )

    top_aircraft = (
        df.groupby("aircraft_type")
        ["profit"]
        .sum()
        .idxmax()
    )

    return {

        "Utilization":
            avg_utilization,

        "Fuel Efficiency":
            fuel_efficiency,

        "CASM":
            avg_casm,

        "RASK":
            avg_rask,

        "Fleet Profit":
            fleet_profit,

        "Top Aircraft":
            top_aircraft
    }