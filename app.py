
import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")
st.write("Manage Student Records using CRUD Operations")

# CSV File
FILE = "students.csv"

# Load Data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course", "Marks"]
    )

# Sidebar Menu
st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":

    st.subheader("➕ Add New Student")

    with st.form("add_form"):
        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        marks = st.number_input("Marks", min_value=0, max_value=100)

        submit = st.form_submit_button("Add Student")

        if submit:
            if not name.strip() or not course.strip():
                st.error("Please enter Name and Course")
            elif roll in df["Roll No"].values:
                st.error("Roll Number already exists!")
            else:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                df = pd.concat([df, new_student], ignore_index=True)
                df.to_csv(FILE, index=False)

                st.success("Student Added Successfully!")

# READ
elif menu == "View Students":

    st.subheader("📋 All Student Records")

    df = pd.read_csv(FILE) if os.path.exists(FILE) else df

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.write("Total Students:", len(df))
    else:
        st.info("No Student Records Found")

# UPDATE
elif menu == "Update Student":

    st.subheader("✏️ Update Student Details")

    if not df.empty:

        roll = st.selectbox(
            "Select Roll Number",
            df["Roll No"].tolist()
        )

        student = df[df["Roll No"] == roll].iloc[0]

        with st.form("update_form"):

            name = st.text_input("Name", student["Name"])
            age = st.number_input(
                "Age", min_value=1, max_value=100,
                value=int(student["Age"])
            )
            course = st.text_input("Course", student["Course"])
            marks = st.number_input(
                "Marks", min_value=0, max_value=100,
                value=int(student["Marks"])
            )

            update = st.form_submit_button("Update Student")

            if update:
                df.loc[df["Roll No"] == roll, "Name"] = name
                df.loc[df["Roll No"] == roll, "Age"] = age
                df.loc[df["Roll No"] == roll, "Course"] = course
                df.loc[df["Roll No"] == roll, "Marks"] = marks

                df.to_csv(FILE, index=False)

                st.success("Student Updated Successfully!")
    else:
        st.info("No Records Available")

# DELETE
elif menu == "Delete Student":

    st.subheader("🗑️ Delete Student Record")

    if not df.empty:

        roll = st.selectbox(
            "Select Roll Number to Delete",
            df["Roll No"].tolist()
        )

        if st.button("Delete Student"):
            df = df[df["Roll No"] != roll]
            df.to_csv(FILE, index=False)

            st.success("Student Deleted Successfully!")
    else:
        st.info("No Records Available")