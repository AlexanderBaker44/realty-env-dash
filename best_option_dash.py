import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df_market = pd.read_csv('data/edited_market.csv')
df_effective = pd.read_csv('data/edited_effective.csv')

df_market.drop('index',axis = 1, inplace=True)
df_effective.drop('index',axis = 1, inplace=True)

market_list =list(set([str(i).split('_')[0] for i in df_market['MSA/Submarket']]))
market_list.sort()

market_selection = st.selectbox('Select Market From List:', market_list)

df_market.index = df_market['MSA/Submarket']
df_mar_edited=df_market.drop('MSA/Submarket',axis=1)
df_effective.index = df_effective['MSA/Submarket']
df_eff_edited=df_effective.drop('MSA/Submarket',axis=1)

def get_differences(df,df_type,market_selection):
    df.loc['value_difference'] = df.loc['mean value'] - df.loc[f'{market_selection}_{df_type}']
    return df


df_mar_select_diff = get_differences(df_mar_edited,'market',market_selection)
df_eff_select_diff = get_differences(df_eff_edited,'effective',market_selection)

df_full_selection = pd.concat([df_mar_select_diff,df_eff_select_diff])
df_full_selection.loc['eff_mar_difference'] = df_full_selection.loc[f'{market_selection}_market'] - df_full_selection.loc[f'{market_selection}_effective']

df_mar_line = df_mar_select_diff.loc[[f'{market_selection}_market','value_difference']].T
st.table(df_mar_line)
df_mar_line.index = pd.to_datetime(df_mar_line.index)
df_eff_line = df_eff_select_diff.loc[[f'{market_selection}_effective','value_difference']].T
st.table(df_eff_line)
df_eff_line.index = pd.to_datetime(df_eff_line.index)
dff_line = df_full_selection.loc['eff_mar_difference'].T
dff_line.index = pd.to_datetime(dff_line.index)

fig,[axe,axs] = plt.subplots(2,1)
df_mar_line['value_difference'].plot(kind = 'line',ax=axe)
#st.pyplot()
df_eff_line['value_difference'].plot(kind = 'line',ax=axe)
dff_line.plot(kind = 'line',ax=axs)
fig.tight_layout(pad=1.0)
st.pyplot(fig)

df_vel = pd.read_csv('data/full_vel_df.csv')

df_percent = pd.read_csv('data/full_percent_df.csv')

df_vel_filter = df_vel[df_vel['MSA/Submarket'].str.contains(market_selection)]
df_vel_plot = df_vel_filter
df_vel_plot.index = df_vel_filter['MSA/Submarket']
df_vel_plot.drop('MSA/Submarket',axis=1,inplace=True)
df_vel_plot = df_vel_plot.T
df_vel_plot.plot(kind = 'bar')
st.pyplot()
df_percent_filter = df_percent[df_percent['MSA/Submarket'].str.contains(market_selection)]
df_percent_plot = df_percent_filter
df_percent_plot.index = df_percent_plot['MSA/Submarket']
df_percent_plot.drop('MSA/Submarket',axis=1,inplace=True)
df_percent_plot = df_percent_plot.T
df_percent_plot.plot(kind = 'bar')
st.pyplot()
