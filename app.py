import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- הגדרות חיבור ואבטחה ---
GROQ_API_KEY = st.secrets["GROQ_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"
client = Groq(api_key=GROQ_API_KEY)

# --- ניהול הניווט (Session State) ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב האתר ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# עמוד 1: פתיחה
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>פתרונות בינה מלאכותית מתקדמים לעסקים קטנים ובינוניים</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=200)
        if st.button("כניסה למערכת ההטמעה 🚀", use_container_width=True):
            go_to('options')

# עמוד 2: בחירת מסלול ומחירים
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>💳 בחירת מסלול מנוי</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### Basic\n250₪")
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"; st.session_state.price = "250"; go_to('payment')
    with col2:
        st.success("### Pro ⭐\n750₪")
        if st.button("בחר Pro"):
            st.session_state.plan = "Pro"; st.session_state.price = "750"; go_to('payment')
    with col3:
        st.warning("### Enterprise\n2,500₪")
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"; st.session_state.price = "2,500"; go_to('payment')

# עמוד 3: תשלום מעוצב
elif st.session_state.page == 'payment':
    st.title("🔐 תשלום מאובטח")
    st.write(f"מסלול: {st.session_state.plan} | עלות חודשית: {st.session_state.price}₪")
    
    st.markdown("""
        <div style="background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 2px solid #1E3A8A; margin-bottom: 20px;">
            <h4 style="margin-top:0; color: #1E3A8A;">💳 פרטי אשראי</h4>
            <input type="text" placeholder="Card Number" style="width:100%; padding:10px; margin-bottom:10px;">
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("אשר תשלום והמשך ✅", use_container_width=True):
        bar = st.progress(0)
        for i in range(100): time.sleep(0.01); bar.progress(i + 1)
        go_to('main')

# עמוד 4: הטמעה (ללא PDF שגורם לקריסות - במקום זה הורדת טקסט נקייה)
elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל למשלוח")
        challenge = st.text_area("פרטי המשימה להטמעה")
        submit = st.form_submit_button("הפעל סוכן AI ⚡")
        
    if submit and biz_name and challenge:
        with st.status("ה-AI של מירום מנתח את העסק...", expanded=True):
            prompt = f"Role: CTO Meirom AI. Create a professional implementation report IN HEBREW for {biz_name}. Plan: {st.session_state.plan}. Task: {challenge}. Structure: Summary, Roadmap, ROI."
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = response.choices[0].message.content
            st.balloons()

    if st.session_state.report:
        st.success("הטמעת ה-AI הושלמה בהצלחה!")
        
        # פתרון חלופי ומגניב במקום ה-PDF הבעייתי: הורדת קובץ טקסט מעוצב
        st.download_button(
            label="📥 הורד דו''ח הטמעה רשמי (TXT)",
            data=st.session_state.report,
            file_name=f"Meirom_AI_{biz_name}.txt",
            mime="text/plain"
        )
        
        with st.expander("צפה בדו''ח המלא כאן"):
            st.write(st.session_state.report)

    if st.button("⬅️ חזרה לדף הבית"):
        st.session_state.report = None
        go_to('welcome')
