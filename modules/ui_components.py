import streamlit as st


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def page_header(title, subtitle):
    st.markdown(
        f'<div class="page-header-card">'
        f'<div style="display:flex;align-items:center;gap:12px;">'
        f'<div class="page-header-icon">✈</div>'
        f'<div><div class="executive-title">{title}</div>'
        f'<div class="executive-subtitle">{subtitle}</div></div>'
        f'</div>'
        f'<div style="background:#EFF6FF;border:1px solid #BFDBFE;color:#1D4ED8;'
        f'font-size:11px;font-weight:600;padding:4px 10px;border-radius:20px;'
        f'letter-spacing:0.04em;">&#9679; Live</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# (border-top color, label color, value color)
_THEMES = {
    "blue":   ("#2563EB", "#9CA3AF", "#1D4ED8"),
    "green":  ("#059669", "#9CA3AF", "#047857"),
    "slate":  ("#475569", "#9CA3AF", "#334155"),
    "warn":   ("#D97706", "#9CA3AF", "#B45309"),
    "danger": ("#DC2626", "#9CA3AF", "#B91C1C"),
    "purple": ("#7C3AED", "#9CA3AF", "#6D28D9"),
    "sky":    ("#0284C7", "#9CA3AF", "#0369A1"),
    "teal":   ("#0D9488", "#9CA3AF", "#0F766E"),
}

_METRIC_COLORS = {
    "revenue":           "blue",
    "revenue / pax":     "blue",
    "revenue / flight":  "blue",
    "passenger yield":   "blue",
    "profit":            "green",
    "profit margin":     "green",
    "fleet profit":      "green",
    "margin":            "green",
    "passengers":        "slate",
    "load factor":       "warn",
    "occupancy":         "warn",
    "otp":               "danger",
    "delay rate":        "danger",
    "cancellation rate": "danger",
    "completion rate":   "green",
    "utilization":       "purple",
    "fuel efficiency":   "teal",
    "casm":              "danger",
    "rask":              "green",
    "health":            "purple",
    "top route":         "sky",
    "top aircraft":      "sky",
}


def _resolve(title, theme):
    if theme and theme in _THEMES:
        return _THEMES[theme]
    return _THEMES.get(
        _METRIC_COLORS.get(title.lower().strip(), "blue"),
        _THEMES["blue"]
    )


def metric_card(title, value, delta=None, delta_suffix="", theme=None):
    border, label_color, value_color = _resolve(title, theme)

    delta_html = ""
    if delta is not None:
        pos = not str(delta).lstrip(" ").startswith("-")
        arrow = "&#9650;" if pos else "&#9660;"
        dc = "#059669" if pos else "#DC2626"
        delta_html = (
            f"<p style='margin:3px 0 0;font-size:0.65rem;font-weight:600;"
            f"color:{dc};text-align:center;white-space:nowrap;'>"
            f"{arrow} {delta}{delta_suffix}</p>"
        )

    st.markdown(
        f"<div style='background:#FFFFFF;border-radius:8px;"
        f"border:1px solid #E5E7EB;border-top:3px solid {border};"
        f"padding:12px 8px 10px;display:flex;flex-direction:column;"
        f"align-items:center;text-align:center;gap:4px;height:100%;'>"
        f"<p style='margin:0;font-size:0.62rem;font-weight:700;"
        f"color:{label_color};text-transform:uppercase;"
        f"letter-spacing:0.09em;white-space:nowrap;'>{title}</p>"
        f"<p style='margin:0;font-size:1.8rem;font-weight:700;"
        f"color:{value_color};line-height:1.15;"
        f"font-family:\"Inter\",Inter,monospace;"
        f"white-space:nowrap;'>{value}</p>"
        f"{delta_html}</div>",
        unsafe_allow_html=True,
    )


def section_container(title):
    st.markdown(
        f"<div class='section-card'><p style='margin:0 0 10px;font-size:11px;"
        f"font-weight:700;text-transform:uppercase;letter-spacing:0.08em;"
        f"color:#9CA3AF;'>{title}</p>",
        unsafe_allow_html=True,
    )


def close_container():
    st.markdown("</div>", unsafe_allow_html=True)