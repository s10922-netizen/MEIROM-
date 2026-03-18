import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות דף ---
st.set_page_config(page_title="Meirom Magic OS", page_icon="✨", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. THE MAGIC APPLE DESIGN (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        color: #1d1d1f;
    }

    /* אנימציית הופעה חלקה */
    @keyframes fadeIn { 
        from { opacity: 0; transform: translateY(20px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    .stApp { animation: fadeIn 1s ease-out; }

    /* כותרת יוקרתית */
    .magic-header {
        font-size: 50px; font-weight: 600; text-align: center;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 40px; margin-bottom: 5px;
    }
    .magic-sub {
        font-size: 18px; color: #86868b; text-align: center; margin-bottom: 40px;
    }

    /* כרטיסיות 'זכוכית' (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* כפתורי קסם */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white; border-radius: 50px; border: none;
        height: 55px; font-size: 18px; font-weight: 600; width: 100%;
        transition: all 0.3s ease; box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 15px 25px rgba(168, 85, 247, 0.4);
    }

    /* עיצוב שדות קלט */
    .stTextInput>div>div>input {
        border-radius: 15px; border: 1px solid #d2d2d7;
        padding: 15px; background: #f5f5f7; transition: 0.3s;
    }
    .stTextInput>div>div>input:focus { border-color: #a855f7; box-shadow: 0 0 10px rgba(168, 85, 247, 0.2); }

    /* טאבים נקיים */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: 400; }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה חסינה (בדיקת משתמש) ---
def verify_user(email, password):
    try:
        url = f"{SHEET_CSV_URL}&nocache={time.time()}"
        df = pd.read_csv(url)
        # ניקוי נתונים
        df_clean = df.astype(str).apply(lambda x: x.str.strip().str.lower())
        # מחפש שורה שבה המייל והסיסמה מופיעים יחד
        for _, row in df_clean.iterrows():
            row_content = " ".join(row.values)
            if email.lower() in row_content and password.lower() in row_content:
                return True
        return False
    except: return False

# --- 4. זרימת האתר ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

# --- א. דף כניסה מעוצב ---
if st.session_state.page == "auth":
    st.markdown("<div class='magic-header'>Meirom Magic OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='magic-sub'>המערכת החכמה לניהול העסק שלך</div>", unsafe_allow_html=True)
    
    t_in, t_up = st.tabs(["🔒 כניסה מהירה", "✨ הצטרפות לנבחרת"])
    
    with t_in:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        l_mail = st.text_input("אימייל", key="l_m").strip()
        l_pass = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("בואי נתחיל 🚀"):
            if verify_user(l_mail, l_pass):
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("אופס! המייל או הסיסמה לא תואמים. נסי שוב.")
        st.markdown("</div>", unsafe_allow_html=True)

    with t_up:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("עדיין לא רשומה? בואי נקים לך אימפריה!")
        r_m = st.text_input("מייל לעסק", key="r_m")
        r_p = st.text_input("בחרי סיסמה", type="password", key="r_p")
        if st.button("התחלת הקמה ✨"):
            st.session_state.temp_m, st.session_state.temp_p = r_m, r_p
            st.session_state.page = "onboarding"
            st.rerun()
        st.markdown("</div>", unsafe
