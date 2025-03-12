############ Employee Data Manipulation App - to insert, update, delete records using streamlit

import streamlit as st
import pyodbc
import pandas as pd
from tabulate import tabulate
from datetime import datetime


image = "database_icon.jpg"
st.set_page_config(layout="wide",page_title="Employee Data Manipulation App",page_icon=image)
col1,col2 = st.columns([1,14])
with col1:
    st.image("database_icon.jpg",width=80)

with col2:
    st.title("Employee Data Manipulation App ")


# Initialize the dataset if file doesn't exist
def load_data():
    try:
        return pd.read_excel("employee_data.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["EmployeeID", "Name", "Age", "Department", "Salary"])
        df.to_excel(employee_data.xlsx, index=False)
        return df

def fetch_eno():
    df= load_data()
    emp_num = df["Employee_Number"]
    return emp_num



num = st.selectbox("Select Employee Number To Update Record",fetch_eno())
name=st.text_input(label="Employee Name")
dept= st.text_input(label="Department")
hire_date= st.date_input(label="Hire Date")
term_date= st.date_input(label="Termination Date")

hire_date = hire_date.strftime('%Y-%m-%d')
term_date = term_date.strftime('%Y-%m-%d')

css = """
    <style>
        .sidebar-header {
            background-color: #add8e6; 
            color: black; 
            padding: 24px;
            border-radius: 5px;
        }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)
st.sidebar.markdown('<h2 class="sidebar-header">Menu</h2>', unsafe_allow_html=True)

st.sidebar.write("")
st.sidebar.write("")

insert_button = st.sidebar.button("Insert",key="Insert")
delete_button = st.sidebar.button("Delete",key="Delete")
update_button = st.sidebar.button("Update",key="update")


# Save data back to Excel
def save_data(df):
    df.to_excel("employee_data.xlsx", index=False)

# Fetch the latest data
df = load_data()

df.index +=1

st.subheader("📋 Employee Records")
st.dataframe(df)

load_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



if __name__ == '__main__':
    if insert_button:
        # Ensure DataFrame is initialized
        if df.empty:
            df = pd.DataFrame(columns=["Employee_Number", "Name", "Department", "Hire_Date", "Term_Date"])

        new_id = df["Employee_Number"].max() + 1 if not df.empty else 1
        new_employee = pd.DataFrame([[new_id, name, dept, hire_date, term_date]], columns=df.columns)
        df = pd.concat([df, new_employee], ignore_index=True)
        save_data(df)
        st.success("✅ Employee Added!")
        st.write(df.columns)

    if update_button:
        if num in df["Employee_Number"].values:
            df.loc[df["Employee_Number"] == num, ["Name", "Department", "Hire_Date", "Term_Date"]] = [name, dept,hire_date,term_date]
            save_data(df)
            st.success(f"✅ Employee {num} Updated Successfully!")
        else:
            st.error("⚠ Employee Number not found!")
    # Delete Button
    if delete_button:
        if num in df["Employee_Number"].values:
            df = df[df["Employee_Number"] != num]  # Remove selected employee
            save_data(df)
            st.success(f"Employee {num} Deleted Successfully!")
        else:
            st.error("⚠ Employee Number not found!")

