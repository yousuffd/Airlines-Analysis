import plotly.graph_objects as go
import plotly.graph_objects as go
from modules.forecasting import generate_forecast

# ── Design tokens — Executive Light Theme ────────────────────────────────────
_BG    = "#FFFFFF"
_PLOT  = "#F9FAFB"
_GRID  = "#E5E7EB"
_TICK  = "#9CA3AF"
_TITLE = "#111827"
_TEXT  = "#6B7280"
_FONT  = "Inter, Segoe UI, sans-serif"

# Semantic palette — matched to the UI system
_BLUE   = "#2563EB"
_GREEN  = "#059669"
_WARN   = "#D97706"
_DANGER = "#DC2626"
_PURPLE = "#7C3AED"
_SKY    = "#0284C7"
_TEAL   = "#0D9488"
_SLATE  = "#475569"

# Muted fills for area charts (low opacity)
_BLUE_F   = "rgba(37,99,235,0.07)"
_GREEN_F  = "rgba(5,150,105,0.07)"
_WARN_F   = "rgba(217,119,6,0.07)"
_DANGER_F = "rgba(220,38,38,0.07)"
_PURPLE_F = "rgba(124,58,237,0.07)"
_SKY_F    = "rgba(2,132,199,0.07)"

_COLORWAY = [_BLUE, _GREEN, _WARN, _SKY, _DANGER, _PURPLE, _TEAL, _SLATE]


def _base_layout(title: str, height: int = 360) -> dict:
    return dict(
        template=None,
        height=height,
        paper_bgcolor=_BG,
        plot_bgcolor=_PLOT,
        font=dict(family=_FONT, color=_TEXT, size=12),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=13, color=_TITLE, family=_FONT),
            x=0.02, xanchor="left",
            y=0.97, yanchor="top",
        ),
        margin=dict(l=56, r=20, t=46, b=44),
        xaxis=dict(
            gridcolor=_GRID, linecolor=_GRID,
            zerolinecolor=_GRID, zeroline=False,
            tickcolor=_TICK, tickfont=dict(color=_TICK, size=11),
            title_font=dict(color=_TICK, size=11),
            showgrid=False,
        ),
        yaxis=dict(
            gridcolor=_GRID, linecolor=_GRID,
            zerolinecolor=_GRID, zeroline=False,
            tickcolor=_TICK, tickfont=dict(color=_TICK, size=11),
            title_font=dict(color=_TICK, size=11),
            showgrid=True,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=_GRID,
            font=dict(color=_TEXT, size=11),
        ),
        colorway=_COLORWAY,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=_GRID,
            font=dict(color=_TITLE, size=12),
        ),
    )


def _line_area(x, y, title, color=_BLUE, fill=_BLUE_F, y_title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line=dict(color=color, width=2, shape="spline", smoothing=0.6),
        fill="tozeroy",
        fillcolor=fill,
        hovertemplate="%{x}<br><b>%{y:,.2s}</b><extra></extra>",
    ))
    layout = _base_layout(title)
    layout["yaxis"]["title"] = y_title
    layout["xaxis"]["title"] = ""
    fig.update_layout(**layout)
    return fig


def _make_bar_colors(n, color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    return [
        f"rgba({r},{g},{b},{round(0.35 + 0.65 * i / max(n - 1, 1), 2)})"
        for i in range(n)
    ]


def _bar_h(df, x_col, y_col, title, color=_BLUE):
    colors = _make_bar_colors(len(df), color)
    fig = go.Figure(go.Bar(
        x=df[x_col], y=df[y_col],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{y}</b>  %{x:,.2s}<extra></extra>",
    ))
    layout = _base_layout(title, height=400)
    layout["yaxis"]["autorange"] = "reversed"
    layout["xaxis"]["showgrid"] = True
    layout["yaxis"]["showgrid"] = False
    layout["margin"]["l"] = 90
    fig.update_layout(**layout)
    return fig


def _bar_v(df, x_col, y_col, title, color=_BLUE):
    colors = _make_bar_colors(len(df), color)
    fig = go.Figure(go.Bar(
        x=df[x_col], y=df[y_col],
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{x}</b>  %{y:,.2s}<extra></extra>",
    ))
    layout = _base_layout(title, height=360)
    layout["xaxis"]["showgrid"] = False
    layout["yaxis"]["showgrid"] = True
    fig.update_layout(**layout)
    return fig


def _pie(df, names_col, values_col, title):
    colors = [_BLUE, _GREEN, _WARN, _SKY, _DANGER, _PURPLE, _TEAL]
    fig = go.Figure(go.Pie(
        labels=df[names_col],
        values=df[values_col],
        hole=0.44,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color="#111827", size=12),
        hovertemplate="<b>%{label}</b><br>%{value:,.2s} (%{percent})<extra></extra>",
    ))
    layout = _base_layout(title)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)
    fig.update_layout(**layout)
    return fig


