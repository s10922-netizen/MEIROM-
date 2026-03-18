import streamlit as st
from groq import Groq
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור מאובטח ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets!")
    st.stop()

# --- בדיקת לקוח חיצוני ---
query_params = st.query_params
is_customer_view = query_params.get("view") == "customer"

# --- זיכרון זמני (הבעיה שציינת) ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"} # המשתמש היחיד שנשמר כרגע
if 'biz_info' not in st.session_state:
    st.session_state.biz_info = "ברוכים הבאים לעסק שלנו!"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'plan' not in st.session_state: st.session_state.plan = None

# --- ✨ עיצוב CSS ---
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
        font-size: 60px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- 🌐 תצוגת לקוח (בלי התחברות) ---
if is_customer_view:
    st.markdown("<div class='magic-title'>ברוכים הבאים</div>", unsafe_allow_html=True)
    st.write(st.session_state.biz_info)
    # כאן הצ'אטבוט והיומן... (השארתי מקום)
    st.stop()

# --- 🔑 מערכת ניהול (התחברות והרשמה) ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה חדשה"])
    
    with tab1:
        email = st.text_input("אימייל", key="login_email")
        password = st.text_input("סיסמה", type="password", key="login_pass")
        if st.button("כניסה 🚀", key="login_btn"):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("מייל או סיסמה לא נכונים")
            
    with tab2:
        new_email = st.text_input("מייל להרשמה", key="reg_email")
        new_pass = st.text_input("סיסמה", type="password", key="reg_pass")
        if st.button("צרי חשבון ✨", key="reg_btn"):
            st.session_state.users[new_email] = new_pass
            st.success(f"חשבון עבור {new_email} נוצר! עברי ללשונית התחברות.")

# --- 👑 דף הניהול (אחרי התחברות) ---
elif st.session_state.plan is None:
    st.header("בחרי מסלול")
    if st.button("Enterprise (2500₪)"): st.session_state.plan = "Enterprise"; st.rerun()

else:
    with st.sidebar:
        st.write(f"מנכ\"לית: {st.session_state.plan}")
        page = st.radio("ניווט:", ["✨ דף הבית", "🏢 הגדרות עסק", "🔗 קישור ללקוחות"])
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    
    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות עסק")
        st.session_state.biz_info = st.text_area("פרטי העסק:", value=st.session_state.biz_info)
        st.button("שמור ✅")

    elif page == "🔗 קישור ללקוחות":
        st.header("הקישור שלך 🌐")
        # פה אנחנו יוצרים את הלינק
        st.code("https://YOUR-APP.streamlit.app/?view=customer")
