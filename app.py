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