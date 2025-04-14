import streamlit as st
import mysql.connector

# ---------- DATABASE CONNECTION ----------
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",              # Replace with your MySQL username
        password="admin", # Replace with your MySQL password
        database="test"
    )
    return conn

# ---------- ADD PATIENT ----------
def add_patient(name, age, gender, contact, address):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO patient (name, age, gender, contact, address) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, age, gender, contact, address))
    conn.commit()
    conn.close()

# ---------- VIEW PATIENTS ----------
def get_all_patients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Hospital Management System", layout="wide")
st.title("🏥 Hospital Management System")

menu = ["Add Patient", "View Patients"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Patient":
    st.subheader(" Add New Patient")
    with st.form(key="add_form"):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact = st.text_input("Contact")
        address = st.text_area("Address")
        submit = st.form_submit_button("Add Patient")

        if submit:
            add_patient(name, age, gender, contact, address)
            st.success(f"Patient '{name}' added successfully!")

elif choice == "View Patients":
    st.subheader("📋 All Patients")
    patients = get_all_patients()

    if patients:
        st.dataframe(patients, use_container_width=True)
    else:
        st.info("No patient records found.")
