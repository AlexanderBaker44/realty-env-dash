import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/m_and_e_stacked.csv')
market_selection = df['MSA/Submarket']
market_list =list(set([str(i).split('_')[0] for i in market_selection]))
market_selection = st.selectbox('Select Market', market_list)
filtered_df = df[df['MSA/Submarket'].str.contains(market_selection)]
st.table(filtered_df)
