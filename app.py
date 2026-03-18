import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. Apple-Style Page Config ---
st.set_page_config(page_title="Magic OS", page_icon="🍏", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. THE APPLE DESIGN (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #ffffff; color: #1d1d1f;
    }

    /* Glass Card Effect */
    .apple-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 30px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.04);
        margin-bottom: 25px;
    }

    /* Typography */
    .hero-text {
        font-size: 42px; font-weight: 600; text-align: center;
        background: linear-gradient(180deg, #1d1d1f 0%, #434344 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* Premium Buttons */
    .stButton>button {
        background-color: #0071e3;
        color: white; border-radius: 50px; border: none;
        height: 52px; font-size: 17px; font-weight: 400;
        width: 100%; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0077ed; transform: scale(1.02);
    }

    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 12px; border: 1px solid #d2d2d7;
        padding: 15px; background: #f5f5f7;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Core Functions ---
def check_user_exists(email):
    try:
        url = f"{SHEET_CSV_URL}&t={pd.Timestamp.now().timestamp()}"
        df = pd.read_csv(url)
        # חיפוש חסין בכל התאים בטבלה
        search_email = str(email).strip().lower()
        for row in df.values:
            if any(search_email == str(cell).strip().lower() for cell in row):
                return True
        return False
    except: return False

def save_to_google(email, data):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    info = " | ".join([f"{k}: {v}" for k, v in data.items()])
    requests.post(url, data={"entry.855862094": email, "entry.1847739029": info})

# --- 4. Navigation Logic ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

# דף כניסה/הרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='hero-text'>Magic OS</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#86868b;'>העתיד של העסק שלך מתחיל כאן.</p>", unsafe_allow_html=True)
    
    tab_in, tab_up = st.tabs(["כניסה", "הרשמה"])
    
    with tab_in:
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        login_mail = st.text_input("אימייל", key="li_m").strip().lower()
        if st.button("התחבר"):
            if check_user_exists(login_mail):
                st.session_state.user_email = login_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("לא מצאנו את החשבון שלך. ודאי שנרשמת.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_up:
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        reg_mail = st.text_input("מייל לעסק", key="re_m")
        reg_pass = st.text_input("סיסמה", type="password", key="re_p")
        if st.button("צור חשבון"):
            st.session_state.temp_mail, st.session_state.temp_pass = reg_mail, reg_pass
            st.session_state.page = "onboarding"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# דף הגדרת עסק
elif st.session_state.page == "onboarding":
    st.markdown("<div class='hero-text'>הגדרת עסק</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        b_name = st.text_input("שם המותג")
        b_desc = st.text_area("תיאור העסק עבור ה-AI")
        if st.button("שמור והמשך"):
            st.session_state.biz_data = {"name": b_name, "desc": b_desc}
            st.session_state.page = "packages"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# דף חבילות
elif st.session_state.page == "packages":
    st.markdown("<div class='hero-text'>בחירת מסלול</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='apple-card' style='text-align:center;'><h3>VIP</h3><p>AI ללא הגבלה</p><h2>₪199</h2></div>", unsafe_allow_html=True)
        if st.button("בחרתי VIP"):
            save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "VIP", "pass": st.session_state.temp_pass})
            st.session_state.user_email = st.session_state.temp_mail
            st.session_state.page = "dashboard"
            st.rerun()

# מרכז הבקרה
elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='hero-text' style='font-size:30px;'>שלום, {st.session_state.user_email.split('@')[0]}</div>", unsafe_allow_html=True)
    
    option = st.selectbox("", ["🏠 דף הבית", "✍️ סוכן תוכן AI", "💬 צ'אט שירות"])
    
    st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
    if option == "🏠 דף הבית":
        st.write("כל המערכות פועלות. ה-AI שלך מוכן לפקודה.")
        if st.button("התנתק"):
            st.session_state.page = "auth"
            st.rerun()
            
    elif option == "✍️ סוכן תוכן AI":
        goal = st.text_input("מה נכתוב היום?")
        if st.button("ייצור פוסט ✨"):
            biz = st.session_state.get('biz_data', {})
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"אתה מומחה שיווק. כתוב פוסט לעסק {biz.get('name')} (תיאור: {biz.get('desc')}). מטרה: {goal}."}])
            st.info(res.choices[0].message.content)

    elif option == "💬 צ'אט שירות":
        q = st.chat_input("שאלת לקוח...")
        if q:
            biz = st.session_state.get('biz_data', {})
            sys_msg = f"אתה נציג שירות של {biz.get('name')}. ענה רק על שאלות מקצועיות."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":sys_msg}, {"role":"user","content":q}])
            st.markdown(f"<div style='background:#f5f5f7; padding:15px; border-radius:15px;'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
