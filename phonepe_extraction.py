import os
import subprocess
import pandas as pd
import plotly.express as px
import mysql.connector
import os
import json
import streamlit as st
# Specify the GitHub repository URL
repository_url = "https://github.com/PhonePe/pulse.git"

# Define the directory where you want to clone the repository
clone_directory = "phonepe_pulse_data"

# Clone the repository
subprocess.run(["git", "clone", repository_url, clone_directory])


#st.write(df)
db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sql1795@",
        database="capstone"
    )

cursor1 = db_connection.cursor()
query1 = 'select * from Agg_Trans_table'
cursor1.execute(query1)
data1 = cursor1.fetchall()
query2 = 'select * from agg_userbydevice_table'
cursor1.execute(query2)
user_device= cursor1.fetchall()
query3 = 'select * from district_map_transaction_table'
cursor1.execute(query3)
district_tran= cursor1.fetchall()
query4 = 'select * from district_map_registering_table'
cursor1.execute(query4)
app_opening = cursor1.fetchall()
#############################################################################

df = pd.read_csv('Agg_Trans.csv', index_col=0)
st.write(df)
districts_tran = pd.read_csv('district_map_transaction.csv', index_col=0)
st.write(districts_tran)
app_open = pd.read_csv('district_registering_map.csv', index_col=0)
st.write(app_open)
user_bydevice = pd.read_csv('user_by_device.csv', index_col=0)
st.write(user_bydevice)
state = pd.read_csv('state_lat_long_columns.csv')
st.write(state)
districts = pd.read_csv('District_lat_long_columns.csv')
st.write(districts)


with st.container():
    st.title(':violet[PhonePe Pulse Data Visualization(2018-2022)📈]')
    #st.image('data/Data-Vizualisation.png')
    st.write(' ')
    st.subheader(
        ':violet[Registered user & App installed -> State and Districtwise:]')
    st.write(' ')
    scatter_year = st.selectbox('Please select the Year',
                                ('2018', '2019', '2020', '2021', '2022'))
    st.write(' ')
    scatter_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10)
    scatter_year = int(scatter_year)
    scatter_reg_df = app_open[(app_open['Year'] == scatter_year) & (
        app_open['State'] == scatter_state)]
    scatter_register = px.scatter(scatter_reg_df, x="District", y="Registered_user",  color="District",
                                  hover_name="District", hover_data=['Year', 'Quater', 'App_opening'], size_max=60)
    st.plotly_chart(scatter_register)
st.write(' ')


# ------------------------------------- Streamlit Tabs for various analysis -----------------------------------------------------------------
geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(
    ["Geographical analysis", "User device analysis", "Payment Types analysis", "Transacion analysis of States"])
# --------------------------------------------------- Device analysis statewise ------------------------------------------------------------
with Device_analysis:
    st.subheader(':violet[User Device analysis->Statewise:]')
    tree_map_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                          'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                          'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                          'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                          'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                          'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                          'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                          'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                          'uttarakhand', 'west-bengal'), index=10, key='tree_map_state')
    tree_map_state_year = int(st.radio('Please select the Year',
                                       ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='tree_map_state_year'))
    tree_map_state_quater = int(st.radio('Please select the Quarter',
                                         ('1', '2', '3', '4'), horizontal=True, key='tree_map_state_quater'))
    user_device_treemap = user_bydevice [(user_bydevice ['State'] == tree_map_state) & (user_bydevice ['Year'] == tree_map_state_year) &
                                      (user_bydevice ['Quater'] == tree_map_state_quater)]
    user_device_treemap['Brand_count'] = user_device_treemap['Brand_count'].astype(
        str)
    # ----------------------------------------- Treemap view of user device ----------------------------------------------------------------
    user_device_treemap_fig = px.treemap(user_device_treemap, path=['State', 'Brand'], values='Brand_percentage', hover_data=['Year', 'Quater'],
                                         color='Brand_count',
                                         title='User device distribution in ' + tree_map_state +
                                         ' in ' + str(tree_map_state_year)+' at '+str(tree_map_state_quater)+' quater',)
    st.plotly_chart(user_device_treemap_fig)
    # ---------------------------------------- Barchart view of user device -----------------------------------------------------------------
    bar_user = px.bar(user_device_treemap, x='Brand', y='Brand_count', color='Brand',
                      title='Bar chart analysis', color_continuous_scale='sunset',)
    st.plotly_chart(bar_user)


