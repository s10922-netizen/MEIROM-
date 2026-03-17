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
    st.markdown("<h1 style='padding-top:30px;'>MEIROM MAGIC AI</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # שימוש באייקון פייה איכותי ויציב
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2105/2105020.png", width=200)
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("ברוכה הבאה לעולם של אוטומציה קסומה")
        st.write("מפל של קסם AI שמטמיע את הפתרונות בעסק שלך.")
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
                    st.session_state.plan = name; go_to('payment')

# --- דף 3: תשלום ---
elif st.session_state.page == 'payment':
    st.header("תשלום מאובטח")
    with st.container(border=True):
        st.write(f"מסלול: **{st.session_state.plan}**")
        st.text_input("מספר כרטיס")
        c1, c2 = st.columns(2)
        c1.text_input("תוקף")
        c2.text_input("CVV")
        if st.button("אשר תשלום והפעל קסם ✅", use_container_width=True):
            bar = st.progress(0)
            for i in range(100): time.sleep(0.01); bar.progress(i + 1)
            go_to('main')

# --- דף 4: מסוף הביצוע ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ביצוע: {st.session_state.plan}")
    with st.container(border=True):
        st.subheader("🔗 חיבור תשתיות")
        ws = st.checkbox("WhatsApp API")
        cal = st.checkbox("Google Calendar")
        with st.form("magic_form"):
            biz_name = st.text_input("שם העסק")
            biz_email = st.text_input("אימייל לדו''ח")
            task = st.text_area("מה המשימה לביצוע?")
            if st.form_submit_button("הפעל סוכן מבצע ⚡"):
                if biz_name and task:
                    with st.status("הפייה מטמיעה את הקסם..."):
                        st.code("> Running magic_core_v18...")
                        p = f"Implementer summary for {biz_name}. Task: {task}. Tools: WS:{ws}, Cal:{cal}. REPORT ACTIONS IN HEBREW."
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                        st.session_state.report = res.choices[0].message.content
                        msg = EmailMessage()
                        msg['Subject'] = f"Action Log - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                        msg.set_content(st.session_state.report, charset='utf-8')
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                            s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                        st.balloons()
    if st.session_state.report:
        st.info(st.session_state.report)
    if st.button("⬅️ יציאה"): go_to('welcome')
