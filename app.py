import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS Elite", page_icon="⚡", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"

MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב Cyber-SaaS (נקי וממורכז) ---
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
        font-size: 42px; font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 50px; margin-bottom: 30px;
    }

    /* כפתורי ענק נקיים */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white; border-radius: 20px; height: 80px;
        font-size: 24px; font-weight: 700; width: 100%;
        border: none; margin: 10px 0;
        box-shadow: 0 8px 15px rgba(124, 58, 237, 0.2);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02); box-shadow: 0 12px 25px rgba(0, 242, 254, 0.4);
    }

    /* תיבות קלט נקיות בלי ריבועים שחורים מסביב */
    input {
        background-color: #111 !important;
        color: #00f2fe !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        height: 50px !important;
        text-align: center !important;
    }

    /* הסתרת כותרות Tabs שיוצרות בלגן */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. פונקציות ליבה ---
def get_user_status(email):
    if email.lower().strip() == MY_ADMIN_EMAIL.lower().strip():
        return "ADMIN", "מנכ\"לית"
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        search_m = str(email).strip().lower()
        for _, row in df.iterrows():
            if search_m in " ".join(row.astype(str)).lower():
                biz_name = str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
                return "RETURNING", biz_name
        return "NEW", None
    except: return "NEW", None

def register_user(email, password, biz_name):
    payload = {"entry.855862094": email, "entry.1847739029": f"Pass: {password} | Biz: {biz_name}"}
    try: requests.post(FORM_URL, data=payload); return True
    except: return False

# --- 4. זרימת עמודים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

# דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 כניסה", "✨ הרשמה"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        l_mail = st.text_input("אימייל", key="l_m", placeholder="הכניסי מייל...").strip().lower()
        l_pass = st.text_input("סיסמה", key="l_p", type="password", placeholder="הכניסי סיסמה...")
        if st.button("שיגור למערכת 🚀"):
            status, name = get_user_status(l_mail)
            if status != "NEW" or l_mail == MY_ADMIN_EMAIL:
                st.session_state.user_email = l_mail
                st.session_state.biz_name = name if name else "מנכ\"לית"
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("לא מצאנו אותך. אולי תירשמי?")

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        r_mail = st.text_input("מייל לעסק", key="r_m").strip().lower()
        r_pass = st.text_input("סיסמה", key="r_p", type="password")
        r_biz = st.text_input("שם העסק", key="r_b")
        if st.button("צור לי אימפריה ✨"):
            if r_mail and r_pass and r_biz:
                if register_user(r_mail, r_pass, r_biz):
                    st.session_state.user_email = r_mail
                    st.session_state.biz_name = r_biz
                    st.session_state.page = "dashboard"
                    st.rerun()
                else: st.error("שגיאה ברישום.")

# דף לוח בקרה
elif st.session_state.page == "dashboard":
    # פנייה מותאמת אישית
    if st.session_state.user_email == MY_ADMIN_EMAIL:
        welcome = "ברוכה הבאה מנכ\"לית מיי ✨"
    else:
        welcome = f"ברוכה השבה לעסק {st.session_state.biz_name}"

    st.markdown(f"<div class='cyber-title' style='font-size:32px;'>{welcome}</div>", unsafe_allow_html=True)
    
    if st.session_state.tool == "home":
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🤖 סוכן תוכן AI"): st.session_state.tool = "ai"; st.rerun()
        if st.button("💬 צ'אט שירות לקוחות"): st.session_state.tool = "chat"; st.rerun()
        
        st.markdown("---")
        if st.button("התנתקות"): st.session_state.page = "auth"; st.rerun()
    
    else:
        if st.session_state.tool == "ai":
            st.header("סוכן תוכן AI")
            topic = st.text_input("נושא הפוסט?")
            if st.button("צור פוסט"):
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"פוסט ל{st.session_state.biz_name} על {topic}"}])
                st.info(res.choices[0].message.content)
        
        elif st.session_state.tool == "chat":
            st.header("צ'אט שירות")
            q = st.chat_input("דברי איתי...")
            if q:
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":f"נציגת שירות של {st.session_state.biz_name}"},{"role":"user","content":q}])
                st.write(res.choices[0].message.content)

        if st.button("חזרה לתפריט 🏠"): st.session_state.tool = "home"; st.rerun()
