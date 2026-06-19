import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_airline_data(num_records=15000):

    np.random.seed(42)
    random.seed(42)

    airlines = [
        "SkyJet Airways",
        "Global Wings",
        "AeroConnect",
        "Nimbus Air",
        "Blue Horizon"
    ]

    airports = [
        "DEL",
        "BOM",
        "BLR",
        "HYD",
        "MAA",
        "CCU",
        "DXB",
        "SIN",
        "LHR",
        "JFK"
    ]

    aircraft_types = [
        "A320",
        "A321",
        "B737",
        "B787",
        "A350"
    ]
    weather_conditions = [
        "Clear",
        "Rain",
        "Storm",
        "Fog"
    ]

    market_types = [
        "Domestic",
        "International"
    ]

    fare_mix = [
        "Economy Heavy",
        "Balanced",
        "Premium Heavy"
    ]

    start_date = datetime(2021, 1, 1)
    end_date = datetime(2025, 12, 31)

    date_range = (end_date - start_date).days

    rows = []

    for i in range(num_records):

        flight_date = start_date + timedelta(
            days=random.randint(0, date_range)
        )

        origin, destination = random.sample(airports, 2)

        route = f"{origin}-{destination}"

        market_type = (
            "International"
            if destination in ["DXB", "SIN", "LHR", "JFK"]
            else "Domestic"
        )

        fare_class_mix = np.random.choice(
            fare_mix,
            p=[0.60, 0.30, 0.10]
        )

        weather_condition = np.random.choice(
            weather_conditions,
            p=[0.70, 0.15, 0.10, 0.05]
        )
        
        delay_reason = np.random.choice(
            [
                "Weather",
                "ATC",
                "Technical",
                "Crew",
                "Airport Congestion"
            ],
            p=[0.25, 0.20, 0.15, 0.10, 0.30]
        )

        fuel_price_index = round(
            np.random.uniform(80, 140),
            2
        )

        airport_congestion_index = round(np.random.uniform(40, 100),2)

        aircraft = random.choice(aircraft_types)

        distance = random.randint(300, 7500)

        seats = random.randint(120, 320)

        passengers = int(seats * np.random.uniform(0.60, 0.98))

        load_factor = round((passengers / seats) * 100, 2)

        occupancy = load_factor

        base_delay = max(0,int(np.random.normal(15, 10)))

        weather_delay = {
            "Clear": 0,
            "Rain": 10,
            "Storm": 30,
            "Fog": 20
        }

        delay = (
            base_delay +
            weather_delay[weather_condition] +
            int(airport_congestion_index / 10)
        )
        status = np.random.choice(
            ["Completed", "Cancelled"],
            p=[0.97, 0.03]
        )

        otp_flag = 1 if delay <= 15 else 0

        completed_flag = (1 if status == "Completed" else 0)

        cancelled_flag = (1 if status == "Cancelled" else 0)

        scheduled_dep = datetime.combine(flight_date.date(),datetime.min.time()) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))

        actual_dep = scheduled_dep + timedelta(minutes=delay)

        flight_hours = distance / 800

        scheduled_arr = scheduled_dep + timedelta(hours=flight_hours)

        actual_arr = scheduled_arr + timedelta(minutes=delay)

        ticket_revenue = (passengers * np.random.uniform(120, 550))

        ancillary_revenue = (passengers * np.random.uniform(5, 45))

        fuel_cost = distance * np.random.uniform(2.5,5.5)

        crew_cost = distance * np.random.uniform(0.4,1.2)

        maintenance_cost = distance * np.random.uniform(0.5,1.8)

        operating_cost = (fuel_cost + crew_cost + maintenance_cost)

        total_revenue = (ticket_revenue + ancillary_revenue)

        profit = (total_revenue - operating_cost)

        profit_margin = (profit / total_revenue) * 100

        fuel_burn = (distance * np.random.uniform(2,4))

        utilization_hours = round(flight_hours,2)

        casm = (operating_cost / (distance * seats))

        rask = (total_revenue / (distance * seats))

        co2 = fuel_burn * 3.16

        rows.append({

            "flight_id": f"FLT{i+1:06d}",
            "date": flight_date,
            "airline": random.choice(airlines),
            "route": route,
            "origin": origin,
            "destination": destination,
            "aircraft_type": aircraft,
            "market_type": market_type,
            "fare_class_mix": fare_class_mix,
            "weather_condition": weather_condition,
            "delay_reason": delay_reason,
            "fuel_price_index": fuel_price_index,
            "airport_congestion_index": airport_congestion_index,
            "otp_flag": otp_flag,
            "completed_flag": completed_flag,
            "cancelled_flag": cancelled_flag,
            "distance_km": distance,
            "scheduled_departure": scheduled_dep,
            "actual_departure": actual_dep,
            "scheduled_arrival": scheduled_arr,
            "actual_arrival": actual_arr,
            "delay_minutes": delay,
            "status": status,
            "available_seats": seats,
            "occupied_seats": passengers,
            "passengers": passengers,
            "load_factor": load_factor,
            "occupancy": occupancy,
            "ticket_revenue": round(ticket_revenue, 2),
            "ancillary_revenue": round(ancillary_revenue, 2),
            "fuel_cost": round(fuel_cost, 2),
            "crew_cost": round(crew_cost, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "operating_cost": round(operating_cost, 2),
            "profit": round(profit, 2),
            "profit_margin": round(profit_margin, 2),
            "fuel_burn_liters": round(fuel_burn, 2),
            "utilization_hours": utilization_hours,
            "casm": round(casm, 4),
            "rask": round(rask, 4),
            "co2_emissions": round(co2, 2)
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_airline_data(
        num_records=15000
    )

    df.to_csv(
        "data/airline_data.csv",
        index=False
    )

    print(
        f"Generated {len(df)} rows."
    )
 