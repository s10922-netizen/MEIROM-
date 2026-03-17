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

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- DESIGN ---
st.set_page_config(page_title="Meirom AI")
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .stButton>button { background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border-radius: 12px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- PAGES ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align:center;'>MEIROM AI</h1>", unsafe_allow_html=True)
    if st.button("START 🚀"): go_to('options')

elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align:center;'>CHOOSE PLAN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with c2:
        if st.button("Pro"): st.session_state.plan = "Pro"; go_to('payment')
    with col3 if 'col3' in locals() else c3: # תיקון קטן ליציבות
        if st.button("Enterprise"): st.session_state.plan = "Enterprise"; go_to('payment')

elif st.session_state.page == 'payment':
    st.title("PAYMENT")
    st.text_input("Card Number")
    if st.button("CONFIRM ✅"): go_to('main')

elif st.session_state.page == 'main':
    st.title(f"AGENT: {st.session_state.plan}")
    with st.form("my_form"):
        name = st.text_input("Business Name")
        email = st.text_input("Email")
        task = st.text_area("Task")
        submitted = st.form_submit_button("RUN AGENT ⚡")
        
        if submitted:
            if name and task:
                with st.spinner("Processing..."):
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":f"Report in Hebrew for {name}: {task}"}]
                    )
                    st.session_state.report = res.choices[0].message.content
                    msg = EmailMessage()
                    msg['Subject'] = f"Report - {name}"
                    msg['From'] = MY_EMAIL
                    msg['To'] = email
                    msg.set_content(st.session_state.report)
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                        s.login(MY_EMAIL, APP_PASSWORD)
                        s.send_message(msg)
                    st.success("Done!")

    if st.session_state.report:
        st.write(st.session_state.report)
    if st.button("LOGOUT"): 
        st.session_state.report = None
        go_to('welcome')
