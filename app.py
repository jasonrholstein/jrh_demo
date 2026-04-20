import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set page title and layout
st.set_page_config(page_title="Investment Risk Simulator", layout="centered")

def run_simulation(investment, years, growth_rate, crash_year, crash_drop):
    time = np.arange(0, years + 1)
    target_double = investment * 2
    
    # 1. Calculate No-Crash Baseline
    baseline = investment * (1 + growth_rate) ** time
    double_yr_baseline = next((yr for yr, val in enumerate(baseline) if val >= target_double), None)
    
    # 2. Calculate Actual (with Crash)
    actual_values = []
    current_val = investment
    peak_val = 0  # High water mark before the crash
    recoup_year = None
    double_yr_actual = None

    for yr in time:
        if yr > 0:
            current_val *= (1 + growth_rate)
            # Apply crash logic
            if yr == crash_year:
                peak_val = actual_values[-1]
                current_val *= (1 - crash_drop)
        
        actual_values.append(current_val)
        
        # Check if investment has doubled
        if double_yr_actual is None and current_val >= target_double:
            double_yr_actual = yr
        
        # Check if investment has recouped crash losses
        if peak_val > 0 and recoup_year is None and current_val >= peak_val:
            recoup_year = yr

    return time, baseline, actual_values, recoup_year, peak_val, double_yr_baseline, double_yr_actual

# --- Sidebar Controls ---
st.sidebar.header("Investment Parameters")
inv = st.sidebar.slider("Initial Investment ($)", 100, 10000, 1000, 100)
yrs = st.sidebar.slider("Timeline (Years)", 5, 60, 30)
rate = st.sidebar.slider("Annual Growth Rate (%)", 0.0, 30.0, 10.0, 0.5) / 100

st.sidebar.header("Crash Scenario")
c_yr = st.sidebar.slider("Year of Crash", 1, yrs, 15)
c_drop = st.sidebar.slider("Crash Severity (%)", 0, 90, 25) / 100

# Run calculation logic
time, baseline, actual, recoup_yr, peak_val, dbl_base, dbl_act = run_simulation(inv, yrs, rate, c_yr, c_drop)

# --- Visualizations ---
st.title("📈 Investment Growth & Recovery Simulator")
st.write("Compare your projected growth against a baseline to see the 'time cost' of a market crash.")

fig, ax = plt.subplots(figsize=(10, 6))

# Plot lines
ax.plot(time, baseline, label="No-Crash Baseline", color='grey', linestyle='--', alpha=0.3)
ax.plot(time, actual, label="Actual Growth (with Crash)", color='#2ca02c', linewidth=2.5)

# Add horizontal line for the Pre-Crash Peak (Recoup Line)
if peak_val > 0:
    ax.axhline(y=peak_val, color='darkred', linestyle=':', linewidth=1.5, label="Pre-Crash Peak (Recoup Level)")

# Add horizontal line for Doubling Point
target_val = inv * 2
ax.axhline(y=target_val, color='gold', linestyle='--', alpha=0.5, label="2x Initial Investment")

# Add Doubling Star Markers
if dbl_act:
    ax.scatter(dbl_act, actual[dbl_act], color='gold', s=150, marker='*', edgecolors='black', zorder=6, label="Actual Double Point")
    ax.annotate(f"Doubled at Yr {dbl_act}", xy=(dbl_act, actual[dbl_act]), xytext=(dbl_act, actual[dbl_act]*1.15),
                arrowprops=dict(arrowstyle="->", color='black'), ha='center')

ax.set_ylabel("Portfolio Value ($)")
ax.set_xlabel("Years")
ax.legend(loc='upper left', fontsize='small')
ax.grid(True, alpha=0.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

st.pyplot(fig)

# --- Detailed Summary ---
st.subheader("📊 Key Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Final Value", f"${actual[-1]:,.2f}")
with col2:
    status = f"Year {recoup_yr}" if recoup_yr else "Never"
    st.metric("Recouped by", status)
with col3:
    delay = (dbl_act - dbl_base) if (dbl_act and dbl_base) else "N/A"
    st.metric("Doubling Delay", f"+{delay} Years" if delay != "N/A" else "Incomplete")

st.info(f"**Insight:** Without a crash, you would have doubled your money in **{dbl_base} years**. "
        f"The crash in Year {c_yr} delayed that milestone by **{delay} years**.")
