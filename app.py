import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- AI SETUP ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("API Key Missing!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- DESIGN ---
st.set_page_config(page_title="Meirom AI")
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; }
    .stButton>button { background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border-radius: 12px; height: 3em; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- PAGES ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align:center;'>MEIROM AI</h1>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=150)
    if st.button("START"): go_to('options')
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align:center;'>CHOOSE PLAN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Basic (250)"): st.session_state.plan = "Basic"; go_to('payment')
    with c2:
        if st.button("Pro (750)"): st.session_state.plan = "Pro"; go_to('payment')
    with c3:
        if st.button("Enterprise (2500)"): st.session_state.plan = "Enterprise"; go_to('payment')

elif st.session_state.page == 'payment':
    st.markdown("<h2 style='text-align:center;'>PAYMENT</h2>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.text_input("Card Number")
    if st.button("PAY NOW"):
        b = st.progress(0)
        for i in range(100): time.sleep(0.01); b.progress(i+1)
        go_to('main')
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'main':
    st.markdown(f"<h2 style='text-align:center;'>DASHBOARD: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    with st.form("agent_form"):
        name = st.text_input("Business Name")
        email = st.text_input("Email")
        task = st.text_area("Task")
        if st.form_submit_button("RUN AGENT"):
