import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS Elite", page_icon="⚡", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

# המייל שלך - זיהוי מנכ"לית
MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב Cyber UI - הכל במרכז וגדול ---
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
        font-size: 38px; font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }

    /* כרטיס תפריט מרכזי */
    .menu-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        width: 100%; max-width: 500px; margin: 0 auto;
    }

    /* כפתורי ענק */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white; border-radius: 25px; height: 90px;
        font-size: 26px; font-weight: 700; width: 100%;
        border: none; margin: 15px 0;
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05); box-shadow: 0 15px 30px rgba(0, 242, 254, 0.5);
    }

    /* התנתקות */
    .logout-btn button {
        background: transparent !important; border: 1px solid #ff4b4b !important;
        height: 50px !important; font-size: 16px !important; margin-top: 50px !important;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה ---
def get_biz_name(email):
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        search_m = str(email).strip().lower()
        for _, row in df.iterrows():
            if search_m in " ".join(row.astype(str)).lower():
                return str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
        return None
    except: return None

# --- 4. ניהול דפים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

# א. כניסה
if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    u_mail = st.text_input("אימייל", placeholder="הכניסי מייל...").strip().lower()
    u_pass = st.text_input("סיסמה", type="password", placeholder="הכניסי סיסמה...")
    
    if st.button("כניסה למערכת ⚡"):
        if u_mail:
            biz = get_biz_name(u_mail)
            st.session_state.user_email = u_mail
            if biz or u_mail == MY_ADMIN_EMAIL:
                st.session_state.biz_name = biz if biz else "מנכ\"לית"
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "onboarding"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ב. אונבורדינג
elif st.session_state.page == "onboarding":
    st.markdown("<div class='cyber-title'>נעים להכיר!</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    new_biz = st.text_input("מה שם העסק שלך?")
    if st.button("בואי נתחיל ✨"):
        if new_biz:
            st.session_state.biz_name = new_biz
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            requests.post(url, data={"entry.855862094": st.session_state.user_email, "entry.1847739029": f"Biz: {new_biz}"})
            st.session_state.page = "dashboard"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ג. לוח בקרה מרכזי
elif st.session_state.page == "dashboard":
    # פנייה אישית
    if st.session_state.user_email == MY_ADMIN_EMAIL:
        header_msg = "ברוכה הבאה מנכ\"לית מיי ✨"
    else:
        header_msg = f"ברוכה השבה, עסק {st.session_state.biz_name}"

    st.markdown(f"<div class='cyber-title'>{header_msg}</div>", unsafe_allow_html=True)
    
    # הצגת התפריט רק אם לא בתוך כלי
    if st.session_state.tool == "home":
        st.markdown("### מה את רוצה לעשות היום?")
        if st.button("🤖 סוכן תוכן AI"): 
            st.session_state.tool = "ai"
            st.rerun()
        if st.button("💬 צ'אט שירות לקוחות"): 
            st.session_state.tool = "chat"
            st.rerun()
    
    # תצוגת הכלים
    if st.session_state.tool == "ai":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("סוכן תוכן AI")
        goal = st.text_input("על מה נכתוב?")
        if st.button("צור קסם ✨"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"פוסט ל{st.session_state.biz_name} על {goal}"}])
            st.write(res.choices[0].message.content)
        if st.button("חזרה לתפריט"):
            st.session_state.tool = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.tool == "chat":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("צ'אט שירות")
        q = st.chat_input("שאלי אותי...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":f"נציגת שירות של {st.session_state.biz_name}"},{"role":"user","content":q}])
            st.write(res.choices[0].message.content)
        if st.button("חזרה לתפריט"):
            st.session_state.tool = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # התנתקות למטה
    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("התנתקות מהמערכת"):
        st.session_state.page = "auth"
        st.session_state.tool = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
