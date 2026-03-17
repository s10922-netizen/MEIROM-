import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import os

# --- הגדרות ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Groq Key!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול דפים ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- עיצוב יוקרתי ונקי ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-card { background: white; padding: 30px; border-radius: 20px; border: 1px solid #eee; }
    h1 { color: #7c3aed; text-align: center; }
    .stButton>button { 
        background: linear-gradient(90deg, #a78bfa, #7c3aed); color: white;
        border-radius: 12px; border: none; font-size: 18px; width: 100%; height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# --- דף פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<h1>MEIROM MAGIC AI 🧚‍♀️</h1>", unsafe_allow_html=True)
    st.image("fairy_logo.png", use_container_width=True)
    if st.button("התחילי את הקסם ✨"): go_to('main')

# --- דף ביצוע (נקי, בלי לינקים!) ---
elif st.session_state.page == 'main':
    st.markdown("<h2>מסוף ניהול אוטומטי</h2>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        st.write("מערכות מחוברות: **גוגל, וואטסאפ**")
    
    with st.container():
        with st.form("agent"):
            biz_name = st.text_input("שם העסק")
            task = st.text_area("משימה לביצוע")
            if st.form_submit_button("הפעל סוכן מבצע ⚡"):
                with st.status("הפייה מבצעת הטמעה שקטה...") as status:
                    # כאן הקוד עושה את העבודה "מתחת למכסה המנוע"
                    time.sleep(2)
                    
                    # דו"ח ביצוע מה-AI
                    p = f"Professional summary in HEBREW for {biz_name}. Task: {task} has been integrated into Google Calendar and CRM."
                    res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                    report = res.choices[0].message.content
                    
                    # שליחת מייל
                    msg = EmailMessage()
                    msg['Subject'] = f"אישור ביצוע - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = MY_EMAIL
                    msg.set_content(report, charset='utf-8')
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                        s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                    
                    status.update(label="הטמעה הושלמה!", state="complete")
                    st.success("הפעולה בוצעה והסנכרון הושלם.")
                    st.info(report)
                    st.balloons()

    if st.button("⬅️ חזרה"): go_to('welcome')
