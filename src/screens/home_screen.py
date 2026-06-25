import streamlit as st
from src.components.header_home import header_home

def home_screen():
    st.header("Home screen")
    header_home()
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Go to teacher portal",type='primary'):
            st.session_state['login_type']='teacher'
            st.rerun()
    with col2:
        if st.button("Go to student portal"):
            st.session_state['login_type']='student'
            st.rerun()