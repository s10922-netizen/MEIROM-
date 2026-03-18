import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
# הערה: כדאי בהמשך להעביר את המפתח ל-Secrets של Streamlit
client = Groq(api_key="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")

# --- זיכרון המערכת (Session State) ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'biz_info' not in st.session_state:
    st.session_state.biz_info = ""

# --- פונקציות עזר ---
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"Source: {r['title']}\nContent: {r['body']}" for r in results])
    except: return "לא נמצא מידע עדכני."

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
    [data-testid="stSidebar"] { background-color: #f3f0ff; border-left: 2px solid #7c3aed; }
</style>
""", unsafe_allow_html=True)

# --- לוגיקת דפים ---

# 1. דף כניסה והרשמה
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    
    with tab_login:
        l_email = st.text_input("אימייל", key="login_email_input")
        l_pass = st.text_input("סיסמה", type="password", key="login_pass_input")
        if st.button("כניסה 🚀", use_container_width=True):
            if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")
            
    with tab_signup:
        s_email = st.text_input("אימייל להרשמה", key="signup_email_input")
        s_pass = st.text_input("סיסמה חדשה", type="password", key="signup_pass_input")
        if st.button("צרי חשבון 🧚‍♀️", use_container_width=True):
            if s_email in st.session_state.users:
                st.warning("המייל כבר רשום!")
            else:
                st.session_state.users[s_email] = s_pass
                st.success("נרשמת בהצלחה! עכשיו אפשר להתחבר בלשונית הקודמת.")

# 2. דף בחירת חבילה
elif st.session_state.logged_in and st.session_state.plan is None:
    st.markdown("<h2 style='text-align:center;'>בחרי מסלול קסם ✨</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("### Basic 🧚‍♀️\n250₪/mo")
        if st.button("בחר Basic"): st.session_state.plan = "Basic"; st.rerun()
    with c2:
        st.success("### Pro ⭐\n750₪/mo")
        if st.button("בחר Pro"): st.session_state.plan = "Pro"; st.rerun()
    with c3:
        st.warning("### Enterprise 👑\n2500₪/mo")
        if st.button("בחר Enterprise"): st.session_state.plan = "Enterprise"; st.rerun()

# 3. האפליקציה המלאה
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
            menu.append("🏢 הגדרות עסק")
            menu.append("🤖 צ'אטבוט לקוחות")
        page = st.radio("ניווט:", menu)

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write(f"שלום! חבילת ה-{st.session_state.plan} שלך פעילה.")

    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק חכם")
        biz = st.text_input("שם העסק")
        task = st.text_area("מה לכתוב?")
        if st.button("הפעל קסם ⚡"):
            with st.status("חושבת..."):
                prompt = f"Write a marketing post for {biz}: {task}. Hebrew."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                ans = res.choices[0].message.content
                st.write(ans)
                whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(ans)}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer;">שלחי בוואטסאפ 📱</button></a>', unsafe_allow_html=True)

    elif page == "📅 קביעת פגישות":
        st.header("סוכן יומן אישי 📅")
        col_date, col_time = st.columns(2)
        with col_date: d = st.date_input("תאריך", datetime.now())
        with col_time: t = st.time_input("שעה", datetime.now())
        client_name = st.text_input("שם הלקוח")
        if st.button("צור אישור פגישה 🪄"):
            details = f"פגישה עם {client_name} בתאריך {d} בשעה {t}"
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Write a WhatsApp confirmation: {details}. Hebrew."}])
            msg = res.choices[0].message.content
            st.write(msg)
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank"><button style="background:#7c3aed; color:white; border:none; padding:15px; border-radius:15px; cursor:pointer;">שלחי אישור 📱</button></a>', unsafe_allow_html=True)

    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות ה'אתר' של העסק 🏢")
        biz_details = st.text_area("מידע על העסק (שעות, מחירים, שירותים):", value=st.session_state.biz_info)
        if st.button("שמור הגדרות 💾"):
            st.session_state.biz_info = biz_details
            st.success("נשמר!")

    elif page == "🤖 צ'אטבוט לקוחות":
        st.header("🤖 צ'אטבוט לקוחות (Simulation)")
        if not st.session_state.biz_info:
            st.warning("נא להזין פרטי עסק בהגדרות!")
        else:
            user_msg = st.chat_input("איך אפשר לעזור?")
            if user_msg:
                st.chat_message("user").write(user_msg)
                prompt = f"Assistant for: {st.session_state.biz_info}. Answer: {user_msg}. Hebrew."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                st.chat_message("assistant").write(res.choices[0].message.content)
