import pandas as pd
import numpy as np
import streamlit as st
import plotly as pt
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.offline as py
from pathlib import Path

# Web Settings
st.set_page_config(page_title="BASF Sales Analysis by Ellin", layout="wide")


st.write("Hi, It's Ellin")



########          ########          ########          ########          ########          ########          ######## 

def covid_impact_graph() :
    def calc_quantity_sales (sheet_name):
        df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
        df_data = df_data.dropna(axis=1)
        Y= df_data['Total'].values
        Yzip=[]
        for i in range (5):
            Yzip.append(Y[i*12:(i+1)*12].sum())
        return Yzip
    
    list_yearly_quantity_sales = []

    for i in ['A','B','C','D','E','F']:
        list_yearly_quantity_sales.append(calc_quantity_sales(i))

    np_total = np.array(list_yearly_quantity_sales)

    year = list(range(2016,2021))               # X
    Quantity = np_total.sum(axis = 0)           # Y


    def calc_net_sales (sheet_name):
        df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
        df_data = df_data.dropna(axis=1)
        Y= df_data['Sales'].values
        Yzip=[]
        for i in range (5):
            Yzip.append(Y[i*12:(i+1)*12].sum())
        return Yzip

    list_yearly_net_sales = []

    for i in ['A','B','C','D','E','F']:
        list_yearly_net_sales.append(calc_net_sales(i))

    np_total = np.array(list_yearly_net_sales)
    Net_Sales = np_total.sum(axis = 0)           # Y

    ########## ############# ############### ############## ###################

    # Tsble for Business Growth Rate  
    Q=[]
    for i in range (5):
        Current = Quantity[i]
        Previous = Quantity[i-1]
        YoY_Quantity = ((Current-Previous)/Previous)*100
        if YoY_Quantity > 100:
            Q.append("N/A")
        else:
            Q.append(YoY_Quantity)
    NS=[]
    for i in range (5):
        Current = Net_Sales[i]
        Previous = Net_Sales[i-1]
        YoY_Net_Sales = ((Current-Previous)/Previous)*100
        if YoY_Net_Sales > 100:
            NS.append("N/A")
        else:
            NS.append(YoY_Net_Sales)


    def round_up(object):
        rounded=[]
        for i in range (5):
            round_obj = object[i]
            if type(round_obj) == str:
                rounded.append(round_obj)
            else:
                round_obj = round(round_obj,3)
                rounded.append(round_obj)
        return rounded

    rounded_Quantity = round_up(Quantity)
    rounded_Q = round_up(Q)
    rounded_Net_Sales = round_up(Net_Sales)
    rounded_NS = round_up(NS)


    table_trace1 = go.Table(
            domain=dict(x=[0, 1],
                        y=[0, 1]),
            columnwidth = [100] + [130,130,130,130],  # Table Column Width
            columnorder=[0, 1, 2, 3, 4],
            header = dict(height = 25,
                        values = [['<b>Year</b>'],['<b>Quantity</b> (mT) '], ['<b>YoY_Quantity</b> (%)'],
                                    ['<b>Net Sales</b> (k€) '],['<b>YoY_Net_Sales</b> (%) ']],
                        line = dict(color='rgb(50, 50, 50)'),
                        align = ['left'] * 5,
                        font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                        fill = dict(color='#d562be')),
            cells = dict(values = [['2016','2017','2018','2019','2020'], rounded_Quantity, rounded_Q,  rounded_Net_Sales,  rounded_NS
                                    ],
                        line = dict(color='#506784'),
                        align = ['left'] * 5,
                        font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                        format = [None] + [", .2f"] * 2 + [',.4f'],
                        suffix=[None] * 4,
                        height = 27,
                        fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
        )
    layout1 = dict(
            width=1300,
            height=350,
            autosize=False,
            title='Annual Business Growth Rate',
            margin = dict(t=100),
            

            plot_bgcolor='rgba(228, 222, 249, 0.65)'
        )
    YoY_figure = dict(data=[table_trace1], layout=layout1)

    ########## ############# ############### ############## ###################
    # Plotting
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Original 2016-2020
    fig.add_trace(go.Scatter(name='Actual Net Sales ', x=year, y=Net_Sales), secondary_y=True)
    fig.add_trace(go.Bar(name='Actual Quantity Sales ', x=year, y=Quantity,width=[0.3, 0.3, 0.3, 0.3, 0.3]))

    # Predicted 2020 w/o COVID
    exp_quantity= np.array(716.68-Quantity[4])
    yr_2020=np.array(2020)
    

    Net_Sales[4] = np.array(21414.95)
    new_x = year[3:5]
    new_y = Net_Sales[3:5]
    
    fig.add_trace(go.Scatter(name='Expected Net Sales w/o COVID', x=new_x, y=new_y, mode='lines', line={'dash': 'dash', 'color': 'blue'}), secondary_y=True)
    fig.add_trace(go.Bar(name='Expected Quantity Sales w/o COVID', x=yr_2020, y=exp_quantity, width=[0.3]))


         
    # Add figure title
    fig.update_layout(
        width=1100,
        height=600,
        title_text="2016~2020yr Yearly Breakdown of UV Filter Sales vs. Month",
        yaxis_tickformat='M'
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # Set x-axis title
    fig.update_xaxes(title_text='<b>Year</b>')
    fig.update_layout(
        barmode='stack',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [2016,2017,2018,2019,2020],
        )
    )
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Quantity Sales</b> (tons) ", range=[0,900], secondary_y=False)
    fig.update_yaxes(title_text="<b>Net Sales</b> (k€) ", secondary_y=True)

    


    st.write(YoY_figure)
    st.markdown("""The average business growth for the past five years is X % for quantity and X % for net sales, respectively. With the calculated average YoY, the 2020 sales data should have been X mT for quantity sales and X k€ for net sales. These results are implemented in the yearly sales overview figure below.
    <br>""", unsafe_allow_html = True)

    st.write(fig)  
    st.markdown("""<br>The graph clearly shows the impact of COVID-19 on the UV filter business. In specific, the business growth from 2019 to 2020 decreased by X % for quantity sales and by X % for net sales. These negative business growth rates imply the UV filter product sales is heavily influenced in 2020. To return to the normal business growth rate more quickly, a thorough analysis of the sales trend and the understanding of the competitive sales profiles are required.
    <br>""", unsafe_allow_html = True)





covid_impact_graph()