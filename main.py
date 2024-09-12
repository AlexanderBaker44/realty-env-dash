import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

model_files = os.listdir('models')

model_files.sort()

df = pd.read_csv('data/m_and_e_stacked.csv')
df_supply = pd.read_excel('data/dallas_apartment_data_rent_sf.xlsx',sheet_name = 'Supply')
market_list =list(set([str(i).split('_')[0] for i in df['MSA/Submarket']]))
market_list.sort()

market_dict = dict(zip(market_list,model_files))

with st.sidebar:
    page  = st.radio('Choose Page', ('Time Series','General Stats', 'Models'))

if page == 'Time Series':

    market_selection = st.selectbox('Select Market', market_list)
    filtered_df = df[df['MSA/Submarket'].str.contains(market_selection)]

    markets = list(filtered_df['MSA/Submarket'])
    filtered_df.drop(['Unnamed: 0','MSA/Submarket'],axis=1, inplace=True)
    p_df = filtered_df.T
    p_df.index = pd.to_datetime(p_df.index)
    p_df.columns = markets
    st.markdown('## Markets Over Time:')
    st.write('This page observes the historical data of both the market and effective rent.')
    fig,x = plt.subplots(1,1)
    p_df.plot(kind = 'line', ax=x)
    st.pyplot(fig)



if page == 'General Stats':
    market_list_pop = list(set(df_supply['MSA/Submarket']))
    market_selection_pop = st.selectbox('Select Market', market_list_pop,key = '1')
    df_supply_filtered = df_supply[df_supply['MSA/Submarket'] == market_selection_pop]
    st.markdown('## Market Metrics:')
    st.markdown('This page displays the additional overall metrics of each market.')
    for i in df_supply_filtered.columns:
        values = list(df_supply_filtered[i])[0]
        st.subheader(f'{i}: {values}',divider =True)

if page == 'Models':
    market_selection = st.selectbox('Select Market', market_list)
    market_file = market_dict[market_selection]
    df_input = pd.read_csv(f'models/{market_file}')
    df_selection = df_input[['ds','yhat','m']]
    df_selection.index = pd.to_datetime(df_input['ds'])
    df_selection.columns = ['ds','effective_rent','market_rent']
    print(df_selection)
    st.markdown('## Facebook Prophet Models:')
    st.markdown('This page displays the deconstructed results of the Facebook Prophet model. The model predicts the effective rent for a market, while the market rate is used as a feature.')
    fig,(x1,x2) = plt.subplots(2,1)
    fig.tight_layout(pad=1.0)
    df_selection.plot(y='effective_rent',kind ='line',ax=x1, color = 'blue')
    df_selection.plot(y='market_rent',kind ='line',ax=x2,color='red')
    st.pyplot(fig)
