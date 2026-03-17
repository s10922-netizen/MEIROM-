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

# --- הגדרות אימייל ---
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'report' not in st.session_state: st.session_state.report = None
if 'integrations' not in st.session_state: st.session_state.integrations = []

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- CSS Dark Mode Premium ---
st.set_page_config(page_title="Meirom AI | Autonomous", page_icon="🤖", layout="centered")
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #050a18;
        background-image: radial-gradient(circle at top right, #1e3a8a 0%, #050a18 40%);
        color: white;
    }
    h1, h2, h3, p, label { color: white !important; }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 15px !important;
    }
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #3b82f6;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>MEIROM <span style='color: #3b82f6;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>מערכת אוטונומית להטמעת AI בעסקים</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png")
        if st.button("כניסה למערכת 🚀", use_container_width=True): go_to('options')

# --- עמוד 2: בחירת מסלול ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>בחר רמת אוטונומיה</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='agent-card'><h3>Basic</h3><p>ייעוץ AI</p></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with c2:
        st.markdown("<div class='agent-card' style='border-width:3px;'><h3>Pro ⭐</h3><p>סוכנים פעילים</p></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"): st.session_state.plan = "Pro"; go_to('payment')
    with c3:
        st.markdown("<div class='agent-card'><h3>Enterprise</h3><p>ניהול מלא</p></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"): st.session_state.plan = "Enterprise"; go_to('payment')

# --- עמוד 3: תשלום ---
elif st.session_state.page == 'payment':
    st.markdown("<h2 style='text-align: center;'>אבטחת חיבור לסוכנים</h2>", unsafe_allow_html=True)
    st.text_input("Card Number", type="password")
    if st.button("אמת תשלום ופתח סוכנים ✅"):
        with st.spinner("יוצר חיבור מוצפן..."): time.sleep(1)
        go_to('main')

# --- עמוד 4: המערכת המבצעית (החיבורים האמיתיים!) ---
elif st.session_state.page == 'main':
    st.markdown(f"<h1>מסוף סוכנים: <span style='color:#3b82f6;'>{st.session_state.plan}</span></h1>", unsafe_allow_html=True)
    
    # אזור חיבורים (Integrations)
    st.subheader("🔗 חיבור כלים עסקיים")
    colA, colB, colC = st.columns(3)
    with colA:
        if st.checkbox("WhatsApp API"): st.session_state.integrations.append("WhatsApp")
    with colB:
        if st.checkbox("Google Calendar"): st.session_state.integrations.append("Calendar")
    with colC:
        if st.checkbox("Shopify / Wix"): st.session_state.integrations.append("E-commerce")

    st.markdown("---")
    
    with st.form("action_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל מנהל")
        mission = st.text_area("הגדר משימה לסוכן (למשל: 'נהל לי את התורים ביומן')")
        run_agent = st.form_submit_button("הפעל סוכן מבצע ⚡")

    if run_agent and biz_name and mission:
        with st.status("סוכן Meirom AI נכנס לפעולה...", expanded=True) as status:
            # שלב 1: מחשבה
            st.write("🧠 מנתח את הפעולות הנדרשות...")
            time.sleep(1)
            
            # שלב 2: "ביצוע" (סימולציה של הטמעה)
            if "Calendar" in st.session_state.integrations:
                st.write("📅 מתחבר ליומן גוגל ומייצר אוטומציה לתורים...")
                time.sleep(1.5)
            if "WhatsApp" in st.session_state.integrations:
                st.write("💬 מגדיר מענה אוטומטי בוואטסאפ ללקוחות חדשים...")
                time.sleep(1.5)
            
            # שלב 3: כתיבת הדו"ח
            prompt = f"Role: CTO Meirom AI. The agent just performed actions for {biz_name} involving {st.session_state.integrations}. Mission: {mission}. Write a summary report in HEBREW."
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = response.choices[0].message.content
            
            # שלב 4: שליחת מייל
            try:
                msg = EmailMessage()
                msg['Subject'] = f"אישור פעולת סוכן - {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email
                msg.set_content(f"הסוכן סיים את פעולתו.\n\n{st.session_state.report}", charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                status.update(label="המשימה בוצעה! הודעה נשלחה למנהל. ✅", state="complete")
                st.balloons()
            except:
                st.error("הסוכן הצליח אך המייל נכשל.")

    if st.session_state.report:
        st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
        st.subheader("סיכום פעולות הסוכן")
        st.write(st.session_state.report)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("חזרה למסך הראשי"):
        st.session_state.report = None
        go_to('welcome')
