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
if 'report' not in st.session_state: st.session_state.report = None

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- עיצוב בהיר ונעים (ללא HTML שביר) ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")

# --- דף 1: פתיחה קסומה ---
if st.session_state.page == 'welcome':
    st.title("MEIROM MAGIC AI 🧚‍♀️")
    st.write("---")
    
    # הלוגו שביקשת: פייה עם מפל קסם AI
    st.image("https://img.freepik.com/premium-photo/fairy-with-magic-wand-creating-sparkling-waterfall-digital-particles-ai-concept_1161245-1234.jpg", caption="מפל הקסם של Meirom AI", width=400)
    
    with st.container(border=True):
        st.subheader("ברוכה הבאה לעולם של אוטומציה קסומה")
        st.write("אנחנו לא רק מדברים, אנחנו מטמיעים את הקסם בעסק שלך.")
        if st.button("בואי נתחיל! ✨", use_container_width=True):
            go_to('options')

# --- דף 2: בחירת מסלול (מחירים וצבעים) ---
elif st.session_state.page == 'options':
    st.header("בחרי את עוצמת הקסם")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### Basic\n**₪250**")
            if st.button("בחר Basic", key="b1"):
                st.session_state.plan = "Basic"; go_to('payment')
                
    with col2:
        with st.container(border=True):
            st.markdown("### Pro ⭐\n**₪750**")
            if st.button("בחר Pro", key="b2"):
                st.session_state.plan = "Pro"; go_to('payment')
                
    with col3:
        with st.container(border=True):
            st.markdown("### Enterprise\n**₪2,500**")
            if st.button("בחר Enterprise", key="b3"):
                st.session_state.plan = "Enterprise"; go_to('payment')

# --- דף 3: תשלום מלא ---
elif st.session_state.page == 'payment':
    st.header("תשלום מאובטח")
    with st.container(border=True):
        st.write(f"מסלול נבחר: **{st.session_state.plan}**")
        st.text_input("מספר כרטיס")
        c1, c2 = st.columns(2)
        c1.text_input("תוקף (MM/YY)")
        c2.text_input("CVV")
        
        if st.button("אשר תשלום והפעל קסם ✅", use_container_width=True):
            bar = st.progress(0)
            for i in range(100):
                time.sleep
