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

# --- עיצוב Premium Minimalist ---
st.set_page_config(page_title="Meirom AI", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #fdfbfb 0%, #ebedee 100%); }
    h1 { color: #1e293b !important; font-weight: 800 !important; letter-spacing: -1px; }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white !important; border: none !important; border-radius: 12px !important;
        font-weight: 600 !important; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    .card-style {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='text-align: center; padding-top: 60px;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color: #6366f1;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Empowering business through autonomous intelligence.</p>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=200)
    if st.button("Get Started ✨", use_container_width=True): go_to('options')
    st.markdown("</div>", unsafe_allow_html=True)

# --- עמוד 2: Options ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>Select Your Plan</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card-style'><h3>Basic</h3><p>₪250</p></div>", unsafe_allow_html=True)
        if st.button("Choose Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with c2:
        st.markdown("<div class='card-style' style='border: 2px solid #6366f1;'><h3>Pro</h3><p>₪750</p></div>", unsafe_allow_html=True)
        if st.button
