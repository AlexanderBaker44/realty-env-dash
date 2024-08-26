import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/m_and_e_stacked.csv')
df_supply = pd.read_excel('data/dallas_apartment_data_rent_sf.xlsx',sheet_name = 'Supply')




with st.sidebar:
    page  = st.radio('Choose Page', ('Time Series','General Stats'))

if page == 'Time Series':
    market_list =list(set([str(i).split('_')[0] for i in df['MSA/Submarket']]))
    market_selection = st.selectbox('Select Market', market_list)
    filtered_df = df[df['MSA/Submarket'].str.contains(market_selection)]

    markets = list(filtered_df['MSA/Submarket'])
    filtered_df.drop(['Unnamed: 0','MSA/Submarket'],axis=1, inplace=True)
    p_df = filtered_df.T
    p_df.index = pd.to_datetime(p_df.index)
    p_df.columns = markets
    fig,x = plt.subplots(1,1)
    p_df.plot(kind = 'line', ax=x)
    st.pyplot(fig)



if page == 'General Stats':
    market_list_pop = list(set(df_supply['MSA/Submarket']))
    market_selection_pop = st.selectbox('Select Market', market_list_pop,key = '1')
    df_supply_filtered = df_supply[df_supply['MSA/Submarket'] == market_selection_pop]
    for i in df_supply_filtered.columns:
        values = list(df_supply_filtered[i])[0]
        st.subheader(f'{i}: {values}',divider =True)
