import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import urllib.parse
from datetime import datetime, timedelta

# --- הגדרות חיבור ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Groq Key in Secrets!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ומצב ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- עיצוב האתר (הפיה והמפל) ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1, h2 { color: #7c3aed !important; text-align: center; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        background: linear-gradient(90deg, #a78bfa, #7c3aed); color: white;
        border-radius: 15px; font-weight: bold; border: none; height: 3.5em;
        transition: all 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 4px 15px rgba(124, 58, 237, 0.3); }
    .sidebar .sidebar-content { background-image: linear-gradient(#f3e8ff, #ffffff); }
</style>
""", unsafe_allow_html=True)

# --- דף 1: ברוכים הבאים ---
if st.session_state.page == 'welcome':
    st.title("MEIROM MAGIC AI 🧚‍♀️")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("ברוכה הבאה לעולם האוטומציות הקסום")
        st.write("אני פיית ה-AI שלך, ואני כאן כדי להפוך את העסק שלך לאוטומטי באמת.")
        if st.button("בואי נתחיל את הקסם! ✨", use_container_width=True):
            go_to('options')

# --- דף 2: בחירת מסלול ---
elif st.session_state.page == 'options':
    st.header("בחרי את חבילת ההטמעה שלך")
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "₪250"), ("Pro ⭐", "₪750"), ("Enterprise", "₪2,500")]
    for i, (name, price) in enumerate(plans):
        with [c1, c2, c3][i]:
            with st.container(border=True):
                st.markdown(f"### {name}\n## {price}")
                st.write("כולל סוכן חכם, חיבור ליומן ודיווח במייל.")
                if st.button(f"בחר {name}", key=f"btn_{name}"):
                    st.session_state.plan, st.session_state.price = name, price
                    go_to('payment')

# --- דף 3: תשלום אשראי ---
elif st.session_state.page == 'payment':
    st.header("💳 סליקה מאובטחת")
    with st.container(border=True):
        st.write(f"את רוכשת את מסלול: **{st.session_state.plan}**")
        st.write(f"סה''כ לתשלום: **{st.session_state.price}**")
        st.text_input("שם מלא על הכרטיס")
        st.text_input("מספר כרטיס אשראי", placeholder="0000 0000 0000 0000")
        col1, col2 = st.columns(2)
        col1.text_input("תוקף (MM/YY)")
        col2.text_input("CVV", type="password")
        
        if st.button("
