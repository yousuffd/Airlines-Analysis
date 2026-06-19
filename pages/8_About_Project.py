import streamlit as st

from modules.config import configure_page
configure_page()

from modules.ui_components import load_css
load_css()

st.set_page_config(
    page_title="About Project",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ About This Project")

st.markdown("---")

st.subheader("Business Problem")

st.write("""
Airline executives require a unified view of financial,
operational, fleet, passenger and sustainability performance.

This platform was designed to provide executive decision makers
with a centralized analytics environment that combines:

- Commercial Performance
- Operational Reliability
- Fleet Efficiency
- Passenger Demand
- Sustainability Metrics
- Predictive Forecasting

into a single command center.
""")

st.markdown("---")

st.subheader("Executive Users")

st.write("""
- Chief Executive Officer (CEO)
- Chief Operating Officer (COO)
- Chief Financial Officer (CFO)
- VP Commercial
- VP Operations
- Director of Analytics
""")

st.markdown("---")

st.subheader("Technology Stack")

st.write("""
### Data Engineering

- Pandas
- NumPy

### Analytics & Data Science

- Scikit-Learn
- Forecasting Models

### Visualization

- Plotly
- Streamlit

### Application Framework

- Python
- Streamlit
""")

st.markdown("---")

st.subheader("Key Business Domains")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    Commercial Analytics

    Revenue
    Profit
    Yield
    Route Performance
    """)

with col2:
    st.info("""
    Operations

    OTP
    Delays
    Cancellations
    Airport Performance
    """)

with col3:
    st.info("""
    Fleet

    Utilization
    Fuel Efficiency
    CASM
    RASK
    """)

st.markdown("---")

st.subheader("Dataset")

st.write("""
Synthetic Airline Dataset

- 15,000 Flight Records
- 5 Years of Data
- Multiple Routes
- Multiple Aircraft Types
- Operational Metrics
- Commercial Metrics
- Sustainability Metrics
""")

st.markdown("---")

st.subheader("Capabilities Demonstrated")

st.success("""
✓ Analytics Engineering

✓ Business Intelligence

✓ Executive Reporting

✓ KPI Framework Design

✓ Forecasting

✓ Product Thinking

✓ Streamlit Development

✓ Data Visualization
""")