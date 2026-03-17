import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing GROQ_KEY!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'price' not in st.session_state:
    st.session_state.price = "0"
if 'report' not in st.session_state:
    st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב האפליקציה ---
st.set_page_config(page_title="Meirom AI", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3 { color: #1e3a8a !important; text-align: center; }
    .app-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
        margin-bottom: 20px; text-align: center;
    }
    .stButton>button { border-radius: 12px !important; width: 100%; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- דפים ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='padding-top:50px;'>MEIROM AI</h1>", unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=150)
    if st.button("כניסה 🚀"):
        go_to('options')
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="app-card" style="border-top:5px solid #3b82f6;"><h3>Basic</h3></div>', unsafe_allow_html=True)
        if st.button("בחר Basic"):
            st.session_state.plan, st.session_state.price = "Basic", "250"
            go_to('payment')
    with c2:
        st.markdown('<div class="app-card" style="border-top:5px solid #22c55e;"><h3>Pro ⭐</h3></div>', unsafe_allow_html=True)
        if st.button("בחר Pro"):
            st.session_state.plan, st.session_state.price = "Pro", "750"
            go_to('payment')
    with c3:
        st.markdown('<div class="app-card" style="border-top:5px solid #eab308;"><h3>Enterprise</h3></div>', unsafe_allow_html=True)
        if st.button("בחר Enterprise"):
            st.session_state.plan, st.session_state.price = "Enterprise", "2,500"
            go_to('payment')

elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום</h2>", unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write(f"מסלול: {st.session_state.plan}")
    st.text_input("מספר כרטיס")
    if st.button("אשר תשלום ✅"):
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == 'main':
    st.markdown(f"<h2>מסוף: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    with st.form("agent_form"):
        name = st.text_input("שם העסק")
        email = st.text_input("מייל לדו''ח")
        mission = st.text_area("משימה להטמעה")
        if st.form_submit_button("הפעל סוכן ⚡"):
            if name and mission:
                with st.status("
