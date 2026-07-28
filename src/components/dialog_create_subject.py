import streamlit as st
from src.database.db import create_subject

@st.dialog("Create a new subject")
def create_subject_dialog(teacher_id):
    sub_id = st.text_input("Enter subject id",placeholder="CSE101")
    sub_name = st.text_input("Enter subject name",placeholder="Intro to AI")
    sub_section = st.text_input("Enter section",placeholder="e.g. A")
    if st.button("Create subject"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.rerun()
            except Exception as e:
                st.error(f"Error : {e}")
        else:
            st.error("All fields are required")
    