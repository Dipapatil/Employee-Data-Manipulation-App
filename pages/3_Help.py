import streamlit as st


image = "database_icon.jpg"
st.set_page_config(layout="wide",page_title="Employee Data Upadation App",page_icon=image)


st.title("How to use Employee Data Upadation App")


st.write("")
st.info("This app can be used to Insert, Update or Delete records from Employee table")

st.write("<b>Insert New Record</b> :  Enter Employee Name, Departement, Hire Date, Termination Date"
         " in the input box, employee number is automatically generated ",unsafe_allow_html=True)
st.write("<b>Update Record</b> : select Employee Employee Number from drop down list at top and then"
         " enter other details to override existing"
         ,unsafe_allow_html=True)
st.write("<b>Delete program</b> : Select Employee Number to delete existing employee record",unsafe_allow_html=True)
st.write("")
st.write("")
