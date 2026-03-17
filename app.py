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

# --- ניהול הניווט והמידע (Session State) ---
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

# --- עיצוב כללי ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# --- עמוד 1: עמוד פתיחה (שדרוג עיצובי) ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>אנחנו לא רק מייעצים. אנחנו מטמיעים מערכות AI אוטונומיות שעובדות בשבילך 24/7.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=200)
        st.write("")
        if st.button("כניסה למערכת ההטמעה 🚀", use_container_width=True):
            go_to('options')

# --- עמוד 2: בחירת מסלול ומחירים ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>💳 בחירת מסלול מנוי חודשי</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### Basic")
        st.markdown("**250₪ / חודש**")
        st.write("ייעוץ חודשי + אוטומציית מייל")
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"
            st.session_state.price = "250"
            go_to('payment')
            
    with col2:
        st.success("### Pro ⭐")
        st.markdown("**750₪ / חודש**")
        st.write("3 סוכני AI פעילים + ניטור")
        if st.button("בחר Pro"):
            st.session_state.plan = "Pro"
            st.session_state.price = "750"
            go_to('payment')
            
    with col3:
        st.warning("### Enterprise")
        st.markdown("**2,500₪ / חודש**")
        st.write("ניהול AI מלא + פיתוח אישי")
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"
            st.session_state.price = "2,500"
            go_to('payment')

# --- עמוד 3: עמוד תשלום ---
elif st.session_state.page == 'payment':
    st.title("🔐 תשלום מאובטח")
    st.write(f"הנך נרשם למסלול **{st.session_state.plan}** בעלות חודשית של **{st.session_state.price}₪**.")
    
    st.markdown("""
        <div style="background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 2px solid #1E3A8A;">
            <h4 style="margin-top:0; color: #1E3A8A;">💳 פרטי תשלום (Simulation)</h4>
            <input type="text" placeholder="מספר כרטיס" style="width:100%; padding:10px; margin-bottom:10px; border-radius:5px; border:1px solid #ccc;">
            <div style="display:flex; gap:10px;">
                <input type="text" placeholder="תוקף" style="width:50%; padding:10px; border-radius:5px; border:1px solid #ccc;">
                <input type="text" placeholder="CVV" style="width:50%; padding:10px; border-radius:5px; border:1px solid #ccc;">
            </div>
            <p style="font-size: 12px; color: #666; margin-top: 10px;">🔒 התשלום מאובטח בתקן PCI-DSS</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("אשר תשלום והפעל את ה-AI ✅", use_container_width=True):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        st.success("התשלום עבר! המערכת מוכנה להטמעה.")
        go_to('main')

# --- עמוד 4: הטמעה וביצוע (השדרוג הגדול) ---
elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("מייל למשלוח קבצי ההטמעה")
        challenge = st.text_area("פרטי המשימה שה-AI צריך לנהל")
        submit = st.form_submit_button("הפעל סוכן AI ⚡")
        
    if submit:
        if biz_name and challenge and biz_email:
            with st.status("מבצע הטמעה טכנולוגית...", expanded=True) as status:
                st.write("מתחבר לשרתי Groq...")
                time.sleep(1)
                st.write(f"מנתח אתגרים עבור {biz_name}...")
                
                try:
                    # פרומפט עמוק יותר למנוי חודשי
                    prompt = f"Role: CTO Meirom AI. Plan: {st.session_state.plan}. Business: {biz_name}. Task: Implement AI for {challenge}. Provide a detailed 4-week implementation schedule in Hebrew. Include ROI estimates."
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4
                    )
                    st.session_state.report = response.choices[0].message.content
                    
                    st.write("מכין קבצי עבודה...")
                    # שליחת מייל
                    msg = EmailMessage()
                    msg.set_content(f"אישור הטמעה חודשי - Meirom AI\nעסק: {biz_name}\n\nדו''ח:\n{st.session_state.report}", charset='utf-8')
                    msg['Subject'] = f"מערכת Meirom AI הוטמעה בהצלחה - {biz_name}"
                    msg['From'] = MY_EMAIL
                    msg['To'] = biz_email
                    
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(MY_EMAIL, APP_PASSWORD)
                        smtp.send_message(msg)
                    
                    status.update(label="ההטמעה הושלמה בהצלחה!", state="complete", expanded=False)
                    st.balloons()
                except Exception as e:
                    st.error(f"שגיאה: {e}")

    # הצגת תוצאות ואפשרות הורדה (זה מה שהופך את זה ל"לא ראשוני")
    if st.session_state.report:
        st.markdown("### 📄 דו''ח הטמעה וקבצי עבודה")
        st.info("הדו''ח נשלח למייל שלך. ניתן גם להוריד עותק טקסט כאן:")
        
        st.download_button(
            label="הורד תוכנית עבודה (TXT)",
            data=st.session_state.report,
            file_name=f"Meirom_AI_{biz_name}.txt",
            mime="text/plain"
        )
        
        with st.expander("צפייה בדו''ח המלא"):
            st.markdown(st.session_state.report)

    if st.button("⬅️ יציאה וניתוק מנוי"):
        st.session_state.report = None
        go_to('welcome')
