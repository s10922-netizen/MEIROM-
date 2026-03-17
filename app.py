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

# --- CSS נקי וקליל (Clean Minimalist) ---
st.set_page_config(page_title="Meirom AI", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    /* רקע לבן ונקי */
    .stApp {
        background-color: #ffffff;
        color: #1e293b;
    }
    
    /* כותרות עדינות */
    h1, h2, h3 {
        color: #0f172a !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-weight: 600 !important;
    }

    /* כפתורים אלגנטיים */
    .stButton>button {
        background-color: #f1f5f9;
        color: #1e40af !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1e40af !important;
        color: white !important;
        border: 1px solid #1e40af !important;
    }

    /* כרטיסי שירות עדינים */
    .service-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #f1f5f9;
        background-color: #f8fafc;
        margin-bottom: 15px;
        text-align: center;
    }

    /* תיבות טקסט נקיות */
    input, textarea {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='text-align: center; padding-top: 80px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3rem;'>Meirom <span style='color: #1e40af;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.2rem;'>Simple. Powerful. Autonomous.</p>", unsafe_allow_html=True)
    st.write("")
    if st.button("התחל עכשיו", use_container_width=True):
        go_to('options')
    st.markdown("</div>", unsafe_allow_html=True)

# --- עמוד 2: Options ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>בחירת מסלול</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='service-card'><h3>Basic</h3><p>Consulting</p></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with col2:
        st.markdown("<div class='service-card' style='border-color: #1e40af;'><h3>Pro</h3><p>Agents</p></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"): st.session_state.plan = "Pro"; go_to('payment')
    with col3:
        st.markdown("<div class='service-card'><h3>Enterprise</h3><p>Full-Sync</p></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"): st.session_state.plan = "Enterprise"; go_to('payment')

# --- עמוד 3: Payment ---
elif st.session_state.page == 'payment':
    st.markdown("<h2 style='text-align: center;'>תשלום מאובטח</h2>", unsafe_allow_html=True)
    st.text_input("מספר כרטיס", placeholder="xxxx-xxxx-xxxx-xxxx")
    if st.button("אשר תשלום והמשך ✅", use_container_width=True):
        go_to('main')

# --- עמוד 4: Main ---
elif st.session_state.page == 'main':
    st.title("מרכז שליטה")
    
    st.markdown("### 🔗 חיבור סוכנים")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.checkbox("WhatsApp"): st.session_state.integrations.append("WhatsApp")
    with c2: 
        if st.checkbox("Google Cal"): st.session_state.integrations.append("Calendar")
    with c3: 
        if st.checkbox("Wix/Shopify"): st.session_state.integrations.append("Ecom")
    
    st.markdown("---")
    with st.form("clean_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל מנהל")
        mission = st.text_area("משימה להטמעה")
        submit = st.form_submit_button("הפעל מערכת ⚡")

    if submit and biz_name and mission:
        with st.status("סוכן Meirom AI מעבד נתונים...", expanded=True):
            prompt = f"Professional AI report in HEBREW for {biz_name}. Mission: {mission}. Integrations: {st.session_state.integrations}."
            response = client.chat.completions.create(model="llama-
