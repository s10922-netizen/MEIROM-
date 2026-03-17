import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("חסר מפתח GROQ_KEY ב-Secrets!")

# --- הגדרות אימייל (שלך) ---
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢")

# --- עמודי המערכת ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    if st.button("כניסה למערכת 🚀", use_container_width=True): go_to('options')

elif st.session_state.page == 'options':
    st.title("💳 בחירת מסלול")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with col2:
        if st.button("Pro"): st.session_state.plan = "Pro"; go_to('payment')
    with col3:
        if st.button("Enterprise"): st.session_state.plan = "Enterprise"; go_to('payment')

elif st.session_state.page == 'payment':
    st.title("🔐 תשלום מאובטח")
    if st.button("אשר תשלום והפעל AI ✅", use_container_width=True): go_to('main')

elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    
    with st.form("ai_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל למשלוח הדו''ח")
        challenge = st.text_area("מה האתגר העסקי?")
        submit = st.form_submit_button("הפעל סוכן ושילח מייל ⚡")

    if submit and biz_name and challenge and biz_email:
        with st.status("הסוכן של מירום מייצר ושולח את הדו''ח...", expanded=True) as status:
            # 1. יצירת הדו"ח
            prompt = f"Write a professional AI implementation report in HEBREW for {biz_name}. Plan: {st.session_state.plan}. Challenge: {challenge}."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            report = response.choices[0].message.content
            st.session_state.report = report
            
            # 2. שליחת המייל באופן אוטומטי
            try:
                msg = EmailMessage()
                msg.set_content(f"שלום {biz_name},\n\nהשלמנו את ניתוח ה-AI עבור העסק שלך.\n\nלהלן הדו''ח המלא:\n\n{report}\n\nבברכה,\nצוות Meirom AI Solutions", charset='utf-8')
                msg['Subject'] = f"דו''ח הטמעה רשמי - {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                status.update(label="הדו''ח נוצר והמייל נשלח בהצלחה! ✅", state="complete")
                st.balloons()
            except Exception as e:
                st.error(f"הדו''ח נוצר אך המייל נכשל: {e}")

    if st.session_state.report:
        st.markdown("---")
        st.subheader("📋 הדו''ח שנוצר:")
        st.write(st.session_state.report)
        st.download_button("📥 הורד דו''ח (TXT)", data=st.session_state.report, file_name="Report.txt")

    if st.button("חזרה לדף הבית"):
        st.session_state.report = None
        go_to('welcome')
