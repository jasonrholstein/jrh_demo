import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set page title and layout
st.set_page_config(page_title="Investment Growth Simulator", layout="centered")

def plot_model(investment, years, growth_rate, crash_year, crash_drop):
    """
    Core calculation logic from your notebook
    """
    # Create the timeline
    time = np.arange(0, years + 1)
    # Calculate compound growth
    values = investment * (1 + growth_rate) ** time
    
    # Simulate the crash impact if it falls within the timeline
    if 0 < crash_year <= years:
        crash_index = int(crash_year)
        # Apply the drop to the value at that specific year and all subsequent years
        impact_factor = (1 - crash_drop)
        values[crash_index:] = values[crash_index:] * impact_factor

    # Create the visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, values, marker='o', linestyle='-', color='#2ca02c', linewidth=2)
    ax.set_title(f"Projected Growth over {years} Years", fontsize=16)
    ax.set_xlabel("Years", fontsize=12)
    ax.set_ylabel("Value ($)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Format the Y-axis for currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${x:,.0f}"))
    
    return fig

# --- Web Interface ---
st.title("📈 Family Investment Simulator")
st.write("Adjust the sliders below to see how your money could grow over time.")

# Sidebar for user inputs (replacing the Jupyter sliders)
st.sidebar.header("Simulation Settings")
inv = st.sidebar.slider("Initial Investment ($)", 100, 10000, 1000, 100)
yrs = st.sidebar.slider("Number of Years", 5, 60, 30)
rate = st.sidebar.slider("Annual Growth Rate (%)", 0.0, 30.0, 10.0, 0.5) / 100
c_yr = st.sidebar.slider("Market Crash Year", 1, 60, 15)
c_drop = st.sidebar.slider("Crash Impact (Drop %)", 0, 90, 25) / 100

# Run the model and display the results
figure = plot_model(inv, yrs, rate, c_yr, c_drop)
st.pyplot(figure)

# Display a summary table
st.subheader("Results Summary")
final_val = inv * ((1 + rate) ** yrs)
if c_yr <= yrs:
    final_val *= (1 - c_drop)

col1, col2 = st.columns(2)
col1.metric("Initial Investment", f"${inv:,.0f}")
col2.metric("Estimated Final Value", f"${final_val:,.2f}")
