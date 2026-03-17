import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- הגדרות חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing GROQ_KEY in Secrets!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ואחסון מצב (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'price' not in st.session_state:
    st.session_state.price = "0"
if 'tools' not in st.session_state:
    st.session_state.tools = []
if 'report' not in st.session_state:
    st.session_state.report = None

# פונקציה למעבר בין דפים
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה בהיר ונעים (מבוסס על "כרטיסים") ---
st.set_page_config(page_title="Meirom AI | Magical Integration", page_icon="🧚‍♀️", layout="centered")

# הגדרות CSS גלובליות
st.markdown("""
<style>
    /* רקע בהיר ונעים */
    .stApp { background-color: #f8fafc; }
    
    /* כותרות */
    h1, h2, h3 { color: #1e3a8a !important; text-align: center; }
    
    /* כרטיס אפליקציה */
    .app-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* כפתור בהיר ונעים */
    .stButton>button {
        background: linear-gradient(135deg, #a78bfa, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3.5em !important;
    }
</style>
""", unsafe_allow_html=True)

# === עמוד 1: פתיחה ===
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color: #8b5cf6;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    # שינוי התמונה לפייה קסומה
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=180)
    st.write("מערכת אוטונומית להטמעת AI בעסק שלך")
    st.write("חוויה בהירה, נעימה וקסומה")
    if st.button("בואי נתחיל! 🚀"):
        go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# === עמוד 2: בחירת מסלול (עם המחירים והצבעים!) ===
elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # כרטיס Basic כחול
        st.markdown("<div class='app-card' style='border-top: 5px solid #3b82f6;'>", unsafe_allow_html=True)
        st.markdown("<h3>Basic</h3><h3>₪250</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"):
            st.session_state.plan, st.session_state.price = "Basic", "250"
            go_to('payment')
            
    with col2:
        # כרטיס Pro ירוק
        st.markdown("<div class='app-card' style='border-top: 5px solid #22c55e;'>", unsafe_allow_html=True)
        st.markdown("<h3>Pro ⭐</h3><h3>₪750</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"):
            st.session_state.plan, st.session_state.price = "Pro", "750"
            go_to('payment')
            
    with col3:
        # כרטיס Enterprise זהב
        st.markdown("<div class='app-card' style='border-top: 5px solid #eab308;'>", unsafe_allow_html=True)
        st.markdown("<h3>Enterprise</h3><h3>₪2,500</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"):
            st.session_state.plan, st.session_state.price = "Enterprise", "2,500"
            go_to('payment')
    
    st.write("")
    if st.button("⬅️ חזרה לדף הבית"):
        go_to('welcome')

# === עמוד 3: תשלום מלא ===
elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום מאובטח</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.write(f"מסלול: **{st.session_state.plan}** | סכום: **₪{st.session_state.price}**")
    
    # טופס אשראי מלא
    st.text_input("מספר כרטיס", placeholder="0000 0000 0000 0000")
    colA, colB = st.columns(2)
    with colA:
        st.text_input("תוקף", placeholder="MM/YY")
    with colB:
        st.text_input("CVV", placeholder="000")
    
    st.write("")
    if st.button("אשר תשלום ✅"):
        bar = st.progress(0)
        # סימולציית טעינה של תשלום
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.success("התשלום עבר בהצלחה!")
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("⬅️ חזרה למסלולים"):
        go_to('options')

# === עמוד 4: מסוף השליטה (הסוכן) ===
elif st.session_state.page == 'main':
    st.markdown(f"<h2>מסוף ניהול: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    
    # חיבור כלים
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader("🔗 חיבור כלים")
    c1, c2, c3 = st.columns(3)
    with c1: ws = st.checkbox("WhatsApp")
    with c2: cal = st.checkbox("Calendar")
    with c3: shop = st.checkbox("Shopify")
    # עדכון רשימת הכלים ב-Session State
    if ws: st.session_state.tools.append("WhatsApp")
    if cal: st.session_state.tools.append("Calendar")
    st.markdown("</div>", unsafe_allow_html=True)

    # טופס הסוכן
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    with st.form("agent_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לשליחת הדו''ח")
        mission = st.text_area("מה המשימה להטמעה?")
        submit = st.form_submit_button("הפעל סוכן מבצע ⚡")

        if submit and biz_name and mission:
            with st.status("סוכן Meirom AI עובד..."):
                p = f"Report in HEBREW for {biz_name}. Task: {mission}. Tools used: {st.session_state.tools}."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                st.session_state.report = res.choices[0].message.content
                
                # שליחת מייל
                msg = EmailMessage()
                msg['Subject'] = f"דו''ח הטמעה - {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(st.session_state.report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                    s.login(MY_EMAIL, APP_PASSWORD); s.send_message(msg)
                
                st.success("המשימה הושלמה!"); st.balloons()

    if st.session_state.report:
        st.markdown("---")
        st.write(st.session_state.report)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("⬅️ יציאה לדף הבית"):
        st.session_state.report = None
        go_to('welcome')
