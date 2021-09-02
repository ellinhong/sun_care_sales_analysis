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
covid_impact_graph()