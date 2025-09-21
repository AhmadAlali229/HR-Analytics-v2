## import Libaries
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from PIL import Image
conn = sqlite3.connect("..\data\employees.db") #connecting with database

##Loading Database
def load_employees():
    return pd.read_sql_query("SELECT * FROM employees;", conn)

df = load_employees()

#Add logo
LOGO = Image.open('..\Picture1.png')
left, mid, right = st.columns([1,3,1])
st.image(LOGO, width=180)

st.set_page_config(page_title="HR Dashboard", page_icon="📊", layout="wide")# Title
st.markdown('<h1 style="font-size:50px; font-weight:800; margin-bottom:10px;">HR Analytics Dashboard</h1>', unsafe_allow_html=True)#Styling Title
st.markdown("An interactive dashboard where you can analyze employees, add new records, and update salaries easily.")#Descreption

tab_overview, tab_add, tab_update = st.tabs(["Overview", "Add Employee", "Update Income"])#Creating Taps to be usesd later

# --- ultra simple theme ---
PURPLE = "#5B2BE0"
PINK   = "#FF3B6A"

st.markdown(f"""
<style>
/* Shading color */
.stApp {{
  background: linear-gradient(135deg, {PURPLE} 0%, {PINK} 100%);
  color: #FFFFFF;
}}
/*    button color */
button[kind="primary"], button[data-baseweb="button"] {{
  background: {PINK};
  color: #FFFFFF;
}}
</style>
""", unsafe_allow_html=True)


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
    
    #Creatin Tavle to show Employee details
    st.subheader(f"Employee Details ({dept})")
    st.dataframe(df_view, use_container_width=True)

#Using add employee Tab
with tab_add:
    # crearing roles maps for selection based on department
    job_roles_map = {
        "Human Resources": ["Human Resources", "Manager"],
        "Research & Development": ["Research Scientist","Laboratory Technician", "Manufacturing Director",
                                    "Healthcare Representative", "Manager","Research Director",],
        "Sales": ["Sales Executive", "Sales Representative", "Manager"],
    }

    # This container is to figure out the employees Department and jobrole before form
    with st.container():
        st.markdown("### Adding New Employee ")
        department = st.selectbox("Department", list(job_roles_map.keys()), key="dept_live")
        job_role   = st.selectbox("JobRole", job_roles_map[department], key="role_live")

        #creating form
    with st.form("Add new Employee"):
        #creating Cells
        Age = st.number_input("**Age**", min_value=18, max_value=80, value=30,placeholder="Enter Employee's Age") #creatin age cell
        MonthlyIncome = st.number_input("**MonthlyIncome**",placeholder="Enter Employee's MonthlyIncome", min_value=0, value=5000)
        ot     = st.selectbox("OverTime", ["No","Yes"])
        #Submit Button
        submit = st.form_submit_button("Add Employee ",use_container_width=True,type='primary')
        
        if submit:
            try:
                with sqlite3.connect("employees.db") as c: # When Submiting a form it connects to the DB
                    
                    #this command is to Insert Enterd Data into The DB using SQL Query
                    c.execute(
                        """
                        INSERT INTO employees
                        (Age, Department, JobRole, MonthlyIncome, OverTime)
                        VALUES (?, ?, ?, ?, ?);
                        """,
                        (
                        int(Age),
                        department.strip(),
                        job_role.strip(),
                        int(MonthlyIncome),
                        ot,
                            ),
                )
                    c.commit()

                #notifactions 
                st.success("Employee inserted ✅")
                st.rerun()
                st.success("Form Submitted Successfully")
            #if Insert fail this comes up
            except Exception as e:
                st.error(f"Insert failed: {e}")
#Using Update Income Tab
with tab_update:            
    st.subheader("Update Employee Monthly Income")#header for tab



    with st.form("update_income"):
        #creatin cells for entering
        emp_id = st.number_input("EmployeeNumber", min_value=1, step=1)#creating a cell for primary key is the employee number 
        new_income = st.number_input("New MonthlyIncome", min_value=0, step=1000)# cell for setting new income
        update_btn = st.form_submit_button("Update Income", use_container_width=True, type="primary")  #Submit Button

    if update_btn:
        try:
            with sqlite3.connect("employees.db") as c:# When Submiting a form it connects to the DB
                
                #this command is to UPDATE Enterd Data into The DB using SQL Query
                c.execute(
                    """
                    UPDATE employees
                    SET MonthlyIncome = ?
                    WHERE EmployeeNumber = ?;
                    """,
                    (int(new_income), int(emp_id)),
                )
                c.commit()
            #notifactions 
            st.success(f"Employee {emp_id} income updated to {new_income} ✅")
            st.rerun()
        #if Insert fail this comes up
        except Exception as e:
            st.error(f"Update failed: {e}")

