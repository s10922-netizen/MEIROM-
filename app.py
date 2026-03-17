import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import urllib.parse

# --- חיבורים ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Groq Key!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
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
        border-radius: 15px; font-weight: bold; border: none; height: 3.5em; width: 100%;
    }
    /* עיצוב כפתור היומן המיוחד */
    .cal-button {
        display: inline-block; padding: 15px 25px; background-color: #7c3aed;
        color: white !important; text-decoration: none !important; border-radius: 15px;
        font-weight: bold; text-align: center; width: 100%; margin: 10px 0;
        box-shadow: 0px 4px 10px rgba(124, 58, 237, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- דף 1: ברוכים הבאים ---
if st.session_state.page == 'welcome':
    st.title("MEIROM MAGIC AI 🧚‍♀️")
    st.image("fairy_logo.png", width=350)
    with st.container(border=True):
        st.subheader("ברוכה הבאה לעולם האוטומציות הקסום")
        if st.button("בואי נתחיל! ✨"): go_to('options')

# --- דף 2: בחירת מסלול ---
elif st.session_state.page == 'options':
    st.header("בחרי את חבילת ההטמעה")
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "₪250"), ("Pro ⭐", "₪750"), ("Enterprise", "₪2,500")]
    for i, (p_name, p_price) in enumerate(plans):
        with [c1, c2, c3][i]:
            with st.container(border=True):
                st.markdown(f"### {p_name}\n## {p_price}")
                if st.button(f"בחר {p_name}", key=f"p_{i}"):
                    st.session_state.plan, st.session_state.price = p_name, p_price
                    go_to('payment')

# --- דף 3: תשלום אשראי ---
elif st.session_state.page == 'payment':
    st.header("💳 סליקה מאובטחת")
    with st.container(border=True):
        st.write(f"מסלול: {st.session_state.plan} | סכום: {st.session_state.price}")
        st.text_input("מספר כרטיס אשראי", placeholder="0000 0000 0000 0000")
        if st.button("אשר תשלום והמשך ✅"):
            with st.spinner("מאמת..."): time.sleep(1)
            go_to('main')
    if st.button("⬅️ חזור"): go_to('options')

# --- דף 4: מסוף הביצוע ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        st.subheader("הגדרות סוכן")
        g_on = st.toggle("סנכרון יומן", value=True)
        w_on = st.toggle("הודעת WhatsApp")

    with st.form("magic_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לדו''ח")
        task = st.text_area("משימה (למשל: תקבע פגישה למחר ב-10:00)")
        if st.form_submit_button("
