import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_bg_home
from src.ui.base_layout import style_base_layout
from src.components.footer import footer

def home_screen():
    style_bg_home()
    style_base_layout()
    header_home()
    col1,col2,col3 = st.columns([2,1,2])
    with col1:
        html_content = """
        <div class="teacher-card">
            <h2>I'm<br>Teacher</h2>
            <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="145" style="margin-top: 10px;">
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        
        # 3. Place the Streamlit button immediately underneath
        # Use use_container_width=True to make the button match the card's width
        if st.button("Go to teacher portal", type='primary', use_container_width=True,icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    with col3:
        html_content = """
        <div class="teacher-card">
            <h2>I'm<br>Student</h2>
            <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" width="120" style="margin-top: 10px;">
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        if st.button("Go to student portal", use_container_width=True,icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()
    footer()