import streamlit as st

def student_screen():
    st.header("Student screen")
    if st.button('Back to home screen'):
        st.session_state['login_type'] = None
        st.rerun()