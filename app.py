import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור מאובטח ל-AI ---
# הקוד מושך את המפתח מה-Secrets שהגדרת ב-Streamlit Cloud
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("שגיאת אבטחה: מפתח ה-API לא נמצא ב-Secrets. וודאי שהגדרת GROQ_API_KEY ב-Streamlit Cloud.")
    st.stop()

# --- זיכרון המערכת ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'biz_info' not in st.session_state:
    st.session_state.biz_info = ""

# --- עיצוב CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- לוגיקת דפים ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    with tab_login:
        l_email = st.text_input("אימייל", key="l_email_unique")
        l_pass = st.text_input("סיסמה", type="password", key="l_pass_unique")
        if st.button("כניסה 🚀", use_container_width=True):
            if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")
    with tab_signup:
        s_email = st.text_input("מייל להרשמה", key="s_email_unique")
        s_pass = st.text_input("סיסמה חדשה", type="password", key="s_pass_unique")
        if st.button("צרי חשבון 🧚‍♀️", use_container_width=True):
            st.session_state.users[s_email] = s_pass
            st.success("נרשמת! עברי להתחברות.")

elif st.session_state.plan is None:
    st.markdown("<h2 style='text-align:center;'>בחרי מסלול ✨</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("Basic (250₪)"): st.session_state.plan = "Basic"; st.rerun()
    if c2.button("Pro (750₪)"): st.session_state.plan = "Pro"; st.rerun()
    if c3.button("Enterprise (2500₪)"): st.session_state.plan = "Enterprise"; st.rerun()

else:
    with st.sidebar:
        st.markdown(f"### מנכ\"לית מיי 👑\n**חבילה:** {st.session_state.plan}")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.session_state.plan = None
            st.rerun()
        st.divider()
        menu = ["✨ דף הבית", "🚀 סוכן שיווק", "📅 קביעת פגישות"]
        if st.session_state.plan == "Enterprise":
            menu.append("🏢 הגדרות עסק")
            menu.append("🤖 צ'אטבוט לקוחות")
        page = st.radio("ניווט:", menu)

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write("ברוכה הבאה לאימפריית האוטומציה שלך!")

    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות ה'אתר' של העסק 🏢")
        biz_details = st.text_area("מידע על העסק:", value=st.session_state.biz_info)
        if st.button("שמור הגדרות 💾"):
            st.session_state.biz_info = biz_details
            st.success("נשמר!")

    elif page == "🤖 צ'אטבוט לקוחות":
        st.header("🤖 צ'אטבוט לקוחות")
        if not st.session_state.biz_info:
            st.warning("נא להזין פרטי עסק בהגדרות!")
        else:
            user_msg = st.chat_input("איך אפשר לעזור?")
            if user_msg:
                st.chat_message("user").write(user_msg)
                prompt = f"Assistant for: {st.session_state.biz_info}. Answer: {user_msg}. Hebrew."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                st.chat_message("assistant").write(res.choices[0].message.content)

    # (שאר הסוכנים נשארים כרגיל)
