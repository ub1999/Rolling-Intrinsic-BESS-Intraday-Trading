import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.relpath("./Code/Rolling Intrinsic/"))
from Rolling_Intrinsic_QH import simulate_period
# ================== Helper Function ==================
# ======== Plotting Data ================
def load_plotting_data(start_date ="02.01.2025" ,end_date = "03.01.2025", profitpath = "")->pd.DataFrame:
    filter = slice(start_date, end_date)
    initial_results = pd.read_csv(profitpath,
                            index_col="day",
                            parse_dates=True
                            )
    initial_results.index = initial_results.index.strftime("%D")
    initial_results = initial_results[filter]
    return initial_results

# ==== Plot main chart
def plot_base_chart(initial_results : pd.DataFrame):
    # Initial Plots
    fig = px.bar(initial_results.reset_index(),x="day",y="profit")
    fig.update_xaxes(tickangle=-80)
    fig = px.bar(
        initial_results.reset_index(),
        x="day",
        y="profit",
        labels={"profit": "Daily profit (€)"}
    )

    # cumulative line (right y-axis)
    fig.add_trace(
        go.Scatter(
            x=initial_results.reset_index()["day"],
            y=initial_results["profit"].cumsum(),
            mode="lines+markers",
            name="Cumulative profit",
            yaxis="y2"                 # <- tell Plotly to use the 2nd axis
        )
    )

    # define and format the second y-axis
    fig.update_layout(
        yaxis2=dict(
            title="Cumulative (€)",
            overlaying="y",           # share the same x-axis
            side="right"              # draw on the right
        ),
        xaxis_title="Day",
        title = f"Profits for {initial_results.index[0]} - {initial_results.index[-1]}",
        xaxis = dict(
            rangeslider = dict(visible=True,
                            thickness=0.1,
                            
                            )
            )
    ) 

    st.plotly_chart(fig)
    return

# ========== Create the files if its a new simulation ============= 
def create_simulation_results_path(path,tradepath,profitpath)->None:
    if not os.path.exists(path):
        # Create a new path 
        os.mkdir(path=path)
        st.write(f"Created new directory : {path}")
        if not os.path.exists(tradepath): 
            st.write(f"File {tradepath} not found!")
            st.write(f"Creating new file : {tradepath}")
            os.mkdir(tradepath)
        if not os.path.exists(profitpath):
            st.write(f"File {profitpath} not found!")
            st.write(f"Creating new file: {profitpath}")
            f = open(profitpath, "w")
        return 


@st.cache_data
def load_price_data(path = "id_prices.parquet")->pd.DataFrame:
    df = pd.read_parquet(path)
    return df

@st.cache_data()
def simulate_bess()->None:
    period_start = pd.Timestamp("2025-02-01 00:00:00",tz="Europe/Berlin")
    period_end = pd.Timestamp("2025-02-05 02:00:00",tz="Europe/Berlin")
    
    simulate_period(
    period_start,
    period_end,
    threshold = st.session_state.bess["threshold"],
    threshold_abs_min = st.session_state.bess["threshold_abs_min"],
    discount_rate = 0,
    bucket_size = st.session_state.bess["bucket_size"],
    c_rate = st.session_state.bess["c_rate"],
    roundtrip_eff = st.session_state.bess["roundtrip_eff"],
    max_cycles = st.session_state.bess["max_cycles"],# only feb 
    min_trades = st.session_state.bess["min_trades"],
    #df = load_real_data(real_path)
    df = load_price_data()
    )
    
    return None





# Assume everything is run from the Rolling Intrinsic Parent directory
# ─────────────────────────────────────────────────────────────
# init the dict in session_state (only first run)
# ────────────────────────────────────────────────────────────
if "bess" not in st.session_state:
    st.session_state.bess = {}

st.markdown("### Welcome to Battery Data Charts")

with open("./Dashboard/ToDo_Streamlit.md","r") as f:
    mkdow_str = f.read()
    st.markdown(body=mkdow_str)


# ========== LEFT COLUMN ==========
left_column,right_column = st.columns(2)
with left_column:
    st.markdown("### BESS Simulation Parameters")  
    with st.form("add_param"):
        threshold = 0
        threshold_abs_min = 0
        discount_rate = 0
        bucket_size = st.number_input("Bucket Size of Rolling Window [mins]",value=15)
        c_rate = st.number_input("C_Rate",value=1)
        roundtrip_eff = st.number_input("Round Trip Efficiency",value=0.85)
        max_cycles = (365/12)*1
        min_trades = st.number_input("Min No. Trades",value=5)
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
        st.success("Parameters stored")
        # ========== Results File Paths ==========
        path = os.path.join(
                "output",
                "quarterhourly",
                "bs"
                + str(bucket_size)
                + "cr"
                + str(c_rate)
                + "rto"
                + str(roundtrip_eff)
                + "mc"
                + str(max_cycles)
                + "mt"
                + str(min_trades)
            )
        tradepath = os.path.join(path, "trades")
        profitpath = os.path.join(path, "profit.csv")
        if (os.path.exists(profitpath) & (os.path.exists(tradepath))) & (os.path.exists(path)):
            st.write("Simulation results already exist!")
            plot_base_chart(initial_results=load_plotting_data(profitpath=profitpath))
        else:
            st.write("Simulation results don't exist! Run a new simulation")
            create_simulation_results_path(path,tradepath=tradepath,profitpath=profitpath)



# ========== RIGHT COLUMN ==========
with right_column:
    if st.session_state.bess:
        st.write("Current parameters")
        st.json(st.session_state.bess)
    if st.button("Run Simulation"):
        st.write("Simulation will run now")
        with st.spinner("Running simulation…"):
            simulate_bess()
            st.success("Simulation Finished")
        plot_base_chart(load_plotting_data(profitpath = profitpath))

