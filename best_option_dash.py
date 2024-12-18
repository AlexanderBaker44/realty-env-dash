import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df_market = pd.read_csv('data/edited_market.csv')
df_effective = pd.read_csv('data/edited_effective.csv')
df_supply = pd.read_excel('data/dallas_apartment_data_rent_sf.xlsx',sheet_name = 'Supply')

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
#st.table(df_mar_line)
df_mar_line.index = pd.to_datetime(df_mar_line.index)
df_eff_line = df_eff_select_diff.loc[[f'{market_selection}_effective','value_difference']].T
#st.table(df_eff_line)
df_eff_line.index = pd.to_datetime(df_eff_line.index)
dff_line = df_full_selection.loc['eff_mar_difference'].T
dff_line.index = pd.to_datetime(dff_line.index)

with st.sidebar:
    page  = st.radio('Choose Page', ('Differences','Velocity', 'Percent Change','Total Rating'))



if page == 'Differences':
    st.title('Difference Plots')
    fig,[axe,axs] = plt.subplots(2,1)
    df_mar_line['value_difference'].plot(kind = 'line',ax=axe,title = 'Difference Between Market Means and Values Over Time', xlabel = 'Time',ylabel = 'Value Difference')

    df_eff_line['value_difference'].plot(kind = 'line',ax=axe)
    axe.legend(labels = ['value_difference_market','value_difference_effective'])
    dff_line.plot(kind = 'line',ax=axs, title = 'Difference Between Market and Effective Rates Over Time', xlabel = 'Time',ylabel = 'Market and Effective Difference')
    fig.tight_layout(pad=1.0)
    st.pyplot(fig)

df_vel = pd.read_csv('data/full_vel_df.csv')

df_percent = pd.read_csv('data/full_percent_df.csv')

df_vel_filter = df_vel[df_vel['MSA/Submarket'].str.contains(market_selection)]
df_vel_plot = df_vel_filter
df_vel_plot.index = df_vel_filter['MSA/Submarket']
df_vel_plot.drop('MSA/Submarket',axis=1,inplace=True)
df_vel_plot = df_vel_plot.T

if page == 'Velocity':
    st.title('Velocity Plot')
    fig2, ax5 = plt.subplots()

    df_vel_plot.plot(kind = 'bar',ax=ax5, title = 'Market and Effective Rate Velocity Over Time', xlabel = 'Time',ylabel = 'Value Velocity')
    st.pyplot(fig2)

df_percent_filter = df_percent[df_percent['MSA/Submarket'].str.contains(market_selection)]
df_percent_plot = df_percent_filter
df_percent_plot.index = df_percent_plot['MSA/Submarket']
df_percent_plot.drop('MSA/Submarket',axis=1,inplace=True)
df_percent_plot = df_percent_plot.T

if page == 'Percent Change':
    st.title('Percent Change')
    fig3, ax6 = plt.subplots()

    df_percent_plot.plot(kind = 'bar',ax=ax6, title = 'Market and Effective Rate Percent Change Over Time', xlabel = 'Time',ylabel = 'Percent Change')
    st.pyplot(fig3)

final_line_vel = df_vel_plot.tail(1)[f'{market_selection}_effective'].iloc[0]
final_line_percent_change = df_percent_plot.tail(1)[f'{market_selection}_effective'].iloc[0]
final_line_eff = df_eff_select_diff.tail(1).T.tail(1)['value_difference'].iloc[0]
final_line_mar_eff_diff = df_full_selection.loc['eff_mar_difference'].T.tail(1).iloc[0]


supply_data = df_supply[df_supply['MSA/Submarket'] == market_selection]
print(supply_data.columns)
net_absorption = supply_data['2024 Net Absorption (YTD)'].iloc[0]
net_delivery = supply_data['2024 Deliveries (YTD)'].iloc[0]
total_units = supply_data['Total Units '].iloc[0]

if page == 'Total Rating':
    st.title('Select Weight for Each Factor')
    weight_vel_val = st.slider('Select weight of the latest effective velocity',0,100,key = '1')

    weight_per_val = st.slider('Select weight of the latest effective percent difference',0,100,key ='2')

    weight_eff_val = st.slider('Select weight of the latest effective mean difference',0,100,key ='3')

    weight_eff_mar_diff_val = st.slider('Select weight of the latest effective and market difference',0,100,key = '4')

    weight_net_absorption_val = st.slider('Select weight of the 2024 net asorption',0,100,key = '5')

    weight_net_delivery_val = st.slider('Select weight of the 2024 net delivery',0,100,key = '6')

    total_units_weight_val = st.slider('Select total unit weight',0,100,key = '7')

    print(final_line_mar_eff_diff)
    print(final_line_vel)
    print(final_line_percent_change)
    print(final_line_eff)
    print(net_absorption)
    try:
        total_val = weight_vel_val/100*final_line_vel+final_line_percent_change*weight_per_val/100+\
        final_line_eff/100*weight_eff_val+weight_eff_mar_diff_val/100*final_line_mar_eff_diff+\
        weight_net_absorption_val/100*net_absorption+weight_net_delivery_val/100*net_delivery+\
        total_units*1/1000*total_units_weight_val/100

        total_val_formatted = round(total_val,5)
        st.markdown(f' ## Weighted Value: {total_val_formatted}')
    except:
        st.write('Please Enter a Total of Four Weights')
