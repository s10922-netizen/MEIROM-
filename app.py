import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"

MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. ZARA MINIMALIST DESIGN (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Assistant:wght@200;300;400&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: center;
        background-color: #ffffff; color: #000000;
    }

    /* כותרת בסגנון זרה - Serif יוקרתי */
    .zara-title {
        font-family: 'Playfair Display', serif;
        font-size: 55px; font-weight: 400;
        letter-spacing: 5px; text-transform: uppercase;
        margin-top: 60px; margin-bottom: 5px;
        color: #000;
    }
    
    .zara-sub {
        font-size: 14px; letter-spacing: 2px; color: #666;
        text-transform: uppercase; margin-bottom: 50px;
    }

    /* כפתורי ZARA - שחור נקי */
    .stButton>button {
        background-color: #000000;
        color: #ffffff; border-radius: 0px; /* פינות חדות זה זרה */
        height: 50px; font-size: 15px; font-weight: 300;
        width: 100%; border: none; letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #333333; color: #fff;
    }

    /* שדות קלט - קו תחתון נקי */
    input {
        background-color: transparent !important;
        color: #000 !important;
        border: none !important;
        border-bottom: 1px solid #ccc !important;
        border-radius: 0px !important;
        text-align: center !important;
        font-size: 18px !important;
        padding: 10px 0 !important;
    }
    input:focus { border-bottom: 1px solid #000 !important; }

    /* הסתרת אלמנטים מיותרים */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; justify-content: center; border-bottom: none; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; letter-spacing: 1px; color: #999; }
    .stTabs [aria-selected="true"] { color: #000 !important; border-bottom: 1px solid #000 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. פונקציות לוגיקה ---
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

# --- 4. ניווט דפים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

if st.session_state.page == "auth":
    st.markdown("<div class='zara-title'>ZARA</div>", unsafe_allow_html=True) # רק לצורך העיצוב, תשני ל-MEIROM
    st.markdown("<div class='zara-sub'>Management & Magic</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["LOGIN", "REGISTER"])
    
    with t1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        l_mail = st.text_input("EMAIL", key="z_mail").strip().lower()
        l_pass = st.text_input("PASSWORD", key="z_pass", type="password")
        if st.button("ENTER"):
            status, name = get_user_status(l_mail)
            if status != "NEW" or l_mail == MY_ADMIN_EMAIL:
                st.session_state.user_email = l_mail
                st.session_state.biz_name = name if name else "ADMIN"
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("User not found.")

    with t2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        r_mail = st.text_input("NEW EMAIL", key="rz_mail")
        r_pass = st.text_input("NEW PASSWORD", key="rz_pass", type="password")
        r_biz = st.text_input("BUSINESS NAME", key="rz_biz")
        if st.button("CREATE ACCOUNT"):
            if register_user(r_mail, r_pass, r_biz):
                st.session_state.user_email = r_mail
                st.session_state.biz_name = r_biz
                st.session_state.page = "dashboard"
                st.rerun()

elif st.session_state.page == "dashboard":
    # פנייה אלגנטית
    if st.session_state.user_email == MY_ADMIN_EMAIL:
        welcome = "WELCOME ADMIN. SYSTEMS ONLINE."
    else:
        welcome = f"WELCOME, {st.session_state.biz_name.upper()}"

    st.markdown(f"<div class='zara-title' style='font-size:30px;'>{welcome}</div>", unsafe_allow_html=True)
    
    if st.session_state.tool == "home":
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("AI CONTENT AGENT"): st.session_state.tool = "ai"; st.rerun()
        if st.button("CUSTOMER CHAT"): st.session_state.tool = "chat"; st.rerun()
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("LOGOUT"): st.session_state.page = "auth"; st.rerun()
    
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.session_state.tool == "ai":
            topic = st.text_input("TOPIC")
            if st.button("GENERATE"):
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Post for {st.session_state.biz_name}: {topic}"}])
                st.info(res.choices[0].message.content)
        
        elif st.session_state.tool == "chat":
            q = st.chat_input("MESSAGE...")
            if q:
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":f"Support for {st.session_state.biz_name}"},{"role":"user","content":q}])
                st.write(res.choices[0].message.content)

        if st.button("BACK TO MENU"): st.session_state.tool = "home"; st.rerun()
