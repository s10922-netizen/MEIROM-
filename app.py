import streamlit as st
from groq import Groq
import requests

st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY")
    st.stop()

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
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
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- לוגיקה ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])
    
    with t1:
        e = st.text_input("מייל", key="l_e")
        p = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה 🚀"):
            if e == "admin@magic.com" and p == "1234":
                st.session_state.logged_in = True
                st.rerun()

    with t2:
        st.subheader("הרשמה")
        new_mail = st.text_input("מייל חדש", key="r_e")
        new_pass = st.text_input("סיסמה חדשה", type="password", key="r_p")
        
        if st.button("צרי חשבון ✨"):
            if new_mail and new_pass:
                # הכתובת הישירה לשליחה
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
                
                # המידע כפי שגוגל מצפה לקבל
                payload = {
                    "entry.855862094": new_mail,
                    "entry.1847739029": new_pass,
                    "draftResponse": "[]",
                    "pageHistory": "0"
                }
                
                try:
                    # שיטת POST פשוטה
                    response = requests.post(form_url, data=payload)
                    # גם אם גוגל מחזיר שגיאת תצוגה, המידע לרוב נכנס
                    st.balloons()
                    st.success("הבקשה נשלחה! בדקי את הגיליון החדש שפתחת.")
                except Exception as ex:
                    st.error(f"תקלה: {ex}")

else:
    st.sidebar.button("התנתקות", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
