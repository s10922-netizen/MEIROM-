import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time
from fpdf import FPDF
import io

# --- הגדרות חיבור ואבטחה ---
GROQ_API_KEY = st.secrets["GROQ_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"
client = Groq(api_key=GROQ_API_KEY)

# --- ניהול הניווט והמידע ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'report' not in st.session_state:
    st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- פונקציה לייצור PDF (השדרוג החדש!) ---
def create_pdf(biz_name, plan, content):
    pdf = FPDF()
    pdf.add_page()
    
    # הוספת כותרת מעוצבת
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(30, 58, 138) # כחול Meirom
    pdf.cell(0, 20, "Meirom AI Solutions", ln=True, align='C')
    
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Implementation Report for: {biz_name}", ln=True, align='C')
    pdf.cell(0, 10, f"Plan: {plan}", ln=True, align='C')
    pdf.ln(10)
    
    # הוספת תוכן הדו"ח
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    
    # ניקוי תווים מיוחדים שיכולים לשבור את ה-PDF
    clean_content = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_content)
    
    return pdf.output()

# --- עיצוב כללי ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# --- מבנה הדפים (Welcome, Options, Payment) נשאר דומה, מעדכן רק את ה-Main ---

if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=150)
    if st.button("כניסה למערכת 🚀", use_container_width=True):
        go_to('options')

elif st.session_state.page == 'options':
    st.title("💳 בחר מסלול מנוי")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Basic (250₪)"):
            st.session_state.plan = "Basic"; go_to('main')
    with col2:
        if st.button("Pro (750₪)"):
            st.session_state.plan = "Pro"; go_to('main')
    with col3:
        if st.button("Enterprise (2,500₪)"):
            st.session_state.plan = "Enterprise"; go_to('main')

elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל למשלוח הדו''ח המעוצב")
        challenge = st.text_area("פרטי המשימה להטמעה")
        submit = st.form_submit_button("הפעל סוכן AI והפק PDF ⚡")
        
    if submit:
        if biz_name and challenge and biz_email:
            with st.status("מייצר דוח PDF מקצועי...", expanded=True) as status:
                prompt = f"Role: CTO Meirom AI. Create a professional English implementation report for {biz_name} on {st.session_state.plan} plan. Task: {challenge}. Structure it with: 1. Executive Summary, 2. Weekly Roadmap, 3. ROI Analysis."
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.session_state.report = response.choices[0].message.content
                
                # שליחת מייל (כמו קודם)
                msg = EmailMessage()
                msg.set_content(f"Attached is your professional report from Meirom AI Solutions.\n\nBusiness: {biz_name}")
                msg['Subject'] = f"Official Report - {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                status.update(label="הדו''ח מוכן להורדה!", state="complete")
                st.balloons()

    if st.session_state.report:
        st.markdown("### 📥 הדו''ח המקצועי שלך מוכן")
        
        # יצירת הקובץ להורדה
        pdf_data = create_pdf(biz_name, st.session_state.plan, st.session_state.report)
        
        st.download_button(
            label="📥 הורד דו''ח PDF רשמי",
            data=pdf_data,
            file_name=f"Meirom_AI_Report_{biz_name}.pdf",
            mime="application/pdf"
        )
        
        with st.expander("צפייה בתוכן הדו''ח"):
            st.markdown(st.session_state.report)

    if st.button("חזרה לתפריט"):
        go_to('welcome')
