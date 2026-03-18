import streamlit as st
from groq import Groq
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור מאובטח (Secrets) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("שגיאת אבטחה: וודאי שהמפתח GROQ_API_KEY מוגדר ב-Secrets.")
    st.stop()

# --- זיכרון מערכת ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'plan' not in st.session_state: st.session_state.plan = None
if 'biz_info' not in st.session_state: st.session_state.biz_info = ""

# --- ✨ עיצוב CSS מלא (החזרת הקסם) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white; border: none; border-radius: 20px; padding: 10px 25px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- לוגיקת דפים ---

# 1. דף לקוח חיצוני (?view=customer)
if st.query_params.get("view") == "customer":
    st.markdown("<div class='magic-title'>ברוכים הבאים</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{st.session_state.biz_info if st.session_state.biz_info else 'שלום! איך אפשר לעזור?'}</h3>", unsafe_allow_html=True)
    st.divider()
    customer_msg = st.chat_input("שאל/י אותנו משהו...")
    if customer_msg:
        st.chat_message("user").write(customer_msg)
        prompt = f"You are a helpful assistant for: {st.session_state.biz_info}. Answer: {customer_msg} in Hebrew."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
        st.chat_message("assistant").write(res.choices[0].message.content)
    st.stop()

# 2. דף כניסה/הרשמה
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    with tab1:
        e = st.text_input("אימייל", key="main_login_e")
        p = st.text_input("סיסמה", type="password", key="main_login_p")
        if st.button("כניסה 🚀", key="main_login_btn"):
            if e == "admin@magic.com" and p == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")
    with tab2:
        ne = st.text_input("מייל להרשמה", key="main_reg_e")
        np = st.text_input("סיסמה", type="password", key="main_reg_p")
        if st.button("צרי חשבון ✨", key="main_reg_btn"):
            st.success("נרשמת! (בינתיים בזיכרון זמני)")

# 3. בחירת חבילה
elif st.session_state.plan is None:
    st.markdown("<h2 style='text-align:center;'>בחרי מסלול ✨</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("Basic (250₪)"): st.session_state.plan = "Basic"; st.rerun()
    if c2.button("Pro (750₪)"): st.session_state.plan = "Pro"; st.rerun()
    if c3.button("Enterprise (2500₪)"): st.session_state.plan = "Enterprise"; st.rerun()

# 4. מרכז הבקרה המלא
else:
    with st.sidebar:
        st.markdown(f"### מנכ\"לית מיי 👑\n**חבילה:** {st.session_state.plan}")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.session_state.plan = None
            st.rerun()
        st.divider()
        menu = ["✨ דף הבית", "🚀 סוכן שיווק", "📅 קביעת פגישות", "🏢 הגדרות עסק", "🔗 קישור ללקוחות"]
        page = st.radio("ניווט:", menu)

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    
    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק חכם")
        task = st.text_area("מה לכתוב?")
        if st.button("צור תוכן ⚡"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Write marketing for: {task} in Hebrew"}])
            st.write(res.choices[0].message.content)

    elif page == "📅 קביעת פגישות":
        st.header("ניהול יומן 📅")
        st.date_input("בחר תאריך")
        st.button("שלח אישור")

    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות עסק 🏢")
        st.session_state.biz_info = st.text_area("פרטי העסק שלך (ה-AI ילמד מכאן):", value=st.session_state.biz_info)
        if st.button("שמור ✅"): st.success("המידע נשמר!")

    elif page == "🔗 קישור ללקוחות":
        st.header("הקישור שלך 🌐")
        st.info("שלחי את הלינק הזה ללקוחות שלך:")
        st.code("https://YOUR-APP.streamlit.app/?view=customer")
