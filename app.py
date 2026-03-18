import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. Apple-Zara Config ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"

# המייל הסודי של המנכ"לית
MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. THE ZARA VIBE (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Assistant:wght@200;300;400&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: center;
        background-color: #ffffff; color: #000000;
    }

    .zara-header {
        font-family: 'Playfair Display', serif;
        font-size: 50px; font-weight: 400;
        letter-spacing: 6px; text-transform: uppercase;
        margin-top: 50px; color: #000;
    }
    
    .zara-tagline {
        font-size: 13px; letter-spacing: 3px; color: #888;
        text-transform: uppercase; margin-bottom: 40px;
    }

    /* כפתור ZARA קלאסי */
    .stButton>button {
        background-color: #000000;
        color: #ffffff; border-radius: 0px; 
        height: 55px; font-size: 16px; font-weight: 300;
        width: 100%; border: none; letter-spacing: 2px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #222; }

    /* שדות טקסט נקיים (קו תחתון בלבד) */
    input {
        background-color: transparent !important;
        color: #000 !important;
        border: none !important;
        border-bottom: 1px solid #eee !important;
        border-radius: 0px !important;
        text-align: center !important;
        font-size: 18px !important;
    }
    input:focus { border-bottom: 1px solid #000 !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 40px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { font-size: 13px; letter-spacing: 1px; color: #aaa; }
    .stTabs [aria-selected="true"] { color: #000 !important; border-bottom: 1px solid #000 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה חכמה ---
def check_status(email):
    email_clean = str(email).strip().lower()
    if email_clean == MY_ADMIN_EMAIL.lower():
        return "ADMIN", "מנכ\"לית"
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        for _, row in df.iterrows():
            row_content = " ".join(row.astype(str)).lower()
            if email_clean in row_content:
                biz = str(row.iloc[-1]).split('|')[-1].replace('Biz:', '').strip()
                return "USER", biz
        return "NEW", None
    except: return "NEW", None

# --- 4. עמודים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

if st.session_state.page == "auth":
    st.markdown("<div class='zara-header'>MEIROM MAGIC</div>", unsafe_allow_html=True)
    st.markdown("<div class='zara-tagline'>Creative Agency & AI Systems</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["LOGIN", "REGISTER"])
    
    with t1:
        st.markdown("<br>", unsafe_allow_html=True)
        m = st.text_input("EMAIL", key="log_m").strip().lower()
        p = st.text_input("PASSWORD", key="log_p", type="password")
        if st.button("ENTER"):
            status, name = check_status(m)
            st.session_state.user_email = m
            st.session_state.biz_name = name if name else "NEW"
            st.session_state.status = status
            st.session_state.page = "dashboard"
            st.rerun()

    with t2:
        st.markdown("<br>", unsafe_allow_html=True)
        rm = st.text_input("EMAIL", key="reg_m")
        rp = st.text_input("PASSWORD", key="reg_p", type="password")
        rb = st.text_input("BUSINESS NAME", key="reg_b")
        if st.button("CREATE ACCOUNT"):
            requests.post(FORM_URL, data={"entry.855862094": rm, "entry.1847739029": f"Pass: {rp} | Biz: {rb}"})
            st.session_state.user_email = rm
            st.session_state.biz_name = rb
            st.session_state.status = "USER"
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "dashboard":
    # זיהוי פנייה אישית
    if st.session_state.user_email.lower() == MY_ADMIN_EMAIL.lower():
        header = "WELCOME ADMIN. SYSTEMS READY."
    else:
        # בדיקה אם המשתמש כבר היה פה או שהוא חדש (לפי ה-Session)
        header = f"WELCOME BACK, {st.session_state.biz_name.upper()}"
    
    st.markdown(f"<div class='zara-header' style='font-size:28px;'>{header}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("AI CONTENT"): st.session_state.tool = "ai"
    with col2:
        if st.button("CUSTOMER CHAT"): st.session_state.tool = "chat"
    
    if st.session_state.get('tool') == "ai":
        st.markdown("---")
        goal = st.text_input("TOPIC")
        if st.button("GENERATE"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Post for {st.session_state.biz_name}: {goal}"}])
            st.info(res.choices[0].message.content)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("LOGOUT"):
        st.session_state.page = "auth"
        st.rerun()
