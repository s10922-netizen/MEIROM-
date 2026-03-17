import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing GROQ_KEY in Secrets!")

# --- הגדרות אימייל ---
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'report' not in st.session_state: st.session_state.report = None
if 'integrations' not in st.session_state: st.session_state.integrations = []

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- עיצוב מינימליסטי ונקי ---
st.set_page_config(page_title="Meirom AI", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; }
    h1, h2, h3 { color: #0f172a !important; font-family: sans-serif; }
    .stButton>button {
        background-color: #f1f5f9;
        color: #1e40af !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover { background-color: #1e40af !important; color: white !important; }
    .card { padding: 20px; border-radius: 12px; background-color: #f8fafc; border: 1px solid #e2e8f0; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- דפים ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='text-align: center; padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>Meirom <span style='color: #1e40af;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p>פתרונות אוטונומיים לעסק שלך</p>", unsafe_allow_html=True)
    if st.button("התחל עכשיו", use_container_width=True): go_to('options')
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>בחירת מסלול</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card'><h3>Basic</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with c2:
        st.markdown("<div class='card'><h3>Pro</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"): st.session_state.plan = "Pro"; go_to('payment')
    with c3:
        st.markdown("<div class='card'><h3>Enterprise</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"): st.session_state.plan = "Enterprise"; go_to('payment')

elif st.session_state.page == 'payment':
    st.markdown("<h2 style='text-align: center;'>תשלום מאובטח</h2>", unsafe_allow_html=True)
    st.text_input("מספר כרטיס", placeholder="xxxx-xxxx-xxxx-xxxx")
    if st.button("אישור והמשך ✅", use_container_width=True): go_to('main')

elif st.session_state.page == 'main':
    st.title("מרכז שליטה והטמעה")
    
    st.markdown("### 🔗 חיבור סוכנים")
    colA, colB, colC = st.columns(3)
    with colA: 
        if st.checkbox("WhatsApp"): st.session_state.integrations.append("WhatsApp")
    with colB: 
        if st.checkbox("Google Calendar"): st.session_state.integrations.append("Calendar")
    with colC: 
        if st.checkbox("E-commerce"): st.session_state.integrations.append("Shopify")
    
    with st.form("action_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל מנהל")
        mission = st.text_area("משימה להטמעה")
        submit = st.form_submit_button("הפעל סוכן ⚡")

    if submit and biz_name and mission:
        with st.status("מעבד נתונים...", expanded=True):
            prompt = f"Professional report in HEBREW for {biz_name}. Mission: {mission}. Connect: {st.session_state.integrations}."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.report = response.choices[0].message.content
            
            msg = EmailMessage()
            msg['Subject'] = f"דו''ח Meirom AI - {biz_name}"
            msg['From'] = MY_EMAIL
            msg['To'] = biz_email
            msg.set_content(st.session_state.report, charset='utf-8')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(MY_EMAIL, APP_PASSWORD)
                smtp.send_message(msg)
            st.balloons()

    if st.session_state.report:
        st.markdown("### 📋 סיכום פעולה")
        st.write(st.session_state.report)

    if st.button("חזרה למסך הבית"):
        st.session_state.report = None
        go_to('welcome')
