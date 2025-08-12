import streamlit as st
# Title
st.set_page_config(page_title="Strategies", page_icon="📈")

with open("./Code/pages/1-Compare_Strategies.md", "r", encoding="utf-8") as f:
    st.markdown(f.read())
# Plot results of rolling intrinsic
# Subheading
st.markdown("## Different rolling windows in rolling intrinsic approach")

# Subheading
st.markdown("## Incorporating forecasts")