# ── Chart functions ───────────────────────────────────────────────────────────

def revenue_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))
         [["ticket_revenue", "ancillary_revenue"]].sum().reset_index())
    m["Revenue"] = m["ticket_revenue"] + m["ancillary_revenue"]
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["Revenue"], "Revenue Trend",
                      _BLUE, _BLUE_F, "Revenue ($)")


def profit_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))["profit"]
         .sum().reset_index())
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["profit"], "Profit Trend",
                      _GREEN, _GREEN_F, "Profit ($)")


def top_routes(df):
    r = (df.groupby("route")["profit"].sum()
         .sort_values(ascending=True).tail(10).reset_index())
    return _bar_h(r, "profit", "route", "Top Profitable Routes", _BLUE)


def revenue_by_market(df):
    m = (df.groupby("market_type")[["ticket_revenue", "ancillary_revenue"]]
         .sum().reset_index())
    m["Revenue"] = m["ticket_revenue"] + m["ancillary_revenue"]
    return _pie(m, "market_type", "Revenue", "Revenue by Market Type")


def route_profitability(df):
    r = (df.groupby("route")["profit"].sum()
         .sort_values(ascending=False).head(15).reset_index())
    return _bar_v(r, "route", "profit", "Top Route Profitability", _BLUE)


def top_revenue_routes(df):
    r = (df.groupby("route")[["ticket_revenue", "ancillary_revenue"]]
         .sum().reset_index())
    r["Revenue"] = r["ticket_revenue"] + r["ancillary_revenue"]
    r = r.sort_values("Revenue", ascending=True).tail(10)
    return _bar_h(r, "Revenue", "route", "Top Revenue Routes", _SKY)


def passenger_yield_chart(df):
    r = (df.groupby("route")
         .agg({"ticket_revenue": "sum", "distance_km": "sum"}).reset_index())
    r["yield"] = r["ticket_revenue"] / r["distance_km"]
    r = r.sort_values("yield", ascending=False).head(15)
    return _bar_v(r, "route", "yield", "Passenger Yield by Route", _WARN)


def delay_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))["delay_minutes"]
         .mean().reset_index())
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["delay_minutes"], "Average Delay Trend",
                      _DANGER, _DANGER_F, "Avg Delay (min)")


def delay_root_cause(df):
    c = df.groupby("delay_reason").size().reset_index(name="count")
    return _pie(c, "delay_reason", "count", "Delay Root Cause")


def airport_performance(df):
    a = df.groupby("origin").agg({"otp_flag": "mean"}).reset_index()
    a["otp_flag"] = (a["otp_flag"] * 100).round(1)
    return _bar_v(a, "origin", "otp_flag", "Airport OTP Performance (%)", _GREEN)


def operational_bottlenecks(df):
    b = (df.groupby("origin")["delay_minutes"].mean()
         .sort_values(ascending=True).tail(10).reset_index())
    return _bar_h(b, "delay_minutes", "origin", "Top Delay Bottlenecks", _DANGER)


def aircraft_comparison(df):
    a = df.groupby("aircraft_type").agg({"profit": "sum"}).reset_index()
    return _bar_v(a, "aircraft_type", "profit", "Aircraft Profitability", _SKY)


def utilization_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))["utilization_hours"]
         .mean().reset_index())
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["utilization_hours"], "Fleet Utilization Trend",
                      _PURPLE, _PURPLE_F, "Avg Hours")


