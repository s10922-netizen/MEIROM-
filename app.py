import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"

# המייל של המנכ"לית
MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. THE ZARA HEBREW VIBE (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;700&family=Playfair+Display:wght@700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: center;
        background-color: #ffffff; color: #000000;
    }

    /* כותרת מותג - Serif בעברית/אנגלית מעורב */
    .brand-title {
        font-family: 'Assistant', sans-serif;
        font-size: 45px; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        margin-top: 50px; color: #000;
    }
    
    .brand-tagline {
        font-size: 14px; letter-spacing: 3px; color: #888;
        text-transform: uppercase; margin-bottom: 40px;
    }

    /* כפתורי ZARA שחורים */
    .stButton>button {
        background-color: #000000;
        color: #ffffff; border-radius: 0px; 
        height: 55px; font-size: 16px; font-weight: 300;
        width: 100%; border: none; letter-spacing: 1px;
        transition: 0.3s; margin-top: 10px;
    }
    .stButton>button:hover { background-color: #222; }

    /* שדות קלט נקיים (קו תחתון בלבד) */
    input {
        background-color: transparent !important;
        color: #000 !important;
        border: none !important;
        border-bottom: 1px solid #eee !important;
        border-radius: 0px !important;
        text-align: center !important;
        font-size: 18px !important;
        padding: 10px 0 !important;
    }
    input:focus { border-bottom: 1px solid #000 !important; }

    /* טאבים נקיים */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; color: #aaa; border: none !important; }
    .stTabs [aria-selected="true"] { color: #000 !important; border-bottom: 1px solid #000 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה לבדיקת משתמש ---
def check_user_status(email):
    email_clean = str(email).strip().lower()
    if email_clean == MY_ADMIN_EMAIL.lower():
        return "ADMIN", "מנכ\"לית"
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        for _, row in df.iterrows():
            if email_clean in " ".join(row.astype(str)).lower():
                biz = str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
                return "USER", biz
        return "NEW", None
    except: return "NEW", None

# --- 4. ניווט דפים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-tagline'>מערכות בינה מלאכותית לעסקים</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["כניסה", "הרשמה"])
    
    with t1:
        st.markdown("<br>", unsafe_allow_html=True)
        m = st.text_input("אימייל", key="log_m").strip().lower()
        p = st.text_input("סיסמה", key="log_p", type="password")
        if st.button("כניסה למערכת"):
            status, name = check_user_status(m)
            st.session_state.user_email = m
            st.session_state.biz_name = name if name else "משתמש"
            st.session_state.page = "dashboard"
            st.rerun()

    with t2:
        st.markdown("<br>", unsafe_allow_html=True)
        rm = st.text_input("אימייל", key="reg_m")
        rp = st.text_input("סיסמה", key="reg_p", type="password")
        rb = st.text_input("שם העסק", key="reg_b")
        if st.button("יצירת חשבון חדש"):
            if rm and rp and rb:
                requests.post(FORM_URL, data={"entry.855862094": rm, "entry.1847739029": f"Pass: {rp} | Biz: {rb}"})
                st.session_state.user_email = rm
                st.session_state.biz_name = rb
                st.session_state.page = "dashboard"
                st.rerun()

elif st.session_state.page == "dashboard":
    # פנייה מותאמת
    if st.session_state.user_email.lower() == MY_ADMIN_EMAIL.lower():
        welcome_header = "ברוכה הבאה מנכ\"לית. המערכות מוכנות."
    else:
        welcome_header = f"ברוכה השבה, {st.session_state.biz_name}"

    st.markdown(f"<div class='brand-title' style='font-size:30px;'>{welcome_header}</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("סוכן תוכן AI"): st.session_state.tool = "ai"
    with col2:
        if st.button("צ'אט שירות לקוחות"): st.session_state.tool = "chat"
    
    if st.session_state.get('tool') == "ai":
        st.markdown("<br>---<br>", unsafe_allow_html=True)
        topic = st.text_input("על מה נכתוב היום?")
        if st.button("ייצור תוכן"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"פוסט ל{st.session_state.biz_name}: {topic}"}])
            st.info(res.choices[0].message.content)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("התנתקות"):
        st.session_state.page = "auth"
        st.rerun()
