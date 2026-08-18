import streamlit as st
from src.components.dialog_add_photos import add_photos_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_bg_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer
from src.database.db import create_teacher,check_teacher_exist, get_teacher_subjects,teacher_login

def register_teacher(teacher_name,teacher_username,teacher_pass,teacher_pass_confirm):
    if not teacher_name or not teacher_username or not teacher_pass or not teacher_pass_confirm:
        return False,"All fields are required!"
    if check_teacher_exist(teacher_username):
        return False,"Username already exists"
    if teacher_pass != teacher_pass_confirm :
        return False,"Password doesn't match"
    try:
        create_teacher(teacher_name,teacher_username,teacher_pass)
        return True,"Succesfully registered! Now you can login"
    except Exception as e:
        return False,"Unknown error!"


def login_teacher(teacher_username, teacher_pass):
    if not teacher_username or not teacher_pass:
        return False,"All fields required"
    if not check_teacher_exist(teacher_username):
        return False,"User doesn't exist"
    else:
        try:
            teacher = teacher_login(teacher_username,teacher_pass)
            if teacher:
                st.session_state.user_role = "teacher"
                st.session_state.is_logged_in = True
                st.session_state.teacher_data = teacher
                st.session_state.teacher_id = teacher['teacher_id']
                return True,"Logged in successfully"
            return False,"Unknown Error!"
        except Exception as e:
            print(e)
            return False,"Unknown error!"
            

def teacher_screen_login():
    st.markdown(
        """
        <style>
        div[data-baseweb="input"] input {
            color: #2E86C1 !important; 
            -webkit-text-fill-color: #2E86C1 !important; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("Login into your teacher profile")
    teacher_username = st.text_input("Enter Username",placeholder="Enter username")
    teacher_pass = st.text_input("Enter Password",type="password",placeholder='Enter Password')
    st.divider()
    btncol1, btncol2 = st.columns(2)
    with btncol1 : 
        if st.button("Login",icon=':material/passkey:',shortcut='command+enter',width='stretch'):
            success,message = login_teacher(teacher_username,teacher_pass)
            if success:
                st.toast(message,icon="👋🏻")
                import time 
                time.sleep(2)
                st.rerun()
            else:
                st.error(message)
    with btncol2 : 
        if st.button("Register Instead",icon=':material/passkey:',type='primary',width='stretch'):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()

def teacher_screen_signup():
    st.markdown(
        """
        <style>
        div[data-baseweb="input"] input {
            color: #2E86C1 !important; 
            -webkit-text-fill-color: #2E86C1 !important; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("Register your teacher profile")
    teacher_username = st.text_input("Enter Username",placeholder="Enter username",key='username')
    teacher_name = st.text_input("Enter Name",placeholder="Enter name",key='name')
    teacher_pass = st.text_input("Enter Password",type="password",placeholder='Enter Password',key='password')
    teacher_pass_confirm = st.text_input("Confirm Password",type="password",placeholder='Confirm Password')
    st.divider()
    btncol1, btncol2 = st.columns(2)
    with btncol1 : 
        if st.button("Register",icon=':material/passkey:',shortcut='command+enter',width='stretch'):
            success,message = register_teacher(teacher_name,teacher_username,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type='login'
                st.rerun()
            else:
                st.error(message)

    with btncol2 : 
        if st.button("Login Instead",icon=':material/passkey:',type='primary',width='stretch'):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()

def logout_teacher():
    st.session_state.pop("teacher_data",None)
    st.session_state.is_logged_in=False
    st.session_state.user_role="unverified"

def teacher_dashboard():
    
    if "teacher_data" in st.session_state:
        teacher_data = st.session_state.teacher_data
    else:
        teacher_data = {"name":"Teacher(Error)"}

    col1,col2 = st.columns(2)
    with col1:
        st.subheader(f"Welcome , {teacher_data['name']}")
    with col2:
        st.button("Log out",type="tertiary",on_click=logout_teacher)

    st.space()

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1,tab2 , tab3= st.columns(3)
    with tab1:
        type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()
    with tab3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance records',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == 'attendance_records':
        teacher_tab_attendance_records()
    

def teacher_tab_take_attendance():
    teacherId = st.session_state.teacher_data['teacher_id']
    st.subheader("Take AI attendance") 

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subject_list = get_teacher_subjects(teacherId)
    if not subject_list:
        st.info("You don't have any subjects, please create one first.")
        return 
    subject_options = {f"{s['subject_code']} - {s['subject_name']}":f"{s['subject_id']}" for s in subject_list}

    col1,col2 = st.columns([3,1])
    selected_subject_options = None
    with col1:
        selected_subject_options = st.selectbox("Select a subject",options=list(subject_options.keys()))
    with col2:
        if st.button("➕ Add photos",icon=":materials/monochrome_photos:",type='primary', width='stretch'):
            add_photos_dialog()



def teacher_tab_manage_subjects():
    teacher_id = st.session_state['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Manage Subjects") 
    with col2:
        if st.button("Create new subject",type='primary', width='stretch'):
            create_subject_dialog(teacher_id)

    #list all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students",sub['total_students']),
                ("⏰","Classes",sub['total_classes'])
            ]
            def share_subject():
                if st.button(f"Share code : {sub['subject_code']}",icon=':material/share:',key=f'sub_{sub['subject_code']}'):
                    share_subject_dialog(sub_name = sub['subject_name'], sub_code = sub['subject_code'])
                st.space()

            subject_card(name = sub['subject_name'], code = sub['subject_code'], section = sub['section'], stats = stats, footer_callback = share_subject)
    else:
        st.info("No subjects found , create one.")


def teacher_tab_attendance_records():
    st.subheader("Attendance records") 



def teacher_screen():
    style_bg_dashboard()
    style_base_layout()
    header_dashboard()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_signup()
    footer()
    
    