# ----------------------------------------- Payment type analysis of Transacion data ----------------------------------------------------------
with payment_analysis:
    st.subheader(':violet[Payment type Analysis -> 2018 - 2022:]')
    # querypa = 'select * from agg_transaction_table'
    # payment_mode = pd.read_sql(querypa, con=connection)
    payment_mode = pd.read_csv('Agg_Trans.csv', index_col=0)
    pie_pay_mode_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                              'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                              'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                              'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                              'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                              'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                              'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                              'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                              'uttarakhand', 'west-bengal'), index=10, key='pie_pay_mode_state')
    pie_pay_mode_year = int(st.radio('Please select the Year',
                                     ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='pie_pay_year'))
    pie_pay_mode__quater = int(st.radio('Please select the Quarter',
                                        ('1', '2', '3', '4'), horizontal=True, key='pie_pay_quater'))
    pie_pay_mode_values = st.selectbox(
        'Please select the values to visualize', ('Transacion_count', 'Transacion_amount'))
    pie_payment_mode = payment_mode[(payment_mode['Year'] == pie_pay_mode_year) & (
        payment_mode['Quater'] == pie_pay_mode__quater) & (payment_mode['State'] == pie_pay_mode_state)]
    # -------------------------------- Pie chart analysis of Payment mode --------------------------------------------------------------------
    pie_pay_mode = px.pie(pie_payment_mode, values=pie_pay_mode_values,
                          names='Transacion_type', hole=.5, hover_data=['Year'])
    # ------------------------------------- Bar chart analysis of payment mode ----------------------------------------------------------------
    pay_bar = px.bar(pie_payment_mode, x='Transacion_type',
                     y=pie_pay_mode_values, color='Transacion_type')
    st.plotly_chart(pay_bar)
    st.plotly_chart(pie_pay_mode)

# --------------------------------------- Transacion data analysis statewise ------------------------------------------------------------------
with transac_yearwise:
    st.subheader(':violet[Transaction analysis->Statewise:]')
    transac_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10, key='transac')
    transac__quater = int(st.radio('Please select the Quarter',
                                   ('1', '2', '3', '4'), horizontal=True, key='trans_quater'))
    transac_type = st.selectbox('Please select the Mode',
                                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='transactype')
    transac_values = st.selectbox(
        'Please select the values to visualize', ('Transacion_count', 'Transacion_amount'), key='transacvalues')
    payment_mode_yearwise = pd.read_csv('Agg_Trans.csv', index_col=0)

    # querypay_year = 'select * from agg_transaction_table'
    # payment_mode_yearwise = pd.read_sql(querypay_year, con=connection)

    new_df = payment_mode_yearwise.groupby(
        ['State', 'Year', 'Quater', 'Transacion_type']).sum()
    new_df = new_df.reset_index()
    chart = new_df[(new_df['State'] == transac_state) &
                   (new_df['Transacion_type'] == transac_type) & (new_df['Quater'] == transac__quater)]
    # ------------------------------- Bar chart analysis of transacion data statewise --------------------------------------------------------
    year_fig = px.bar(chart, x=['Year'], y=transac_values, color=transac_values, color_continuous_scale='armyrose',
                      title='Transacion analysis '+transac_state + ' regarding to '+transac_type)
    st.plotly_chart(year_fig)


# -------------------------------------------- Sidebar --> for overall india Data comparisons -------------------------------------------------
with st.sidebar:
    # -------------------------- Bar chart ofoverall india transacion data  -----------------------------------------------------------------
    st.subheader(':violet[Overall India Analysis:]')
    overall_values = st.selectbox(
        'Please select the values to visualize', ('Transacion_count', 'Transacion_amount'), key='values')
    overall = new_df.groupby(['Year']).sum()
    overall.reset_index(inplace=True)

    overall = px.bar(overall, x='Year', y=overall_values, color=overall_values,
                     title='Overall pattern of Transacion all over India', color_continuous_scale='sunset',)
    overall.update_layout(height=350, width=350)
    st.plotly_chart(overall)
    # --------------------------Bar chart of overall india user device analysis --------------------------------------------------------------
    # query_device = 'select * from agg_userbydevice_table'
    # user_device_overall = pd.read_sql(query_device, con=connection)
    user_device_overall = pd.read_csv('user_by_device.csv', index_col=0)
    overall_device = user_device_overall.groupby(['Brand', 'Year']).sum()
    overall_device.reset_index(inplace=True)

    overall_dev_fig = px.bar(overall_device, x='Year', y='Brand_count',
                             color='Brand', title='Customer Device pattern from 2018 - 2022')
    overall_dev_fig.update_layout(height=350, width=350)
    st.plotly_chart(overall_dev_fig)

    # --------------------------Bar chart of overall india registered and app opening --------------------------------------------------------
    # query_reg = 'select * from district_map_registering_table'
    # overall_reg = pd.read_sql(query5, con=connection)
    overall_reg = pd.read_csv('district_registering_map.csv')
    overall_reg = overall_reg.groupby(['State', 'Year']).sum()
    overall_reg.reset_index(inplace=True)

    overall_reg = px.bar(overall_reg, x='Year', y=[
                         'Registered_user', 'App_opening'], barmode='group', title='Phonepe installation from 2018 - 2022')
    overall_reg.update_layout(height=350, width=350)
    st.plotly_chart(overall_reg)