import streamlit as st


def style_bg_home():
    st.markdown(
        """
            <style>
                .stApp{
                    background:#06113A  !important;        
                }
                .teacher-card{
                    background-color:#F0F4FF !important;
                    padding:2rem !important;
                    border-radius:2.5rem !important;
                    color:#121A2B !important;
                    margin-bottom:2rem !important;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

def style_bg_dashboard():
    st.markdown(
        """
            <style>
                .stApp{
                    background:#F0F4FF  !important;        
                }
                
            </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
                #MainMenu, header, footer{
                    visibility:hidden;        
                }
                .block-container{
                    padding-top:1.5rem !important;
                }
                h1,h2{
                    font-family: "Climate Crisis", sans-serif !important;
                    font-size:2rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0 !important;
                }
                h3,h4,p{
                    font-family: "Outfit", sans-serif !important;
                    
                }
                button[kind="primary"]{
                    background:#121A2B !important;
                    border-radius:1.5rem !important;
                    border: 1px solid #C0A060 !important;
                    transition:transform 0.3s ease-in-out !important;
                    padding:0.5rem 0.9rem !important;
                    color:white !important;
                }
                button[kind="secondary"]{
                    background:#947c4d !important;
                    border-radius:1.5rem !important;
                    border: none !important;
                    transition:transform 0.3s ease-in-out !important;
                    padding:0.5rem 0.9rem !important;
                    color:white !important;
                }
                button[kind="tertiary"]{
                    background:#006666 !important;
                    border-radius:1.5rem !important;
                    border: none !important;
                    transition:transform 0.3s ease-in-out !important;
                    padding:0.5rem 0.9rem !important;
                    color:white !important;
                }
                button:hover{
                transform:scale(1.05);}
            </style>
        """,
        unsafe_allow_html=True
    )