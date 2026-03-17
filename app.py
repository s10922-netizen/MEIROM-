import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

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

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב כללי ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# --- עמוד 1: עמוד פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>ברוכים הבאים לעתיד של ניהול העסקים. אנחנו מטמיעים בינה מלאכותית שהופכת לחלק בלתי נפרד מהצוות שלך.</p>", unsafe_allow_html=True)
    
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=200)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("בואו נתחיל - לבחירת מסלול הטמעה 🚀", use_container_width=True):
            go_to('options')

# --- עמוד 2: בחירת אופציות ומסלולים ---
elif st.session_state.page == 'options':
    st.title("🛠️ בחרי את רמת ההטמעה")
    st.write("כדי שה-AI יתאים לעסק שלך בצורה מושלמת, בחרי את המסלול המתאים:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Basic")
        st.write("ייעוץ ואוטומציה בסיסית")
        if st.button("בחר בייסיק", key="btn_basic"):
            st.session_state.plan = "Basic"
            go_to('main')
            
    with col2:
        st.subheader("Pro")
        st.write("הטמעת סוכני AI פעילים")
        if st.button("בחר פרו ⭐", key="btn_pro"):
            st.session_state.plan = "Pro"
            go_to('main')
            
    with col3:
        st.subheader("Enterprise")
        st.write("מחלקה דיגיטלית מלאה")
        if st.button("בחר אנטרפרייז", key="btn_ent"):
            st.session_state.plan = "Enterprise"
            go_to('main')
            
    if st.button("⬅️ חזרה לדף הבית"):
        go_to('welcome')

# --- עמוד 3: טופס ההטמעה והפעלת ה-AI ---
elif st.session_state.page == 'main':
    st.title(f"⚙️ הטמעת מערכת: {st.session_state.plan}")
    st.write(f"הגדרת תשתית Meirom AI עבור העסק שלך.")
    
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל למשלוח הדו''ח")
        challenge = st.text_area("תארי את הצוואר בקבוק בעסק (מה היית רוצה שה-AI ינהל?)")
        
        submit = st.form_submit_button("הפעל הטמעה סופית ⚡")
        
    if submit:
        if biz_name and challenge and biz_email:
            with st.spinner("ה-AI של Meirom Solutions מבצע הטמעה..."):
                try:
                    prompt = f"Role: CTO of Meirom AI Solutions. Goal: Implement AI for {biz_name} under {st.session_state.plan} plan. Issue: {challenge}. Provide a monthly implementation report in Hebrew."
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4
                    )
                    report = response.choices[0].message.content
                    
                    # שליחת מייל (נשאר אותו דבר)
                    msg = EmailMessage()
                    msg.set_content(f"שלום!\nהוטמעה מערכת {st.session_state.plan} עבור {biz_name}.\n\nדו''ח:\n{report}", charset='utf-8')
                    msg['Subject'] = f"אישור הטמעה - Meirom AI"
                    msg['From'] = MY_EMAIL
                    msg['To'] = biz_email
                    
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(MY_EMAIL, APP_PASSWORD)
                        smtp.send_message(msg)
                        
                    st.success("ההטמעה הושלמה! המייל נשלח.")
                    st.balloons()
                    st.markdown(report)
                    
                except Exception as e:
                    st.error(f"שגיאה: {e}")
                    
    if st.button("⬅️ חזרה לבחירת מסלול"):
        go_to('options')
