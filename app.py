import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import requests

# --- AI SETUP ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing API Key")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- WEBHOOK URL (כאן את שמה את הלינק מ-Make/Zapier בעתיד) ---
WEBHOOK_URL = "https://your-webhook-link.com"

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'tools' not in st.session_state: st.session_state.tools = []

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- DESIGN PREMIUM ---
st.set_page_config(page_title="Meirom AI | Autonomous", page_icon="🤖")
st.markdown("""
<style>
    .stApp { background: #f4f7f6; }
    .console-box { 
        background: #0d1117; color: #39d353; font-family: 'Courier New', monospace;
        padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6;
        margin: 10px 0; font-size: 0.9rem;
    }
    .stButton>button { 
        background: linear-gradient(90deg, #4f46e5, #7c3aed); color: white;
        border-radius: 12px; font-weight: bold; border: none; height: 3.5em;
    }
</style>
""", unsafe_allow_html=True)

# --- PAGES ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align:center;'>Meirom <span style='color:#4f46e5;'>AI</span></h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=150)
    if st.button("כניסה למערכת ההטמעה 🚀"): go_to('main')

elif st.session_state.page == 'main':
    st.title("מסוף שליטה מבצעי")
    
    # חיבור כלים
    with st.expander("🔗 חיבור תשתיות (API Connections)", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1: ws = st.checkbox("WhatsApp")
        with col2: cal = st.checkbox("Google Calendar")
        with col3: shp = st.checkbox("Shopify")

    # הזנת משימה
    with st.form("exec_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל מנהל")
        mission = st.text_area("הגדר משימה לסוכן (למשל: 'תקבע לי פגישה עם כל ליד חדש')")
        execute = st.form_submit_button("הפעל סוכן מבצע ⚡")

        if execute and mission:
            with st.status("סוכן Meirom AI נכנס לפעולה...", expanded=True) as status:
                # סימולציית ביצוע בטרמינל
                st.markdown("<div class='console-box'>> initializing Meirom_Core_v13.0...</div>", unsafe_allow_html=True)
                time.sleep(0.8)
                
                if ws:
                    st.markdown("<div class='console-box'>> connecting to WhatsApp Business API... SUCCESS</div>", unsafe_allow_html=True)
                    time.sleep(1)
                if cal:
                    st.markdown("<div class='console-box'>> syncing Google Calendar events... automation set.</div>", unsafe_allow_html=True)
                    time.sleep(1)
                
                st.markdown("<div class='console-box'>> executing AI logic for business optimization...</div>", unsafe_allow_html=True)
                
                # שליחה ל-Webhook (כרגע בסימולציה)
                # requests.post(WEBHOOK_URL, json={"business": biz_name, "task": mission})
                
                # AI Report Logic
                p = f"Implementer summary for {biz_name}. Task: {mission}. Report the actions TAKEN."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                report = res.choices[0].message.content
                
                # Email
                msg = EmailMessage()
                msg['Subject'] = f"Action Log: {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                    s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                
                status.update(label="המשימה בוצעה והוטמעה! ✅", state="complete")
                st.balloons()
                st.markdown("### הדו''ח המבצעי:")
                st.write(report)

    if st.button("⬅️ יציאה"): go_to('welcome')
