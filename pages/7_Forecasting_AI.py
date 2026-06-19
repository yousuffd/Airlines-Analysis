import streamlit as st

from modules.data_loader import load_data
from modules.ui_components import (
    load_css,
    page_header,
    metric_card
)
from modules.ai_insights import generate_ai_insights
from modules.chart_builders import forecast_chart
from modules.forecasting import generate_forecast

load_css()

from modules.filters import global_filters

from modules.config import configure_page
configure_page()

df = load_data()
df = global_filters(df)

page_header(
    "Forecasting & AI",
    "Predictive Analytics & Executive Intelligence"
)

st.caption(
    "Next 4 Quarters Forecast Based on Historical Performance Trends"
)

# revenue = (
#     df["ticket_revenue"].sum() +
#     df["ancillary_revenue"].sum()
# )

# profit = df["profit"].sum()

# passengers = df["passengers"].sum()

# otp = (
#     df["otp_flag"].mean() * 100
# )


_, revenue_fc = generate_forecast(
    df,
    "ticket_revenue",
    periods=4
)

_, profit_fc = generate_forecast(
    df,
    "profit",
    periods=4
)

_, passenger_fc = generate_forecast(
    df,
    "passengers",
    periods=4
)

forecast_revenue = revenue_fc["ticket_revenue"].sum()
forecast_profit = profit_fc["profit"].sum()
forecast_passengers = passenger_fc["passengers"].sum()

otp_df = df.copy()

otp_df["otp_pct"] = (
    otp_df["otp_flag"] * 100
)

_, otp_fc = generate_forecast(
    otp_df,
    "otp_pct",
    periods=4
)

forecast_otp = otp_fc["otp_pct"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    forecast_period = revenue_fc.iloc[-1]["date"]

    metric_card(
        "Revenue Forecast FY2026",
        f"${forecast_revenue/1e6:.1f}M"
    )

with c2:
    metric_card(
        "Profit Forecast FY2026",
        f"${forecast_profit/1e6:.1f}M"
    )

with c3:
    metric_card(
        "Passenger Forecast FY2026",
        f"{forecast_passengers:,.0f}"
    )

with c4:
    metric_card(
        "OTP Forecast FY2026",
        f"{forecast_otp:.1f}%"
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        forecast_chart(
            df,
            "ticket_revenue",
            "Revenue Forecast"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        forecast_chart(
            df,
            "passengers",
            "Passenger Forecast"
        ),
        use_container_width=True
    )

st.plotly_chart(
    forecast_chart(
        df,
        "profit",
        "Profit Forecast"
    ),
    use_container_width=True
)

st.markdown("---")
st.subheader("Executive Forecast Narrative")
insights = generate_ai_insights(df)
narrative = "<br>".join(insights)
st.markdown(f"""
    <div style="
        background:#EAF2FF;
        border-radius:8px;
        padding:20px;
        border:1px solid #D6E4FF;
        font-size:15px;
        line-height:1.8;
        color:#4B5563;
        font-family:Inter,sans-serif;
    ">
        {narrative}
    </div>
    """,
    unsafe_allow_html=True
)