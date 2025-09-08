import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Make your local package importable (adds location of rolling intrinsic to system path variable)
path_RI = os.path.abspath(r"C:\Users\UnmuBhar\Documents\Intraday Research\POCs\Rolling-Intrinsic-BESS-Intraday-Trading\Code\Rolling Intrinsic\\")
sys.path.append(path_RI)

import Rolling_Intrinsic_QH as RI
print(os.path.exists("real_data/id_prices.parquet"))

print(RI.load_real_data("real_data/id_prices.parquet"))

#print(sys.path[-1])

# 
# sys.path.append(os.path.join(sys.path[0], path_RI))