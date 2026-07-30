import streamlit as st

from src.database.db import check_student_already_enrolled, check_subject_exists, enroll_student

@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter your subject code to join")
    sub_code = st.text_input("Subject code",placeholder='CSE101')
    if st.button("Join group"):
        if sub_code:
            subject_data = check_subject_exists(sub_code)
            if subject_data:
                student_id = st.session_state.student_data['student_id']
                check = check_student_already_enrolled(subject_data = subject_data, student_id = student_id)
                if check:
                    st.warning("You are already enrolled in this course")
                else:
                    enroll_student(student_id = student_id, subject_id = subject_data['subject_id'])
            st.rerun()
        else:
            st.warning("Please enter the subject code")