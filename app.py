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

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- פצצת CSS - זה מה שישנה הכל באמת ---
st.set_page_config(page_title="Meirom AI | Enterprise", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* שינוי צבע הרקע של כל האפליקציה */
    [data-testid="stAppViewContainer"] {
        background-color: #050a18;
        background-image: radial-gradient(circle at top right, #1e3a8a 0%, #050a18 40%);
        color: white;
    }
    
    /* שינוי צבע הכותרות */
    h1, h2, h3, h4, p, span, label {
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* עיצוב כפתורים מחדש */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }

    /* עיצוב כרטיסי המחיר */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    /* תיבות טקסט */
    .stTextInput input, .stTextArea textarea {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #1e40af !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-top: 50px;'>MEIROM <span style='color: #3b82f6;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5rem; opacity: 0.8;'>מערכות בינה מלאכותית אוטונומיות לעסקים</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png")
        if st.button("התחל עכשיו 🚀", use_container_width=True):
            go_to('options')

# --- עמוד 2: Options ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; border:1px solid #3b82f6; text-align:center;'><h3>Basic</h3><h2>₪250</h2></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"): st.session_state.plan = "Basic"; go_to('payment')
    with c2:
        st.markdown("<div style='background:rgba(255,255,255,0.1); padding:20px; border-radius:15px; border:2px solid #3b82f6; text-align:center;'><h3>Pro ⭐</h3><h2>₪750</h2></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"): st.session_state.plan = "Pro"; go_to('payment')
    with c3:
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; border:1px solid #3b82f6; text-align:center;'><h3>Enterprise</h3><h2>₪2,500</h2></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"): st.session_state.plan = "Enterprise"; go_to('payment')

# --- עמוד 3: Payment ---
elif st.session_state.page == 'payment':
    st.markdown("<h2 style='text-align: center;'>תשלום מאובטח</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#0f172a; padding:30px; border-radius:20px; border:1px solid #3b82f6;'><p>מסלול: {st.session_state.plan}</p></div>", unsafe_allow_html=True)
    
    st.text_input("מספר כרטיס")
    if st.button("בצע תשלום ✅", use_container_width=True):
        with st.spinner("מאמת נתונים..."): time.sleep(1)
        go_to('main')

# --- עמוד 4: Main ---
elif st.session_state.page == 'main':
    st.title(f"מסוף ניהול: {st.session_state.plan}")
    
    with st.container():
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לשליחת הדו''ח")
        challenge = st.text_area("מה האתגר לפתרון?")
        submit = st.button("הפעל סוכן AI ⚡")

    if submit and biz_name and challenge and biz_email:
        with st.status("מנתח ארכיטקטורה עסקית...", expanded=True) as status:
            prompt = f"Write a professional AI implementation report in HEBREW for {biz_name}. Plan: {st.session_state.plan}. Challenge: {challenge}."
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            report = response.choices[0].message.content
            st.session_state.report = report
            
            # שליחת מייל HTML
            try:
                msg = EmailMessage()
                msg['Subject'] = f"Meirom AI | דו''ח רשמי עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email
                msg.set_content(f"שלום,\n\nמצורף הדו''ח שלך:\n\n{report}", charset='utf-8')
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                status.update(label="הניתוח הושלם והמייל נשלח! ✅", state="complete")
                st.balloons()
            except:
                st.error("הדו''ח נוצר אך הייתה שגיאה בשליחת המייל.")

    if st.session_state.report:
        st.markdown("---")
        st.write(st.session_state.report)
        st.download_button("הורד קובץ TXT", data=st.session_state.report, file_name="Meirom_Report.txt")

    if st.button("יציאה מהמערכת"):
        st.session_state.report = None
        go_to('welcome')
