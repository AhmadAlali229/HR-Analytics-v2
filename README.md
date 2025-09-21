# 📊 HR Analytics Dashboard  

An **HR Analytics web app** built with **Streamlit** and **SQLite**.  
This project focuses on analyzing employee attrition, performance, and satisfaction.  
The dashboard makes it easy to explore HR data, generate insights, and even manage records (add or update employees).  

Dataset used:  
👉 [IBM HR Analytics Employee Attrition & Performance (Kaggle)](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)  

---

## 📂 Project Structure  
 app.py # Streamlit web app (Dashboard + Add/Update employees)
 dbDemo.ipynb # Jupyter Notebook with SQL + Python queries  
 employees.db # SQLite database (generated from CSV)  
 WA_Fn-UseC_-HR-Employee-Attrition.csv # Original dataset   
 requirements.txt # Python dependencies  
 README.md # Project documentation


---

## 🚀 Features  
✔️ **Dashboard (Overview):** Filter employees by department, visualize average monthly income, and view employee details  
✔️ **Add Employee:** Insert new employee records into the database  
✔️ **Update Income:** Update employee salaries directly from the dashboard  
✔️ **Queries:** SQL + Python queries for HR insights

---

## 📑 Dataset  
We use the **IBM HR Analytics Employee Attrition & Performance** dataset from Kaggle.  
It contains **1,470 employee records** with details such as:  
- Department  
- Job Role  
- Age  
- Gender  
- Monthly Income  
- Performance Rating  
- Job Satisfaction  
- Attrition (whether an employee left or not)  

This dataset is widely used for **HR analytics, machine learning practice, and attrition prediction research**.  

---

## 🛠️ Technologies  
Python  
Pandas  
SQLite    
Streamlit   
Plotly

---

## ▶️ How to Run  
Clone the repo and install dependencies:  
```bash
git clone https://github.com/AhmadAlali229/HR-Analytics-v2
cd HR-Analytics
pip install -r requirement.txt

streamlit run app.py