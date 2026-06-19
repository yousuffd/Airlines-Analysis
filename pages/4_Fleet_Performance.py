import streamlit as st

from modules.data_loader import load_data

from modules.ui_components import (
    load_css,
    page_header,
    metric_card
)

from modules.fleet_kpis import (
    calculate_fleet_kpis
)
from modules.config import configure_page
configure_page()

from modules.chart_builders import (
    aircraft_comparison,
    utilization_trend,
    fuel_burn_analysis,
    casm_vs_rask,
    fleet_profitability
)

load_css()

from modules.filters import global_filters

df = load_data()
df = global_filters(df)

kpis = calculate_fleet_kpis(df)

page_header(
    "Fleet Performance",
    "Fleet Economics & Aircraft Efficiency"
)

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    metric_card(
        "Utilization",
        f"{kpis['Utilization']:.1f} hrs"
    )

with c2:
    metric_card(
        "Fuel Efficiency",
        f"{kpis['Fuel Efficiency']:.2f}"
    )

with c3:
    metric_card(
        "CASM",
        f"{kpis['CASM']:.4f}"
    )

with c4:
    metric_card(
        "RASK",
        f"{kpis['RASK']:.4f}"
    )

with c5:
    metric_card(
        "Fleet Profit",
        f"${kpis['Fleet Profit']/1e6:.1f}M"
    )

with c6:
    metric_card(
        "Top Aircraft",
        kpis["Top Aircraft"]
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        aircraft_comparison(df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fleet_profitability(df),
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        utilization_trend(df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        fuel_burn_analysis(df),
        use_container_width=True
    )

st.markdown("---")

st.plotly_chart(
    casm_vs_rask(df),
    use_container_width=True
)

st.markdown("### Fleet Performance Detail")

fleet_table = (
    df.groupby("aircraft_type")
    .agg({
        "profit":"sum",
        "fuel_burn_liters":"sum",
        "utilization_hours":"mean",
        "casm":"mean",
        "rask":"mean"
    })
    .reset_index()
)

st.dataframe(
    fleet_table,
    use_container_width=True
)