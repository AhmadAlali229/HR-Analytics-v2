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

#Style for tabs when used
st.markdown("""
    <style>
    /* make the tabs text a bit bigger */
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 600;
    }
    /* add some padding so tabs look larger */
    button[data-baseweb="tab"] {
        padding: 12px 20px;
    }
    </style>
""", unsafe_allow_html=True)

#Using Overview Tab
with tab_overview:
    #Creating filter and the All is to be ueds later
    ALL = "All Departments"
    dept = st.selectbox("Filter by Department", [ALL] + sorted(df["Department"].dropna().unique().tolist())) # create a dropdown to filter employees by department
    df_view = df if dept == ALL else df[df["Department"] == dept] # if "All" is selected show all data, else show only the chosen department
    
    st.subheader(f"Average Monthly Income by Job Role ({dept})") #Here is the title for bar chart ialso connected it with dept above
    
    #query i used before in python "dbDemo"
    q3 = (
        df_view.groupby("JobRole")["MonthlyIncome"]
        .mean().round(2)
        .reset_index()
        .rename(columns={"MonthlyIncome": "AvgMonthlyIncome"})
        .sort_values("AvgMonthlyIncome", ascending=False)
    )
    #making bar chart read from query to figure out average monthly income by job role
    st.bar_chart(q3.set_index("JobRole")["AvgMonthlyIncome"], use_container_width=True)
    
    st.subheader(f"Employees by Department ({dept})")#Here is the title for bar chart ialso connected it with dept above
    
    #query i used before in python "dbDemo"
    q2 = df_view["Department"].value_counts().rename_axis("Department").reset_index(name="Count")
    
    #making bar chart read from query to figure out Employyes by department and in department
    st.bar_chart(q2.set_index("Department")["Count"], use_container_width=True)

    #making pie chart with title inside to figure out companys distrubtion
    fig = px.pie(q2, values="Count", names="Department", title="Distribution by Department")
    st.plotly_chart(fig, use_container_width=True)
