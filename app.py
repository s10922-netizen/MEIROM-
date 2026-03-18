import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות דף ---
st.set_page_config(page_title="Magic OS", page_icon="🍏", layout="centered")

# הקישור הציבורי שלך מה-Publish to web
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key in Secrets!")
    st.stop()

# --- 2. עיצוב Apple Pro (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #ffffff; color: #1d1d1f;
    }

    /* אנימציית כניסה חלקה */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .stApp { animation: fadeIn 0.8s ease-out; }

    .apple-header {
        font-size: 48px; font-weight: 600; text-align: center;
        margin-top: 40px; color: #1d1d1f;
    }
    .apple-sub {
        font-size: 18px; color: #86868b; text-align: center; margin-bottom: 40px;
    }

    .apple-card {
        background: #ffffff; border-radius: 24px; padding: 30px;
        border: 1px solid #d2d2d7; box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #0071e3; color: white; border-radius: 12px;
        border: none; height: 52px; font-size: 17px; width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #0077ed; }

    .stTextInput>div>div>input {
        border-radius: 12px; border: 1px solid #d2d2d7;
        padding: 12px; background: #f5f5f7;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה לבדיקת משתמש ---
def check_user(email, password):
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        # ניקוי נתונים לבדיקה חסינה
        search_mail = str(email).strip().lower()
        search_pass = str(password).strip().lower()
        
        for _, row in df.iterrows():
            row_str = " ".join(row.astype(str)).lower()
            if search_mail in row_str and search_pass in row_str:
                return True
        return False
    except: return False

# --- 4. ניהול מצבים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- 5. זרימת האתר ---

# דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='apple-header'>Magic OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='apple-sub'>ניהול חכם לעסק שלך.</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["כניסה", "הרשמה"])
    
    with t1:
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        l_mail = st.text_input("אימייל", key="lin_m").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="lin_p").strip().lower()
        if st.button("התחברות 🚀"):
            if check_user(l_mail, l_pass):
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("המייל או הסיסמה לא נמצאו בטבלה. וודאי שנרשמת.")
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        r_mail = st.text_input("מייל חדש", key="rin_m")
        r_pass = st.text_input("סיסמה", type="password", key="rin_p")
        if st.button("המשך להקמת העסק ✨"):
            if r_mail and r_pass:
                st.session_state.temp_m, st.session_state.temp_p = r_mail, r_pass
                st.session_state.page = "onboarding"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# דף אונבורדינג
elif st.session_state.page == "onboarding":
    st.markdown("<div class='apple-header'>פרטי העסק</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
        b_name = st.text_input("שם המותג")
        b_desc = st.text_area("מה העסק עושה?")
        if st.button("שמור וכנס למערכת"):
            st.session_state.biz_data = {"name": b_name, "desc": b_desc}
            # שליחה לגוגל
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            data = {"entry.855862094": st.session_state.temp_m, "entry.1847739029": f"Pass: {st.session_state.temp_p} | Biz: {b_name}"}
            requests.post(url, data=data)
            st.session_state.user_email = st.session_state.temp_m
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# מרכז הבקרה (Dashboard)
elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='apple-header' style='font-size:28px;'>שלום, {st.session_state.user_email.split('@')[0]}</div>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.write("### תפריט ניהול")
        menu = st.radio("", ["🏠 דף הבית", "✍️ סוכן תוכן", "💬 צ'אט שירות"])
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
    if menu == "🏠 דף הבית":
        st.write("כל המערכות פועלות. ה-AI מסונכרן לעסק שלך.")
        
    elif menu == "✍️ סוכן תוכן":
        goal = st.text_input("מה נכתוב היום?")
        if st.button("צור פוסט"):
            biz = st.session_state.biz_data
            prompt = f"כתוב פוסט לעסק בשם {biz.get('name', 'שלי')} שעושה {biz.get('desc', 'דברים מדהימים')}. מטרה: {goal}"
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.info(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        q = st.chat_input("שאלת לקוח...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"ענה רק על שאלות מקצועיות."}, {"role":"user","content":q}])
            st.markdown(f"<div style='background:#f5f5f7; padding:15px; border-radius:15px;'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
