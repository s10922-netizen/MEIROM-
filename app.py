import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
from bidi.algorithm import get_display
import arabic_reshaper
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

# --- פונקציה לייצור PDF בטוחה לחלוטין ---
def create_safe_pdf(biz_name, plan, content):
    pdf = FPDF()
    pdf.add_page()
    
    # ניסיון לטעון עברית, אם נכשל - עובר לאנגלית בטוחה כדי לא להקריס
    try:
        pdf.add_font('HebrewFont', '', 'HebrewFont.ttf')
        pdf.set_font('HebrewFont', '', 16)
        def fix(t): return get_display(arabic_reshaper.reshape(t))
        pdf.cell(0, 10, fix("Meirom AI Solutions - דו''ח הטמעה"), ln=True, align='C')
        pdf.ln(10)
        pdf.multi_cell(0, 10, fix(f"עסק: {biz_name}"), align='R')
        pdf.multi_cell(0, 10, fix(content), align='R')
    except:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Meirom AI Solutions - Implementation Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Business: {biz_name}")
        pdf.multi_cell(0, 10, f"Plan: {plan}")
        pdf.ln(5)
        # ניקוי תווים לא לטיניים כדי למנוע את השגיאה שראינו בתמונה
        clean_content = content.encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 10, clean_content)
    
    return pdf.output()

# --- עיצוב האתר ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# עמוד 1: פתיחה
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=150)
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
    st.write(f"מסלול: {st.session_state.plan} | עלות: {st.session_state.price}₪")
    st.markdown('<div style="background:#f0f2f6;padding:20px;border-radius:15px;border:2px solid #1E3A8A;"><h4>💳 פרטי אשראי</h4><input type="text" placeholder="Card Number" style="width:100%;padding:10px;margin-bottom:10px;"></div>', unsafe_allow_html=True)
    if st.button("אשר תשלום והמשך ✅", use_container_width=True):
        bar = st.progress(0)
        for i in range(100): time.sleep(0.01); bar.progress(i + 1)
        go_to('main')

# עמוד 4: הטמעה
elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל למשלוח")
        challenge = st.text_area("פרטי המשימה")
        submit = st.form_submit_button("הפעל סוכן AI והפק דו''ח ⚡")
        
    if submit and biz_name and challenge:
        with st.status("מייצר דוח AI...", expanded=True):
            prompt = f"Write a professional report for {biz_name}. Plan: {st.session_state.plan}. Task: {challenge}. Structure: Summary, Roadmap, ROI."
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = response.choices[0].message.content
            st.balloons()

    if st.session_state.report:
        st.success("הדו''ח מוכן!")
        pdf_bytes = create_safe_pdf(biz_name, st.session_state.plan, st.session_state.report)
        st.download_button("📥 הורד דו''ח PDF רשמי", data=pdf_bytes, file_name="Meirom_Report.pdf", mime="application/pdf")
        with st.expander("צפה בדו''ח"): st.write(st.session_state.report)

    if st.button("⬅️ חזרה לדף הבית"): go_to('welcome')
