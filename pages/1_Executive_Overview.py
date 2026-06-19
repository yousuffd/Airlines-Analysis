import streamlit as st

from modules.data_loader import load_data

from modules.kpi_calculations import (
    calculate_core_kpis
)

from modules.health_score import (
    calculate_health_score
)

from modules.alert_engine import (
    generate_alerts
)

from modules.executive_summary import (
    generate_executive_summary
)

from modules.chart_builders import (
    revenue_trend,
    profit_trend,
    top_routes
)

from modules.ui_components import (
    page_header,
    metric_card,
    load_css
)
from modules.config import configure_page
configure_page()


def render():

    load_css()

    from modules.filters import global_filters

    df = load_data()
    df = global_filters(df)

    kpis = calculate_core_kpis(df)

    health_score = (
        calculate_health_score(kpis)
    )

    page_header(
        "Executive Overview",
        "CEO Airline Performance Dashboard"
    )

    # KPI Row

    cols = st.columns(6)

    metrics = [

        ("Revenue",
         f"${kpis['Revenue']/1e6:.1f}M"),

        ("Profit",
         f"${kpis['Profit']/1e6:.1f}M"),

        ("Passengers",
         f"{kpis['Passengers']:,}"),

        ("Load Factor",
         f"{kpis['Load Factor']:.1f}%"),

        ("OTP",
         f"{kpis['OTP']:.1f}%"),

        ("Health",
         f"{health_score}/100")

    ]

    for col, metric in zip(cols, metrics):

        with col:
            metric_card(
                metric[0],
                metric[1]
            )

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:

        st.subheader(
            "Executive Narrative"
        )

        st.info(
            generate_executive_summary(df)
        )

    with right:

        st.subheader(
            "Executive Alerts"
        )

        alerts = generate_alerts(
            kpis
        )

        for level, message in alerts:

            if level == "success":
                st.success(message)

            elif level == "warning":
                st.warning(message)

            else:
                st.error(message)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            revenue_trend(df),
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            profit_trend(df),
            use_container_width=True
        )

    st.plotly_chart(
        top_routes(df),
        use_container_width=True
    )


render()