def fuel_burn_analysis(df):
    f = df.groupby("aircraft_type")["fuel_burn_liters"].sum().reset_index()
    return _bar_v(f, "aircraft_type", "fuel_burn_liters", "Fuel Burn by Aircraft", _WARN)


def casm_vs_rask(df):
    fleet = (df.groupby("aircraft_type")
             .agg({"casm": "mean", "rask": "mean"}).reset_index())
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fleet["casm"], y=fleet["rask"],
        mode="markers+text",
        text=fleet["aircraft_type"],
        textposition="top center",
        textfont=dict(color=_BLUE, size=11),
        marker=dict(size=12, color=_BLUE, line=dict(color="#FFFFFF", width=2)),
        hovertemplate="<b>%{text}</b><br>CASM: %{x:.4f}<br>RASK: %{y:.4f}<extra></extra>",
    ))
    layout = _base_layout("CASM vs RASK", height=360)
    layout["xaxis"]["title"] = "CASM"
    layout["yaxis"]["title"] = "RASK"
    fig.update_layout(**layout)
    return fig


def fleet_profitability(df):
    f = df.groupby("aircraft_type")["profit"].sum().reset_index()
    return _bar_v(f, "aircraft_type", "profit", "Fleet Profitability", _GREEN)


def passenger_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))["passengers"]
         .sum().reset_index())
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["passengers"], "Passenger Trend",
                      _SKY, _SKY_F, "Passengers")


def load_factor_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))["load_factor"]
         .mean().reset_index())
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["load_factor"], "Load Factor Trend",
                      _WARN, _WARN_F, "Load Factor (%)")


def occupancy_trend(df):
    m = (df.groupby(df["date"].dt.to_period("M"))["occupancy"]
         .mean().reset_index())
    m["date"] = m["date"].astype(str)
    return _line_area(m["date"], m["occupancy"], "Occupancy Trend",
                      _TEAL, "rgba(13,148,136,0.07)", "Occupancy (%)")


def passenger_mix(df):
    m = df.groupby("market_type")["passengers"].sum().reset_index()
    return _pie(m, "market_type", "passengers", "Passenger Mix by Market")


def route_passenger_analysis(df):
    r = (df.groupby("route")["passengers"].sum()
         .sort_values(ascending=True).tail(15).reset_index())
    return _bar_h(r, "passengers", "route", "Top Passenger Routes", _SKY)


def market_passenger_analysis(df):
    m = df.groupby("market_type")["passengers"].sum().reset_index()
    return _bar_v(m, "market_type", "passengers", "Passengers by Market", _BLUE)


def co2_trend(df):
    monthly = (df.groupby(df["date"].dt.to_period("M"))["co2_emissions"].sum().reset_index())
    monthly["date"] = (monthly["date"].astype(str))
    return _line_area(monthly["date"], monthly["co2_emissions"], "CO2 Emissions Trend", _TEAL, "rgba(13,148,136,0.07)", "CO2")


def fuel_consumption_trend(df):
    monthly = (df.groupby( df["date"].dt.to_period("M"))["fuel_burn_liters"].sum().reset_index())
    monthly["date"] = ( monthly["date"].astype(str))
    return _line_area(monthly["date"], monthly["fuel_burn_liters"], "Fuel Consumption Trend", _WARN, _WARN_F, "Fuel")


def aircraft_emissions(df):
    aircraft = (df.groupby("aircraft_type")["co2_emissions"].sum().reset_index())
    return _bar_v(aircraft, "aircraft_type",
        "co2_emissions", "Aircraft Emissions", _TEAL)


def emissions_by_market(df):
    market = (df.groupby("market_type")["co2_emissions"].sum().reset_index())
    return _pie(market, "market_type", "co2_emissions", "Emissions by Market")


def forecast_chart(df, metric, title):
    actual, forecast = generate_forecast(df, metric)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual["date"], y=actual[metric], name="Actual"))
    fig.add_trace(go.Scatter(x=forecast["date"], y=forecast[metric], name="Forecast", line=dict(dash="dash")))
    fig.update_layout(title=title, template="plotly_white", height=450)
    return fig