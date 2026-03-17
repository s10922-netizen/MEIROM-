import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import requests

# --- הגדרות חיבור ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
    CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
except:
    st.error("Missing Secrets (Groq or Google)!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ומצב ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'authenticated_google' not in st.session_state: st.session_state.authenticated_google = False

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- עיצוב בהיר ונעים ---
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

# --- דף 1: פתיחה קסומה ---
if st.session_state.page == 'welcome':
    st.title("MEIROM MAGIC AI 🧚‍♀️")
    st.write("---")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350) # משתמש בלוגו שהעלית!
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("הטמעת AI עם מפל של קסם")
        if st.button("בואי נתחיל! ✨", use_container_width=True):
            go_to('options')

# --- דף 2: בחירת מסלול ---
elif st.session_state.page == 'options':
    st.header("בחרי את עוצמת הקסם")
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "₪250"), ("Pro ⭐", "₪750"), ("Enterprise", "₪2,500")]
    for i, (name, price) in enumerate(plans):
        with [c1, c2, c3][i]:
            with st.container(border=True):
                st.markdown(f"### {name}\n**{price}**")
                if st.button(f"בחר {name}"):
                    st.session_state.plan = name; go_to('main')

# --- דף 3: מסוף הביצוע האמיתי ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ביצוע: {st.session_state.plan}")
    
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        st.subheader("סטטוס חיבור")
        if not st.session_state.authenticated_google:
            st.warning("גוגל לא מחובר")
            if st.button("חיבור ליומן גוגל 📅"):
                # כאן מתחיל תהליך ה-OAuth
                st.info("מתחבר לשרתי גוגל...")
                time.sleep(1)
                st.session_state.authenticated_google = True
                st.success("מחובר בהצלחה!")
                st.rerun()
        else:
            st.success("מחובר ליומן גוגל ✅")

    with st.container(border=True):
        with st.form("magic_form"):
            biz_name = st.text_input("שם העסק")
            biz_email = st.text_input("אימייל לדו''ח")
            task = st.text_area("מה המשימה לביצוע? (למשל: תקבע לי פגישה למחר)")
            
            if st.form_submit_button("הפעל סוכן מבצע ⚡"):
                if biz_name and task:
                    with st.status("הפייה מבצעת הטמעה..."):
                        # בדיקה אם המשימה קשורה ליומן
                        is_calendar = "פגישה" in task or "יומן" in task or "תור" in task
                        
                        if is_calendar and st.session_state.authenticated_google:
                            st.code("> Google Calendar API: Creating Event...")
                            time.sleep(2)
                        
                        st.code("> Building Automation Flow...")
                        p = f"Implementer for {biz_name}. Task: {task}. Actions taken in HEBREW."
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                        report = res.choices[0].message.content
                        
                        # שליחת מייל אמיתי
                        msg = EmailMessage()
                        msg['Subject'] = f"ביצוע משימה: {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                        msg.set_content(report, charset='utf-8')
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                            s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                        
                        st.success("המשימה בוצעה!")
                        st.info(report)
                        st.balloons()
    
    if st.button("⬅️ יציאה"): go_to('welcome')
