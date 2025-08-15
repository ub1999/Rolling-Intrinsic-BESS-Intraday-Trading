import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as ex
from plotly.subplots import make_subplots

# Title
st.set_page_config(page_title="Strategies", page_icon="📈")

with open("./Code/pages/1-Compare_Strategies.md", "r", encoding="utf-8") as f:
    st.markdown(f.read())

# Plot results of rolling intrinsic
df_bs_5 = pd.read_csv("./Dashboard/demo_output/quarterhourly/bs5cr1rto0.85mc30.416666666666668mt5/profit.csv")
df_bs_10 = pd.read_csv("./Dashboard/demo_output/quarterhourly/bs10cr1rto0.85mc30.416666666666668mt5/profit.csv")
df_bs_15 = pd.read_csv("./Dashboard/demo_output/quarterhourly/bs10cr1rto0.85mc30.416666666666668mt5/profit.csv")
df_bs_1 = pd.read_csv("./Dashboard/demo_output/quarterhourly/bs1cr1rto0.85mc30.416666666666668mt5/profit.csv")

x = df_bs_10["day"]
fig_daily_profits = make_subplots()

# bars on left axis
fig_daily_profits.add_bar(name="BS15", x=x, y=df_bs_15["profit"], offsetgroup=1, secondary_y=False,marker_color="red")

fig_daily_profits.add_bar(name="BS10", x=x, y=df_bs_10["profit"], offsetgroup=0, secondary_y=False,marker_color="blue")

fig_daily_profits.add_bar(name="BS5",  x=x, y=df_bs_5["profit"],  offsetgroup=2, secondary_y=False,marker_color="green")

fig_daily_profits.add_bar(name="BS1",  x=x, y=df_bs_1["profit"],  offsetgroup=3, secondary_y=False,marker_color="purple")


fig_daily_profits.update_layout(barmode="group", xaxis_title="Day",
                  yaxis_title="Daily (€)",
                  title="Daily profits in February with different Bucket Sizes (BS)")

st.plotly_chart(fig_daily_profits)


fig_cummulative_profit = make_subplots(1,2,column_widths=[0.7,0.3],subplot_titles=["Cummulative Revenue for Different BS","relative to  15min BS"])
# cumulative on right axis
fig_cummulative_profit.add_scatter(name="BS15 cummulative", x=x, y=df_bs_15["profit"].cumsum(),
                mode="lines+markers",line_color="red")

fig_cummulative_profit.add_scatter(name="BS10 cummulative", x=x, y=df_bs_10["profit"].cumsum(),
                mode="lines+markers", line_color="blue")

fig_cummulative_profit.add_scatter(name="BS5 cummulative",  x=x, y=df_bs_5["profit"].cumsum(),
                mode="lines+markers", line_color="green")

fig_cummulative_profit.add_scatter(name="BS1 cummulative",  x=x, y=df_bs_1["profit"].cumsum(),
                mode="lines+markers", line_color="purple")

fig_cummulative_profit.update_layout( xaxis_title="Day",
                  yaxis_title="Daily Cummulative (€)",
                  )


df_sum = pd.DataFrame(data=np.array([df_bs_15.profit.sum(),df_bs_10.profit.sum(),df_bs_5.profit.sum(),df_bs_1.profit.sum()]),columns=["revenue"])

df_sum.index = ["BS15","BS10","BS5","BS1"] 
df_sum = df_sum.divide(df_sum.loc["BS15",:],axis=1)
df_sum.loc[:,"color"] = ["red","Blue","Green","Purple"]
fig_cummulative_profit.add_bar(
    row=1,col=2,
    x = df_sum.index,
    y = df_sum["revenue"],
    marker_color = df_sum["color"],
    name = r"rel. rev")

fig_cummulative_profit.update_layout(    
    legend=dict(
        orientation="h",           # Horizontal legend
        yanchor="bottom",          # Anchor the legend to the bottom
        y=-0.3,                    # Place legend below the chart (adjust as needed)
        xanchor="center",          # Center the legend horizontally
        x=0.5                      # Center of the plot
    )
    )

st.plotly_chart(fig_cummulative_profit)

# Subheading
st.markdown("## Incorporating forecasts")