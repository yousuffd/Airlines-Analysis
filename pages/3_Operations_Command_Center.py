import streamlit as st

from modules.data_loader import load_data

from modules.ui_components import (
    load_css,
    page_header,
    metric_card
)

from modules.operations_kpis import (
    calculate_operations_kpis
)
from modules.config import configure_page
configure_page()

from modules.chart_builders import (
    delay_trend,
    delay_root_cause,
    airport_performance,
    operational_bottlenecks
)

load_css()

from modules.filters import global_filters

df = load_data()
df = global_filters(df)

kpis = calculate_operations_kpis(df)

page_header(
    "Operations Command Center",
    "Operational Reliability & Network Performance"
)

# KPI Row

c1,c2,c3,c4 = st.columns(4)

with c1:
    metric_card(
        "OTP",
        f"{kpis['OTP']:.1f}%"
    )

with c2:
    metric_card(
        "Delay Rate",
        f"{kpis['Delay Rate']:.1f}%"
    )

with c3:
    metric_card(
        "Completion Rate",
        f"{kpis['Completion Rate']:.1f}%"
    )

with c4:
    metric_card(
        "Cancellation Rate",
        f"{kpis['Cancellation Rate']:.1f}%"
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        delay_trend(df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        delay_root_cause(df),
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    st.plotly_chart(
        airport_performance(df),
        use_container_width=True
    )

with col4:

    st.plotly_chart(
        operational_bottlenecks(df),
        use_container_width=True
    )

st.markdown("---")

st.subheader(
    "Airport Operations Detail"
)

airport_table = (
    df.groupby("origin")
    .agg({
        "delay_minutes":"mean",
        "otp_flag":"mean",
        "cancelled_flag":"mean"
    })
    .reset_index()
)

airport_table["otp_flag"] *= 100
airport_table["cancelled_flag"] *= 100

st.dataframe(
    airport_table,
    use_container_width=True
)