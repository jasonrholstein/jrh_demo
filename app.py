import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set page title and layout
st.set_page_config(page_title="Investment Growth Simulator", layout="centered")

def plot_model(investment, years, growth_rate, crash_year, crash_drop):
    # 1. Generate the timeline (Year 0 to Year X)
    time = np.arange(0, years + 1)
    
    # 2. Calculate values with compound growth
    # We use a loop or vectorized math to ensure the crash affects the trajectory
    values = []
    current_value = investment
    for yr in time:
        if yr == 0:
            values.append(current_value)
        else:
            current_value *= (1 + growth_rate)
            # Apply the crash impact only at the specific year selected
            if yr == crash_year:
                current_value *= (1 - crash_drop)
            values.append(current_value)

    # 3. Create the visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, values, marker='o', linestyle='-', color='#2ca02c', linewidth=2)
    
    # Add a vertical red line to highlight the crash year visually
    if 0 < crash_year <= years:
        ax.axvline(x=crash_year, color='red', linestyle='--', alpha=0.5, label=f"Market Crash (Yr {crash_year})")
        ax.legend()

    ax.set_title(f"Projected Growth over {years} Years", fontsize=16)
    ax.set_xlabel("Years", fontsize=12)
    ax.set_ylabel("Value ($)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${x:,.0f}"))
    
    return fig, values[-1]

# --- Web Interface ---
st.title("📈 Family Investment Simulator")
st.write("Adjust the sliders to see how your money grows and how market volatility affects it.")

# User inputs based on your notebook sliders
st.sidebar.header("Simulation Settings")
inv = st.sidebar.slider("Initial Investment ($)", 100, 10000, 1000, 100)
yrs = st.sidebar.slider("Number of Years", 5, 60, 30)
rate = st.sidebar.slider("Annual Growth Rate (%)", 0.0, 30.0, 10.0, 0.5) / 100
c_yr = st.sidebar.slider("Market Crash Year", 1, 60, 15)
c_drop = st.sidebar.slider("Crash Impact (Drop %)", 0, 90, 25) / 100

# Run the updated model
figure, final_val = plot_model(inv, yrs, rate, c_yr, c_drop)

# Display the chart
st.pyplot(figure)

# Display Summary Metrics
col1, col2 = st.columns(2)
col1.metric("Initial Investment", f"${inv:,.0f}")
col2.metric("Estimated Final Value", f"${final_val:,.2f}")
