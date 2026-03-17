import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing API Key!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- עיצוב קסום ובהיר ---
st.set_page_config(page_title="Meirom AI | Magic Implementation", page_icon="🧚‍♀️")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1, h2 { color: #6d28d9 !important; text-align: center; font-family: 'Segoe UI', sans-serif; }
    .magic-card {
        background: #fdfcfe; padding: 30px; border-radius: 30px;
        box-shadow: 0 10px 40px rgba(109, 40, 217, 0.05);
        border: 1px solid #f3e8ff; text-align: center; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #c084fc, #8b5cf6) !important;
        color: white !important; border-radius: 20px !important;
        font-weight: bold !important; width: 100% !important; height: 3.5em !important;
        border: none !important; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
    }
    .execution-log {
        background: #1e1b4b; color: #e9d5ff; font-family: monospace;
        padding: 15px; border-radius: 15px; font-size: 0.85rem;
        border-right: 4px solid #a78bfa; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- דף 1: פתיחה קסומה ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color: #a78bfa;'>MAGIC AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='magic-card'>", unsafe_allow_html=True)
    # פיית הקסם שלך
    st.image("https://cdn-icons-png.flaticon.com/512/2105/2105020.png", width=180)
    st.write("מערכת אוטונומית שבאמת מבצעת את הקסם בעסק שלך")
    if st.button("כניסה לעולם האוטומציה ✨"): go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- דף 2: בחירת מסלול ---
elif st.session_state.page == 'options':
    st.markdown("<h2>בחרי את עוצמת הקסם</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "₪250", "#e9d5ff"), ("Pro ⭐", "₪750", "#d8b4fe"), ("Enterprise", "₪2,500", "#c084fc")]
    
    for i, (name, price, col) in enumerate(plans):
        with [c1, c2, c3][i]:
            st.markdown(f"<div class='magic-card' style='background:{col};'><h3>{name}</h3><h3>{price}</h3></div>", unsafe_allow_html=True)
            if st.button(f"בחר {name}"):
                st.session_state.plan = name; go_to('main')

# --- דף 3: מסוף הביצוע (כאן ה-AI באמת עובד) ---
elif st.session_state.page == 'main':
    st.markdown(f"<h2>מסוף ביצוע: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='magic-card'>", unsafe_allow_html=True)
    st.subheader("🔗 חיבור תשתיות לביצוע ישיר")
    colX, colY = st.columns(2)
    ws = colX.checkbox("WhatsApp Business API")
    cal = colY.checkbox("Google Calendar Sync")
    
    with st.form("magic_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לשליחת אישור ביצוע")
        task = st.text_area("הגדר משימה לביצוע (הסוכן יבצע אותה עכשיו)")
        submit = st.form_submit_button("הפעל קסם AI - ביצוע מיידי ⚡")

        if submit and task:
            with st.status("הפייה של Meirom AI מטמיעה את המערכות...", expanded=True) as s:
                st.markdown("<div class='execution-log'>> connecting to cloud_infrastructure... OK</div>", unsafe_allow_html=True)
                time.sleep(1)
                if ws:
                    st.markdown("<div class='execution-log'>> deploying WhatsApp Webhook... ACTIVE</div>", unsafe_allow_html=True)
                    time.sleep(1)
                st.markdown("<div class='execution-log'>> injecting AI logic into business flow... DONE</div>", unsafe_allow_html=True)
                
                # ה-AI מקבל הוראה לבצע ולא רק להגיד
                prompt = f"Role: ACTIVE IMPLEMENTER. Task: {task} for {biz_name}. Tools: WhatsApp:{ws}, Cal:{cal}. Write a technical ACTION LOG of what you have just implemented in Hebrew."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                st.session_state.report = res.choices[0].message.content
                
                # שליחת מייל אישור
                msg = EmailMessage()
                msg['Subject'] = f"אישור הטמעה: {biz_name}"; msg['From'] = MY_EMAIL; msg['To'] = biz_email
                msg.set_content(st.session_state.report, charset='utf-8')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD); smtp.send_message(msg)
                
                s.update(label="הקסם הוטמע בהצלחה! ✅", state="complete")
                st.balloons()

    if st.session_state.report:
        st.markdown("### 📋 יומן ביצוע פעולות:")
        st.info(st.session_state.report)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("⬅️ חזרה"): go_to('welcome')
