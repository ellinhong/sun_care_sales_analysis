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
import datetime as dt
from sklearn.linear_model import LinearRegression
import os
from os.path import join

# Web Settings
st.set_page_config(page_title="BASF Sales Analysis by Ellin", layout="wide")



# Logo
col1, col2, col3 = st.beta_columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.write("")
with col3:
    st.image("./basf_blue.png")


st.markdown("""<style>.subject-font {font-size:40px}</style>""", unsafe_allow_html=True)     
st.markdown("""<style>.big-font {font-size:30px}</style>""", unsafe_allow_html=True)

#### Title #####
st.markdown('<b><p class="subject-font"> **BASF A-EMA/AR: UV Filter Sales Analysis**</p></b>', unsafe_allow_html=True)
st.markdown('<div style="text-align: right"> Author : Ellin Hong </div> <br>', unsafe_allow_html=True)



def run():
    ########          ########          ########          ########          ########          ########          ######## 
    st.markdown("""     <sup>*<sup>  Please note that due to confidentiality, data manipulation was conducted but to the extent that it features the general trends and some of the data are replaced with variables.
    <br><br> """, unsafe_allow_html = True)

    def covid_impact_graph() :
        def calc_quantity_sales (sheet_name):
            df_data = pd.read_excel('blank_file.xlsx', sheet_name = sheet_name, header = 1)
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
                            values = [['<b>Year</b>'],['<b>Quantity</b> (lb) '], ['<b>YoY_Quantity</b> (%)'],
                                        ['<b>Net Sales</b> (k$) '],['<b>YoY_Net_Sales</b> (%) ']],
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
        exp_quantity= np.array(1.0247*Quantity[3]-Quantity[4])
        yr_2020=np.array(2020)
        

        Net_Sales[4] = np.array(39189)
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
        fig.update_yaxes(title_text="<b>Quantity Sales</b> (lb) ", range=[0,900], secondary_y=False)
        fig.update_yaxes(title_text="<b>Net Sales</b> (k$) ", secondary_y=True)

        


        st.write(YoY_figure)
        st.markdown("""The average business growth for the past five years is X % for quantity and X % for net sales, respectively. With the calculated average YoY, the 2020 sales data should have been X lb for quantity sales and X k$ for net sales. These results are implemented in the yearly sales overview figure below.
        <br>""", unsafe_allow_html = True)

        st.write(fig)  
        st.markdown("""<br>The graph clearly shows the impact of COVID-19 on the UV filter business. In specific, the business growth from 2019 to 2020 decreased by X % for quantity sales and by X % for net sales. These negative business growth rates imply the UV filter product sales is heavily influenced in 2020. To return to the normal business growth rate more quickly, a thorough analysis of the sales trend and the understanding of the competitive sales profiles are required.
        <br>""", unsafe_allow_html = True)







    ########          ########          ########          ########          ########          ########          ########          

    def total_relationship():
        Total = np.zeros(60)
        Total_Net_Sales = np.zeros(60)

        Month = ['Jan,2016',  'May, 2016', 'Sep,2016',
        'Jan,2017', 'May, 2017', 'Sep,2017',
        'Jan,2018', 'May, 2018', 'Sep,2018',
        'Jan,2019', 'May, 2019', 'Sep,2019',
        'Jan,2020', 'May, 2020', 'Sep,2020','Dec, 2020'
        ]
        df = pd.DataFrame(index=pd.date_range(start = dt.datetime(2016,1,1), end = dt.datetime(2020,12,31), freq='M'))
        month_year_list=df.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%B %Y')).tolist()

        for i in ['A','B','C','D','E','F']:
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = i, header = 1)
            df_data['Month,Year']=month_year_list
            df_data = df_data.set_index('Month,Year')
            Total = Total + df_data['Total']
            Total_Net_Sales = Total_Net_Sales + df_data['Sales']


        fig = px.line(
                    x=df_data.index, 
                    y=[Total,Total_Net_Sales]
                    )
        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # fig.add_trace(go.Scatter(name='Net Profit Sales ', x=df_data.index, y=Total_Net_Sales), secondary_y=True)
        # fig.add_trace(go.Bar(name='Quantity Sales ', x=df_data.index, y=Total))
        
        fig.add_trace(go.Bar(name='Quantity Sales ', x=df_data.index, y=Total,marker=dict(color='red')))
        fig.add_trace(go.Scatter(name='Net Profit Sales ', x=df_data.index, y=Total_Net_Sales,marker=dict(color='royalblue')), secondary_y=True)
        
            
        # Add figure title
        fig.update_layout(
            width=1100,
            height=600,
            title_text="2016~2020yr Total UV Filter Sales vs. Month",
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
        fig.update_xaxes(title_text='<b>Month, Year</b>')
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,59,60],
                ticktext = Month
            )
        )

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Quantity Sales</b> (lb) ",  secondary_y=False)
        fig.update_yaxes(title_text="<b>Net Profit Sales</b> (k$) ", secondary_y=True)

    
        st.write(fig)  
        




    ########          ########          ########          ########          ########          ########          ########          ########          






    def overall_trend_quantity_by_month():

        Month = ['Jan,2016',  'May, 2016', 'Sep,2016',
        'Jan,2017', 'May, 2017', 'Sep,2017',
        'Jan,2018', 'May, 2018', 'Sep,2018',
        'Jan,2019', 'May, 2019', 'Sep,2019','Dec,2019'
        ]

        df = pd.DataFrame(index=pd.date_range(start = dt.datetime(2016,1,1), end = dt.datetime(2019,12,31), freq='M'))
        month_year_list=df.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%B %Y')).tolist()

        empty = []
        for i in ['A','B','C','D','E','F']:
                df_data = pd.read_excel('blank_file.xlsx',sheet_name = i, header = 1)
                df_data = df_data.dropna(axis=1)
                df_data=df_data[:48]
                month= month_year_list              
                x_input = [[x,1] for x in month]  

                Y= df_data['Total'].values
                empty.append(Y)
        A,B,C,D,E,F = empty

        fig = px.line(
                x=month, 
                y=[A,B,C,D,E,F]
                )
        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(name='A', x=month, y=A))
        fig.add_trace(go.Scatter(name='B', x=month, y=B))
        fig.add_trace(go.Scatter(name='C', x=month, y=C))
        fig.add_trace(go.Scatter(name='D', x=month, y=D))
        fig.add_trace(go.Scatter(name='E', x=month, y=E))
        fig.add_trace(go.Scatter(name='F', x=month, y=F))

        fig.update_layout(
            title_text='Monthly Sales Quantity by Each Product vs. Year'
            )

        # Set x-axis title
        fig.update_xaxes(title_text="<b>Month, Year</b>")
        fig.update_yaxes(title_text="<b>Yearly sales qunatity</b> (Metric lb)")
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0,4,8,12,16,20,24,28,32,36,40,44,47,48],
                ticktext = Month
                ),
            legend = dict(
                x=0.95,
                y=1
            ))
        st.write(fig) 
        



    ########          ########          ########          ########          ########          ########          ########          ########          




    def overall_trend_net_sales_by_month():

        Month = ['Jan,2016',  'May, 2016', 'Sep,2016',
        'Jan,2017', 'May, 2017', 'Sep,2017',
        'Jan,2018', 'May, 2018', 'Sep,2018',
        'Jan,2019', 'May, 2019', 'Sep,2019','Dec,2019'
        ]

        df = pd.DataFrame(index=pd.date_range(start = dt.datetime(2016,1,1), end = dt.datetime(2019,12,31), freq='M'))
        month_year_list=df.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%B %Y')).tolist()


        empty = []
        for i in ['A','B','C','D','E','F']:
                df_data = pd.read_excel('blank_file.xlsx',sheet_name = i, header = 1)
                df_data = df_data.dropna(axis=1)
                df_data=df_data[:48]
                month= month_year_list              # Output : RangeIndex (start=0,stop=60,step=1)
                x_input = [[x,1] for x in month]   # Output : [[0,1],[1,1]..]

                Y= df_data['Sales'].values
                empty.append(Y)
        A,B,C,D,E,F = empty

        fig = px.line(
                x=month, 
                y=[A,B,C,D,E,F]
                )
        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(name='A', x=month, y=A))
        fig.add_trace(go.Scatter(name='B', x=month, y=B))
        fig.add_trace(go.Scatter(name='C', x=month, y=C))
        fig.add_trace(go.Scatter(name='D', x=month, y=D))
        fig.add_trace(go.Scatter(name='E', x=month, y=E))
        fig.add_trace(go.Scatter(name='F', x=month, y=F))

        fig.update_layout(
            title_text='Monthly Net Sales by Each product vs. Month'
            )

        # Set x-axis title
        fig.update_xaxes(title_text="<b>Month, Year</b>")
        fig.update_yaxes(title_text="<b>Yearly Net Sales</b> (k$)")
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0,4,8,12,16,20,24,28,32,36,40,44,47,48],
                ticktext = Month
            ),
            legend = dict(
                x=0.95,
                y=1
            ))
        st.write(fig) 




    ########          ########          ########          ########          ########          ########          ########          ########    





    def overall_trend_quantity_by_year():

        def calc_sales (sheet_name):
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y= df_data['Total'].values
            Yzip=[]
            for i in range (4):
                Yzip.append(Y[i*12:(i+1)*12].sum())
            return Yzip

        year=list(range(2016,2020))
        list_yearly_sales = []
        sheet_name = ['A','B','C','D','E','F']

        for i in sheet_name:
            list_yearly_sales.append(calc_sales(i))
        A,B,C,D,E,F = list_yearly_sales
        
        fig = px.line(
                x=year, 
                y=[A,B,C,D,E,F]
                )
        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(name='A', x=year, y=A))
        fig.add_trace(go.Scatter(name='B', x=year, y=B))
        fig.add_trace(go.Scatter(name='C', x=year, y=C))
        fig.add_trace(go.Scatter(name='D', x=year, y=D))
        fig.add_trace(go.Scatter(name='E', x=year, y=E))
        fig.add_trace(go.Scatter(name='F', x=year, y=F))

        fig.update_layout(
            title_text='Yearly Sales Quantity by Each Product vs. Year'
            )

        # Set x-axis title
        fig.update_xaxes(title_text="<b>Year</b>")
        fig.update_yaxes(title_text="<b>Yearly sales qunatity</b> (Metric lb)")
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [2016,2017,2018,2019],
                ticktext = [2016,2017,2018,2019]
                ),
            legend = dict(
                x=0.95,
                y=1
            ))
        
        st.write(fig) 
        




    ########          ########          ########          ########          ########          ########          ########          ########    






    def overall_trend_money_by_year():

        def calc_sales (sheet_name):
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y= df_data['Sales'].values
            Yzip=[]
            for i in range (4):
                Yzip.append(Y[i*12:(i+1)*12].sum())
            return Yzip

        year=list(range(2016,2020))
        list_yearly_sales = []
        sheet_name = ['A','B','C','D','E','F']

        for i in sheet_name:
            list_yearly_sales.append(calc_sales(i))
        A,B,C,D,E,F = list_yearly_sales
        
        fig = px.line(
                x=year, 
                y=[A,B,C,D,E,F]
                )
        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(name='A', x=year, y=A))
        fig.add_trace(go.Scatter(name='B', x=year, y=B))
        fig.add_trace(go.Scatter(name='C', x=year, y=C))
        fig.add_trace(go.Scatter(name='D', x=year, y=D))
        fig.add_trace(go.Scatter(name='E', x=year, y=E))
        fig.add_trace(go.Scatter(name='F', x=year, y=F))

        fig.update_layout(
            title_text='Yearly Net Sales by Each Product vs. Year'
            )

        # Set x-axis title
        fig.update_xaxes(title_text="<b>Year</b>")
        fig.update_yaxes(title_text="<b>Yearly Net Sales</b> (k$)")
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [2016,2017,2018,2019],
                ticktext = [2016,2017,2018,2019]
            ),
            legend = dict(
                x=0.95,
                y=1
            ))
            
        
        st.write(fig) 





    ########          ########          ########          ########          ########          ########          ########          ########    


    # f'''&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product {i} : ''' 


    def each_prod_monthly_review():
        dict_description = {
            'A':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product A : Sold most in Q1 and almost no sales in Q3', 
            'B':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product B : No trend (order placement after consuming the previous order)', 
            'C':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product C : Highest peaks in H1 and similar trend as Product B (order placement after consuming the previous order)', # just bolded exp
            'D':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product D : Highest sales in Q1 and sales halven for the rest of quarters',  # title 2 (not bolded)
            'E':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product E : Sales slightly higher in H1 than H2 but mostly no trend observed', # italicized
            'F':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Notable trends for Product F : Highest sales in H1 and almost no sales in Q3. Note that 2019 sales is unusually high for H2.'} # just text

        Month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        Year = ['2016','2017','2018','2019','2020']

        df = pd.DataFrame(index=pd.date_range(start = dt.datetime(2016,1,1), end = dt.datetime(2020,12,31), freq='M'))
        month_year_list = df.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%B %Y')).tolist()    


        for i in ['A','B','C','D','E','F']:
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = i , header = 1)
            df_data = df_data.dropna(axis=1)
            df_data['Month,Year']=month_year_list
            df_data.set_index('Month,Year')  
            df = df_data[['Month,Year','Total','Sales','cCM1']]  # use df.map to merge two columns (month+year)
            x = np.array(Month)
            Y = df_data['Sales'].values
            Y = np.reshape(Y, (-1, 12))
            y1,y2,y3,y4,y5 = Y

            table_trace1 = go.Table(
                domain=dict(x=[0, 0.4],
                            y=[0, 1]),
                columnwidth = [85] + [ 80, 80, 70],  # Table Column Width
                columnorder=[0, 1, 2, 3],
                header = dict(height = 25,
                            values = [['<b>Month,Year</b>'], ['<b>Quantity </b> (lb) '],
                                        ['<b>Net Sales</b> (k$) '],['<b>cCM1</b> (k$) ']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = [df['Month,Year'].values, df['Total'].values.round(3), df['Sales'].values.round(3),df['cCM1'].values.round(3)],
                            line = dict(color='#506784'),
                            align = ['left'] * 4,
                            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                            format = [None] + [", .2f"] * 2 + [',.4f'],
                            suffix=[None]*4,
                            height = 27,
                            fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
            )

            trace1=go.Scatter(
                name='2016',
                x=x,
                y=y1,
                xaxis='x',
                yaxis='y',
                mode='lines',
                line=dict(width=2, color='royalblue')
            )

            trace2=go.Scatter(
                name='2017',
                x=x,
                y=y2,
                xaxis='x',
                yaxis='y',
                mode='lines',
                line=dict(width=2, color='indigo')
            )

            trace3=go.Scatter(
                name='2018',
                x=x,
                y=y3,
                xaxis='x',
                yaxis='y',
                mode='lines',
                line=dict(width=2, color='#b04553')
            )

            trace4=go.Scatter(
                name='2019',
                x=x,
                y=y4,
                xaxis='x',
                yaxis='y',
                mode='lines',
                line=dict(width=2, color='#af7bbd')
            )

            trace5=go.Scatter(
                name='2020',
                x=x,
                y=y5,
                xaxis='x',
                yaxis='y',
                mode='lines',
                line=dict(width=2, color='blue')
            )


            axis=dict(
                showline=True,
                zeroline=False,
                showgrid=True,
                mirror=True,
                ticklen=4,
                gridcolor='#ffffff',
                tickfont=dict(size=10)
            )

            layout1 = dict(
                width=1300,
                height=550,
                autosize=False,
                title=f'Product {i} : Net Sales Data',
                margin = dict(t=100),
                
                xaxis1=dict(axis, **dict(domain=[0.45, 1.0], anchor='y')),

                yaxis1=dict(axis, **dict(domain=[0, 1.0], anchor='x', hoverformat='.2f',title='<b> Net Sales</b> (k$)',title_standoff = 0.5)),

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )


            fig_sample = dict(data=[table_trace1, trace1,trace2,trace3,trace4,trace5], layout=layout1)
            st.write(fig_sample)
            st.markdown( dict_description[i], unsafe_allow_html = True)
        
        



    ########          ########          ########          ########          ########          ########          ########          ########  


    def total_relationship_for_quarterly_W():
        Total = np.zeros(60)
        Total_Net_Sales = np.zeros(60)

        Month = ['Jan','Feb','Mar','April','May','June','July','Aug','Sep','Oct','Nov','Dec'
        ]

        for i in ['A','B','C','D','E','F']:
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = i, header = 1)
            Total_Net_Sales = Total_Net_Sales + df_data['Sales']

        count = df_data.index
        x_input = count[36:48]
        
        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        fig.add_trace(go.Scatter(name='2016', x=x_input, y=Total_Net_Sales[0:12]))
        fig.add_trace(go.Scatter(name='2017', x=x_input, y=Total_Net_Sales[12:24]))
        fig.add_trace(go.Scatter(name='2018', x=x_input, y=Total_Net_Sales[24:36]))
        fig.add_trace(go.Scatter(name='2019', x=x_input, y=Total_Net_Sales[36:48]))
        fig.add_trace(go.Scatter(name='2020', x=x_input, y=Total_Net_Sales[48:60]), secondary_y=False)
    
        # Add figure title
        fig.update_layout(
            width=1100,
            height=600,
            title_text="UV Filter Net Sales by Year vs. Month",
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
        fig.update_xaxes(title_text='<b> Month </b>')
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = [36,37,38,39,40,41,42,43,44,45,46,47],
                ticktext = Month
            )
        )

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Net Profit Sales</b> (k$) ",  secondary_y=False)

    
        st.write(fig)  




    ########          ########          ########          ########          ########          ########          ########          ########  



    def net_sales_for_quarterly_W(year):

        year_index = year-2016
        Month = ['Jan','Feb','Mar','April','May','June','July','Aug','Sep','Oct','Nov','Dec']
        Year = ['2016','2017','2018','2019','2020']

        Total = np.zeros(60)
        Total_Net_Sales = np.zeros(60)

        for i in ['A','B','C','D','E','F']:
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = i , header = 1)
            Total = Total + df_data['Total']
            Total_Net_Sales = Total_Net_Sales + df_data['Sales']
            df_data = df_data.dropna(axis=1)
            for month_year in df_data.index:
                df_data.loc[month_year, 'Year' ] = Year[month_year // 12 ]
                df_data.loc[month_year, 'Month'] = Month[month_year % 12]
            df = df_data[['Month','Year','Total','Sales']]  # use df.map to merge two columns (month+year)
            month = np.array(Month)

        def calc_sales (sheet_name):
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name , header = 1)
            df = df_data.dropna(axis=1)
            Y = df['Sales'].values
            Y = Y[year_index*12:year_index*12+12]
            return Y

        y_input = []
        for i in ['A','B','C','D','E','F']:
            y_input.append(calc_sales(i))
        y_input= np.array(y_input)
        A,B,C,D,E,F = y_input[0],y_input[1],y_input[2],y_input[3],y_input[4],y_input[5]

        # Set Traces
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(name='A', x=month, y=A))
        fig.add_trace(go.Scatter(name='B', x=month, y=B))
        fig.add_trace(go.Scatter(name='C', x=month, y=C))
        fig.add_trace(go.Scatter(name='D', x=month, y=D))
        fig.add_trace(go.Scatter(name='E', x=month, y=E))
        fig.add_trace(go.Scatter(name='F', x=month, y=F))
        fig.add_trace(go.Scatter(name=f'{year}', x=month, y=Total_Net_Sales[year_index*12:year_index*12+12],mode='lines',line=dict(width=5)), secondary_y=True)

        fig.update_layout(
            title_text=f'{year} Net Sales by Each Product vs. Year',
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        # Set x-axis title
        fig.update_xaxes(title_text="<b>Month</b>")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Each Product Net Sales</b> (k$) ",  secondary_y=False)
        fig.update_yaxes(title_text=f"<b>{year} Net Sales</b> (k$) ",  secondary_y=True)

        

        st.write(fig)



    ########          ########          ########          ########          ########          ########          ########          ########  





    def W_Sales_Overview():

        def call_out(sheet_name):
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y = df_data['Total'].values
            Y = Y[:48]
            return Y

        list_total = []
        unit_quantity = []

        for i in ['A','B','C','D','E','F']:
            list_total.append(call_out(i))
            x = list_total
            x = np.array(x)
            norm_x = (x-x.mean())/x.std()
            unit_quantity.append(norm_x)
            list_total = []

        # X Assignment

        unit_quantity=np.array(unit_quantity)
        unit_quantity = unit_quantity.reshape(6,48)

        x_input=[]

        for i in range (48):
            xvalue = unit_quantity[:,i].tolist()+[1]
            x_input.append(xvalue)

        x_input = np.array(x_input)
        x_input = np.reshape(x_input,(48,7))

        
        w_zip=[]
        for y_name in ['Sales','cCM1']:
            def y_assign_NS(sheet_name):
                df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
                df_data = df_data.dropna(axis=1)
                Y = df_data[y_name].values
                Y = Y[:48]
                return Y

            list_NS = []

            for i in ['A','B','C','D','E','F']:
                list_NS.append(y_assign_NS(i))

            np_NS = np.array(list_NS)
            Y_NS = np_NS.sum(axis = 0)
            Y_NS = np.reshape(Y_NS,(48,1))
            reg = LinearRegression()
            reg.fit(x_input, Y_NS)
            W = reg.coef_
            w_zip.append(W)
            

        w_zip=np.array(w_zip)
        w_assign=np.array(w_zip)
        w_assign=w_assign.reshape(2,7)
        w_zip=w_zip.T
        w_zip=w_zip.reshape(7,2)

        table_trace1 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'], ['<b>Product B</b>'],
                                        ['<b>Product C</b>'],['<b>Product D</b>'],['<b>Product E</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')), # ['W_Net_Sales','W_cCM1','W_Net_Sales/W_cCM1']
                cells = dict(values = [['W_Net_Sales','W_cCM1'], w_zip[0].round(3), w_zip[1].round(3), w_zip[2].round(3), w_zip[3].round(3), w_zip[4].round(3), w_zip[5].round(3)
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
                height=300,
                autosize=False,
                title='Overview W Coefficients',
                margin = dict(t=100),
                

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        w_figure = dict(data=[table_trace1], layout=layout1)
        st.write(w_figure)

        st.markdown("""Based on the W calculation, the products are arranged from largest to smallest W values: 
        """,unsafe_allow_html = True)
        st.markdown('<div style="text-align: center"> W_Net_Sales : A ~ F >  D > E > C > B </div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center"> W_cCM1 : F ~ A >  D > E > C > B </div>', unsafe_allow_html=True)
        st.markdown("""<br>
        Since A and F have the biggest W values of roughly W_Net_Sales= X and W_cCM1= Y, Product A and F are considered the determining factors for both net sales and cCM1, and thus the most salable products. With W_Net_Sales=X and W_cCM1=Y, Product D is the next driving component, with Product C and B followed next. Note that B and C have relatively smaller W values compared to the other products, or even a negative value if present, which deviates from the highest W value by 10 times. From this, it can be deduced that two types of error — system and measurement — may be present in the modeled system. <br>
        <br>""", unsafe_allow_html=True)
        st.markdown("""
        - System Error from Linearity Assumption: For simplicity of the analysis, the assumption of “linear regression model assumes that the relationship between the dependent variable y and the p-vector of regressors x is linear.” (Wikipedia, n.d.) is made. However, no real system is in fact linear; numerous other aspects should have been considered such as sales price, currency, etc. <br>
        <br>    
        - Measurement Error from Inaccurate data input: There could have been a discrepancy between the time for the sales data entry and the time when the actual product was delivered and used by the customer. This creates an inconsistency in the measured data and shifts the sales data off from where the data should have been placed. <br>
        The larger deviation of the data infers that the data are influenced more heavily by the errors. 
        <br><br>""", unsafe_allow_html=True)
        st.markdown("""
        The presence of these errors needs to be considered for the accuracy of the analysis with an implementation of the measure of each error. Yet, as the general trend is still observable without the error range, the error is neglected. <br>
        <br><br>
        From the W summary of the past 5 years of sales data, Product A and F yield both the highest net sales and cCM1. Indeed, it is significant to consider both the W value itself and the relationship between W_Net_Sales and W_cCM1. The former explains which product is the key component for net sales and cCM1. On the other hand, the latter implies a performance measure that evaluates the profitability of a product, thus the actual amount of return relative to the revenue cost; e.g. if the ratio of two products for W_Net Sales (assuming A=200 and B=100, thus A/B=2) is larger than the ratio of W_cCM1 (assuming A=100 and B=200, thus A/B=0.5), it signifies that product A is less profitable than B. Even if Product A is weighed more heavily on the revenue than Product B, due to the various reasons associated with the sales activities such as manufacturing costs, tariffs, etc., Product A is less profitable than Product B. To figure out the profitability of each product, each W value is divided by the sum of the corresponding W values and is represented in the following table. <br>
        """, unsafe_allow_html=True)


        w_zip=[]
        for index in range (2):
            W_assign=w_assign[index]
            for i in range(6):
                w=W_assign[i]
                w_zip.append(w/sum(W_assign))
        w_zip=np.array(w_zip)
        w_zip=w_zip.reshape(2,6)
        val=w_zip[0]
        divider=w_zip[1]
        for i in range(6):
            value=divider[i]/val[i]
            w_zip=np.append(w_zip,value)
        w_zip=w_zip.reshape(3,6)
        w_zip=w_zip.T

        table_trace1 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'], ['<b>Product B</b>'],
                                        ['<b>Product C</b>'],['<b>Product D</b>'],['<b>Product E</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = [['W_ratio_NS','W_ratio_cCM1','W_ratio_NS/ W_ratio_cCM1'], w_zip[0].round(3), w_zip[1].round(3), w_zip[2].round(3), w_zip[3].round(3), w_zip[4].round(3), w_zip[5].round(3)
                                        ],
                            line = dict(color='#506784'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                            format = [None] + [", .2f"] * 2 + [',.4f'],
                            suffix=[None] * 4,
                            height = 25,
                            fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
            )
        layout1 = dict(
                width=1300,
                height=320,
                autosize=False,
                title='Salability and Profitability W',
                margin = dict(t=100),
                

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        W_figure = dict(data=[table_trace1], layout=layout1)
        st.write(W_figure)



    ########          ########          ########          ########          ########          ########          ######## 




    def W_Sales_Yearly():
        def y_assign(sheet_name):
        
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y = df_data['Sales'].values
            return Y

        list_total = []

        for i in ['A','B','C','D','E','F']:
            list_total.append(y_assign(i))
            
        np_total = np.array(list_total)
        Y_NS = np_total.sum(axis = 0)
        Y_NS_COVID = Y_NS[:60]

        def call_out(sheet_name): 
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y = df_data['Total'].values
            return Y

        list_total = []
        unit_quantity = []

        for i in ['A','B','C','D','E','F']:
            list_total.append(call_out(i))
            x = list_total
            x = np.array(x)


            
        def normalization (product):
            x = np.array(product)
            norm_x = (x-x.mean())/x.std()
            return norm_x


        def x_assign (group_name):
            unit_quantity = np.array(group_name)
            unit_quantity = unit_quantity.reshape(6,12)

            x_input=[]

            for i in range (12):
                xvalue = unit_quantity[:,i].tolist()+[1]
                x_input.append(xvalue)


            x_input = np.array(x_input)
            x_input = np.reshape(x_input,(12,7))
            return x_input

        year_count = [2016,2017,2018,2019,2020]
        W_year = []

        for year in year_count :
            year_index = year-2016
            
            group_one =[]
            
            for i in [0,1,2,3,4,5]:
                a = x[i,12*year_index:12*(year_index+1)]
                group_one.append(normalization(a))
            X = x_assign(group_one)
            y = Y_NS_COVID[12*year_index:12*(year_index+1)].T
            reg = LinearRegression()
            reg.fit(X, y)
            W = reg.coef_
            W_year.append(W)

        W_year_return = np.array(W_year)
        W_year = np.array(W_year)
        W_year = W_year.T
        year_count = np.array(year_count)
        year_count = year_count.T

        table_trace1 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'], ['<b>Product B</b>'],
                                        ['<b>Product C</b>'],['<b>Product D</b>'],['<b>Product E</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = [year_count, W_year[0].round(3),W_year[1].round(3),W_year[2].round(3),W_year[3].round(3),W_year[4].round(3),W_year[5].round(3)
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
                title='Yearly W Coefficients',
                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        w_figure = dict(data=[table_trace1], layout=layout1)
        st.write(w_figure)
        ########
        st.markdown('''The resulting table shows the following yearly trends of the UV filter products.''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2016: the business was growing </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2017: the business was booming </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2018: the business was declining as compared to the previous year </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2019: it was recovering from the negative impact in 2018 </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2020: the business was negatively influenced as compared to the previous year </div>''', unsafe_allow_html=True)
        st.markdown("""<br>
        The observed yearly W trends are explained with the main events that may have caused such trends.<br>
        <br>""",unsafe_allow_html = True)
        st.markdown("""
        - 2016~2017: Cosmetics was booming; a large volume of cosmetics exported into China, and Chinese tour groups surged to 8,067,772 in 2016 according to Korea Tourism Organization (KTO) figures.
        <br><br>
        - 2018: In March 2017, S. Korea refused to halt the deployment of the anti-missile system, known as Terminal High Altitude Area Defense (THAAD), which Beijing deems a threat to its national security. As a result, the national tourism administration of China suspended selling group packages to South Korea, and the number of Chinese tourists visiting South Korea between March to October in 2017 plunged more than 60% from the same period last year. This had come into effect on the sales of UV filter chemicals since the end of 2017 and is reflected on the 2018 sales data. In fact, Company X was heavily hit by this contentious political issue; Company X had reported a sharp fall in profit by more than half in the second quarter of 2017 as compared to the second quarter of 2016. Hard hit on Company X explicates the drop of W values of Product A, D, E, and F, for which Company X is a primary customer.
        <br><br>
        - 2019: The market was recovering from the negative impact of THAAD but supplies shortage issue during the first half year of 2019 slowed down the recovery rate.
        <br><br>
        - 2020 : COVID-19 pandemic started off in Jan 2020 (in S. Korea), and as the coronavirus outbreak spread worsened, the beauty market of South Korea has subsequently had a serious damage; International travel restrictions resulted in a cut-off flow of the Chinese tourists. Moreover, social distancing, work from home, and mask wearing have lessened the outdoor activities and consequently the demand for sun care products.
        <br>""",unsafe_allow_html = True)
        st.markdown("""<br>
        To determine how each product’s weight on net sales had changed, the W values from the previous table are divided by the sum of W values in the corresponding year. The computed ratios are shown below, and the products are arranged from largest to smallest W values. Continuous, multi-year fall in W value indicates its salability is on decline, but if the W drops only in a specific year then it is highly likely to be caused by a temporary event.
        <br><br>""",unsafe_allow_html = True)
        ########
        w_zip=[]
        for year in range (5):
            W_assign=W_year_return[year]
            for i in range(6):
                w=W_assign[i]
                w_zip.append(w/sum(W_assign))
        w_zip=np.array(w_zip)
        w_zip=w_zip.reshape(5,6)
        W_zip=w_zip.T
        w_zip_trans=w_zip.T
        year_count = [2016,2017,2018,2019,2020]
        table_trace2 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'], ['<b>Product B</b>'],
                                        ['<b>Product C</b>'],['<b>Product D</b>'],['<b>Product E</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = [year_count,W_zip[0].round(3), W_zip[1].round(3), W_zip[2].round(3), W_zip[3].round(3), W_zip[4].round(3), W_zip[5].round(3)
                                        ],
                            line = dict(color='#506784'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                            format = [None] + [", .2f"] * 2 + [',.4f'],
                            suffix=[None] * 4,
                            height = 25,
                            fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
            )
        layout2 = dict(
                width=1300,
                height=350,
                autosize=False,
                title='Product Growth W',
                margin = dict(t=100),
                

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        W_figure2 = dict(data=[table_trace2], layout=layout2)
        st.write(W_figure2)


        ########
        st.markdown('''<div style="text-align: center"> 2016 : A ~ F > D > E > C > B </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2017 : A ~ F > D > E > B > C </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2018 : A ~ F > D > E > B > C </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2019 : A > D > F > E > B > C  </div>''', unsafe_allow_html=True)
        st.markdown('''<div style="text-align: center"> 2020 : F > A > B > D > E > C  </div>''', unsafe_allow_html=True)
        st.markdown('''<br>
        <i>Product Trend Interpretation</i> <br>''', unsafe_allow_html=True)
        st.markdown('''<br>
        - Product X&nbsp;&nbsp;: Alternative to Product X / Relatively new product ∴ low demand but growing 
        <br><br>
        - Product Y&nbsp;&nbsp;: Hawaii’s sunscreen ban has officially taken effect in May 2018 (banning sunscreens containing oxybenzone and octinoxate to preserve Hawaii’s marine ecosystems) ∴ dying product; demand is still comparatively high to other products but on decline
        <br><br>
        - Product Z&nbsp;&nbsp;: The patent to manufacture the makeup product of Company X  which uses Product E ended in 2018, and other cosmetics companies have come up with copied products. Thus, the demand for Company X's product had decreased, and the sales fall of Company X was even more intensified by THAAD. Since Company X was the main customer for Product E, meaning that other cosmetics brands do not use Product E, the financial hit on Company X directly resulted in declining demand for Product Z. 
        <br><br>
        - Product U&nbsp;&nbsp;: Its patent expired in 2017. However, it still takes one third of the annual net sales. ∴ high demand and competitive
        <br><br>
        - Product V&nbsp;&nbsp;: The commercial model of this product manipulated stock price of a company, and consumers boycotted the product. Moreover, the supply shortage issue in H1 2019 resulted in lower net sales than its usual H1 trend, and the stock buildup in H2 2019 led to a higher net sales than its usual H2 trend. These abnormal 2019 sales trends suggest a system error from Linear Regression. The reasons will be explained in detail in Section 3.3. 
        <br><br>
        - Product W&nbsp;&nbsp;: Difficult to formulate with, and because relatively new, long-term safety data are not available ∴ low demand
        <br>''', unsafe_allow_html=True)
        st.markdown('''<br><br>
        To evaluate the COVID impact on the sales of each product, the W ratio of 2020 is divided by the median value of W ratios of the years from 2016 to 2019. The results are shown below.
        ''', unsafe_allow_html=True)
        ########

        
        impact_zip=[]
        for index in range(6):
            covid_w=w_zip_trans[index]
            before_covid=covid_w[:4]
            impact_w=covid_w[4]/np.median(before_covid)
            impact_zip.append(impact_w)
        
        table_trace3 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'], ['<b>Product B</b>'],
                                        ['<b>Product C</b>'],['<b>Product D</b>'],['<b>Product E</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = ['2020/ med(2016~19)',impact_zip[0].round(3), impact_zip[1].round(3), impact_zip[2].round(3), impact_zip[3].round(3), impact_zip[4].round(3), impact_zip[5].round(3)
                                        ],
                            line = dict(color='#506784'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                            format = [None] + [", .2f"] * 2 + [',.4f'],
                            suffix=[None] * 4,
                            height = 25,
                            fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
            )
        layout3 = dict(
                width=1300,
                height=270,
                autosize=False,
                title='COVID-19 Impact W',
                margin = dict(t=100),
                

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        W_figure3 = dict(data=[table_trace3], layout=layout3)
        st.write(W_figure3)


    ########          ########          ########          ########          ########          ########          ########          ########  
    def quarter_w_analysis():
        def call_out(sheet_name):
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y = df_data['Total'].values
            Y = Y[:48]
            return Y

        x_input = []
        for i in ['A','D','F']: #'A','B','C','D','E','F'
            x_input.append(call_out(i))

        def quarterly (quarter):
            def summing(product):
                values = []
                prod=x_input[product]
                for i in [0,1,2,3]:
                    count = prod[i*12+quarter:i*12+3+quarter]
                    values.append(np.sum(count))
                return values

            quarters =[]
            for i in range(3):   # Assign which product we are evalulating
                quarters.append(summing(i))    
            quarters = np.array(quarters)

            x=[]
            for i in range (4):
                xvalue = quarters[:,i].tolist()+[1]
                x.append(xvalue)
            return x

        def y_assign(sheet_name):
            
            df_data = pd.read_excel('blank_file.xlsx',sheet_name = sheet_name, header = 1)
            df_data = df_data.dropna(axis=1)
            Y = df_data['Sales'].values
            Y = Y[:48]
            return Y

        list_total = []

        for i in ['A','D','F']:
            list_total.append(y_assign(i))
            
        np_total = np.array(list_total)
        Y_NS = np_total.sum(axis = 0)

        def yvalue(quarter):
            values = []
            for i in [0,1,2,3]:
                count = Y_NS[i*12+quarter:i*12+3+quarter]
                values.append(np.sum(count))
            return values

        w_zip=[]
        for i in [0,3,6,9]:
            x=quarterly(i)
        #     print(i,x)
            y=yvalue(i)
        #     print(i,y)
            reg = LinearRegression()
            reg.fit(x, y)
            W = reg.coef_
            w_zip.append(W)
        w_zip=np.array(w_zip)
        w_zip_assign=w_zip    
        w_zip=w_zip.T

        table_trace1 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'],['<b>Product D</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = [['Q1','Q2','Q3','Q4'],w_zip[0].round(3), w_zip[1].round(3), w_zip[2].round(3)
                                        ],
                            line = dict(color='#506784'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                            format = [None] + [", .2f"] * 2 + [',.4f'],
                            suffix=[None] * 4,
                            height = 25,
                            fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
            )
        layout1 = dict(
                width=1300,
                height=330,
                autosize=False,
                title='Market Dynamics W',
                margin = dict(t=100),
                

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        W_figure1 = dict(data=[table_trace1], layout=layout1)
        st.write(W_figure1)
        ############
        st.markdown('''
        Note that Q4 is one magnitude larger than the other two. This signifies outliers, and since the errors are significant, the results are considered not reliable. In Q3, Products A and F have roughly the same ratio, and D has the lowest ratio. Because the sales trends overlap each other compared to the other quarters due to the low demand for all products, it is deduced that errors have affected the W calculation of Q3.
        <br><br>
        Products are recalculated for the partial ratios as compared to the total for each quarter as shown below.
        ''', unsafe_allow_html=True)

        ############
        ratio=[]
        for i in range(4):
            w=w_zip_assign[i]
            ratio.append(w/sum(w))
        ratio=np.array(ratio)
        ratio=ratio.T
        table_trace2 = go.Table(
                domain=dict(x=[0, 1],
                            y=[0, 1]),
                columnwidth = [120] + [130,130,130,130,130,130],  # Table Column Width
                columnorder=[0, 1, 2, 3, 4, 5, 6],
                header = dict(height = 25,
                            values = [['<b>W Coefficient</b>'],['<b>Product A</b>'],['<b>Product D</b>'],['<b>Product F</b>']],
                            line = dict(color='rgb(50, 50, 50)'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                            fill = dict(color='#d562be')),
                cells = dict(values = [['Q1','Q2','Q3','Q4'],ratio[0].round(3), ratio[1].round(3), ratio[2].round(3)
                                        ],
                            line = dict(color='#506784'),
                            align = ['left'] * 5,
                            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                            format = [None] + [", .2f"] * 2 + [',.4f'],
                            suffix=[None] * 4,
                            height = 25,
                            fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']))
            )
        layout2 = dict(
                width=1300,
                height=330,
                autosize=False,
                title='Product Growth W',
                margin = dict(t=100),
                

                plot_bgcolor='rgba(228, 222, 249, 0.65)'
            )
        W_figure2 = dict(data=[table_trace2], layout=layout2)
        st.write(W_figure2)



    ########          ########          ########          ########          ########          ########          ########          ########  

    def prediction():
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

        year = list(range(2016,2022))               # X
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




        # Plotting
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Original 2016-2020
        fig.add_trace(go.Scatter(name='Actual Net Sales ', x=year, y=Net_Sales), secondary_y=True)
        fig.add_trace(go.Bar(name='Actual Quantity Sales ', x=year, y=Quantity,width=[0.3, 0.3, 0.3, 0.3, 0.3]))

        # Predicted 2021 
        exp_quantity= np.array(500.384)
        yr_2021=np.array(2021)
        

        Net_Sales = np.append(Net_Sales,20569.875)
        new_x = year[4:6]
        new_y = Net_Sales[4:6]
        
        fig.add_trace(go.Scatter(name='Expected Net Sales in 2021', x=new_x, y=new_y, mode='lines', line={'dash': 'dash', 'color': 'blue'}), secondary_y=True)
        fig.add_trace(go.Bar(name='Expected Quantity Sales in 2021', x=yr_2021, y=exp_quantity, marker_color='rgb(255,50,33)', marker_line_color='rgb(8,48,107)',
                    opacity=0.6, width=[0.3]))


            
        # Add figure title
        fig.update_layout(
            width=1100,
            height=600,
            title_text="Forecast of the 2021yr UV Filter Sales vs. Year",
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
                tickvals = [2016,2017,2018,2019,2020,2021],
            )
        )
        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Quantity Sales</b> (lb) ", range=[0,900], secondary_y=False)
        fig.update_yaxes(title_text="<b>Net Sales</b> (k$) ", secondary_y=True)

    
        st.write(fig)  
    



            

    ########### ########### ########### ######### S T A R T ########### ########### ########### ###########    

    #### ABSTRACT ####
    st.markdown('<i><p class="big-font">**Abstract**</p></i>', unsafe_allow_html=True)
    st.markdown('''
    Since the declaration of a global pandemic, the novel coronavirus, also known as COVID-19, has quickly spread across the globe and wreaked havoc on our daily lives. The implementation of stringent guidelines to mitigate the COVID-19 transmission has directly resulted in an unprecedented consumption shock which led to critical influences on the world economies, particularly on the cosmetics market, and further in a sharp drop of demand for sunscreen products. Subsequently, the demand for UV filter products have dramatically decreased. To minimize the COVID-19 impacts and accelerate the economic recovery of the UV filter business, an examination of the historical product sales data and its remarkable features is necessary. This research investigates six different UV filter products on the market and analyzes their characteristic sales profiles and the market dynamics that drive such trends. The report aims to present an in-depth understanding of the sales profiles of the products and to help shape a strategic sales and market development plan. Linear Regression is adapted to identify the key features of the net sales and to evaluate the impacts of the pandemic. The analysis assesses overall, yearly, and quarterly sales data with the interpretation of the results and describes a comprehensive overview of the business performance and the growth rates of the products as well. It further provides a forecast of 2021 sales with the discussion of potential circumstances in which the proposed forecast could further be impacted.
    <br>
    <br>
    <br>''', unsafe_allow_html=True)





    #### INTRODUCTION ####
    st.markdown('<i><p class="big-font">**Section 1. Introduction**</p></i>', unsafe_allow_html=True)

    #### Section 1.1 #####
    st.markdown('''1.1 | <i>Objectives</i>''', unsafe_allow_html=True)
    st.markdown('''Due to the outbreak of Coronavirus Disease 2019 (COVID-19), the beauty market has been shocked resulting in a sharp drop in revenue for cosmetic industry and widespread store closures. According to McKindsey & Company (n.d.), “with the closure of premium beauty-product outlets because of COVID-19, approximately 30 percent of the beauty-industry market was shut down.” Along with the downfall of cosmetic industry, the Business-to-Business (B2B) companies including chemical manufacturing companies associated with the beauty products have been also negatively impacted. To quickly recover the negative effects on business, a comprehensive insight of the past and current sales profile is necessary to plan for the future product demand and shape the sales development strategy. The objective of this project is to understand the sales profile and the market dynamics and to determine the major products and growing products with the timelines for preparation of the future demand.
    <br><br>
    At BASF A-EMA/AR, six Ultraviolet (UV) filter products are selected for the analysis, and the data of the products are obtained for the years 2016 through 2020. The names of the products are not disclosed in this report due to confidentiality.
    <br><br>
    To observe a historical trend of the UV filter business, an overview graph of the monthly quantity sales and monthly net sales of the total six products is generated as below.
    <br>''', unsafe_allow_html=True)

    # Overview of Current
    total_relationship()
    st.markdown("""Based on the figure, a yearly repeating tendency of the higher peaks presence in the first half year (H1) and lower peaks in the second half year (H2) is observed. The lowest peaks are present during 2020 due to the COVID impact. To find how largely the COVID pandemic hit the business, the quantity sales and net sales of 2020 that would have resulted if the pandemic had not been occured are predicted based on the average annual business growth. The year-over-year business growth (YoY) is computed using the equation below.
        <br>""", unsafe_allow_html = True)
    st.markdown('<div style="text-align: center"> Year-over-year Business Growth (%) = (x<sub>current year</sub> – x<sub>previous year</sub>) / (x<sub>previous year</sub>) * 100 % </div>', unsafe_allow_html=True)
    st.markdown("""<br>
    The total quantity sales and net sales values of each year are tabulated below with the respective business growth calculated.""",unsafe_allow_html=True)

    # COVID Impact
    covid_impact_graph()



    #### Section 1.2 ######
    st.markdown('''<br> 1.2 | <i>Qualitative Approach</i>''', unsafe_allow_html=True)
    st.markdown("""Prior to the in-depth assessment of each product, historical sales data of products are used to figure out which product is weighted most for quantity sales and net sales on the usual basis. For this, a breakdown of the overview graph for each product is necessary. Quantity sales and net sales graphs are separately generated to determine the trends more clearly. Figures are shown as below; since the data from 2020 were impacted by COVID-19, 2020 is omitted for clarity of the sales trend.
    <br><br>""",unsafe_allow_html = True)

    # Yearly graphs
    col1,col2 = st.beta_columns(2)         
    with col1:
        overall_trend_quantity_by_year()
    with col2:
        overall_trend_money_by_year()

    # Monthly Graphs
    col1,col2 = st.beta_columns(2)
    with col1:
        overall_trend_quantity_by_month()
    with col2:
        overall_trend_net_sales_by_month()

    st.markdown("""<br>
    The graphs suggest that the quantity sales rank from highest to lowest in order of Product D, E, F, A, B, and C, whereas the net sales rank from Product A, F, D, E, B, to C. Even though Product D is sold most in quantity, Product A yields the highest overall net sales. To closely see the dynamics of the sales trend for each product, the yearly net sales for each product are represented with the explanation of notable trends.
    <br>""",unsafe_allow_html = True)
    # Each Product Graph
    each_prod_monthly_review()

    st.markdown("""<br><br>Most products follow the trend of high peak in H1. Note that the 2020 sales trend is placed at the lowest for most products except B and C even though the 2020 net sales have rapidly decreased. Such complex relationships between quantity and net sales with the dynamics of sales trends are further studied using quantitative analysis method of linear regression, of which the results are evaluated for the total sales trend, yearly sales trend, and quarterly sales trend.
    <br><br>""",unsafe_allow_html = True)







    #### BACKGROUND ####
    st.markdown('<i><p class="big-font">**Section 2. Background**</p></i>', unsafe_allow_html=True)
    st.markdown("""
    Linear Regression is employed to identify the products that contribute most to the net sales. Since there are six products, linear regression is evaluated for six different effects, or regression coefficients, denoted as W. Hence, the system becomes 7-dimensional model, consisting of six x’s for quantity sales of each product and one y for total net sales, and the product with a higher W value indicates a more significant influence on the total net sales.
    <br><br><br>""",unsafe_allow_html = True)

    # Expander for Linear Regression Description
    with st.beta_expander ("See Description for Linear Regression"):
        st.image("./linear_regression.png")
        st. write(""" 
        Wikipedia (n.d.) defines linear regression as the following:
        > In statistics, linear regression is a linear approach to modelling the relationship between a scalar response and one or more explanatory variables (also known as dependent and independent variables).
        >
        > Given a data set $[{y_i,x_{i1},…,x_{ip}}]^{{{n}}}_{{\ri=1}}$ of n statistical units, a linear regression model assumes that the relationship between the dependent variable y and the p-vector of regressors x is linear. This relationship is modeled through a disturbance term or error variable ε — an unobserved random variable that adds "noise" to the linear relationship between the dependent variable and regressors. Thus the model takes the form, <br>
        > > > $y_i=β_0+β_1 x_i1+⋯+β_p x_ip+ε_i=〖x_i〗^T β+ε_i,i=1,…,n$
        > > 
        > , where T denotes the transpose. Often these n equations are stacked together and written in matrix notation as <br>
        > > >       y = X β + ε
        > > 
        > , where 
        > > -	y  is a vector of observed values of the variable called the regressand, endogenous variable, response variable, measured variable, criterion variable, or dependent variable. This variable is also sometimes known as the predicted variable, but this should not be confused with predicted values, which are denoted ŷ.
        >
        > > -	X may be seen as a matrix of row-vectors x<sub>i</sub> or of n-dimensional column-vectors X<sub>j</sub>, which are known as regressors, exogenous variables, explanatory variables, covariates, input variables, predictor variables, or independent variables (not to be confused with the concept of independent random variables). 
        >
        > > - β is a (p+1) -dimensional parameter vector, where 〖<sub>0</sub>〗 is the intercept term (if one is included in the model—otherwise β is p-dimensional). Its elements are known as effects or regression coefficients (although the latter term is sometimes reserved for the estimated effects).
        >
        > > - ε is a vector of values ε<sub>i</sub>. This part of the model is called the error term, disturbance term, or sometimes noise.
        >
        <br>
        > Linear regression has many practical uses. Most applications fall into one of the following two broad categories: 
        >
        > > - If the goal is prediction, forecasting, or error reduction, linear regression can be used to fit a predictive model 
        to an observed data set of values of the response and explanatory variables. After developing such a model, if additional values of 
        the explanatory variables are collected without an accompanying response value, the fitted model can be used to make a prediction of
        the response.
        > 
        > > - If the goal is to explain variation in the response variable that can be attributed to variation in the explanatory variables, 
        linear regression analysis can be applied to quantify the strength of the relationship between the response and the explanatory 
        variables, and in particular to determine whether some explanatory variables may have no linear relationship with the response 
        at all, or to identify which subsets of explanatory variables may contain redundant information about the response.
        <br>""",unsafe_allow_html = True)

    st.markdown("""<br>
    In addition, some data are normalized for the linear regression analysis; along with the quantity sales, various other factors are present such as sales price, currency, etc. that the net sales are dependent of. Thus, to account for all the other aspects normalization is applied to the quantity sales which adjusts those factors on different scales into alignment.
    <br><br><br>""",unsafe_allow_html = True)









    #### Results ####
    st.markdown('<i><p class="big-font">**Section 3. Results **</p></i>', unsafe_allow_html=True)

    #### Section 3.1 #####
    st.markdown('''3.1 | <i>Salable and Profitable Products</i>''', unsafe_allow_html=True)
    st.markdown('''
    Linear Regression is applied to find the W of each product. Data are taken from the years 2016 through 2019. For x, normalized quantity is used for the W computation to take various factors into account such as sales price and quantity sold for each product - by this method, the W accounts for both how well and how expensive each product is sold. Thus, W_Net_Sales denotes the measure of contribution per pound of each product sold to the net sales of a certain period. Similarly, W_cCM1 represents the amount that each product affects the cCM1 of the corresponding period by. The calculated W values are tabulated below.
    <br>''', unsafe_allow_html=True)

    W_Sales_Overview()



    # W_Profit()
    st.markdown("""Based on the W calculation, the products are arranged from largest to smallest W NS/cCM1 ratio svalues:
    """, unsafe_allow_html=True)
    st.markdown('<div style="text-align: center"> F > A > C > B > D > E </div>', unsafe_allow_html=True)
    st.markdown("""<br>
    Since the ratio of W_cCM1 to W_Net_Sales is the highest for Product F, it can be inferred that Product F yields the most profit over revenue. This further deduces a conclusion that promoting F will turn the net sales the most efficiently into cCM1, thus the most profitable. Although Products D is ranked last, it does not indicate that it is the least profitable. Product F should be selected for promotion if only one product must be chosen because it is the most efficient product in terms of yielding the most return on investment.
    <br><br><br>""",unsafe_allow_html = True)



    #### Section 3.2 #####
    st.markdown('''3.2 | <i>Market Dynamics and Product Growth</i>''', unsafe_allow_html=True)
    st.markdown("""
    To understand the dynamics of UV filter market and determine the product growth and the influence of COVID-19 outbreak, the same linear regression method is employed but for yearly W. Data of each year are evaluated for the W of the designated year, which will suggest whether the value of a product, or the demand, is growing or declining as well as how COVID impacted each product in 2020. <br>
    <br>""",unsafe_allow_html = True)
    W_Sales_Yearly()




    st.markdown('''
    These values denote how the net sales of 2020 deviate from the median net sales of 2016 through 2019, thus demonstrating the COVID impact for each product. The ratio less than 1 signifies negative impact due to COVID. Hence, D is the most impacted, E and A followed next. The ratio larger than 1 implies positive growth during COVID. Therefore, B is the most impacted, C and F next. (F should be less than the current value as 2019’s W is impacted by outliers.) <br> 
    <br>
    A and D are sold on a larger scale, so they should be influenced more negatively than Products B and C. As opposed to Products A and D, Products B and C are sold on a smaller scale and should be influenced less negatively than all others. Thus, F is impacted the least, and E is impacted the most. E is impacted the most because it had only one customer, Company X, who was heavily impacted by the pandemic in 2020. In contrast, Product F had the least negative COVID impact since its main customer Company Y had balanced out the struggle of their makeup business by reinforcing their business of household goods and therefore the moderate impact on their financials had enabled to reduce the negative influence on the demand for Product F.
    <br><br><br>
    ''', unsafe_allow_html=True)

    ### Section 3.3 ####

    st.markdown('''3.3 | <i>Supply Management and Order Placement </i>''', unsafe_allow_html=True)
    st.markdown('''
    Another significant task of sales job positions is to provide the requested products to the customers on time. To ensure the products arrive in a timely manner, sales representatives should be aware of when the demand will increase so that they can plan ahead and place the order in advance. For better acknowledgement of the demand trends, a figure with the sales trends of years 2016 through 2020 is generated as below to see which quarter yields the highest net sales.
    ''', unsafe_allow_html=True)
    total_relationship_for_quarterly_W()
    st.markdown('''
    From a qualitative approach, the figure suggests the highest net sales recorded in Q2 on average and the lowest in Q3. More broadly, most sales are achieved in Q1 and Q2, or H1. To specify key driving products for the net sales of each quarter and further enhance the efficiency of sales activities in H1, the quarterly data are quantitatively analyzed using linear regression. Similarly, the same linear regression method is employed but for quarterly W. Data of each quarter are analyzed for the W of the designated year, which will suggest when the product contributes the most to the total net sales of the corresponding time period. 
    <br><br>
    Note that quantity, or the x variable of this W calculation, is not normalized and that only A, D, and F are analyzed; 7 variables and 4 equations are underspecified system. To solve this underspecified model, only A, D, and F are selected because it was previously discussed that A, D, and F are best-selling and key drivers for the total net sales.
    ''', unsafe_allow_html=True)

    quarter_w_analysis()

    st.markdown('''<div style="text-align: center"> Q1 : A > D > F </div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: center"> Q2 : A > F > D </div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: center"> Q3 : A ~ F > D </div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: center"> Q4 : A > F ~ D </div>''', unsafe_allow_html=True)
    st.markdown('''<br>
    The W orders can be compared with the actual sales data for years 2016 through 2019. Higher y coordinates and more congruence with the yearly net sales graph indicates a higher degree of contribution to the yearly net sales. 
    The products are ranked from the most congruence with the highest y axis to the least congruence with the lowest y axis.
    ''', unsafe_allow_html=True)

    col1,col2 = st.beta_columns(2)
    with col1:
        net_sales_for_quarterly_W(2016)
        net_sales_for_quarterly_W(2018)
    with col2:
        net_sales_for_quarterly_W(2017)
        net_sales_for_quarterly_W(2019)

    st.markdown('''<div style="text-align: center"> Q1 : A > D > F </div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: center"> Q2 : A > F > D </div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: center"> Q3 + Q4 : not analyzed due to the outliers and errors in the modeled system </div>''', unsafe_allow_html=True)

    st.markdown('''<br>
    Hence, A is the key driving force for the net sales of the first two quarters. D is the next most important for Q1, and F is the next most significant for Q2 and Q3. In fact, F is more weighted for Q3 than Q2. Nevertheless, this doesn’t denote F is sold more in terms of quantity in Q3.
    For efficient sales planning and order placements, an emphasis on Product A and D during Q1 and on Product F during Q2 and Q3 is required.
    <br><br>''', unsafe_allow_html=True)

    #### Forecast #####
    st.markdown('<i><p class="big-font">**Section 4. Forecast **</p></i>', unsafe_allow_html=True)

    #### Section 4.1 #####
    st.markdown('''4.1 | <i>Forecast of 2021 Sales</i>''', unsafe_allow_html=True)
    st.markdown("""
    2021 sales are forecasted based on two rates that are present for the business growth — annual business growth (YoY) and COVID recovery rate. Despite the presence of various other factors, only two are considered for the simplicity of the analysis. For YoY, the same annual business growth is assumed which was calculated in Section 1.1. To find how much the business in 2021 has recovered from the effect of the pandemic crisis compared to 2020, data from 2020 and 2021 are compared. 
    <br><br>
    For 2021 quantity sales forecast: <br><br>
    2021 April QS w/o COVID recovery = (2021 Jan-April Quantity Sales) – (YoY)*(2021 Jan-April Quantity Sales) <br> 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = X-Y(X) <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = Z lb <br>

    COVID recover rate = 2021 April QS / 2020 April QS <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = X / Y <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = Z  <br>
    <br>
    2021 Dec QS Forecast = 2021 April QS + 2020 May-Dec * (YoY + COVID recover rate) <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = X + Y (U + V) <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = W lb <br>
    <br>
    Similarly, the forecast of 2021 net sales is conducted with the same approach, which is computed to be X kЄ. 
    <br><br>""",unsafe_allow_html = True)

    prediction()

    st.markdown("""
    Based on the forecasted data, the business is predicted to grow X % in quantity and Y % in net sales compared to the previous year 2020.
    Note that the forecast accuracy of 2021 net sales should be relatively much lower than that of quantity sales, since the net sales forecast is conducted without the consideration of different sales prices of the products and varying COVID recovery rates.
    <br><br>""",unsafe_allow_html = True)


    #### Section 4.2 #####
    st.markdown('''4.2 | <i>Forecast Factors for the Market Demand</i>''', unsafe_allow_html=True)
    st.markdown("""
    Still, the proposed method to forecast 2021 sales lacks its accuracy, and the forecast remains to be a conjecture since only average YoY growth rate and COVID-19 are considered though numerous other complex aspects are also interrelated. Hence, to enhance the accuracy of the forecast, potential growth rate factors are evaluated that could also influence the degree of inclination of the 2021 forecasted graph. The conditions are discussed below.
    <br>""",unsafe_allow_html = True)

    st.markdown('''
    - COVID recovery rate: As more vaccines have been readily available in South Korea and with vaccination rates picking up, loosening of COVID restrictions including mask mandates and social distancing for those vaccinated is expected to come into force more quickly. Consequently, the demand for UV filter products is predicted to grow.
    <br><br>
        - Evidence 1: <br>
        The United States, one of the countries with the highest vaccination rate for coronavirus, witnesses the positive effect of COVID vaccines on the growing outdoor recreational activities and travels. The Transportation Security Administration announced that 2.03 million travelers were screened at airport security checkpoints on June 11th. It was the first time in 15 months that the number of security screenings has surpassed 2 million in a single day. Moreover, the Centers for Disease Control and Prevention (CDC) announced on May 13th that fully vaccinated people do not need to wear a mask while resuming pre-pandemic activities. These infer that vaccination can bring forth consumer confidence that drives the behavior of consumer spending and also the economic recovery on the sun care market through an increasing demand for sunscreens.
    <br><br>
        - Evidence 2: <br>
        It is found that the effectiveness of vaccines and exposure to sun are interrelated. A research paper (Hart & Norval, 2020), “Are there differences in immune responses following delivery of vaccines through acutely or chronically sun-exposed compared with sun-unexposed skin?,” demonstrates that increased levels of sun exposure can result in the reduced efficacy of vaccination by stimulating systemic immunosuppression. As vaccination is encouraged to mitigate the COVID-19 transmission and to allow the fully efficacious performance of vaccines, wearing sunscreens is recommended and thus the demand for sun care products will grow.  
    <br><br>
    - Oil prices climb: As mentioned in the previous factor, vaccination has increased the road traffic in the U.S. and Europe. As a result, petroleum has gained on demand recovery, and its price has surged in recent weeks. Since UV filters are petrochemicals, this change in oil price will subsequently decrease the sales margin.
    <br><br>
    - SPF scandal in S. Korea: In Dec 2020, an ingredient database INCIDecoder revealed that the SPF of Centella Green Level Unscented Sunscreen to be 19 which is less than half of its advertised SPF of 50+. After the Purito incident, many other sun care products came under scrutiny. Yet, this scandal does not indicate that the brands are being deceitful overstating their protection levels. However, for the sunscreen companies to regain the trust from customers, they will need to complete more rigorous assessments on the SPF testing, and for those products which do not meet the targeted SPF, more UV filter chemicals will need to be added. As a consequence, the demand for UV filters will grow.
    <br><br>
    - Growing awareness of the importance of sunscreens due to skin cancer: Growing outdoor recreational activities have prompted increasing incidences of skin cancer. According to the American Academy of Dermatology, skin cancer rates are rising faster than any other cancer in the United States. Currently, 3.3 million Americans are diagnosed with nonmelanoma skin cancer each year. These fast-growing skin cancer rates across the globe are directly related to the exposure of UV wavelengths. The research paper (Lee et al., 2014), “Implication of ultraviolet B radiation exposure for non-melanoma skin cancer (NMSC) in Korea,” found out a strong positive correlation between the annual UVB index and NMSC incidence. As consumers have become more aware of the skin cancers caused by the UV rays in sunlight, it will catalyze the sun care market growth.
    <br><br>
    ''',unsafe_allow_html = True)


    #### Section 4.3 #####
    st.markdown('''4.3 | <i>Forecast Factors for Each Product Demand</i>''', unsafe_allow_html=True)
    st.markdown('''
    A detailed examination on the possible causes to increase the demand for each product is conducted as below. Product names are randomly assinged for confidentiality.
    <br><br>
    - Product X: Product X is a physical UV filter commonly found in organic sunscreens which functions by scattering, reflecting, and absorbing the UV rays, whereas chemical UV filters absorb the UV rays before they reach the skin.
    <br><br>
        - Best fit for sensitive skin types: <br>
        Many of today's sunscreens contain both physical and chemical UV filters. However, a growing beauty trend towards natural and organic skincare products amid COVID has been resulted due to mask mandates, and zinc oxide is an anti-irritant and well tolerated by sensitive skin types. Indeed, it is the only sunscreen active ingredient that’s been tested and FDA approved for use on babies under 6 months of age and children. In contrast to zinc oxide, titanium dioxide, another physical UV filter commonly found in the marketplace, creates more free radicals that do oxidative damage to your body and skin cells and increases aging processes. 
    <br><br>
        - Proportional impact from customers: <br>
        Company X is the only customer for Product X. Since Company X’s YoY market share has doubled, it can be anticipated that the demand for Product X will become twice of the last year’s demand at most. 
    <br><br>
    - Product Y: It blocks UV radiation from 280 nm to 400 nm, essentially covering both UVA and UVB ranges, and hence is preferred over other UV filter products. Due to more people being vaccinated and loosened COVID guidelines, the sun care products are expected to grow in demand.
    <br><br>
    - Product Z:  It is mostly used in makeup compacts, and similar to Product Y, its demand will increase with the vaccination rate picking up.
    <br><br>
    ''',unsafe_allow_html = True)


    #### Conclusion #####
    st.markdown('<i><p class="big-font">**Section 5. Conclusions **</p></i>', unsafe_allow_html=True)

    st.markdown('''
    COVID-19 outbreak has critically affected every single industry sector including the cosmetics business. Reduced outdoor activities and mask requirements have lowered the sunscreens demand, and consequently the UV filter sales have dramatically dropped. To reinforce the sales profiles of each product and shape the market development strategies more thoroughly, an extensive overview of the past 5 year sales is conducted, and in-depth product sales interpretations as well as market insights based on the qualitative and quantitative analyses are deduced. 
    <br><br>
    From the sales data of the past 5 years, it is verified that the business had an average year-over-year (YoY) business growth of X % for quantity sales and Y % for net sales. However, the UV filter market had plunged in 2020 due to the outbreak of coronavirus resulting in the YoY growth rates of - X % for quantity sales and - Y% for net sales. The average business growth rates prior to COVID-19 approximate a quantity sales of X lb and net sales of Y k$ that would have resulted for the 2020 sales if the pandemic had not been occurred. Qualitative assessments of the sales trends are performed to postulate the most competitive sales products and their distinctive sales trends. Overall sales data suggest Product D is sold the most in quantity whereas Products A, D, and F yield the highest net sales. It is also presumed that most sales are achieved during the first half year, particularly the first quarter, from the sales graph of individual products.
    <br><br>
    More rigorous evaluations are executed through quantitative analysis adapting the Linear Regression Coefficients method to enhance the reliability and accuracy of the study. Linear regression model for the overall sales trend notes Products A and F are the most responsible factors for the overall net sales with Products B and C contributing the least. The ratio of W_cCM1/ W_Net_Sales determines the most profitable product, which is Product F, and thus Product F should be emphasized for additional promotion. Moreover, a detailed analysis on the market dynamics and each product growth is presented through yearly W computation; THADD caused a sudden drop in sales of all products in 2018 and COVID-19 entailed the lowest 2020 revenue in the past 5 years. The results further validate that Products A, B, and F are growing in demand while Products D and E are declining in their demand trends. The comparison of the results simultaneously designate the impact of coronavirus on the sales of each product that Products D, E, and A are negatively impacted the most and Products B, C, and F are influenced the least by the pandemic. Regarding the past sales trends prior to 2020, it is inferred that the demands for Products E and A are most likely temporarily affected by COVID-19. Product D, however, shows a continuous fall in its linear regression coefficients, and thus its sales value is diminishing. To maintain and further reinforce its salability, it necessitates more effective promotions or product developments such that it could potentially avoid the effect of Hawaii ban. Quarterly W analysis is subsequently performed to draw a conclusion that Product A is the most significant product for the sales of the first two quarters, Product D is the second most for the first quarter sales, and Product F is the second most for the second quarter sales with its importance surge in the third quarter sales. Hence, a well-organized supply management and order placement scheduling for Products A and D for the first quarter and for Products A and F for the second quarter will increase the effectiveness of the sales activities and build customer trust.
    <br><br>
    Forecast of 2021 sales is estimated based on the presumptive calculation of the average YoY business growth rate and COVID-19 recovery rate. The forecast anticipates a quantity sales of X lb and a net sales of Y kЄ, which are an YoY grow of X % in quantity sales and Y % in net sales, respectively. Yet, the forecast lacks its accuracy since only two rates are considered while numerous other aspects should have been also measured. Thus, to supplement the accuracy of the forecast, some circumstances that could transform the forecasted graph are discussed. The COVID-19 vaccination rates, SPF scandal, and growing concerns about skin cancer in response to the UV exposure are deemed to positively affect the sun care demand of 2021. Still, the current inclining trend of petroleum price signals a lower sales margin for petrochemical UV filter products. In addition, the change in the market trend to organic products can intensify the demand growth particularly of Product X, and its main customer, in fact, has shown a sharp recovery in their stock market price as compared to the previous year. Products Y and Z are also considered to proportionally increase in their demand in response to the higher demand for sunscreens due to the vaccination rates.
    <br><br>
    During the course of this project, some factors and statements are hypothesized due to the lack of necessary data and for the simplicity of the study. To improve the accuracy of the proposed results, it should have covered a more wide range of sales data rather than the past five years and have conducted further extensive research and interpretations on the sunscreen market. Nevertheless, the current model succeeded to examine all the sales aspects sufficiently to discover remarkable findings that would help the effective sales of the products.
    <br><br>
    ''', unsafe_allow_html=True)


    #### References #####
    st.markdown('<i><p class="big-font">**Section 6. References **</p></i>', unsafe_allow_html=True)
    st.markdown("""
    McKinsey & Company. (n.d.). How COVID-19 is changing the world of beauty. McKinsey & Company. <br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; https://www.mckinsey.com/industries/consumer-packaged-goods/our-insights/how-covid-19-is-changing-the-world-of-beauty
    <br><br>
    Wikipedia. (n.d.). Linear Regression. Wikipedia. https://en.wikipedia.org/wiki/Linear_regression
    <br><br>
    Hart, P. H., & Norval, M. (2020). Are there differences in immune responses following delivery of vaccines through acutely or chronically sun-exposed compared with <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sun-unexposed skin?. Immunology, 159(2), 133–141. https://pubmed.ncbi.nlm.nih.gov/31593303/
    <br><br>
    Lee, S., & Yoon, H., & Bae, H., & Ha, J., & Pak, H., & Shin, Y., & Son, S. (2014). Implication of ultraviolet B radiation exposure for non-	melanoma skin cancer in Korea. Molecular & &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Cellular Toxicology. 10. 91-94. 10.1007/s13273-014-0011-1. 
    <br><br><br>
    """, unsafe_allow_html=True)

    #### Acknowledgements #####
    st.markdown('<i><p class="big-font">**Section 7. Acknowledgements **</p></i>', unsafe_allow_html=True)
    st.markdown('''
    The accomplishment of this undertaking could not have been possible without the participation and assistance of many colleagues at BASF A-EMA/AR whose names may not all be enumerated. The author would like to express her sincere gratitude to the team for their professional leaderships, insightful suggestions and expertise on data interpretation, and encouragements. This work was supported by the A-EMA/AR site in Republic of Korea, BASF- ASIA PACIFIC.
     ''', unsafe_allow_html=True)


    #### Disclaimer #####
    st.markdown('<i><p class="big-font">**Section 8. Confidentiality **</p></i>', unsafe_allow_html=True)
    st.markdown('''
    Restrictions apply to the availability of the data in this project, which is used under license from A-EMA/AR, BASF-ASIA PACIFIC. Readers can contact at the following URL: https://www.basf.com/kr/en/who-we-are/sites-and-contacts.html
    <br><br>
    The content of this project strictly remains confidential. If you are not the intended audience you must not disclose, distribute or use the information in it as this could be a breach of confidentiality. If you have accessed this website in error, please advise the author immediately by e-mailing the author at hongx296@umn.edu and deleting the link. The address on which this project has been posted is strictly for business use only and the company reserves the right to monitor the contents of communications and take action where and when it is deemed necessary. Thank you for your co-operation.
    <br><br>
    ''', unsafe_allow_html=True)


#### Agreement From ###
st.error('''** User Agreement** : The content of this project strictly remains confidential. If you are not the intended audience you must not disclose, distribute or use the information in it as this could be a breach of confidentiality. 
If you have accessed this website in error, please advise the author immediately by e-mailing the author at hongx296@umn.edu and deleting the link. Restrictions apply to the availability of the data in this project, which is used under license from A-EMA/AR, BASF-ASIA PACIFIC.
Readers can contact at the following URL: https://www.basf.com/kr/en/who-we-are/sites-and-contacts.html. 
The address on which this project has been posted is strictly for business use only and the author reserves the right to monitor the contents of communications and take action where and when it is deemed necessary. Thank you for your co-operation.      
By clicking "I agree," you acknowledge that you have read and accept the User Agreement, and you will shortly be directed to the main content.
''')
if st.button("Yes, I hereby acknowledge that I have read, understand, and agree to the terms and conditions of the User Agreement."):
    run()