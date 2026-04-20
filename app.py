import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Investment Risk Simulator", layout="centered")

def run_simulation(investment, years, growth_rate, crash_year, crash_drop):
    time = np.arange(0, years + 1)
    target_double = investment * 2
    
    # 1. Calculate Baseline
    baseline = investment * (1 + growth_rate) ** time
    double_yr_baseline = next((yr for yr, val in enumerate(baseline) if val >= target_double), None)
    
    # 2. Calculate Actual (with Crash)
    actual_values = []
    current_val = investment
    peak_before_crash = 0
    recoup_year = None
    double_yr_actual = None

    for yr in time:
        if yr > 0:
            current_val *= (1 + growth_rate)
            if yr == crash_year:
                peak_before_crash = actual_values[-1]
                current_val *= (1 - crash_drop)
        
        actual_values.append(current_val)
        
        # Check for doubling
        if double_yr_actual is None and current_val >= target_double:
            double_yr_actual = yr
        
        # Check for recouping
        if peak_before_crash > 0 and recoup_year is None and current_val >= peak_before_crash:
            recoup_year = yr

    return time, baseline, actual_values, recoup_year, peak_val, double_yr_baseline, double_yr_actual

# --- UI Setup ---
st.title("📈 Investment Recovery Tracker")
st.sidebar.header("Parameters")
inv = st.sidebar.slider("Initial Investment ($)", 100, 10000, 1000)
yrs = st.sidebar.slider("Timeline (Years)", 5, 60, 30)
rate = st.sidebar.slider("Avg. Annual Growth (%)", 0.0, 30.0, 10.0) / 100
c_yr = st.sidebar.slider("Year of Market Crash", 1, yrs, 15)
c_drop = st.sidebar.slider("Crash Severity (%)", 0, 90, 25) / 100

time, baseline, actual, recoup_yr, peak_val, dbl_base, dbl_act = run_simulation(inv, yrs, rate, c_yr, c_drop)

# --- Enhanced Graphing ---
fig, ax = plt.subplots(figsize=(10, 6))

# Plot lines
ax.plot(time, baseline, label="No-Crash Baseline", color='grey', linestyle='--', alpha=0.3)
ax.plot(time, actual, label="Actual Growth", color='#2ca02c', linewidth=2.5)

# 1. Add the Recoup (Break-even) line
if peak_val > 0:
    ax.axhline(y=peak_val, color='darkred', linestyle=':', linewidth=1.5, label="Pre-Crash Peak")

# 2. Add the "Doubling" markers
target_val = inv * 2
ax.axhline(y=target_val, color='gold', linestyle='--', alpha=0.5, label="2x Initial Investment")

if dbl_base:
    ax.scatter(dbl_base, baseline[dbl_base], color='orange', s=100, marker='*', zorder=5, label="Doubled (Ideal)")
if dbl_act:
    ax.scatter(dbl_act, actual[dbl_act], color='gold', s=150, marker='*', edgecolors='black', zorder=6, label="Doubled (Actual)")
    ax.annotate("Doubled Here!", xy=(dbl_act, actual[dbl_act]), xytext=(dbl_act-5, actual[dbl_act]*1.2),
                arrowprops=dict(arrowstyle="->", color='black'))

ax.set_title("Investment Growth & Doubling Points", fontsize=14)
ax.set_ylabel("Account Value ($)")
ax.set_xlabel("Years")
ax.legend(loc='upper left', fontsize='small', frameon=True)
ax.grid(True, alpha=0.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

st.pyplot(fig)

# --- Summary & Notes ---
st.subheader("💡 Key Takeaways")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Double Point (No Crash)", f"Yr {dbl_base}" if dbl_base else "N/A")
with col2:
    st.metric("Double Point (Actual)", f"Yr {dbl_act}" if dbl_act else "Never")
with col3:
    delay = (dbl_act - dbl_base) if (dbl_act and dbl_base) else "N/A"
    st.metric("Crash Delay", f"+{delay} Years" if delay != "N/A" else "Unknown")

st.info(f"**The 'Doubling' Goal:** To turn your ${inv:,.0f} into **${inv*2:,.0f}**, it should have taken {dbl_base} years. "
        f"Because of the crash in Year {c_yr}, that goal was delayed by **{delay} years**.")
