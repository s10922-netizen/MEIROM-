import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. System Setup ---
st.set_page_config(page_title="Magic Hub", page_icon="⚡", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. CYBER-NEON DESIGN (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Assistant:wght@300;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #0f172a; color: #f8fafc;
    }

    /* כותרת ניאון */
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px; font-weight: 700; text-align: center;
        color: #fff; text-shadow: 0 0 10px #7c3aed, 0 0 20px #7c3aed;
        margin: 40px 0;
    }

    /* כרטיסיות זוהרות */
    .cyber-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    /* כפתורי ניאון */
    .stButton>button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white; border-radius: 12px; border: none;
        height: 55px; font-size: 18px; font-weight: 700; width: 100%;
        transition: 0.3s; text-transform: uppercase;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(124, 58, 237, 0.7);
    }

    /* עיצוב שדות קלט */
    input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. Core Logic (Table Connection) ---
def verify_login(email, password):
    try:
        # עוקף Cache כדי לקבל נתונים טריים מהטבלה
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        # ניקוי נתונים לבדיקה
        df_clean = df.astype(str).apply(lambda x: x.str.strip().str.lower())
        search_m = email.lower().strip()
        search_p = password.lower().strip()
        
        # עובר שורה-שורה ובודק אם המייל והסיסמה מופיעים באותה שורה
        for _, row in df_clean.iterrows():
            row_str = " ".join(row.values)
            if search_m in row_str and search_p in row_str:
                return True
        return False
    except: return False

# --- 4. Navigation ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🚀 כניסה", "⚡ הרשמה"])
    
    with t1:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        m = st.text_input("אימייל").strip().lower()
        p = st.text_input("סיסמה", type="password")
        if st.button("שיגור למערכת ⚡"):
            if verify_login(m, p):
                st.session_state.user_email = m
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("גישה נדחתה. ודאי שהפרטים נכונים ונמצאים בטבלה.")
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        rm = st.text_input("מייל הרשמה", key="rm")
        rp = st.text_input("סיסמה חדשה", type="password", key="rp")
        if st.button("התחלת תהליך ✨"):
            st.session_state.temp_m, st.session_state.temp_p = rm, rp
            st.session_state.page = "onboarding"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "onboarding":
    st.markdown("<div class='cyber-title'>הגדרת עסק</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        name = st.text_input("שם המותג")
        desc = st.text_area("מה העסק עושה?")
        if st.button("יצירת חשבון"):
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            requests.post(url, data={"entry.855862094": st.session_state.temp_m, "entry.1847739029": f"Pass: {st.session_state.temp_p} | Biz: {name}"})
            st.session_state.user_email = st.session_state.temp_m
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='cyber-title' style='font-size:30px;'>WELCOME, {st.session_state.user_email.split('@')[0]}</div>", unsafe_allow_html=True)
    
    menu = st.selectbox("ניווט מהיר", ["🏠 בסיס", "✍️ סוכן AI", "💬 צ'אט"])
    
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    if menu == "🏠 בסיס":
        st.write("כל המערכות פועלות. מוכנה לכיבוש העולם.")
        if st.button("ניתוק קשר"):
            st.session_state.page = "auth"
            st.rerun()
            
    elif menu == "✍️ סוכן AI":
        goal = st.text_input("משימה לסוכן:")
        if st.button("הפעל פקודה ⚡"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט מגניב על: {goal}"}])
            st.info(res.choices[0].message.content)

    elif menu == "💬 צ'אט":
        q = st.chat_input("דברי איתי...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"אתה סוכן AI מגניב."}, {"role":"user","content":q}])
            st.write(res.choices[0].message.content)
    st.markdown("</div>", unsafe_allow_html=True)
