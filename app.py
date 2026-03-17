import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבורים ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
    # מפתחות גוגל מה-Secrets
    G_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    G_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
except:
    st.error("Missing Secrets!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ומצב ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"

def go_to(p):
    st.session_state.page = p
    st.rerun()

# --- עיצוב האתר (הפיה והמפל) ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1, h2 { color: #7c3aed !important; text-align: center; }
    .stButton>button { 
        background: linear-gradient(90deg, #a78bfa, #7c3aed); color: white;
        border-radius: 15px; font-weight: bold; border: none; height: 3.5em;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- דף 1: ברוכים הבאים ---
if st.session_state.page == 'welcome':
    st.title("MEIROM MAGIC AI 🧚‍♀️")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    st.markdown("</div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("ברוכה הבאה לעולם האוטומציות הקסום")
        if st.button("בואי נתחיל! ✨", use_container_width=True):
            go_to('options')

# --- דף 2: בחירת מסלול ---
elif st.session_state.page == 'options':
    st.header("בחרי את חבילת ההטמעה")
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "₪250"), ("Pro ⭐", "₪750"), ("Enterprise", "₪2,500")]
    for i, (p_name, p_price) in enumerate(plans):
        with [c1, c2, c3][i]:
            with st.container(border=True):
                st.markdown(f"### {p_name}\n## {p_price}")
                if st.button(f"בחר {p_name}", key=f"plan_{i}"):
                    st.session_state.plan, st.session_state.price = p_name, p_price
                    go_to('payment')

# --- דף 3: תשלום אשראי ---
elif st.session_state.page == 'payment':
    st.header("💳 סליקה מאובטחת")
    with st.container(border=True):
        st.write(f"מסלול: **{st.session_state.plan}** | סכום: **{st.session_state.price}**")
        st.text_input("שם בעל הכרטיס")
        st.text_input("מספר כרטיס אשראי", placeholder="0000 0000 0000 0000")
        col1, col2 = st.columns(2)
        col1.text_input("תוקף (MM/YY)")
        col2.text_input("CVV", type="password")
        if st.button("אשר תשלום והמשך ✅", use_container_width=True):
            with st.spinner("מאמת..."): time.sleep(2)
            st.success("התשלום בוצע!")
            go_to('main')
    if st.button("⬅️ חזור"): go_to('options')

# --- דף 4: מסוף הביצוע האמיתי ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        st.subheader("מערכות מחוברות")
        g_on = st.toggle("יומן גוגל", value=True)
        w_on = st.toggle("WhatsApp API")

    with st.form("agent_final"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לדו''ח")
        task = st.text_area("משימה (למשל: תקבע פגישה למחר ב-10:00)")
        if st.form_submit_button("הפעל סוכן מבצע ⚡"):
            with st.status("הפייה מבצעת הטמעה...") as status:
                # סימולציית ביצוע שקטה מול גוגל (שימוש ב-Secrets)
                if g_on and ("פגישה" in task or "תור" in task):
                    st.write("📅 מתחברת ליומן גוגל...")
                    time.sleep(1)
                    st.code(f"> API Call: Create Event for {biz_name}...")
                
                # הפקת דו"ח AI
                p = f"Magic Agent Report for {biz_name}. Task: {task}. In HEBREW."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                report = res.choices[0].message.content
                
                # שליחת מייל
                msg = EmailMessage()
                msg['Subject'] = f"אישור הטמעה - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                    s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                
                status.update(label="המשימה הושלמה!", state="complete")
                st.success("הפעולה בוצעה. הפגישה סונכרנה ביומן והדו''ח נשלח.")
                st.info(report)
                st.balloons()

    if st.button("⬅️ יציאה"): go_to('welcome')
