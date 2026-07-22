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