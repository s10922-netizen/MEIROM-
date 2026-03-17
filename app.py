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

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- עיצוב האפליקציה (Premium UI) ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    
    /* כותרות */
    h1, h2, h3 { color: #1e3a8a !important; font-family: 'Inter', sans-serif; text-align: center; }

    /* כרטיסים מעוצבים */
    .app-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        text-align: center;
    }

    /* כפתורים */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        width: 100%;
        transition: 0.3s;
    }
    
    /* עיצוב תיבות טקסט */
    input, textarea { border-radius: 10px !important; border: 1px solid #cbd5e1 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color: #2563eb;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #64748b;'>הטמעת בינה מלאכותית אוטונומית בעסקים</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=200)
    st.write("")
    if st.button("כניסה למערכת ההטמעה 🚀"):
        go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- עמוד 2: בחירת מסלול (עם הצבעים שאהבנו!) ---
elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='app-card' style='border-top: 5px solid #3b82f6;'><h3>Basic</h3><p>₪250</p></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"; st.session_state.price = "250"; go_to('payment')
            
    with col2:
        st.markdown("<div class='app-card' style='border-top: 5px solid #22c55e;'><h3>Pro ⭐</h3><p>₪750</p></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"):
            st.session_state.plan = "Pro"; st.session_state.price = "750"; go_to('payment')
            
    with col3:
        st.markdown("<div class='app-card' style='border-top: 5px solid #eab308;'><h3>Enterprise</h3><p>₪2,500</p></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"; st.session_state.price = "2,500"; go_to('payment')
    
    if st.button("⬅️ חזרה"): go_to('welcome')

# --- עמוד 3: תשלום (מעוצב ומלא) ---
elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום מאובטח</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.write(f"מסלול: **{st.session_state.plan}** | סכום לחיוב: **₪{st.session_state.price}**")
    
    st.markdown("### 💳 פרטי אשראי", unsafe_allow_html=True)
    st.text_input("מספר כרטיס", placeholder="0000 0000 0000 0000")
    c1, c2 = st.columns(2)
    with c1: st.text_input("תוקף", placeholder="MM/YY
