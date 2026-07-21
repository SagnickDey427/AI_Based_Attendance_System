import streamlit as st

def footer():
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='margin-top:5rem; font-size:0.8rem;'>
            <p>&copy; Copyright | 2024 -  All Rights Reserved | Face In</p>
            <span style='color:#947c4d; margin-right:0.3rem;'>Sagnick</span> 
            <span style='color:#F0F4FF;'>Dey</span>
        </div>
        """, unsafe_allow_html=True)