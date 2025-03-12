############ Employee Data Manipulation App using sql server- to insert, update, delete records using streamlit

import streamlit as st
import pyodbc
import pandas as pd
from tabulate import tabulate
import database_connection
from datetime import datetime


image = "database_icon.jpg"
st.set_page_config(layout="wide",page_title="Employee Data Upadation App",page_icon=image)
col1,col2 = st.columns([1,14])
with col1:
    st.image("database_icon.jpg",width=80)

with col2:
    st.title("Employee Data Updation App ")


server = 'YOUR_SERVER_NAME'
database = 'YOUR_DATABASE_NAME'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Connection string for SQL Server with authentication
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(conn_str)

def create_table():
  #  conn = database_connection.database_connection_rstudio()
    cursor = conn.cursor()
    cursor = cursor.execute("create table #Employee(Employee_Number int,Name varchar(50), Department varchar(50), Hire_Date Date,Term_Date Date,Load_Date Datetime) ")

    cursor= cursor.execute("INSERT INTO #Employee values (1,'Ram','People Team','02/02/2024','02/03/2025','2025-03-10 16:01:06.984 '), (2,'Geeta','Procurement','01/01/2023','01/01/1900','2025-03-10 16:01:06.984 ')")
    return cursor

def fetch_eno():
   # conn = database_connection_rstudio.database_connection_rstudio()
    cursor = conn.cursor()
    cursor = create_table()
    cursor = cursor.execute(
        "select Employee_Number from  #Employee ")
    rows = cursor.fetchall()
    emp_no_table = []

    columns = ['Employee_Number']
    df_list = []
    for row in rows:
        # print(row[0])
        # print()
        df_row = [(row[0])]
        # print(df_row)
        df = pd.DataFrame(df_row, columns=columns)
        df_list.append(df)
        emp_df = pd.concat(df_list, ignore_index=True)
    cursor.close()
    conn.close()
    return emp_df['Employee_Number']


print(create_table())
num = st.text_input(label="Employee Number")
#num = st.selectbox("Select Employee Number To Update Record",fetch_eno())
name=st.text_input(label="Employee Name")
dept= st.text_input(label="Department")
hire_date= st.date_input(label="Hire Date")
term_date= st.date_input(label="Termination Date")

hire_date = hire_date.strftime('%Y-%m-%d')
term_date = term_date.strftime('%Y-%m-%d')
#
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

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':

    #conn = database_connection_rstudio.database_connection_rstudio()
    cursor = conn.cursor()
    cursor = create_table()
    cursor = cursor.execute("select * from #Employee")

    rows = cursor.fetchall()
    columns = ['Employee_Number', 'Name', 'Department','Hire_Date','Term_Date','Load_Date']
    df_list = []
    for row in rows:
        #print(row)
        # print()
        df_row = [(row[0],row[1], row[2], row[3],row[4],row[5])]
        print(df_row)

        df = pd.DataFrame(df_row, columns=columns)
        df_list.append(df)
        final_df = pd.concat(df_list, ignore_index=True)
    final_df.index += 1
    st.data_editor(final_df, use_container_width=500, key="data_bonus")

    load_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(load_date)


    if insert_button:
            try:
                insert_statement = ("insert into #Employee(Employee_Number,Name,Department,Hire_Date,Term_Date,Load_Date) values (?,?,?,?,?,?)")

                new_row = (num,name,dept,hire_date,term_date,load_date)
                cursor.execute(insert_statement,new_row)
                cursor.commit()
                st.sidebar.success("Record Inserted Successfully")
            except Exception as e:
                st.sidebar.error("Error while inserting data in database, please try again")
                print(e)

    elif update_button:
        try:
            e_no = final_df['Employee_Number']
            if int(num) in e_no.values:

                # st.write("Program ID, Item Type, Item ID is Available in table")
                update_statement = (
                    "update #Employee set Employee_Number=?,"
                    "Name=?,Department=?,Hire_Date=?,Term_Date=?, Load_Date=? where Employee_Number=? "
                 )
                updated_row = (num,name,dept,hire_date,term_date,load_date,num)
                cursor.execute(update_statement, updated_row)
                cursor.commit()
                st.sidebar.success(
                    f"Record updated with these values : Emp_Number : {num}")
            else:
                st.sidebar.error("Please enter valid employee number")
        except Exception as e:
            st.sidebar.error("Error while Updating, please try again",e)

    elif delete_button:
        try:
            e_no = final_df['Employee_Number']

            if int(num) in e_no.values:

                update_statement = (
                    "Delete from #Employee where Employee_Number=?")
                updated_row = (num)
                cursor.execute(update_statement, updated_row)
                cursor.commit()
                st.sidebar.success("Record Deleted Successfully")

            else:
                st.sidebar.error("Please enter valid employee number")
        except Exception as e:
            st.sidebar.error("Error while Updating, please try again")
            print(e)

    cursor.close()
    conn.close()