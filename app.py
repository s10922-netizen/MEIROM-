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

# --- 2. עיצוב CYBER-MAGIC UI ---
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
        margin-bottom: 25px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white; border-radius: 25px; height: 85px;
        font-size: 24px; font-weight: 700; width: 100%;
        border: none; margin: 15px 0;
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px; padding: 40px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    input { background-color: #1a1a1a !important; color: #00f2fe !important; border: 1px solid #444 !important; }
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
            row_str = " ".join(row.astype(str)).lower()
            if search_m in row_str:
                biz_name = str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
                return "RETURNING", biz_name
        return "NEW", None
    except: return "NEW", None

def register_user(email, password, biz_name):
    # שליחה ל-Google Form
    payload = {
        "entry.855862094": email, 
        "entry.1847739029": f"Pass: {password} | Biz: {biz_name}"
    }
    try:
        requests.post(FORM_URL, data=payload)
        return True
    except:
        return False

# --- 4. זרימת עמודים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

# א. דף כניסה והרשמה (משולב)
if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 כניסה", "✨ הרשמה חדשה"])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        l_mail = st.text_input("אימייל", key="login_m").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="login_p")
        if st.button("שיגור למערכת 🚀"):
            status, name = get_user_status(l_mail)
            if status != "NEW":
                st.session_state.user_email = l_mail
                st.session_state.biz_name = name
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("לא מצאנו אותך. אולי תירשמי בלשונית השנייה?")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        r_mail = st.text_input("מייל לעסק", key="reg_m").strip().lower()
        r_pass = st.text_input("בחרי סיסמה", type="password", key="reg_p")
        r_biz = st.text_input("שם העסק שלך", key="reg_b")
        if st.button("צור לי אימפריה ✨"):
            if r_mail and r_pass and r_biz:
                if register_user(r_mail, r_pass, r_biz):
                    st.session_state.user_email = r_mail
                    st.session_state.biz_name = r_biz
                    st.session_state.is_new = True
                    st.session_state.page = "dashboard"
                    st.rerun()
                else: st.error("משהו השתבש ברישום. נסי שוב.")
            else: st.warning("בבקשה מלאי את כל הפרטים.")
        st.markdown("</div>", unsafe_allow_html=True)

# ב. לוח בקרה
elif st.session_state.page == "dashboard":
    if st.session_state.user_email.lower() == MY_ADMIN_EMAIL.lower():
        welcome = "ברוכה הבאה מנכ\"לית מיי ✨"
    elif st.session_state.get('is_new'):
        welcome = f"ברוכה הבאה לעסק {st.session_state.biz_name}!"
    else:
        welcome = f"ברוכה השבה לעסק {st.session_state.biz_name}!"

    st.markdown(f"<div class='cyber-title' style='font-size:30px;'>{welcome}</div>", unsafe_allow_html=True)
    
    if st.session_state.tool == "home":
        st.markdown("### מה היעד הבא שלך?")
        if st.button("🤖 סוכן תוכן AI"): 
            st.session_state.tool = "ai"
            st.rerun()
        if st.button("💬 צ'אט שירות לקוחות"): 
            st.session_state.tool = "chat"
            st.rerun()
        
        st.markdown("---")
        if st.button("התנתקות", key="logout"):
            st.session_state.page = "auth"
            st.session_state.tool = "home"
            st.rerun()
    
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if st.session_state.tool == "ai":
            st.header("סוכן תוכן AI")
            topic = st.text_input("על מה נכתוב?")
            if st.button("צור פוסט"):
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"פוסט ל{st.session_state.biz_name} על {topic}"}])
                st.info(res.choices[0].message.content)
        
        elif st.session_state.tool == "chat":
            st.header("צ'אט שירות")
            q = st.chat_input("דברי איתי...")
            if q:
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":f"נציגת שירות של {st.session_state.biz_name}"},{"role":"user","content":q}])
                st.write(res.choices[0].message.content)

        if st.button("חזרה לתפריט 🏠"):
            st.session_state.tool = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
