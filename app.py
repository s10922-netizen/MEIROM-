import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS Admin", page_icon="⚡", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

# 🔑 המייל של המנכ"לית
MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב CYBER UI (נקי, גדול, ממורכז) ---
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
        font-size: 35px; font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* כפתורי ענק במרכז */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white; border-radius: 25px; height: 100px;
        font-size: 28px; font-weight: 700; width: 100%;
        border: none; margin: 20px 0;
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px; padding: 40px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px; width: 100%;
    }

    /* התנתקות */
    .logout-btn button {
        background: transparent !important; border: 1px solid #ff4b4b !important;
        height: 45px !important; font-size: 14px !important; margin-top: 40px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. פונקציית בדיקה חסינה ---
def get_user_data(email):
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        search_m = str(email).strip().lower()
        # חיפוש המייל בכל התאים
        for _, row in df.iterrows():
            if search_m in " ".join(row.astype(str)).lower():
                # מחלץ את השם (בדרך כלל בעמודה האחרונה)
                return str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
        return None
    except: return None

# --- 4. ניהול דפים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

# א. דף כניסה
if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    u_mail = st.text_input("אימייל", placeholder="מייל...").strip().lower()
    u_pass = st.text_input("סיסמה", type="password", placeholder="סיסמה...")
    
    if st.button("שיגור ⚡"):
        if u_mail == MY_ADMIN_EMAIL:
            st.session_state.user_email = u_mail
            st.session_state.biz_name = "מנכ\"לית"
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            biz = get_user_data(u_mail)
            st.session_state.user_email = u_mail
            if biz:
                st.session_state.biz_name = biz
                st.session_state.is_new = False
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "onboarding"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ב. אונבורדינג (למשתמשים חדשים)
elif st.session_state.page == "onboarding":
    st.markdown("<div class='cyber-title'>ברוכה הבאה!</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    b_name = st.text_input("מה שם העסק?")
    b_loc = st.text_input("איפה אתם ממוקמים?")
    if st.button("בואי נתחיל ✨"):
        if b_name:
            st.session_state.biz_name = b_name
            st.session_state.is_new = True
            # שליחה לגוגל
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            requests.post(url, data={"entry.855862094": st.session_state.user_email, "entry.1847739029": f"Biz: {b_name} | Loc: {b_loc}"})
            st.session_state.page = "dashboard"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ג. לוח בקרה
elif st.session_state.page == "dashboard":
    # --- מערכת הפנייה האישית ---
    if st.session_state.user_email == MY_ADMIN_EMAIL:
        welcome = "ברוכה הבאה מנכ\"לית מיי. כל המערכות פועלות כשורה."
    elif st.session_state.get('is_new'):
        welcome = f"ברוכה הבאה לעסק {st.session_state.biz_name}!"
    else:
        welcome = f"ברוכה השבה לעסק {st.session_state.biz_name}!"

    st.markdown(f"<div class='cyber-title'>{welcome}</div>", unsafe_allow_html=True)
    
    if st.session_state.tool == "home":
        st.markdown("### מה היעד הבא שלך?")
        if st.button("🤖 סוכן תוכן AI"): 
            st.session_state.tool = "ai"
            st.rerun()
        if st.button("💬 צ'אט שירות לקוחות"): 
            st.session_state.tool = "chat"
            st.rerun()
    
    if st.session_state.tool != "home":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if st.session_state.tool == "ai":
            st.subheader("סוכן התוכן שלך")
            topic = st.text_input("נושא:")
            if st.button("צור פוסט ✨"):
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"פוסט ל{st.session_state.biz_name} על {topic}"}])
                st.write(res.choices[0].message.content)
        elif st.session_state.tool == "chat":
            st.subheader("צ'אט שירות")
            q = st.chat_input("דברי איתי...")
            if q:
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":f"נציגת שירות של {st.session_state.biz_name}"},{"role":"user","content":q}])
                st.write(res.choices[0].message.content)
        
        if st.button("חזרה לתפריט"):
            st.session_state.tool = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("התנתקות"):
        st.session_state.page = "auth"
        st.session_state.tool = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
