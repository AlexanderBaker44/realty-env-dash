import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/m_and_e_stacked.csv')
market_selection = df['MSA/Submarket']
market_list =list(set([str(i).split('_')[0] for i in market_selection]))
market_selection = st.selectbox('Select Market', market_list)


filtered_df = df[df['MSA/Submarket'].str.contains(market_selection)]
markets = list(filtered_df['MSA/Submarket'])
st.write(markets)

filtered_df.drop(['Unnamed: 0','MSA/Submarket'],axis=1, inplace=True)

p_df = filtered_df.T
p_df.columns = markets
st.table(filtered_df)
fig,x = plt.subplots(1,1)
p_df.plot(kind = 'line', ax=x)
st.pyplot(fig)
