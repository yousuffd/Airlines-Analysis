import streamlit as st

from modules.data_loader import load_data

from modules.ui_components import (
    load_css,
    page_header,
    metric_card
)

from modules.sustainability_kpis import (
    calculate_sustainability_kpis
)

from modules.config import configure_page
configure_page()

from modules.chart_builders import (
    co2_trend,
    fuel_consumption_trend,
    aircraft_emissions,
    emissions_by_market
)

load_css()

from modules.filters import global_filters

df = load_data()
df = global_filters(df)

kpis = calculate_sustainability_kpis(df)

page_header(
    "Sustainability",
    "Environmental & ESG Performance"
)

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    metric_card(
        "CO2",
        f"{kpis['CO2']/1e6:.1f}M"
    )

with c2:
    metric_card(
        "CO2 / Pax",
        f"{kpis['CO2 Per Passenger']:.2f}"
    )

with c3:
    metric_card(
        "Fuel Burn",
        f"{kpis['Fuel']/1e6:.1f}M"
    )

with c4:
    metric_card(
        "Fuel Efficiency",
        f"{kpis['Fuel Efficiency']:.2f}"
    )

with c5:
    metric_card(
        "Greenest Aircraft",
        kpis["Greenest Aircraft"]
    )

with c6:
    metric_card(
        "ESG Score",
        f"{kpis['Score']:.0f}"
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        co2_trend(df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fuel_consumption_trend(df),
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        aircraft_emissions(df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        emissions_by_market(df),
        use_container_width=True
    )

st.markdown("---")

st.subheader("Sustainability Detail")

table = (
    df.groupby("aircraft_type")
    .agg({
        "co2_emissions":"sum",
        "fuel_burn_liters":"sum",
        "distance_km":"sum"
    })
    .reset_index()
)

st.dataframe(
    table,
    use_container_width=True
)