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

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- עיצוב אפליקציה (Clean & Premium App UI) ---
st.set_page_config(page_title="Meirom AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* רקע בהיר ונעים */
    .stApp { background-color: #F7F9FC; }
    
    /* כותרות אפליקציה */
    h1, h2 { color: #1A202C !important; font-family: 'Inter', sans-serif; font-weight: 700 !important; text-align: center; }

    /* כרטיס אפליקציה מרכזי */
    .app-card {
        background: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #EDF2F7;
    }

    /* כפתור כחול אפליקטיבי */
    .stButton>button {
        background-color: #3182CE !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); background-color: #2B6CB0 !important; }
    
    /* עיצוב תיבות קלט */
    input { border-radius: 12px !important; border: 1px solid #E2E8F0 !important; padding: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- דף פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 40px;'>", unsafe_allow_html=True)
    st.markdown("<h1>Meirom <span style='color: #3182CE;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #718096;'>Autonomous Business Solutions</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=150)
    st.write("")
    if st.button("כניסה למערכת 🚀"): go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- דף בחירת מסלול ---
elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    plans = [("Basic", "₪250"), ("Pro", "₪750"), ("Enterprise", "₪2,500")]
    
    for name, price in plans:
        with locals()[f"col{plans.index((name, price))+1}"]:
            st.markdown(f"<div class='app-card'><h3>{name}</h3><p style='color:#3182CE; font-weight:bold;'>{price}</p></div>", unsafe_allow_html=True)
            if st.button(f"בחר {name}"):
                st.session_state.plan = name
                go_to('payment')

# --- דף תשלום (כמו אפליקציה אמיתית) ---
elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום מאובטח</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>מסלול נבחר: <b>{st.session_state.plan}</b></p>", unsafe_allow_html=True)
    
    # טופס תשלום מלא
    card_num = st.text_input("מספר כרטיס", placeholder="0000 0000 0000 0000")
    c1, c2 = st.columns(2)
    with c1: st.text_input("תוקף", placeholder="MM/YY")
    with c2: st.text_input("CVV", placeholder="000")
    
    st.write("")
    if st.button("בצע תשלום ✅"):
        with st.spinner("מאמת כרטיס..."): time.sleep(1.5)
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("⬅️ חזרה"): go_to('options')

# --- דף הפעלה ---
elif st.session_state.page == 'main':
    st.markdown(f"<h2>מרכז שליטה: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    biz_name = st.text_input("שם העסק")
    biz_email = st.text_input("אימייל לשליחת הדו''ח")
    mission = st.text_area("מה המשימה להיום?")
    
    if st.button("הפעל סוכן AI ⚡"):
        if biz_name and mission and biz_email:
            with st.status("סוכן Meirom AI מבצע הטמעה..."):
                prompt = f"Professional report for {biz_name}. Mission: {mission}."
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                report = response.choices[0].message.content
                
                # שליחת מייל
                msg = EmailMessage()
                msg['Subject'] = f"Report - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD); smtp.send_message(msg)
                
                st.success("הסוכן סיים והמייל נשלח!")
                st.balloons()
                st.write(report)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("⬅️ יציאה"): go_to('welcome')
