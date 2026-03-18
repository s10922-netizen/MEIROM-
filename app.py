import streamlit as st
from groq import Groq
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור מאובטח ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("חסר מפתח API ב-Secrets!")
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
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    with tab1:
        l_email = st.text_input("אימייל", key="login_user")
        l_pass = st.text_input("סיסמה", type="password", key="login_password")
        if st.button("כניסה 🚀", key="btn_login"):
            if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")
    with tab2:
        s_email = st.text_input("מייל להרשמה", key="reg_user")
        s_pass = st.text_input("סיסמה חדשה", type="password", key="reg_password")
        if st.button("צרי חשבון 🧚‍♀️", key="btn_reg"):
            st.session_state.users[s_email] = s_pass
            st.success("נרשמת!")

elif st.session_state.plan is None:
    st.markdown("<h2 style='text-align:center;'>בחרי מסלול ✨</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("Basic (250₪)", key="p1"): st.session_state.plan = "Basic"; st.rerun()
    if c2.button("Pro (750₪)", key="p2"): st.session_state.plan = "Pro"; st.rerun()
    if c3.button("Enterprise (2500₪)", key="p3"): st.session_state.plan = "Enterprise"; st.rerun()

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
            menu.append("🌐 תצוגת לקוח")
        page = st.radio("ניווט:", menu)

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)

    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק")
        biz = st.text_input("שם העסק")
        task = st.text_area("מה לכתוב?")
        if st.button("הפעל קסם ⚡"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Write marketing for {biz}: {task} in Hebrew"}])
            st.write(res.choices[0].message.content)

    elif page == "📅 קביעת פגישות":
        st.header("סוכן יומן 📅")
        d = st.date_input("תאריך")
        t = st.time_input("שעה")
        if st.button("צור אישור"):
            st.success(f"נקבע ל-{d} ב-{t}")

    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות עסק")
        st.session_state.biz_info = st.text_area("מידע על העסק:", value=st.session_state.biz_info)
        st.button("שמור ✅")

    elif page == "🤖 צ'אטבוט לקוחות" or page == "🌐 תצוגת לקוח":
        st.header("🤖 הצ'אטבוט של העסק")
        if not st.session_state.biz_info:
            st.warning("הזינו מידע בהגדרות עסק!")
        else:
            u_msg = st.chat_input("שאל/י משהו...")
            if u_msg:
                st.chat_message("user").write(u_msg)
                r = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Biz info: {st.session_state.biz_info}. User: {u_msg}. Hebrew."}])
                st.chat_message("assistant").write(r.choices[0].message.content)
