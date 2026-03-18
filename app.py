import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI (תחליפי למפתח החדש שלך ב-Secrets!) ---
# client = Groq(api_key=st.secrets["GROQ_API_KEY"]) 
client = Groq(api_key="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")

# --- זיכרון המערכת ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'biz_info' not in st.session_state:
    st.session_state.biz_info = ""

# --- עיצוב CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- לוגיקת דפים ---

if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    with tab1:
        l_email = st.text_input("אימייל")
        l_pass = st.text_input("סיסמה", type="password")
        if st.button("כניסה 🚀", use_container_width=True):
            if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
                st.session_state.logged_in = True
                st.rerun()
    with tab2:
        s_email = st.text_input("מייל להרשמה")
        s_pass = st.text_input("סיסמה", type="password")
        if st.button("צרי חשבון 🧚‍♀️"):
            st.session_state.users[s_email] = s_pass
            st.success("נרשמת!")

elif st.session_state.logged_in and st.session_state.plan is None:
    st.markdown("<h2 style='text-align:center;'>בחרי מסלול ✨</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("Basic (250₪)"): st.session_state.plan = "Basic"; st.rerun()
    if c2.button("Pro (750₪)"): st.session_state.plan = "Pro"; st.rerun()
    if c3.button("Enterprise (2500₪)"): st.session_state.plan = "Enterprise"; st.rerun()

else:
    with st.sidebar:
        st.markdown(f"### מנכ\"לית מיי 👑\n**חבילה:** {st.session_state.plan}")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.session_state.plan = None
            st.rerun()
        st.divider()
        menu = ["✨ דף הבית", "🚀 סוכן שיווק", "📅 קביעת פגישות"]
        if st.session_state.plan == "Enterprise":
            menu.append("🏢 הגדרות עסק (Enterprise)")
            menu.append("🤖 צ'אטבוט לקוחות")
        page = st.radio("ניווט:", menu)

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write(f"ברוכה הבאה! החבילה שלך: {st.session_state.plan}")

    elif page == "🏢 הגדרות עסק (Enterprise)":
        st.header("הגדרות ה'אתר' של העסק שלך 🏢")
        st.write("כאן בעל העסק מזין את המידע שה-AI צריך לדעת:")
        biz_name = st.text_input("שם העסק", "הפיצה של מיי")
        biz_details = st.text_area("ספרי על העסק (שעות, מחירים, שירותים):", 
                                  value=st.session_state.biz_info, 
                                  placeholder="למשל: אנחנו פתוחים מ-12:00, פיצה משפחתית עולה 60 שח...")
        if st.button("שמור הגדרות עסק 💾"):
            st.session_state.biz_info = biz_details
            st.success("המידע נשמר! עכשיו הצ'אטבוט מוכן לדבר עם לקוחות.")

    elif page == "🤖 צ'אטבוט לקוחות":
        st.header("🤖 הצ'אטבוט שבנינו לעסק")
        st.write("ככה הלקוחות של העסק יראו את הצ'אט:")
        
        if not st.session_state.biz_info:
            st.warning("קודם צריך להגדיר את פרטי העסק בדף הגדרות!")
        else:
            user_msg = st.chat_input("שלום, איך אפשר לעזור?")
            if user_msg:
                st.chat_message("user").write(user_msg)
                with st.spinner("הסוכן עונה..."):
                    prompt = f"You are a helpful assistant for the business. Details: {st.session_state.biz_info}. Answer the customer in Hebrew: {user_msg}"
                    res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                    ans = res.choices[0].message.content
                    st.chat_message("assistant").write(ans)

    # ... (כאן נשארים הדפים של סוכן שיווק ויומן כרגיל)
