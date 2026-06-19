import streamlit as st

from modules.data_loader import load_data

from modules.ui_components import (
    load_css,
    page_header,
    metric_card
)
from modules.config import configure_page
configure_page()

from modules.commercial_kpis import (
    calculate_commercial_kpis
)

from modules.chart_builders import (
    revenue_trend,
    revenue_by_market,
    route_profitability,
    top_revenue_routes,
    passenger_yield_chart
)


load_css()

from modules.filters import global_filters

df = load_data()
df = global_filters(df)

kpis = calculate_commercial_kpis(df)

page_header(
    "Commercial Analytics",
    "Revenue, Yield & Route Performance"
)

# KPI ROW

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    metric_card(
        "Revenue",
        f"${kpis['Revenue']/1e6:.1f}M"
    )

with c2:
    metric_card(
        "Revenue / Pax",
        f"${kpis['Revenue Per Passenger']:.0f}"
    )

with c3:
    metric_card(
        "Revenue / Flight",
        f"${kpis['Revenue Per Flight']:.0f}"
    )

with c4:
    metric_card(
        "Profit Margin",
        f"{kpis['Profit Margin']:.1f}%"
    )

with c5:
    metric_card(
        "Passenger Yield",
        f"{kpis['Passenger Yield']:.2f}"
    )

with c6:
    metric_card(
        "Top Route",
        kpis["Top Route"]
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        revenue_trend(df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        revenue_by_market(df),
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    st.plotly_chart(
        route_profitability(df),
        use_container_width=True
    )

with col4:

    st.plotly_chart(
        passenger_yield_chart(df),
        use_container_width=True
    )

st.markdown("---")

st.plotly_chart(
    top_revenue_routes(df),
    use_container_width=True
)

st.markdown("### Route Performance Detail")

route_table = (
    df.groupby("route")
    .agg({
        "passengers":"sum",
        "profit":"sum",
        "load_factor":"mean"
    })
    .reset_index()
    .sort_values(
        "profit",
        ascending=False
    )
)

st.dataframe(
    route_table,
    use_container_width=True
)