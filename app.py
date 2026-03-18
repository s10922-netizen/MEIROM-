import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות וחיבורים ---
st.set_page_config(page_title="Business OS", page_icon="💼", layout="wide")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key Missing")
    st.stop()

# --- 2. פונקציות ליבה ---
def get_users_df():
    try:
        url = f"{SHEET_CSV_URL}&refresh={pd.Timestamp.now().timestamp()}"
        return pd.read_csv(url)
    except: return pd.DataFrame()

def save_to_google(email, data_dict):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    # אנחנו שולחים את כל המידע (מייל, חבילה, פרטי עסק) לשדה הסיסמה/מידע בטבלה
    info_string = " | ".join([f"{k}: {v}" for k, v in data_dict.items()])
    payload = {"entry.855862094": email, "entry.1847739029": info_string}
    requests.post(url, data=payload)

# --- 3. עיצוב CSS (נקי, עסקי, לא סוכנותי) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .main-title { color: #1e293b; font-size: 40px; font-weight: bold; text-align: center; padding: 20px; }
    .stButton>button { background: #4f46e5; color: white; border-radius: 8px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבים ---
if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = {}

# --- 5. ניווט דפים ---

# א. דף כניסה/הרשמה
if st.session_state.page == "login":
    st.markdown("<div class='main-title'>Business OS - כניסה למערכת</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 יצירת חשבון"])
    
    with t1:
        email = st.text_input("אימייל").strip().lower()
        if st.button("כניסה למרכז הניהול"):
            df = get_users_df()
            if not df.empty and email in df.astype(str).values:
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("משתמש לא נמצא. אנא הירשמי.")

    with t2:
        r_email = st.text_input("מייל לעסק", key="re")
        r_pass = st.text_input("סיסמה", type="password", key="rp")
        if st.button("המשך להקמת העסק"):
            st.session_state.temp_email = r_email
            st.session_state.temp_pass = r_pass
            st.session_state.page = "onboarding"
            st.rerun()

# ב. דף הגדרת עסק (זה הפתרון לסעיף 3 שלך!)
elif st.session_state.page == "onboarding":
    st.markdown("<h2 style='text-align:center;'>ספרי לנו על העסק שלך 🖋️</h2>", unsafe_allow_html=True)
    biz_name = st.text_input("שם העסק")
    biz_desc = st.text_area("מה העסק מוכר/עושה? (פירוט עבור ה-AI)")
    target = st.text_input("מי קהל היעד שלך?")
    
    if st.button("שמור והמשך לבחירת חבילה"):
        st.session_state.biz_data = {"name": biz_name, "desc": biz_desc, "target": target}
        st.session_state.page = "packages"
        st.rerun()

# ג. דף חבילות
elif st.session_state.page == "packages":
    st.markdown("<h2 style='text-align:center;'>בחירת מסלול שירות</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("מסלול פרימיום (AI מלא)"):
            data = {**st.session_state.biz_data, "plan": "Premium"}
            save_to_google(st.session_state.temp_email, data)
            st.session_state.page = "dashboard"
            st.session_state.user_email = st.session_state.temp_email
            st.rerun()
    with c2:
        if st.button("מסלול בסיסי"):
            data = {**st.session_state.biz_data, "plan": "Basic"}
            save_to_google(st.session_state.temp_email, data)
            st.session_state.page = "dashboard"
            st.session_state.user_email = st.session_state.temp_email
            st.rerun()

# ד. מרכז הבקרה (הפורטל הלבן)
elif st.session_state.page == "dashboard":
    st.sidebar.title("Business Manager")
    menu = st.sidebar.radio("תפריט", ["🏠 לוח בקרה", "🤖 סוכן שיווק חכם"])
    
    if menu == "🏠 לוח בקרה":
        st.markdown(f"## ברוך הבא לפורטל הניהול")
        st.write(f"החשבון שלכם פעיל במערכת (משתמש: {st.session_state.user_email})")
        
    elif menu == "🤖 סוכן שיווק חכם":
        st.header("יצירת תוכן מותאם לעסק")
        goal = st.text_input("מה המטרה של הפוסט היום?")
        
        if st.button("צור תוכן מבוסס נתוני העסק"):
            # כאן הקסם: ה-AI מקבל את הנתונים שהלקוח מילא ב-Onboarding!
            biz = st.session_state.get('biz_data', {'desc': 'עסק כללי', 'target': 'כולם'})
            prompt = f"כתוב פוסט שיווקי עבור עסק ששמו {biz.get('name')}. תיאור העסק: {biz.get('desc')}. קהל יעד: {biz.get('target')}. מטרה: {goal}."
            
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.write(res.choices[0].message.content)
