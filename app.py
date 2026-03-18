import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. Apple-Style Config ---
st.set_page_config(page_title="Magic OS", page_icon="🍏", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. THE PURE APPLE CSS (Animations & Design) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #ffffff; color: #1d1d1f;
    }

    /* Smooth Fade-in Animation */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .stApp { animation: fadeIn 0.8s ease-out; }

    /* Header Apple Style */
    .apple-header {
        font-size: 48px; font-weight: 600; text-align: center;
        margin-top: 60px; margin-bottom: 5px; color: #1d1d1f;
    }
    .apple-sub {
        font-size: 20px; color: #86868b; text-align: center; margin-bottom: 50px; font-weight: 300;
    }

    /* Ultra-Clean Cards */
    .apple-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 40px;
        border: 1px solid #d2d2d7;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 30px;
    }

    /* Apple Blue Button */
    .stButton>button {
        background-color: #0071e3;
        color: white; border-radius: 14px; border: none;
        height: 54px; font-size: 18px; font-weight: 400; width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #0077ed; box-shadow: 0 4px 15px rgba(0,113,227,0.3); }

    /* Clean Inputs */
    .stTextInput>div>div>input {
        border-radius: 12px; border: 1px solid #d2d2d7;
        padding: 15px; background: #f5f5f7; font-size: 16px;
    }

    /* Tabs UI */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { color: #86868b; font-size: 18px; }
    .stTabs [aria-selected="true"] { color: #0071e3 !important; border-bottom-color: #0071e3 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
def get_verified_data():
    try:
        # עוקף Cache כדי לקבל נתונים טריים
        url = f"{SHEET_CSV_URL}&nocache={time.time()}"
        df = pd.read_csv(url)
        # ניקוי יסודי של כל תא בטבלה
        return df.astype(str).apply(lambda x: x.str.strip().str.lower())
    except:
        return pd.DataFrame()

# --- 4. APP FLOW ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

# --- A. AUTHENTICATION PAGE ---
if st.session_state.page == "auth":
    st.markdown("<div class='apple-header'>Magic OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='apple-sub'>Designed for Management.</div>", unsafe_allow_html=True)
    
    tab_in, tab_up = st.tabs(["כניסה", "הרשמה"])
    
    with tab_in:
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        login_mail = st.text_input("אימייל", key="li_mail").strip().lower()
        login_pass = st.text_input("סיסמה", type="password", key="li_pass")
        
        if st.button("התחברות"):
            with st.spinner("Checking..."):
                df = get_verified_data()
                if not df.empty:
                    # מחפש שורה שבה גם המייל וגם הסיסמה מופיעים (בדיקה חסינה)
                    all_rows_str = df.apply(lambda row: " ".join(row.values), axis=1)
                    found = all_rows_str.str.contains(login_mail) & all_rows_str.str.contains(login_pass.lower())
                    
                    if found.any():
                        st.session_state.user_email = login_mail
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("פרטי כניסה שגויים או שהחשבון טרם אושר.")
                else:
                    st.error("חיבור לשרת נכשל.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_up:
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        reg_mail = st.text_input("מייל לעסק", key="re_mail")
        reg_pass = st.text_input("סיסמה חדשה", type="password", key="re_pass")
        if st.button("התחלת הקמה ✨"):
            st.session_state.temp_m, st.session_state.temp_p = reg_mail, reg_pass
            st.session_state.page = "onboarding"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- B. ONBOARDING PAGE ---
elif st.session_state.page == "onboarding":
    st.markdown("<div class='apple-header'>Business Setup</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        b_name = st.text_input("שם המותג")
        b_desc = st.text_area("מה העסק עושה?")
        if st.button("שמור והמשך"):
            # שליחה לטבלה
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            requests.post(url, data={"entry.855862094": st.session_state.temp_m, "entry.1847739029": f"Password: {st.session_state.temp_p} | Name: {b_name} | Desc: {b_desc}"})
            st.session_state.user_email = st.session_state.temp_m
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- C. DASHBOARD PAGE ---
elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='apple-header' style='font-size:32px;'>Welcome, {st.session_state.user_email.split('@')[0]}</div>", unsafe_allow_html=True)
    
    # תפריט נקי בתוך קארד
    st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
    menu = st.selectbox("תפריט ניהול", ["🏠 לוח בקרה", "✍️ סוכן תוכן AI", "💬 צ'אט שירות"])
    
    if menu == "🏠 לוח בקרה":
        st.write("כל המערכות פועלות. ה-AI מסונכרן לעסק שלך.")
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()
            
    elif menu == "✍️ סוכן תוכן AI":
        goal = st.text_input("מה נכתוב היום?")
        if st.button("ייצור פוסט ✨"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט שיווקי: {goal}"}])
            st.info(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        q = st.chat_input("שאלת לקוח...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"ענה רק על שאלות מקצועיות."}, {"role":"user","content":q}])
            st.markdown(f"<div style='background:#f5f5f7; padding:20px; border-radius:18px;'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
