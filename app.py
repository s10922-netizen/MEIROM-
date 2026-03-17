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
if 'price' not in st.session_state:
    st.session_state.price = "0"
if 'report' not in st.session_state:
    st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- פונקציה לייצור PDF בעברית (מתוקנת ובטוחה) ---
def create_hebrew_pdf(biz_name, plan, content):
    pdf = FPDF()
    pdf.add_page()
    
    # פונקציה פנימית לתיקון עברית הפוכה
    def fix(text):
        if not text: return ""
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    try:
        # טעינת הגופן - בודק אם הוא קיים לפני השימוש
        pdf.add_font('HebrewFont', '', 'HebrewFont.ttf')
        pdf.set_font('HebrewFont', '', 25)
        pdf.cell(0, 20, fix("Meirom AI Solutions - דו''ח הטמעה"), ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('HebrewFont', '', 14)
    except:
        # אם יש תקלה בגופן, משתמש ב-Arial כברירת מחדל כדי שהאתר לא יקרוס
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 20, "Meirom AI Report (Font Error - Hebrew)", ln=True, align='C')
        pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, fix(f"עבור עסק: {biz_name}"), align='R')
    pdf.multi_cell(0, 10, fix(f"מסלול מנוי: {plan}"), align='R')
    pdf.ln(5)
    pdf.multi_cell(0, 10, fix(content), align='R')
    
    return pdf.output()

# --- עיצוב האתר ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# עמוד 1: פתיחה (החזרנו את העיצוב!)
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>אנחנו מטמיעים בינה מלאכותית שהופכת לחלק בלתי נפרד מהצוות שלך.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=200)
        if st.button("כניסה למערכת ההטמעה 🚀", use_container_width=True):
            go_to('options')

# עמוד 2: בחירת מסלול ומחירים (החזרנו את הצבעים!)
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>💳 בחירת מסלול מנוי חודשי</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### Basic\n**250₪ / חודש**\nייעוץ ואוטומציה בסיסית")
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"; st.session_state.price = "250"; go_to('payment')
    with col2:
        st.success("### Pro ⭐\n**750₪ / חודש**\nסוכני AI פעילים וניטור")
        if st.button("בחר Pro"):
            st.session_state.plan = "Pro"; st.session_state.price = "750"; go_to('payment')
    with col3:
        st.warning("### Enterprise\n**2,500₪ / חודש**\nניהול AI מלא ופיתוח אישי")
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"; st.session_state.price = "2,500"; go_to('payment')
    
    if st.button("⬅️ חזרה לדף הבית"): go_to('welcome')

# עמוד 3: תשלום מעוצב (החזרנו את הטופס!)
elif st.session_state.page == 'payment':
    st.title("🔐 תשלום מאובטח")
    st.write(f"הנך נרשם למסלול **{st.session_state.plan}** בעלות של **{st.session_state.price}₪**.")
    
    st.markdown("""
        <div style="background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 2px solid #1E3A8A; margin-bottom: 20px;">
            <h4 style="margin-top:0; color: #1E3A8A;">💳 פרטי אשראי (סימולציה)</h4>
            <input type="text" placeholder="מספר כרטיס" style="width:100%; padding:10px; margin-bottom:10px; border-radius:5px; border:1px solid #ccc;">
            <div style="display:flex; gap:10px;">
                <input type="text" placeholder="תוקף" style="width:50%; padding:10px; border-radius:5px; border:1px solid #ccc;">
                <input type="text" placeholder="CVV" style="width:50%; padding:10px; border-radius:5px; border:1px solid #ccc;">
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("אשר תשלום והפעל את ה-AI ✅", use_container_width=True):
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01); bar.progress(i + 1)
        st.success("התשלום עבר בהצלחה!")
        go_to('main')

# עמוד 4: הטמעה ו-PDF
elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל למשלוח הדו''ח")
        challenge = st.text_area("פרטי המשימה להטמעה")
        submit = st.form_submit_button("הפעל סוכן AI והפק PDF בעברית ⚡")
        
    if submit and biz_name and challenge:
        with st.status("מייצר דוח PDF מקצועי בעברית...", expanded=True) as status:
            prompt = f"Role: CTO Meirom AI. Create a professional implementation report IN HEBREW for {biz_name}. Plan: {st.session_state.plan}. Task: {challenge}. Structure: Summary, Roadmap, ROI."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.report = response.choices[0].message.content
            status.update(label="ההטמעה הושלמה!", state="complete")
            st.balloons()

    if st.session_state.report:
        st.markdown("### 📥 הדו''ח המקצועי שלך מוכן")
        pdf_bytes = create_hebrew_pdf(biz_name, st.session_state.plan, st.session_state.report)
        st.download_button(label="📥 הורד דו''ח PDF רשמי", data=pdf_bytes, file_name="Meirom_AI_Report.pdf", mime="application/pdf")
        with st.expander("צפייה בתוכן הדו''ח"):
            st.write(st.session_state.report)

    if st.button("⬅️ יציאה למסך הבית"):
        st.session_state.report = None; go_to('welcome')
