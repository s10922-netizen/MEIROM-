import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- הגדרות חיבור ---
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

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה פרימיום ---
st.set_page_config(page_title="Meirom AI Solutions", page_icon="🏢", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3 { color: #1e3a8a !important; text-align: center; }
    .app-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
        margin-bottom: 20px; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white !important; border: none !important;
        border-radius: 12px !important; font-weight: bold !important;
        width: 100%; height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# --- עמוד 1: פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color: #6366f1;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=180)
    st.write("מערכת אוטונומית להטמעת AI בעסקים")
    if st.button("כניסה למערכת 🚀"):
        go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- עמוד 2: בחירת מסלול (הצבעים חזרו!) ---
elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="app-card" style="border-top:5px solid #3b82f6;"><h3>Basic</h3><p>₪250</p></div>', unsafe_allow_html=True)
        if st.button("בחר Basic"):
            st.session_state.plan, st.session_state.price = "Basic", "250"
            go_to('payment')
            
    with c2:
        st.markdown('<div class="app-card" style="border-top:5px solid #22c55e;"><h3>Pro ⭐</h3><p>₪750</p></div>', unsafe_allow_html=True)
        if st.button("בחר Pro"):
            st.session_state.plan, st.session_state.price = "Pro", "750"
            go_to('payment')
            
    with c3:
        st.markdown('<div class="app-card" style="border-top:5px solid #eab308;"><h3>Enterprise</h3><p>₪2,500</p></div>', unsafe_allow_html=True)
        if st.button("בחר Enterprise"):
            st.session_state.plan, st.session_state.price = "Enterprise", "2,500"
            go_to('payment')

# --- עמוד 3: תשלום מלא ומעוצב ---
elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום מאובטח</h2>", unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write(f"מסלול: **{st.session_state.plan}** | סכום: **₪{st.session_state.price}**")
    st.text_input("מספר כרטיס", placeholder="0000 0000 0000 0000")
    colA, colB = st.columns(2)
    with colA: st.text_input("תוקף", placeholder="MM/YY")
    with colB: st.text_input("CVV", placeholder="000")
    if st.button("אשר תשלום ✅"):
        bar = st.progress(0)
        for i in range(101):
            time.sleep(0.01)
            bar.progress(i)
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)

# --- עמוד 4: מסוף השליטה (הסוכן) ---
elif st.session_state.page == 'main':
    st.markdown(f"<h2>מסוף שליטה: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    with st.form("agent_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לדו''ח")
        mission = st.text_area("אתגר להטמעה")
        if st.form_submit_button("הפעל סוכן מבצע ⚡"):
            if biz_name and mission:
                with st.status("Meirom AI מבצע הטמעה..."):
                    p = f"Professional report in HEBREW for {biz_name}. Mission: {mission}."
                    res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                    st.session_state.report = res.choices[0].message.content
                    # שליחת מייל
                    msg = EmailMessage()
                    msg['Subject'] = f"Report - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                    msg.set_content(st.session_state.report, charset='utf-8')
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                        s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                    st.success
