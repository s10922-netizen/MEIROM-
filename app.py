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

# --- הגדרות אימייל ---
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט וזיכרון ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- עיצוב CSS מותאם אישית (הסוד לעיצוב יפה) ---
st.set_page_config(page_title="Meirom AI Solutions", page_icon="🏢", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .price-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-bottom: 10px;
    }
    .payment-box {
        background-color: #f8fafc;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: פתיחה (Welcome) ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A; font-size: 3.5rem;'>🏢 Meirom AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #475569;'>בונים את העתיד האוטונומי של העסק שלך</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", use_container_width=True)
        st.write("")
        if st.button("כניסה למערכת ההטמעה 🚀"):
            go_to('options')

# --- עמוד 2: בחירת מסלול (Options) ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>💳 בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="price-card" style="background-color: #E0F2FE;">', unsafe_allow_html=True)
        st.subheader("Basic")
        st.write("### 250₪")
        st.write("אוטומציה בסיסית")
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"; st.session_state.price = "250"; go_to('payment')
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="price-card" style="background-color: #DCFCE7; border: 2px solid #16A34A;">', unsafe_allow_html=True)
        st.subheader("Pro ⭐")
        st.write("### 750₪")
        st.write("סוכני AI פעילים")
        if st.button("בחר Pro"):
            st.session_state.plan = "Pro"; st.session_state.price = "750"; go_to('payment')
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col3:
        st.markdown('<div class="price-card" style="background-color: #FEF3C7;">', unsafe_allow_html=True)
        st.subheader("Enterprise")
        st.write("### 2,500₪")
        st.write("ניהול AI מלא")
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"; st.session_state.price = "2,500"; go_to('payment')
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⬅️ חזרה למסך הבית"): go_to('welcome')

# --- עמוד 3: תשלום (Payment) ---
elif st.session_state.page == 'payment':
    st.markdown(f"<h2 style='text-align: center;'>🔐 תשלום מאובטח: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center;'>עלות חודשית: {st.session_state.price}₪</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="payment-box">
            <h4 style="color: #1E3A8A; margin-bottom: 20px;">💳 פרטי אשראי לחיוב חודשי</h4>
            <div style="margin-bottom: 15px;">
                <label style="font-size: 14px;">מספר כרטיס</label>
                <input type="text" placeholder="0000 0000 0000 0000" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1;">
            </div>
            <div style="display: flex; gap: 15px;">
                <div style="flex: 1;">
                    <label style="font-size: 14px;">תוקף</label>
                    <input type="text" placeholder="MM/YY" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1;">
                </div>
                <div style="flex: 1;">
                    <label style="font-size: 14px;">CVV</label>
                    <input type="text" placeholder="123" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1;">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("אשר תשלום והפעל את המערכת ✅"):
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.success("התשלום אושר! המערכת מוכנה.")
        go_to('main')

# --- עמוד 4: הטמעה (Main) ---
elif st.session_state.page == 'main':
    st.title(f"⚙️ מרכז הטמעה: {st.session_state.plan}")
    
    with st.form("ai_logic"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל למשלוח הדו''ח")
        challenge = st.text_area("תארי את האתגר של העסק (מה ה-AI צריך לעשות?)")
        submit = st.form_submit_button("הפעל סוכן AI ושילח מייל ⚡")
    
    if submit and biz_name and challenge and biz_email:
        with st.status("Meirom AI בתהליך ניתוח ושליחה...", expanded=True) as status:
            # 1. AI Generation
            prompt = f"Create a professional AI implementation report in HEBREW for {biz_name}. Plan: {st.session_state.plan}. Challenge: {challenge}."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            report = response.choices[0].message.content
            st.session_state.report = report
            
            # 2. Email Sending
            try:
                msg = EmailMessage()
                msg.set_content(f"שלום {biz_name},\n\nהשלמנו את ניתוח ה-AI עבור העסק שלך.\n\n{report}", charset='utf-8')
                msg['Subject'] = f"דו''ח הטמעה רשמי - {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                status.update(label="הדו''ח מוכן והמייל נשלח! ✅", state="complete")
                st.balloons()
            except Exception as e:
                st.error(f"שגיאה בשליחת מייל: {e}")

    if st.session_state.report:
        st.markdown("---")
        st.subheader("📋 הדו''ח שנוצר:")
        st.write(st.session_state.report)
        st.download_button("📥 הורד דו''ח (TXT)", data=st.session_state.report, file_name=f"Meirom_AI_{biz_name}.txt")

    if st.button("⬅️ יציאה למסך הבית"):
        st.session_state.report = None
        go_to('welcome')
