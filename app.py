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
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'report' not in st.session_state:
    st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- פונקציה לייצור PDF בעברית תקינה ---
def create_hebrew_pdf(biz_name, plan, content):
    pdf = FPDF()
    pdf.add_page()
    
    # טעינת הגופן שהעלית ל-GitHub
    try:
        pdf.add_font('HebrewFont', '', 'HebrewFont.ttf')
        pdf.set_font('HebrewFont', '', 16)
    except:
        # גיבוי למקרה שהקובץ לא נמצא
        pdf.set_font("Arial", size=12)

    # פונקציה פנימית לתיקון עברית הפוכה
    def fix(text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    # כותרת הדו"ח
    pdf.set_font('HebrewFont', '', 25)
    pdf.cell(0, 20, fix("Meirom AI Solutions - דו''ח הטמעה"), ln=True, align='C')
    pdf.ln(10)
    
    # פרטי לקוח
    pdf.set_font('HebrewFont', '', 14)
    pdf.multi_cell(0, 10, fix(f"עבור עסק: {biz_name}"), align='R')
    pdf.multi_cell(0, 10, fix(f"מסלול מנוי: {plan}"), align='R')
    pdf.ln(10)
    
    # תוכן הדו"ח מה-AI
    pdf.set_font('HebrewFont', '', 12)
    pdf.multi_cell(0, 10, fix(content), align='R')
    
    return pdf.output()

# --- עיצוב דפי האתר ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢")

# עמוד 1: פתיחה
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=150)
    if st.button("כניסה למערכת 🚀", use_container_width=True):
        go_to('options')

# עמוד 2: מחירים
elif st.session_state.page == 'options':
    st.title("💳 בחירת מסלול מנוי")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Basic (250₪)"): st.session_state.plan = "Basic"; go_to('payment')
    with col2:
        if st.button("Pro (750₪)"): st.session_state.plan = "Pro"; go_to('payment')
    with col3:
        if st.button("Enterprise (2,500₪)"): st.session_state.plan = "Enterprise"; go_to('payment')

# עמוד 3: תשלום
elif st.session_state.page == 'payment':
    st.title("🔐 תשלום מאובטח")
    st.write(f"מסלול נבחר: {st.session_state.plan}")
    if st.button("אישור תשלום (Demo) ✅"): go_to('main')

# עמוד 4: הטמעה ו-PDF
elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    
    with st.form("implementation_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל למשלוח הדו''ח")
        challenge = st.text_area("מה האתגר העסקי?")
        submit = st.form_submit_button("הפעל AI והפק PDF בעברית ⚡")

    if submit and biz_name and challenge:
        with st.status("מייצר דו''ח מפורט בעברית...", expanded=True):
            prompt = f"Role: CTO Meirom AI. Create a professional business implementation report IN HEBREW for {biz_name}. Plan: {st.session_state.plan}. Issue: {challenge}. Structure: 1. Summary, 2. Roadmap, 3. ROI."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.report = response.choices[0].message.content
            st.balloons()

    if st.session_state.report:
        st.success("הדו''ח מוכן!")
        pdf_bytes = create_hebrew_pdf(biz_name, st.session_state.plan, st.session_state.report)
        
        st.download_button(
            label="📥 הורד דו''ח PDF בעברית",
            data=pdf_bytes,
            file_name=f"Report_{biz_name}.pdf",
            mime="application/pdf"
        )
        with st.expander("צפה בדו''ח"):
            st.write(st.session_state.report)

    if st.button("חזרה לדף הבית"): go_to('welcome')
