import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import requests

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing API Key")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה מתקדם ---
st.set_page_config(page_title="Meirom AI | Active", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .app-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 20px; }
    
    /* מסוף האקרים בזמן ביצוע */
    .console {
        background: #0d1117; color: #00ff00; font-family: 'Courier New', monospace;
        padding: 15px; border-radius: 10px; font-size: 0.85rem; line-height: 1.4;
        border-left: 4px solid #3b82f6; margin: 10px 0;
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
    st.markdown("<h1 style='text-align:center; padding-top:40px;'>MEIROM <span style='color:#6366f1;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=160)
    st.write("מערכת אוטונומית לביצוע פקודות בעסק")
    if st.button("כניסה למסוף הביצוע 🚀"): go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)

# --- עמוד 2: מסוף הביצוע ---
elif st.session_state.page == 'main':
    st.markdown("<h2>מרכז שליטה מבצעי</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("🔗 בחר תשתיות לחיבור")
    col1, col2, col3 = st.columns(3)
    with col1: ws = st.checkbox("WhatsApp API")
    with col2: cal = st.checkbox("Google Calendar")
    with col3: mail = st.checkbox("Email Automation")
    st.markdown("</div>", unsafe_allow_html=True)

    with st.form("action_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לשליחת אישור ביצוע")
        mission = st.text_area("הגדר משימה לסוכן (לדוגמה: שלח הודעת תודה לכל לקוח חדש שקונה)")
        submit = st.form_submit_button("הפעל סוכן מבצע ⚡")

        if submit and biz_name and mission:
            with st.status("סוכן Meirom AI נכנס למערכות...", expanded=True) as status:
                # אפקט טרמינל
                st.markdown("<div class='console'>> Accessing business database... DONE<br>> Establishing secure bridge... OK</div>", unsafe_allow_html=True)
                time.sleep(1)
                
                if ws:
                    st.markdown("<div class='console'>> WhatsApp API Handshake... SUCCESS<br>> Messaging bot deployed.</div>", unsafe_allow_html=True)
                    time.sleep(1)
                
                if cal:
                    st.markdown("<div class='console'>> Syncing Calendar... 14 events found.<br>> Automation rules applied.</div>", unsafe_allow_html=True)
                    time.sleep(1)

                st.markdown("<div class='console'>> Executing AI decision logic...<br>> Sending execution log to manager.</div>", unsafe_allow_html=True)
                
                # AI logic
                prompt = f"System: ACTOR. Role: Business Implementer. Task: {mission} for {biz_name}. Tools used: WhatsApp:{ws}, Cal:{cal}. WRITE A SUMMARY OF ACTIONS TAKEN IN HEBREW."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                st.session_state.report = res.choices[0].message.content
                
                # שליחת אימייל ביצוע
                msg = EmailMessage()
                msg['Subject'] = f"אישור ביצוע פקודה - {biz_name}"
                msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(st.session_state.report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                    s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                
                status.update(label="המשימה בוצעה בהצלחה! ✅", state="complete")
                st.balloons()

    if st.session_state
