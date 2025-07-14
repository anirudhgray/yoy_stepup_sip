import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from yoy_stepup_sip import calculate_yearly_growth, plot_growth

st.set_page_config(page_title="Investment Growth Calculator", layout="centered")

st.title("📈 Investment Growth Calculator")
st.caption("Visualize how your investment grows with SIP, Step-up, and Rate of Return")

# Sidebar inputs
st.sidebar.header("📊 Investment Parameters")
initial = st.sidebar.number_input("Initial Lump Sum (INR)", value=700000, step=10000)
sip = st.sidebar.number_input("Monthly SIP (INR)", value=70000, step=1000)
step_up = st.sidebar.slider("Annual Step-up (%)", 0, 50, 10)
rate = st.sidebar.slider("Rate of Return (%)", 0, 25, 12)
years = st.sidebar.slider("Investment Duration (Years)", 1, 40, 25)
inflation = st.sidebar.slider("Inflation Rate (%)", 0, 15, 6)

show_invested = st.sidebar.checkbox("Show Invested Amount", value=True)
show_nominal = st.sidebar.checkbox("Show Nominal Value", value=True)

# Calculate growth
yearly_data = calculate_yearly_growth(initial, sip, step_up, rate, years, inflation)

# Plotting
fig, ax = plt.subplots()
plt.sca(ax)
plot_growth(
    years=years,
    yearly_data=yearly_data,
    title=f"Portfolio Value Over {years} Years",
    color='green',
    marker='o',
    label=f"",
    show_invested=show_invested,
    show_nominal=show_nominal
)

st.pyplot(fig)

# Summary
final = yearly_data[-1]
st.write(f"📥 Total Invested: ₹{final['invested']:,} (not adjusted for inflation)")
st.write(f"💰 Final Value (Real): ₹{final['real_value']:,} (inflation adjusted)")
st.write(f"📉 Real Gain: ₹{final['real_gain']:,} (inflation adjusted)")
st.write(f"💰 Final Value (Nominal): ₹{final['value']:,} (not adjusted for inflation)")
st.write(f"📈 Nominal Gain: ₹{final['gain']:,} (not adjusted for inflation)")

# Dataframe
df = pd.DataFrame(yearly_data)
df_display = df[["year", "invested", "value", "gain", "real_value", "real_gain", "value_crore", "real_value_crore"]]
df_display.columns = [
    "Year", "Total Invested (₹)", "Portfolio Value (₹)", "Gain (₹)",
    "Real Value (₹)", "Real Gain (₹)", "Value (Cr)", "Real Value (Cr)"
]
st.dataframe(df_display, use_container_width=True)

# Download CSV
csv = df_display.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, "growth_summary.csv", "text/csv")
