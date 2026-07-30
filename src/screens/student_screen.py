import time

import streamlit as st
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialog
from src.database.db import create_student, get_all_students, get_student_attendance, get_student_subjects, unenroll_student
from src.pipelines.face_pipeline import get_face_embeddings, predict_attendance, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_bg_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer
import numpy as np 
from PIL import Image

def student_dashboard():
    if "student_data" in st.session_state:
            student_data = st.session_state.student_data
    else:
        student_data = {"name":"Student(Error)"}

    col1,col2 = st.columns(2)
    with col1:
        st.subheader(f"Welcome , {student_data['name']}")
    with col2:
        if st.button("Logout",type='tertiary'):
            del st.session_state['student_data']
            del st.session_state['user_role']
            st.rerun()

    st.space()

    c1,c2 = st.columns(2)
    with c1:
        st.header("Show subjects")
    with c2:
        if st.button("Enroll in subject"):
            enroll_dialog()

    st.divider()
    st.space()

    #List all enrolled subjects
    if st.spinner("Loading your subjects..."):
        subjects = get_student_subjects(student_data['student_id'])
        logs = get_student_attendance(student_data['student_id'])

        stats_map={}

        for log in logs:
            sid = log['subject_id']
            if sid not in stats_map:
                stats_map[sid] = {'total':0,'attended':0}
            stats_map[sid]['total']+=1
            if logs.get('is_present'):
                stats_map[sid]['attended']+=1
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']
            stats = stats_map.get(sid,{'total':0,'attended':0})
            def unenroll_btn():
                if st.button("Unenroll from the subject",type='secondary', key=f'id_{sid}'):
                    unenroll_student(student_data['student_id'],sid)
                    st.rerun()
            with cols[i%2]:
                subject_card(
                    name=sub['subject_name'],
                    code = sub['subject_code'],
                    section = sub['section'],
                    stats = [
                        ('📆','Total',stats['total']),
                        ('☑️','Attended',stats['attended']),
                    ],
                    footer_callback=unenroll_btn
                )


def student_screen():
    style_bg_dashboard()
    style_base_layout()
    header_dashboard()
    if 'student_data' in st.session_state:
        student_dashboard()
        
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