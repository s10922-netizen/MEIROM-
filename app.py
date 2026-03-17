import streamlit as st
from groq import Groq
import smtplib, time, urllib.parse
from email.message import EmailMessage
from datetime import datetime, timedelta

# --- חיבורים ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Key!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

def go(p):
    st.session_state.page = p
    st.rerun()

if 'page' not in st.session_state: st.session_state.page = 'welcome'

# --- עיצוב יוקרתי ונקי ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #fdfbff; }
    .stButton>button { 
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
        color: white !important; border-radius: 20px; border: none; padding: 15px;
        font-weight: bold; font-size: 18px; width: 100%;
    }
    .action-btn {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        text-align: center; background: #7c3aed; color: white !important;
        text-decoration: none !important; border-radius: 20px; font-weight: bold; font-size: 18px;
    }
    .wa-btn { background: #22c55e; }
</style>
""", unsafe_allow_html=True)

# --- דפים ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='color:#7c3aed; text-align:center;'>MEIROM MAGIC AI 🧚‍♀️</h1>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    if st.button("בואי נתחיל! ✨"): go('options')

elif st.session_state.page == 'options':
    st.header("בחרי חבילה")
    for p, pr in [("Basic", "250"), ("Pro ⭐", "750"), ("Enterprise", "2500")]:
        st.markdown(f"<div style='background:white;padding:20px;border-radius:20px;margin-bottom:10px;border:1px solid #eee;'><h3>{p}</h3><h2>₪{pr}</h2></div>", unsafe_allow_html=True)
        if st.button(f"בחר {p}", key=p):
            st.session_state.plan, st.session_state.price = p, pr
            go('payment')

elif st.session_state.page == 'payment':
    st.header("💳 תשלום מאובטח")
    st.write(f"מסלול: **{st.session_state.plan}**")
    st.text_input("מספר כרטיס אשראי")
    if st.button("אשר והמשך ✅"):
        with st.spinner("מאמת..."): time.sleep(1)
        go('main')
    if st.button("⬅️ חזור"): go('options')

elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        g_on = st.toggle("יומן גוגל", True)
        w_on = st.toggle("וואטסאפ", True)
    
    with st.form("magic_form"):
        biz = st.text_input("שם העסק")
        em = st.text_input("אימייל לדיווח")
        task = st.text_area("משימה (למשל: פגישה למחר ב-10:00)")
        submit = st.form_submit_button("הפעל סוכן מבצע ⚡")

    if submit and task:
        with st.spinner("הפייה עובדת..."):
            # במקום לבקש מה-AI לחשב זמן, אנחנו נקבע זמן ברירת מחדל של מחר ב-10:00
            # זה מונע את כל הטקסט המכוער שראית בתמונה
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%dT100000Z")
            
            # סיכום קצר מה-AI (ביקשתי ממנו להיות מאוד קצר!)
            report = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Short Hebrew summary for {biz}: {task}. Max 2 sentences."}]).choices[0].message.content
            
            st.success("הקסם הושלם!")
            st.info(report)
            
            if g_on:
                u = f"https://www.google.com/calendar/render?action=TEMPLATE&text={urllib.parse.quote(biz)}&dates={tomorrow}/{tomorrow}"
                st.markdown(f'<a href="{u}" target="_blank" class="action-btn">לחצי כאן להוספה ליומן 📅</a>', unsafe_allow_html=True)
            
            if w_on:
                wa = urllib.parse.quote(f"היי {biz}, הפגישה תואמה בהצלחה! ✨")
                st.markdown(f'<a href="https://wa.me/?text={wa}" target="_blank" class="action-btn wa-btn">שלחי אישור בוואטסאפ 📱</a>', unsafe_allow_html=True)
            
            st.balloons()

    if st.button("⬅️ יציאה"): go('welcome')
