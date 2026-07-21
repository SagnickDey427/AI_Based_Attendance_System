import time

import streamlit as st
from src.database.db import create_student, get_all_students
from src.pipelines.face_pipeline import get_face_embeddings, predict_attendance, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_bg_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer
import numpy as np 
from PIL import Image

def student_dashboard():
    st.header("Dashboard")

def student_screen():
    style_bg_dashboard()
    style_base_layout()
    header_dashboard()
    if 'student_data' in st.session_state:
        student_dashboard()
        if st.button("Logout",type='tertiary'):
            del st.session_state['student_data']
            del st.session_state['user_role']
            st.rerun()
    else:
        show_registration = False
        st.header("Login using faceId",text_alignment='center')
        photo_source  = st.camera_input("Position your face in the center")
        if photo_source :
            img = np.array(Image.open(photo_source))
            with st.spinner("AI is scanning.."):
                detected_students, all_ids, encodings_cnt = predict_attendance(img)
                if encodings_cnt == 0 :
                    st.warning("No face detected")
                elif encodings_cnt > 1 :
                    st.warning("Multiple faces detected")
                else:
                    if detected_students:
                        student_id = list(detected_students.keys())[0]
                        all_students = get_all_students()
                        student = None
                        for s in all_students :
                            if s['student_id'] == student_id:
                                student= s
                                break
                        if student:
                            st.session_state.is_logged_in=True
                            st.session_state.user_role='student'
                            st.session_state.student_data = student
                            st.toast(f'Welcome back , {student['name']}')
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info("Face not recognised , might be a new student!")
                        show_registration = True
        if show_registration:
            with st.container(border=True):
                st.header("Register your profile")
                new_name = st.text_input("Enter your name", placeholder="E.g. Sagnick Dey")

                st.subheader("Optional : Voice enrollment")
                st.info("enroll your voice for voice-based attendance")
                audio_data = None
                try:
                    audio_data = st.audio_input("Try saying something")
                except Exception:
                    st.error("Audio input error")
                
                if st.button("Create account",type='primary'):
                    if new_name:
                        with st.spinner("Creating account.."):
                            img = np.array(Image.open(photo_source))
                            embedding = get_face_embeddings(img)
                            if embedding:
                                face_emb = embedding[0].tolist()
                                audio_emb = None
                                if audio_data:
                                    audio_emb = get_voice_embedding(audio_data.read())

                                response_data= create_student(new_name,face_emb, audio_emb)
                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in=True
                                    st.session_state.user_role='student'
                                    st.session_state.student_data = response_data.data[0]
                                    st.toast(f'Onboarding ,welcome  {new_name}')
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Couldn't capture youtr face")
                    else:
                        st.warning("Name is required")
                

                    

    footer()