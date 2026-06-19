def calculate_sustainability_kpis(df):

    total_co2 = (
        df["co2_emissions"]
        .sum()
    )

    total_fuel = (
        df["fuel_burn_liters"]
        .sum()
    )

    passengers = (
        df["passengers"]
        .sum()
    )

    co2_per_passenger = (
        total_co2 / passengers
    )

    fuel_efficiency = (
        df["distance_km"].sum()
        /
        total_fuel
    )

    greenest_aircraft = (
        df.groupby("aircraft_type")
        ["co2_emissions"]
        .mean()
        .idxmin()
    )

    sustainability_score = max(
        0,
        min(
            100,
            100 - co2_per_passenger
        )
    )

    return {

        "CO2":
            total_co2,

        "CO2 Per Passenger":
            co2_per_passenger,

        "Fuel":
            total_fuel,

        "Fuel Efficiency":
            fuel_efficiency,

        "Greenest Aircraft":
            greenest_aircraft,

        "Score":
            sustainability_score
    }