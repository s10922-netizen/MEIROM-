import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import urllib.parse
from datetime import datetime

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

# --- עיצוב האתר ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1, h2 { color: #7c3aed !important; text-align: center; }
    .stButton>button { 
        background: linear-gradient(90deg, #a78bfa, #7c3aed); color: white;
        border-radius: 15px; font-weight: bold; border: none; height: 3.5em;
    }
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
                if st.button(f"בחר {name}", key=f"btn_{name}"):
                    st.session_state.plan, st.session_state.price = name, price
                    go_to('payment')

# --- דף 3: תשלום אשראי ---
elif st.session_state.page == 'payment':
    st.header("💳 סליקה מאובטחת")
    with st.container(border=True):
        st.write(f"מסלול: **{st.session_state.plan}** | סכום: **{st.session_state.price}**")
        st.text_input("מספר כרטיס אשראי", placeholder="0000 0000 0000 0000")
        if st.button("אשר תשלום והמשך ✅", use_container_width=True):
            with st.spinner("מאמת..."): time.sleep(1)
            st.success("התשלום בוצע!")
            go_to('main')
    if st.button("⬅️ חזור"): go_to('options')

# --- דף 4: מסוף הביצוע ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול AI: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=120)
        st.subheader("חיבורים")
        google_active = st.toggle("חיבור ליומן גוגל 📅", value=True)
        whatsapp_active = st.toggle("חיבור WhatsApp 📱")

    with st.container(border=True):
        with st.form("agent_form"):
            biz_name = st.text_input("שם הלקוח")
            biz_email = st.text_input("אימייל לדו''ח")
            task = st.text_area("משימה (למשל: תקבע פגישה למחר ב-10:00)")
            if st.form_submit_button("הפעל סוכן מבצע ⚡"):
                if task:
                    with st.status("הפייה עובדת...") as status:
                        # חילוץ זמן
                        prompt = f"Extract date and time from: '{task}'. Use YYYYMMDDTHHMMSSZ format. Return ONLY the code."
                        res_time = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"
