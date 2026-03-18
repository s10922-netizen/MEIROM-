import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS Elite", page_icon="⚡", layout="centered")

# הקישור הציבורי שלך
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב CYBER-NEON (מגניב רצח) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;700&family=Orbitron:wght@700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #050505; color: #e0e0e0;
    }

    /* כותרת ניאון מטורפת */
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px; text-align: center;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(79, 172, 254, 0.5);
        margin-bottom: 30px;
    }

    /* כרטיסיות כהות עם מסגרת זוהרת */
    .cyber-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #333;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.7);
        margin-bottom: 20px;
    }

    /* כפתורי ניאון סגול-כחול */
    .stButton>button {
        background: linear-gradient(45deg, #6366f1, #a855f7);
        color: white; border-radius: 15px; border: none;
        height: 55px; font-size: 19px; font-weight: 700; width: 100%;
        transition: 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6);
    }

    /* שדות קלט בסגנון הייטק */
    input {
        background-color: #1a1a1a !important;
        color: #00f2fe !important;
        border: 1px solid #444 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקת בדיקה חסינה (הפתרון לבעיית הטבלה) ---
def verify_user(email, password):
    try:
        # עוקף Cache כדי לקבל מידע טרי
        url = f"{SHEET_CSV_URL}&refresh={time.time()}"
        df = pd.read_csv(url)
        
        # אנחנו הופכים את כל הטבלה לשורות של טקסט פשוט
        # ככה לא משנה באיזו עמודה המייל, אנחנו נמצא אותו
        search_m = str(email).strip().lower()
        search_p = str(password).strip().lower()
        
        for index, row in df.iterrows():
            # מחברים את כל התאים בשורה לטקסט אחד
            row_text = " ".join(row.astype(str)).lower()
            if search_m in row_text and search_p in row_text:
                return True
        return False
    except Exception as e:
        return False

# --- 4. זרימת האתר ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

if st.session_state.page == "auth":
    st.markdown("<div class='cyber-title'>MAGIC OS</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⚡ כניסה", "💎 הרשמה"])
    
    with tab1:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        l_mail = st.text_input("מייל משתמש", key="l_m").strip()
        l_pass = st.text_input("סיסמה", type="password", key="l_p").strip()
        if st.button("שיגור למערכת 🚀"):
            if verify_user(l_mail, l_pass):
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("גישה נדחתה: המשתמש לא נמצא בטבלה או שהפרטים שגויים.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        r_mail = st.text_input("מייל חדש", key="r_m")
        r_pass = st.text_input("סיסמה", type="password", key="r_p")
        if st.button("התחלת תהליך ✨"):
            st.session_state.temp_m, st.session_state.temp_p = r_mail, r_pass
            st.session_state.page = "onboarding"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "onboarding":
    st.markdown("<div class='cyber-title'>הגדרת עסק</div>", unsafe_allow_html=True)
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    b_name = st.text_input("שם העסק")
    b_desc = st.text_area("תיאור העסק ל-AI")
    if st.button("סיום ויצירת חשבון"):
        url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
        requests.post(url, data={"entry.855862094": st.session_state.temp_m, "entry.1847739029": f"Pass: {st.session_state.temp_p} | Biz: {b_name}"})
        st.session_state.user_email = st.session_state.temp_m
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='cyber-title' style='font-size:30px;'>WELCOME, {st.session_state.user_email}</div>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### ניווט מהיר")
        menu = st.radio("", ["🏠 דף הבית", "🤖 סוכן AI", "💬 צ'אט שירות"])
        if st.button("ניתוק קשר"):
            st.session_state.page = "auth"
            st.rerun()

    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    if menu == "🏠 דף הבית":
        st.write("מנכ\"לית, כל המערכות פועלות כשורה.")
        
    elif menu == "🤖 סוכן AI":
        task = st.text_input("מה המשימה?")
        if st.button("הפעל סוכן"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט על: {task}"}])
            st.info(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        q = st.chat_input("דברי איתי...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"אתה סוכן AI מגניב."}, {"role":"user","content":q}])
            st.write(res.choices[0].message.content)
    st.markdown("</div>", unsafe_allow_html=True)
