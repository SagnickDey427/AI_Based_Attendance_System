import streamlit as st

def header_home():
    logo_url = "static/icon.png"
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(logo_url,width=100)
    st.markdown("""
        <div style='margin-bottom:2rem; Smargin:auto;'>
        <h2 style='text-align:center; font-size:3rem;'>Face<br/> In</h2>
                </div>
    """,unsafe_allow_html=True)
    
        
    