import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Investment Risk Simulator", layout="centered")

def run_simulation(investment, years, growth_rate, crash_year, crash_drop):
    time = np.arange(0, years + 1)
    baseline = investment * (1 + growth_rate) ** time
    
    actual_values = []
    current_val = investment
    peak_before_crash = 0
    recoup_year = None

    for yr in time:
        if yr > 0:
            current_val *= (1 + growth_rate)
            if yr == crash_year:
                peak_before_crash = actual_values[-1] # This is our "Waterline"
                current_val *= (1 - crash_drop)
        
        actual_values.append(current_val)
        
        if peak_before_crash > 0 and recoup_year is None and current_val >= peak_before_crash:
            recoup_year = yr

    return time, baseline, actual_values, recoup_year, peak_before_crash

# --- UI Setup ---
st.title("📈 Investment Recovery Tracker")
st.sidebar.header("Parameters")
inv = st.sidebar.slider("Initial Investment ($)", 100, 10000, 1000)
yrs = st.sidebar.slider("Timeline (Years)", 5, 60, 30)
rate = st.sidebar.slider("Avg. Annual Growth (%)", 0.0, 30.0, 10.0) / 100
c_yr = st.sidebar.slider("Year of Market Crash", 1, yrs, 15)
c_drop = st.sidebar.slider("Crash Severity (%)", 0, 90, 25) / 100

time, baseline, actual, recoup_yr, peak_val = run_simulation(inv, yrs, rate, c_yr, c_drop)

# --- Enhanced Graphing ---
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the lines
ax.plot(time, baseline, label="No-Crash Baseline", color='grey', linestyle='--', alpha=0.4)
ax.plot(time, actual, label="Actual Growth (with Crash)", color='#2ca02c', linewidth=2.5)

# Add the Dark Red Recoup Line
if peak_val > 0:
    ax.axhline(y=peak_val, color='darkred', linestyle='-', linewidth=1.5, label="Pre-Crash Peak (Recoup Level)")
    
    # Optional: Highlight the intersection point
    if recoup_yr:
        ax.annotate(f'Recouped in Yr {recoup_yr}', 
                    xy=(recoup_yr, peak_val), 
                    xytext=(recoup_yr + 2, peak_val * 1.1),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

ax.set_title("How Long to Get Back to Even?", fontsize=14)
ax.set_ylabel("Account Value ($)")
ax.set_xlabel("Years")
ax.legend()
ax.grid(True, alpha=0.2)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

st.pyplot(fig)

# --- Impact Summary ---
st.subheader("📊 Recovery Metrics")
col1, col2 = st.columns(2)

with col1:
    st.metric("Pre-Crash Peak", f"${peak_val:,.2f}")
    st.write(f"This is the 'High Water Mark' you hit in Year {c_yr-1}.")

with col2:
    years_to_wait = recoup_yr - c_yr if recoup_yr else (yrs - c_yr)
    status = "Recouped ✅" if recoup_yr else "Still Below Peak ❌"
    st.metric("Recovery Status", status, delta=f"{years_to_wait} yrs to break even" if recoup_yr else "Incomplete")

if not recoup_yr:
    st.warning(f"Based on a {rate*100:.1f}% growth rate, {yrs} years isn't enough time to recover the ${peak_val - actual[c_yr]:,.2f} lost in the crash.")
