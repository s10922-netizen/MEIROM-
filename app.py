import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except Exception as e:
    st.error("Missing API Key in Secrets!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'report' not in st.session_state:
    st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה מתקדם ---
st.set_page_config(page_title="Meirom AI | Operational", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .app-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 20px; }
    
    /* מסוף מבצעי - מראה של האקרים */
    .console {
        background: #0d1117; color: #00ff00; font-family: 'Courier New', monospace;
        padding: 15px; border-radius: 10px; font-size: 0.85rem; line-height: 1.4;
        border-left: 4px solid #6366f1; margin: 10px 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7) !important;
        color: white !important; border-radius: 12px !important; font-weight: bold !important;
        width: 100% !important; height: 3.5em !important;
    }
</style>
""", unsafe_allow_html=True)

# --- עמוד 1: פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 40px; text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color:#6366f1;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=160)
    st.write("מערכת אוטונומית לביצוע פקודות והטמעה בעסק")
    if st.button("כניסה למסוף הביצוע 🚀"):
        go_to('main')
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- עמוד 2: מסוף הביצוע ---
elif st.session_state.page == 'main':
    st.markdown("<h2 style='text-align:center;'>מרכז שליטה מבצעי</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("🔗 חיבור תשתיות פעילות")
    c1, c2, c3 = st.columns(3)
    with c1: ws_active = st.checkbox("WhatsApp API")
    with c2: cal_active = st.checkbox("Google Calendar")
    with c3: mail_active = st.checkbox("Automated Email")
    st.markdown("</div>", unsafe_allow_html=True)

    with st.form("action_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לשליחת דו''ח ביצוע")
        mission = st.text_area("מה המשימה לביצוע? (למשל: 'שלח הודעת תודה לכל לקוח חדש')")
        submit = st.form_submit_button("הפעל סוכן מבצע ⚡")

        if submit and biz_name and mission:
            with st.status("סוכן Meirom AI מבצע הטמעה...", expanded=True) as status:
                st.markdown("<div class='
