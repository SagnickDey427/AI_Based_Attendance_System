import time
import streamlit as st
from PIL import Image



@st.dialog("Upload or take photos for attendance")
def add_photos_dialog(join_code):
    st.write("Upload or take photos for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"
    tab1,tab2 = st.columns(2)

    with tab1:
        type_cam = "primary" if st.session_state.photo_tab=="camera" else "tertiary"
        if st.button("Camera",type=type_cam,width='stretch'):
            st.session_state.photo_tab = "camera"
    with tab2:
        type_cam = "primary" if st.session_state.photo_tab=="upload" else "tertiary"
        if st.button("Upload photos",type=type_cam,width='stretch'):
            st.session_state.photo_tab = "upload"

    if st.session_state.photo_tab == "camera":
        cam_input = st.camera_input("Take snapshot",key="dialog_cam")
        if cam_input:
            st.session_state.attendance_iamges.append(Image.open(cam_input))
        st.toast("Photo captured successfully✅")
        st.rerun()
    
    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader("Upload files",type=['jpg','png','jpeg'],accept_multiple_files=True)
        for f in uploaded_files:
            st.session_state.attendance_images.append(Image.open(f))
        st.toast("Photos uploaded successfully✅")
        st.rerun()

    st.divider()
    if st.button("Done"):
        st.rerun()
    