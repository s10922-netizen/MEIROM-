import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import urllib.parse

# --- Connections ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Secrets!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- Navigation ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- Design ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    .stApp { background-color: #ffffff; direction: rtl; }
    h1, h2, p, span { text-align: right !important; color: #7c3aed; }
    .stButton>button { 
        background: linear-gradient(90deg, #a78bfa, #7c3aed); color: white;
        border-radius: 15px; font-weight: bold; width: 100%; height: 3.5em;
    }
    .cal-button {
        display: block; padding: 15px; background-color: #7c3aed;
        color: white !important; text-decoration: none !important; border-radius: 15px;
        font-weight: bold; text-align: center; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Page 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<h1>MEIROM MAGIC AI 🧚‍♀️</h1>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    st.write("ברוכה הבאה לעולם האוטומציות הקסום")
    if st.button("בואי נתחיל"):
        go_to('options')

# --- Page 2: Options ---
elif st.session_state.page == 'options':
    st.header("בחרי חבילה")
    c1, c2, c3 = st.columns(3)
    p_list = [("Basic", "250"), ("Pro", "750"), ("Enterprise", "2500")]
    for i, (name, price) in enumerate(p_list):
        with [c1, c2, c3][i]:
            st.info(f"### {name}\n## {price} ILS")
            if st.button(f"Select {name}", key=f"p{i}"):
                st.session_state.plan, st.session_state.price = name, price
                go_to('payment')

# --- Page 3: Payment ---
elif st.session_state.page == 'payment':
    st.header("סליקה מאובטחת")
    st.write(f"Plan: {st.session_state.plan} | Price: {st.session_state.price}")
    st.text_input("Card Number", placeholder="0000 0000 0000 0000")
    if st.button("Pay Now"):
        with st.spinner("Processing..."): time.sleep(1)
        go_to('main')
    if st.button("Back"): go_to('options')

# --- Page 4: Main Console ---
elif st.session_state.page == 'main':
    st.header(f"Console: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        g_on = st.toggle("Google Calendar", value=True)
        w_on = st.toggle("WhatsApp", value=True)

    with st.form("magic_form"):
        biz_name = st.text_input("Business Name")
        biz_email = st.text_input("Client Email")
        task_desc = st.
