## import Libaries
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect("employees.db") #connecting with database

##Loading Database
def load_employees():
    return pd.read_sql_query("SELECT * FROM employees;", conn)

df = load_employees()
st.set_page_config(page_title="HR Dashboard", page_icon="📊", layout="wide")# Title
st.markdown('<h1 style="font-size:50px; font-weight:800; margin-bottom:10px;">HR Analytics Dashboard</h1>', unsafe_allow_html=True)#Styling Title
st.markdown("An interactive dashboard where you can analyze employees, add new records, and update salaries easily.")#Descreption

tab_overview, tab_add, tab_update = st.tabs(["Overview", "Add Employee", "Update Income"])#Creating Taps to be usesd later
