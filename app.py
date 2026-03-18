import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS Elite", page_icon="⚡", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

# 🔑 המייל שלך - המערכת תזהה אותך כמנכ"לית
MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב CYBER-MAGIC UI (גדול ונגיש) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;700&family=Orbitron:wght@700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #050505; color: #e0e0e0;
    }

    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 40px; text-align: center;
        background: linear-gradient(90deg, #00f2fe 0%, #7c3aed 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 25px; padding: 10px;
    }

    /* כרטיסי ניווט ענקיים */
    .nav-card {
        background: rgba(20, 20, 20, 0.9);
        border: 2px solid #7c3aed;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin-bottom: 20px;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.2);
    }
    .nav-card:hover {
        border-color: #00f2fe;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.4);
        transform: translateY(-5px);
    }

    /* כפתורים גדולים במיוחד */
    .stButton>button {
        background: linear-gradient(45deg, #6366f1, #a855f7);
        color: white; border-radius: 20px; height: 80px; font-size: 24px; font-weight: 700; width: 100%;
        border: none; margin-top: 10px;
    }
    
    .logout-btn>div>button {
        background: transparent !important; border: 1px solid #ff4b4b !important; height: 40px !important; font-size: 14px !important;
    }

    input { background-color: #1a1a1a !important; color: #00f2fe !important; border: 1px solid #444 !important; height: 50px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה לזיהוי עסק ---
def get_biz_name(email):
    try:
        url = f"{SHEET_CSV_URL}&refresh={time.time()}"
        df = pd.read_csv(url)
        search_m = str(email).strip().lower()
        for _, row in df.iterrows():
            row_str = " ".join(row.astype(str)).lower()
            if search_m in row_str:
                # מנסה לחלץ את שם העסק (העמודה האחרונה בדרך כלל)
                return str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
        return None
    except: return None

# --- 4. ניווט דפים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_name' not in st.session_state: st.session_state.biz_name = ""

# א. דף כניסה
if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='nav-card'>", unsafe_allow_html=True)
    u_mail = st.text_input("מייל מנכ\"לית / עסק").strip().lower()
    u_pass = st.text_input("סיסמה", type="password").strip()
    
    if st.button("כניסה למערכת ⚡"):
        if u_mail and u_pass:
            biz = get_biz_name(u_mail)
            st.session_state.user_email = u_mail
            if biz:
                st.session_state.biz_name = biz
                st.session_state.is_new = False
                st.session_state.page = "dashboard"
            elif u_mail == MY_ADMIN_EMAIL:
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "onboarding"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ב. דף אונבורדינג (שם עסק ומיקום)
elif st.session_state.page == "onboarding":
    st.markdown("<div class='cyber-title'>הגדרת עסק חדש</div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-card'>", unsafe_allow_html=True)
    new_biz = st.text_input("שם העסק שלך")
    new_loc = st.text_input("מיקום (עיר / אונליין)")
    if st.button("בואי נצא לדרך ✨"):
        if new_biz:
            st.session_state.biz_name = new_biz
            st.session_state.is_new = True
            # שליחה לגוגל
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            requests.post(url, data={"entry.855862094": st.session_state.user_email, "entry.1847739029": f"Business: {new_biz} | Location: {new_loc}"})
            st.session_state.page = "dashboard"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ג. לוח בקרה (התפריט המרכזי הענק)
elif st.session_state.page == "dashboard":
    # לוגיקת פנייה אישית
    if st.session_state.user_email == MY_ADMIN_EMAIL:
        welcome = "ברוכה הבאה מנכ\"לית מיי. כל המערכות פועלות כשורה."
    elif st.session_state.get('is_new'):
        welcome = f"ברוכה הבאה לעסק {st.session_state.biz_name}! בואי נתחיל."
    else:
        welcome = f"ברוכה השבה לעסק {st.session_state.biz_name}!"

    st.markdown(f"<div class='cyber-title' style='font-size:26px;'>{welcome}</div>", unsafe_allow_html=True)
    
    # תפריט ענקי באמצע
    st.markdown("### מה את רוצה לעשות היום?")
    
    if st.button("🤖 סוכן תוכן AI"): st.session_state.tool = "ai"
    if st.button("💬 צ'אט שירות לקוחות"): st.session_state.tool = "chat"
    
    st.markdown("---")
    
    current_tool = st.session_state.get('tool', 'home')
    
    if current_tool == "ai":
        st.markdown("<div class='nav-card'>", unsafe_allow_html=True)
        st.header("סוכן התוכן שלך")
        goal = st.text_input("נושא הפוסט?")
        if st.button("צור פוסט ✨"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט לעסק {st.session_state.biz_name} בנושא {goal}"}])
            st.info(res.choices[0].message.content)
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif current_tool == "chat":
        st.markdown("<div class='nav-card'>", unsafe_allow_html=True)
        st.header("נציג שירות AI")
        q = st.chat_input("שאלת לקוח...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":f"את נציגת שירות של {st.session_state.biz_name}"}, {"role":"user","content":q}])
            st.write(res.choices[0].message.content)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("התנתקות מהמערכת"):
        st.session_state.page = "auth"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
