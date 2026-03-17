import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing API Key")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"
if 'report' not in st.session_state: st.session_state.report = None
if 'tools' not in st.session_state: st.session_state.tools = []

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה פרימיום ---
st.set_page_config(page_title="Meirom AI", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%); }
    h1, h2, h3 { color: #1e293b !important; text-align: center; font-weight: 800 !important; }
    
    /* כרטיס אפליקציה */
    .app-card {
        background: white; padding: 30px; border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #ffffff;
        margin-bottom: 20px;
    }

    /* כפתור Gradient */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important; border: none !important;
        border-radius: 14px !important; font-weight: bold !important;
        width: 100% !important; height: 3.5em !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- דף 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 60px;'>", unsafe_allow_html=True)
    st.markdown("<h1>Meirom <span style='color: #6366f1;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=180)
    st.write("מערכת אוטונומית להטמעת AI בעסק שלך")
    if st.button("בואי נתחיל 🚀"): go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- דף 2: Options ---
elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    plans = [
        ("Basic", "₪250", "#3b82f6"),
        ("Pro ⭐", "₪750", "#22c55e"),
        ("Enterprise", "₪2,500", "#eab308")
    ]
    
    for i, (name, price, color) in enumerate(plans):
        with [c1, c2, c3][i]:
            st.markdown(f"<div class='app-card' style='border-top: 6px solid {color};'><h3>{name}</h3><h3>{price}</h3></div>", unsafe_allow_html=True)
            if st.button(f"בחר {name}"):
                st.session_state.plan, st.session_state.price = name, price
                go_to('payment')

# --- דף 3: Payment ---
elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום מאובטח</h2>", unsafe_allow_html=True)
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.write(f"מסלול נבחר: **{st.session_state.plan}** | סכום: **{st.session_state.price}**")
    
    st.text_input("מספר כרטיס אשראי")
    colA, colB = st.columns(2)
    with colA: st.text_input("תוקף (MM/YY)")
    with colB: st.text_input("CVV")
    
    if st.button("אשר והפעל מערכת ✅"):
        bar = st.progress(0)
        for i in range(101):
            time.sleep(0.01); bar.progress(i)
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)

# --- דף 4: Main Terminal (האינטגרציות חזרו!) ---
elif st.session_state.page == 'main':
    st.markdown(f"<h2>מסוף ניהול: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    
    # אזור חיבור כלים
    st.markdown("<div class='app-card'>", unsafe_allow_html
