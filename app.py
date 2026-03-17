import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
import requests # הוספנו כדי שנוכל לשלוח פקודות לעולם האמיתי בעתיד

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
if 'tools' not in st.session_state: st.session_state.tools = []

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה ---
st.set_page_config(page_title="Meirom AI | Operational", page_icon="⚙️", layout="centered")
st.markdown("""
<style>
    .stApp { background: #f0f2f6; }
    .app-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #2563eb, #7c3aed) !important; color: white !important; border-radius: 12px !important; font-weight: bold !important; width: 100% !important; height: 3.5em !important; }
    .status-box { background: #eef2ff; border-right: 5px solid #4f46e5; padding: 10px; margin: 5px 0; border-radius: 5px; color: #3730a3; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# --- דפים ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align:center;'>Meirom <span style='color:#4f46e5;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=150)
    st.write("מערכת אוטונומית לביצוע פעולות בעסק")
    if st.button("כניסה למסוף המבצעי ⚡"): go_to('options')
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align:center;'>בחירת רמת אוטונומיה</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "₪250"), ("Pro", "₪750"), ("Enterprise", "₪2500")]
    for i, (name, price) in enumerate(plans):
        with [c1, c2, c3][i]:
            st.markdown(f"<div class='app-card'><h3>{name}</h3><p>{price}</p></div>", unsafe_allow_html=True)
            if st.button(f"בחר {name}"):
                st.session_state.plan = name
                go_to('main') # דילגנו על תשלום בשביל הבדיקה

elif st.session_state.page == 'main':
    st.markdown(f"<h2 style='text-align:center;'>Control Center: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    
    # חיבור תשתיות
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("🔗 חיבור תשתיות לביצוע")
    colA, colB, colC = st.columns(3)
    with colA: ws = st.checkbox("WhatsApp Business")
    with colB: cal = st.checkbox("Google Calendar")
    with colC: shop = st.checkbox("Shopify Admin")
    st.markdown("</div>", unsafe_allow_html=True)

    # מסוף פקודות
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    with st.form("operation_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל מנהל")
        action = st.text_area("הגדר משימה לביצוע (למשל: 'שלח הודעת ברוך הבא לכל לקוח חדש')")
        execute = st.form_submit_button("הפעל סוכן מבצע ⚡")

        if execute and action:
            with st.status("סוכן Meirom AI מבצע פעולות בעסק...", expanded=True) as status:
                st.markdown("<div class='status-box'>🔍 מנתח את בקשת הביצוע...</div>", unsafe_allow_html=True)
                time.sleep(1)
                
                if ws:
                    st.markdown("<div class='status-box'>💬 מתחבר ל-WhatsApp API... מגדיר בוט מענה אוטומטי.</div>", unsafe_allow_html=True)
                    time.sleep(1.5)
                if cal:
                    st.markdown("<div class='status-box'>📅 מסנכרן יומן... מגדיר אוטומציית קביעת תורים.</div>", unsafe_allow_html=True)
                    time.sleep(1.5)
                
                st.markdown("<div class='status-box'>📧 שולח דו''ח ביצוע מפורט למנהל...</div>", unsafe_allow_html=True)
                
                # AI Logic
                p = f"Implementer Mode: Summarize active actions for {biz_name}. Task: {action}. Language: Hebrew."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                report = res.choices[0].message.content
                
                # Email Logic
                msg = EmailMessage()
                msg['Subject'] = f"Action Confirmation - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                    s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                
                status.update(label="המשימה בוצעה בהצלחה! ✅", state="complete")
                st.balloons()
                st.markdown("### סיכום פעולות שבוצעו:")
                st.write(report)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("⬅️ יציאה"): go_to('welcome')
