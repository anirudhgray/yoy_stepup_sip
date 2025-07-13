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

# Calculate growth
yearly_data = calculate_yearly_growth(initial, sip, step_up, rate, years)

# Plotting
fig, ax = plt.subplots()
plt.sca(ax)
plot_growth(
    years=years,
    yearly_data=yearly_data,
    title=f"Portfolio Value Over {years} Years",
    color='green',
    marker='o',
    label=f"Step-up: {step_up}%",
    show_invested=True,
)

st.pyplot(fig)

# Summary
final = yearly_data[-1]
st.subheader(f"💰 Final Value: ₹{final['value']:,}")
st.write(f"📥 Total Invested: ₹{final['invested']:,}")
st.write(f"📈 Total Gain: ₹{final['gain']:,}")

# Dataframe
df = pd.DataFrame(yearly_data)
df_display = df[["year", "invested", "value", "gain", "value_crore"]]
df_display.columns = ["Year", "Total Invested (₹)", "Portfolio Value (₹)", "Gain (₹)", "Value (Cr)"]
st.dataframe(df_display, use_container_width=True)

# Download CSV
csv = df_display.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, "growth_summary.csv", "text/csv")
