import streamlit as st


def header_home():
    logo_url = "static/icon.png"
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(logo_url,width=100)
    col_space1,col_text,col_space2 = st.columns([3,2,3])
    with col_text:
        st.markdown("""
            <div style='margin-bottom:2rem; Smargin:auto;'>
            <h2 style='text-align:left; font-size:3rem;'>Face<br/> In</h2>
                    </div>
        """,unsafe_allow_html=True)
        


def header_dashboard():
    logo_url = "static/icon.png"
    col_img, col_text, col_space, col_button = st.columns(
        [1, 2,2,4], 
        vertical_alignment="center"
    )  
    with col_img:
        st.image(logo_url,width=100)
    with col_text:
        st.markdown("""
            <div style='margin-bottom:2rem; margin:auto;'>
            <h2 style='text-align:left; font-size:3rem;'>Face<br/> In</h2>
                    </div>
        """,unsafe_allow_html=True)
    with col_space:
        st.empty()
    with col_button:
        if st.button('Back to home screen',use_container_width=True,shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()
        
        
    
        
    