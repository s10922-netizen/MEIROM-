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
if 'price' not in st.session_state:
    st.session_state.price = "0"

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב כללי ---
st.set_page_config(page_title="Meirom AI Enterprise", page_icon="🏢", layout="centered")

# --- עמוד 1: עמוד פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center;'>🏢 Meirom AI Solutions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>ברוכים הבאים למערכת ההטמעה האוטונומית. אנחנו הופכים את הבינה המלאכותית לעובד הכי יעיל בעסק שלכם.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=200)
        if st.button("בואו נתחיל - לבחירת מסלול הטמעה 🚀", use_container_width=True):
            go_to('options')

# --- עמוד 2: בחירת אופציות ומחירים ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>💳 בחירת מסלול מנוי חודשי</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### Basic")
        st.markdown("**250₪ / חודש**")
        st.write("אוטומציה בסיסית וייעוץ")
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"
            st.session_state.price = "250"
            go_to('payment')
            
    with col2:
        st.success("### Pro ⭐")
        st.markdown("**750₪ / חודש**")
        st.write("סוכני AI פעילים וניטור")
        if st.button("בחר Pro"):
            st.session_state.plan = "Pro"
            st.session_state.price = "750"
            go_to('payment')
            
    with col3:
        st.warning("### Enterprise")
        st.markdown("**2,500₪ / חודש**")
        st.write("ניהול AI מלא לעסק")
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"
            st.session_state.price = "2,500"
            go_to('payment')
            
    if st.button("⬅️ חזרה לדף הבית"):
        go_to('welcome')

# --- עמוד 3: עמוד תשלום אשראי ---
elif st.session_state.page == 'payment':
    st.title("🔐 תשלום מאובטח")
    st.write(f"הנך נרשם למסלול **{st.session_state.plan}** בעלות של **{st.session_state.price}₪** לחודש.")
    
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 25px; border-radius: 15px; border: 1px solid #d1d5db;">
            <h4 style="margin-top:0;">💳 פרטי אשראי (מצב הדמיה)</h4>
            <p>בגרסה המלאה, רכיב סליקה מאובטח של <b>Stripe</b> יוטמע כאן.</p>
            <p style="font-size: 14px; color: #666;">כל פרטי התשלום מוצפנים מקצה לקצה בתקן PCI-DSS.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("אשר תשלום והמשך להטמעה ✅", use_container_width=True):
        st.success("התשלום עבר בהצלחה!")
        go_to('main')

    if st.button("⬅️ חזרה לבחירת מסלול"):
        go_to('options')

# --- עמוד 4: טופס ההטמעה והפעלת ה-AI ---
elif st.session_state.page == 'main':
    st.title(f"⚙️ הטמעה פעילה: {st.session_state.plan}")
    
    with st.form("main_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל למשלוח הדו''ח")
        challenge = st.text_area("מה היית רוצה שה-AI ינהל או יפתור בעסק?")
        submit = st.form_submit_button("הפעל הטמעה סופית ⚡")
        
    if submit:
        if biz_name and challenge and biz_email:
            with st.spinner("ה-AI של Meirom Solutions מבצע הטמעה..."):
                try:
                    prompt = f"Role: CTO of Meirom AI Solutions. Plan: {st.session_state.plan}. Business: {biz_name}. Goal:
