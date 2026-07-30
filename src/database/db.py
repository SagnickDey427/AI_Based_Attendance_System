from src.database.config import supabase
import bcrypt

def check_teacher_exist(username):
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data) > 0

def hash_pass(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hash_pwd):
    return bcrypt.checkpw(pwd.encode(),hash_pwd.encode())


def create_teacher(name,username,password):
    data={"name":name,"username":username,"password":hash_pass(password)}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data :
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name, face_emb=None, audio_emb=None):
    data = {'name':new_name,'face_embedding':face_emb,'voice_embedding':audio_emb}
    resp = supabase.table('students').insert(data).execute()
    return resp

def create_subject(sub_id, sub_name, sub_section, teacher_id):
    data = {"subject_code":sub_id,"subject_name":sub_name,"section":sub_section,"teacher_id":teacher_id}
    resp = supabase.table("subjects").insert(data).execute()
    return resp.data
    
def get_all_subjects():
    resp = supabase.table("subjects").select("*").execute()
    return resp.data

# Understand how did we wrote relational query to fetch all details here 👇🏻
def get_teacher_subjects(teacher_id):
    resp = supabase.table("subjects").select("*,subject_students(count), attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subjects = resp.data
    for sub in subjects:
        sub['total_students'] = sub.get("subject_students",[{}])[0].get("count",0) if sub.get("subject_students") else 0
        attendance = sub.get("attendance_logs",[])
        unique_sessions = len((set(log['timestamp'] for log in attendance)))
        sub['total_classes'] = unique_sessions
        sub.pop('attendance_logs',None)
        sub.pop('subject_students',None)
    return subjects


def check_subject_exists(sub_code):
    res = supabase.table('subjects').select('*').eq('subject_code',sub_code).execute()
    subjects = res.data[0]
    if subjects:
        return subjects
    return None

def check_student_already_enrolled(subject_data, student_id):
    check = supabase.table('subject_students').select('*').eq('subject_id',subject_data['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        return True
    return False

def enroll_student(student_id,subject_id):
    data = {"student_id":student_id,"subject_id":subject_id}
    resp = supabase.table("subject_students").insert(data).execute()
    return resp.data

def unenroll_student(student_id,subject_id):
    resp = supabase.table('subject_students').delete().eq('subject_id',subject_id).eq('student_id',student_id).execute()
    return resp.data


def get_student_subjects(student_id):
    resp = supabase.table('subject_students').select('*,subjects(*)').eq('student_id',student_id).execute()
    return resp.data

def get_student_attendance(student_id):
    resp = supabase.table('attendance_logs').select('*,subjects(*)').eq('student_id',student_id).execute()
    return resp.data