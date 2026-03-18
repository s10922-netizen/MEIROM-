import streamlit as st
from groq import Groq
import urllib.parse

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# --- זיכרון משתמשים (Database זמני) ---
if 'users' not in st.session_state:
    # משתמש מנהל כברירת מחדל
    st.session_state.users = {"admin@magic.com": "1234"}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- עיצוב (CSS) ---
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

# --- דף כניסה והרשמה ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    
    # טאבים לבחירה בין התחברות להרשמה
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה חדשה"])
    
    with tab1:
        login_email = st.text_input("אימייל", key="l_email")
        login_password = st.text_input("סיסמה", type="password", key="l_pass")
        if st.button("כניסה 🚀"):
            if login_email in st.session_state.users and st.session_state.users[login_email] == login_password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("מייל או סיסמה לא נכונים")

    with tab2:
        new_email = st.text_input("מייל להרשמה", key="r_email")
        new_password = st.text_input("בחרי סיסמה", type="password", key="r_pass")
        confirm_password = st.text_input("אימות סיסמה", type="password", key="r_confirm")
        
        if st.button("צור חשבון 🧚‍♀️"):
            if new_email in st.session_state.users:
                st.warning("המייל הזה כבר רשום במערכת!")
            elif new_password != confirm_password:
                st.error("הסיסמאות לא תואמות!")
            elif len(new_password) < 4:
                st.error("הסיסמה חייבת להיות לפחות 4 תווים")
            else:
                # כאן הקסם קורה: האתר רושם את המשתמש לבד!
                st.session_state.users[new_email] = new_password
                st.success("נרשמת בהצלחה! עברי ללשונית התחברות.")

# --- תוכן האפליקציה (אחרי התחברות) ---
else:
    with st.sidebar:
        st.markdown("### מחוברת בהצלחה! 👑")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.rerun()
    st.write("### ברוכה הבאה לסביבת העבודה שלך!")
    # כאן יבוא שאר הקוד של הסוכנים...
