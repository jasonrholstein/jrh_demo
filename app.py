import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Investment Risk Simulator", layout="centered")

def run_simulation(investment, years, growth_rate, crash_year, crash_drop):
    time = np.arange(0, years + 1)
    
    # Calculate No-Crash Baseline
    no_crash_values = investment * (1 + growth_rate) ** time
    
    # Calculate Actual (with Crash)
    actual_values = []
    current_val = investment
    peak_before_crash = 0
    recoup_year = None

    for yr in time:
        if yr > 0:
            current_val *= (1 + growth_rate)
            if yr == crash_year:
                peak_before_crash = actual_values[-1] # Value just before crash
                current_val *= (1 - crash_drop)
        
        actual_values.append(current_val)
        
        # Check if we've recouped the loss (surpassed the pre-crash peak)
        if peak_before_crash > 0 and recoup_year is None and current_val >= peak_before_crash:
            recoup_year = yr

    return time, no_crash_values, actual_values, recoup_year

# --- Web Interface ---
st.title("📉 Investment Loss & Recovery Simulator")
st.write("Compare your actual projected growth against a 'No-Crash' scenario.")

st.sidebar.header("Parameters")
inv = st.sidebar.slider("Initial Investment ($)", 100, 10000, 1000)
yrs = st.sidebar.slider("Timeline (Years)", 5, 60, 30)
rate = st.sidebar.slider("Avg. Annual Growth (%)", 0.0, 30.0, 10.0) / 100
c_yr = st.sidebar.slider("Year of Market Crash", 1, yrs, 15)
c_drop = st.sidebar.slider("Crash Severity (%)", 0, 90, 25) / 100

# Run logic
time, baseline, actual, recoup_yr = run_simulation(inv, yrs, rate, c_yr, c_drop)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time, baseline, label="No-Crash Baseline", color='grey', linestyle='--', alpha=0.6)
ax.plot(time, actual, label="Actual (With Crash)", color='#2ca02c', linewidth=2.5)

if c_yr <= yrs:
    ax.scatter(c_yr, actual[c_yr], color='red', zorder=5, label="Crash Event")

ax.set_title("Potential Gain vs. Actual Growth", fontsize=14)
ax.set_ylabel("Account Value ($)")
ax.set_xlabel("Years")
ax.legend()
ax.grid(True, alpha=0.3)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

st.pyplot(fig)

# --- Impact Analysis Summary ---
st.subheader("📊 Crash Impact Analysis")

final_actual = actual[-1]
final_baseline = baseline[-1]
total_loss = final_baseline - final_actual

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Final Value", f"${final_actual:,.2f}")
with col2:
    st.metric("Lost Potential", f"-${total_loss:,.2f}", delta_color="inverse")
with col3:
    recovery_text = f"{recoup_yr - c_yr} Years" if recoup_yr else "Never"
    st.metric("Time to Recoup", recovery_text)

st.info(f"**Note:** A {c_drop*100:.0f}% crash in year {c_yr} requires your investment to grow back to its previous peak of ${actual[c_yr-1]:,.2f}. "
        f"In this scenario, it takes **{recovery_text}** just to get back to where you were before the drop.")
