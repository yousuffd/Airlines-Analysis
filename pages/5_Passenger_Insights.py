import streamlit as st

from modules.data_loader import load_data

from modules.ui_components import (
    load_css,
    page_header,
    metric_card
)

from modules.passenger_kpis import (
    calculate_passenger_kpis
)

from modules.config import configure_page
configure_page()

from modules.chart_builders import (
    passenger_trend,
    load_factor_trend,
    occupancy_trend,
    passenger_mix,
    route_passenger_analysis,
    market_passenger_analysis
)

load_css()

from modules.filters import global_filters

df = load_data()
df = global_filters(df)

kpis = calculate_passenger_kpis(df)

page_header(
    "Passenger Insights",
    "Demand, Occupancy & Customer Analytics"
)

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    metric_card(
        "Passengers",
        f"{kpis['Passengers']:,}"
    )

with c2:
    metric_card(
        "Occupancy",
        f"{kpis['Occupancy']:.1f}%"
    )

with c3:
    metric_card(
        "Load Factor",
        f"{kpis['Load Factor']:.1f}%"
    )

with c4:
    metric_card(
        "Passenger Yield",
        f"${kpis['Passenger Yield']:.2f}"
    )

with c5:
    metric_card(
        "Top Route",
        kpis["Top Route"]
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        passenger_trend(df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        passenger_mix(df),
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        load_factor_trend(df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        occupancy_trend(df),
        use_container_width=True
    )

st.markdown("---")

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(
        route_passenger_analysis(df),
        use_container_width=True
    )

with col6:
    st.plotly_chart(
        market_passenger_analysis(df),
        use_container_width=True
    )

st.markdown("### Passenger Performance Detail")

passenger_table = (
    df.groupby("route")
    .agg({
        "passengers":"sum",
        "load_factor":"mean",
        "occupancy":"mean",
        "profit":"sum"
    })
    .reset_index()
    .sort_values(
        "passengers",
        ascending=False
    )
)

st.dataframe(
    passenger_table,
    use_container_width=True
)