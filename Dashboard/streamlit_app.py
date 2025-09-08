import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Make your local package importable (adds location of rolling intrinsic to system path variable)
path_RI = os.path.relpath(r"Code\Rolling Intrinsic\\")
sys.path.append(path_RI)

from Rolling_Intrinsic_QH import simulate_period
# -------------------------- Page Description --------------------------
st.set_page_config(page_title="Simulate February 2025", page_icon="👋")
path_RI
# -------------------------- Helpers --------------------------

def build_paths(bess: dict) -> dict:
    """Build output paths from parameters and stash in session_state."""
    base = os.path.join(
        "output",
        "quarterhourly",
        f"bs{bess['bucket_size']}cr{bess['c_rate']}rto{bess['roundtrip_eff']}mc{bess['max_cycles']}mt{bess['min_trades']}",
    )
    return {
        "base": base,
        "trades": os.path.join(base, "trades"),
        "profit": os.path.join(base, "profit.csv"),
    }

def ensure_paths(paths: dict):
    """Create dirs/files if missing."""
    os.makedirs(paths["base"], exist_ok=True)
    os.makedirs(paths["trades"], exist_ok=True)
    # 'profit' is a CSV file; ensure it exists
    if not os.path.exists(paths["profit"]):
        with open(paths["profit"], "w", encoding="utf-8") as f:
            f.write("day,profit\n")  # optional header

@st.cache_data # Caches the LOB data so it doesnt have to be loaded each time.
def load_price_data(path="../real_data/id_prices.parquet") -> pd.DataFrame:
    return pd.read_parquet(path)

def load_plotting_data(profitpath: str, start=None, end=None) -> pd.DataFrame:
    """Load profit.csv, keep a DateTimeIndex, and (optionally) slice by date."""
    df = pd.read_csv(profitpath, parse_dates=["day"])
    if df.empty:
        return df
    df = df.set_index("day").sort_index()
    if start or end:
        df = df.loc[start:end]
    return df

def plot_base_chart(df: pd.DataFrame):
    """ Bar (daily) + line (cumulative) with secondary y-axis and rangeslider."""
    if df.empty:
        st.info("No profit data to plot yet.")
        return

    cumulative_sum = df["profit"].cumsum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(x=df.index, y=df["profit"], name="Daily profit (€)")
    fig.add_scatter(x=df.index, y=cumulative_sum, name="Cumulative (€)", mode="lines+markers", secondary_y=True)

    fig.update_yaxes(title_text="Daily (€)", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative (€)", secondary_y=True)

    fig.update_xaxes(
        tickangle=-80,
        tickformat="%d %b",               # show day + month only
        rangeslider=dict(visible=True, thickness=0.10),
    )

    fig.update_layout(
        xaxis_title = "Day",
        title = f"Profits for {df.index[0].date()} – {df.index[-1].date()}",
        legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    st.plotly_chart(fig, use_container_width=True)




# -------------------------- Simulation --------------------------

def simulate_bess(period_start: pd.Timestamp,
                  period_end: pd.Timestamp,
                  bess: dict) -> None:
    """Run the simulation (side-effect: writes to files)."""
    # You can pass df directly or a path. Here we use the cached loader:
    df_prices = load_price_data()
    simulate_period(
        period_start,
        period_end,
        threshold=bess["threshold"],
        threshold_abs_min=bess["threshold_abs_min"],
        discount_rate=bess["discount_rate"],
        bucket_size=bess["bucket_size"],
        c_rate=bess["c_rate"],
        roundtrip_eff=bess["roundtrip_eff"],
        max_cycles=bess["max_cycles"],
        min_trades=bess["min_trades"],
        df=df_prices,
    )

# -------------------------- App State --------------------------

if "bess" not in st.session_state:
    st.session_state.bess = {}
if "paths" not in st.session_state:
    st.session_state.paths = {}
if "last_run_ok" not in st.session_state:
    st.session_state.last_run_ok = False

# -------------------------- UI --------------------------

st.markdown("### Welcome to Battery Data Charts")

with open("./Dashboard/ToDo_Streamlit.md", "r", encoding="utf-8") as f:
    st.markdown(f.read())

left_column, right_column = st.columns(2)

# ===== Left column: parameters and path resolution =====
with left_column:
    st.markdown("### BESS Simulation Parameters")
    with st.form("add_param"):
        # Explicit controls for all fields you store
        bucket_size    = st.number_input("Bucket Size of Rolling Window [mins]", value=15, step=1)
        c_rate         = st.number_input("C_Rate", value=1.0, step=0.1)
        roundtrip_eff  = st.number_input("Round Trip Efficiency", value=0.85, step=0.01)
        max_cycles     = st.number_input("Max cycles per year", value=float(365/12), step=1.0)
        min_trades     = st.number_input("Min No. Trades", value=5, step=1)

        # previously hard-coded; expose if needed
        discount_rate  = st.number_input("Discount rate", value=0.0, step=0.005, format="%.3f")
        threshold      = st.number_input("Threshold", value=0.0, step=0.1)
        threshold_abs_min = st.number_input("Absolute min threshold", value=0.0, step=0.1)

        saved = st.form_submit_button("Save / update")
        
    if saved:
        st.session_state.bess = {
            "bucket_size": bucket_size,
            "c_rate": c_rate,
            "roundtrip_eff": roundtrip_eff,
            "max_cycles": max_cycles,
            "min_trades": min_trades,
            "discount_rate": discount_rate,
            "threshold": threshold,
            "threshold_abs_min": threshold_abs_min,
        }
        # compute and store paths so both columns can use them
        st.session_state.paths = build_paths(st.session_state.bess)
        ensure_paths(st.session_state.paths)
        st.session_state.last_run_ok = False  # new params → require (re)run
        st.success("Parameters stored and paths prepared.")



# ===== Right column: current params and run button =====
with right_column:
    if st.session_state.bess:
        st.subheader("Current parameters")
        st.json(st.session_state.bess)

    if st.button("Run Simulation", type="primary", use_container_width=True):
        if not st.session_state.bess:
            st.error("Please save parameters first.")
        else:
            st.write("Simulation will run now")
            
            with st.spinner("Running simulation…"):
                try:
                    # Define the period here or make it user-configurable
                    period_start = pd.Timestamp("2025-02-01 00:00:00", tz="Europe/Berlin")
                    period_end   = pd.Timestamp("2025-03-01 02:00:00", tz="Europe/Berlin")

                    simulate_bess(period_start, period_end, st.session_state.bess)
                    st.session_state.last_run_ok = True
                    st.success("Simulation finished.")
                except Exception as ex:
                    st.session_state.last_run_ok = False
                    st.error(f"Simulation failed: {ex}")




# ===== Final: only plot when both sides are resolved and run succeeded (or results already exist) =====
profit_csv = st.session_state.paths.get("profit") if st.session_state.paths else None
if profit_csv and os.path.exists(profit_csv):
    # Plot if (a) last run finished OK, or (b) we already had historical results
    st.session_state.last_run_ok = True  if load_plotting_data(profit_csv).shape[0]>0 else st.info("Path Exists, but no simulation results exist! Run the Simulation")
    if st.session_state.last_run_ok or not st.session_state.bess:
        df_plot = load_plotting_data(profit_csv)
        plot_base_chart(df_plot)

