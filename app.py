import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS Admin", page_icon="⚡", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

# המייל המדויק שלך
MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב Cyber UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;700&family=Orbitron:wght@700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: center;
        background-color: #050505; color: #e0e0e0;
    }

    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px; font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white; border-radius: 20px; height: 90px;
        font-size: 24px; font-weight: 700; width: 100%;
        border: none; margin: 15px 0;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 25px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה ---
def get_user_status(email):
    # זיהוי מנכ"לית מיידי
    if email.lower().strip() == MY_ADMIN_EMAIL.lower().strip():
        return "ADMIN", "מנכ\"לית"
    
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        search_m = str(email).strip().lower()
        
        for _, row in df.iterrows():
            row_str = " ".join(row.astype(str)).lower()
            if search_m in row_str:
                # מחלץ שם עסק מהעמודה האחרונה
                biz_name = str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
                return "RETURNING", biz_name
        return "NEW", None
    except:
        return "NEW", None

# --- 4. זרימת עמודים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    u_mail = st.text_input("אימייל").strip().lower()
    u_pass = st.text_input("סיסמה", type="password")
    
    if st.button("כניסה למערכת 🚀"):
        if u_mail:
            status, name = get_user_status(u_mail)
            st.session_state.user_email = u_mail
            st.session_state.biz_name = name
            
            if status == "ADMIN":
                st.session_state.page = "dashboard"
            elif status == "RETURNING":
                st.session_state.is_new = False
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "onboarding"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "onboarding":
    st.markdown("<div class='cyber-title'>ברוכה הבאה!</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    b_name = st.text_input("מה שם העסק שלך?")
    if st.button("בואי נתחיל ✨"):
        if b_name:
            st.session_state.biz_name = b_name
            st.session_state.is_new = True
            requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse", 
                          data={"entry.855862094": st.session_state.user_email, "entry.1847739029": f"Biz: {b_name}"})
            st.session_state.page = "dashboard"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    # הפנייה האישית
    if st.session_state.user_email.lower() == MY_ADMIN_EMAIL.lower():
        welcome = "ברוכה הבאה מנכ\"לית מיי. כל המערכות פועלות מושלם."
    elif st.session_state.get('is_new'):
        welcome = f"ברוכה הבאה לעסק {st.session_state.biz_name}!"
    else:
        welcome = f"ברוכה השבה לעסק {st.session_state.biz_name}!"

    st.markdown(f"<div class='cyber-title'>{welcome}</div>", unsafe_allow_html=True)
    
    if st.session_state.tool == "home":
        if st.button("🤖 סוכן תוכן AI"): 
            st.session_state.tool = "ai"
            st.rerun()
        if st.button("💬 צ'אט שירות לקוחות"): 
            st.session_state.tool = "chat"
            st.rerun()
    
    if st.session_state.tool != "home":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if st.button("חזרה לתפריט 🏠"):
            st.session_state.tool = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("התנתקות"):
        st.session_state.page = "auth"
        st.session_state.tool = "home"
        st.rerun()
