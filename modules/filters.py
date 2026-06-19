import streamlit as st
import pandas as pd


def global_filters(df):

    # ── Section heading ───────────────────────────────────────────────────────
    st.sidebar.markdown(
        "<p style='font-size:10px;font-weight:700;text-transform:uppercase;"
        "letter-spacing:0.12em;color:#9CA3AF;padding-bottom:8px;"
        "border-bottom:1px solid #F3F4F6;margin-bottom:4px;'>Filters</p>",
        unsafe_allow_html=True,
    )

    # ── Date Range ────────────────────────────────────────────────────────────
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date)
    )

    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
        df = df[
            (df["date"] >= pd.to_datetime(start_date)) &
            (df["date"] <= pd.to_datetime(end_date))
        ]

    # ── Aircraft Type ─────────────────────────────────────────────────────────
    aircraft = st.sidebar.multiselect(
        "Aircraft Type",
        sorted(df["aircraft_type"].unique()),
        placeholder="All aircraft"
    )

    if aircraft:
        df = df[df["aircraft_type"].isin(aircraft)]

    # ── Route ─────────────────────────────────────────────────────────────────
    routes = st.sidebar.multiselect(
        "Route",
        sorted(df["route"].unique()),
        placeholder="All routes"
    )

    if routes:
        df = df[df["route"].isin(routes)]

    return df