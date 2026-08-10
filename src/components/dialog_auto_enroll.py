import time

import streamlit as st

from src.database.db import check_student_already_enrolled, enroll_student, get_subject_name


@st.dialog("Quick enrollment")
def auto_enroll_dialog(join_code):

    # Get student details
    std_id = st.session_state.student_data['student_id']

    # Get subject details
    subject = get_subject_name(join_code)
    if not subject:
        st.error("No subject found!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    # Verify if user is in that group already or not
    check = check_student_already_enrolled(subject_data = subject, student_id = std_id)
    if check:
        st.info("You are already enrolled in this subject.")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to join **{subject['subject_name']}**?")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("No, thanks"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Yes,enroll me in."):
            enroll_student(student_id = std_id, subject_id=subject['subject_id'])
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
    