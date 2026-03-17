import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- הגדרות חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing GROQ_KEY in Secrets!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ואחסון מצב (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'price' not in st.session_state:
    st.session_state.price = "0"
if 'report' not in st.session_state:
    st.session_state.report = None

# פונקציה למעבר בין דפים
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב אפליקציה בהיר ונעים ---
st.set_page_config(page_title="Meirom Magic AI | Magical Integration", page_icon="🧚‍♀️", layout="centered")

# הגדרות CSS גלובליות
st.markdown("""
<style>
    /* רקע בהיר ונעים */
    .stApp { background-color: #f8fafc; }
    
    /* כותרות */
    h1, h2, h3 { color: #1e3a8a !important; text-align: center; }
    
    /* כרטיס אפליקציה */
    .app-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* כפתור בהיר ונעים */
    .stButton>button {
        background: linear-gradient(135deg, #a78bfa, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3.5em !important;
    }
</style>
""", unsafe_allow_html=True)

# === עמוד 1: פתיחה (הלוגו הקסום שלך!) ===
if st.session_state.page == 'welcome':
    st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1>MEIROM <span style='color: #8b5cf6;'>MAGIC AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    
    # הצגת הלוגו שנוצר על בסיס הרעיון שלך
    st.image("https://replicate.delivery/xpbkg/q4e91r8c4k1mP4A14E3f1725A6C0B5E0D048e42/output.png", width=250)
    
    st.write("מערכת אוטונומית להטמעת AI בעסק שלך")
    st.write("חוויה בהירה, נעימה וקסומה")
    if st.button("בואי נתחיל! 🚀"):
        go_to('options')
    st.markdown("</div></div>", unsafe_allow_html=True)

# === עמוד 2: בחירת מסלול (עם המחירים והצבעים!) ===
elif st.session_state.page == 'options':
    st.markdown("<h2>בחר מסלול צמיחה</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # כרטיס Basic כחול
        st.markdown("<div class='app-card' style='border-top: 5px solid #3b82f6;'>", unsafe_allow_html=True)
        st.markdown("<h3>Basic</h3><h3>₪250</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Basic"):
            st.session_state.plan, st.session_state.price = "Basic", "250"
            go_to('payment')
            
    with col2:
        # כרטיס Pro ירוק
        st.markdown("<div class='app-card' style='border-top: 5px solid #22c55e;'>", unsafe_allow_html=True)
        st.markdown("<h3>Pro ⭐</h3><h3>₪750</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Pro"):
            st.session_state.plan, st.session_state.price = "Pro", "750"
            go_to('payment')
            
    with col3:
        # כרטיס Enterprise זהב
        st.markdown("<div class='app-card' style='border-top: 5px solid #eab308;'>", unsafe_allow_html=True)
        st.markdown("<h3>Enterprise</h3><h3>₪2,500</h3></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise"):
            st.session_state.plan, st.session_state.price = "Enterprise", "2,500"
            go_to('payment')
    
    st.write("")
    if st.button("⬅️ חזרה לדף הבית"):
        go_to('welcome')

# === עמוד 3: תשלום מלא ===
elif st.session_state.page == 'payment':
    st.markdown("<h2>תשלום מאובטח</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.write(f"מסלול: **{st.session_state.plan}** | סכום: **₪{st.session_state.price}**")
    
    # טופס אשראי מלא
    st.text_input("מספר כרטיס", placeholder="0000 0000 0000 0000")
    colA, colB = st.columns(2)
    with colA:
        st.text_input("תוקף", placeholder="MM/YY")
    with colB:
        st.text_input("CVV", placeholder="000")
    
    st.write("")
    if st.button("אשר תשלום ✅"):
        bar = st.progress(0)
        # סימולציית טעינה של תשלום
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.success("התשלום עבר בהצלחה!")
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("⬅️ חזרה למסלולים"):
        go_to('options')

# === עמוד 4: מסוף השליטה (הסוכן) ===
elif st.session_state.page == 'main':
    st.markdown(f"<h2>מסוף ניהול: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    
    # טופס הסוכן
    st.markdown("<div
