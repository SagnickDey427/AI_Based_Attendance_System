import streamlit as st

def teacher_screen():
    st.header("Teacher screen")
    if st.button('Back to home screen'):
        st.session_state['login_type'] = None
        st.rerun()