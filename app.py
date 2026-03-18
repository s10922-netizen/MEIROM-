import streamlit as st
from groq import Groq
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור מאובטח ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets!")
    st.stop()

# --- בדיקה: האם זה לקוח חיצוני? ---
query_params = st.query_params
is_customer_view = query_params.get("view") == "customer"

# --- זיכרון המערכת ---
if 'biz_info' not in st.session_state:
    st.session_state.biz_info = "ברוכים הבאים! אנחנו כאן לכל שאלה."
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'plan' not in st.session_state: st.session_state.plan = None

# --- ✨ עיצוב CSS המלא (החזרנו את הקסם) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    /* כותרת מנצנצת */
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center;
        padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* עיצוב כפתורים */
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
    }
    
    /* סרגל צד */
    [data-testid="stSidebar"] {
        background-color: #f3f0ff;
        border-left: 2px solid #7c3aed;
    }
</style>
""", unsafe_allow_html=True)

# --- 🌐 דף לקוח חיצוני (נקי ויוקרתי) ---
if is_customer_view:
    st.markdown("<div class='magic-title'>ברוכים הבאים</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{st.session_state.biz_info}</h3>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("צ'אט עם העוזר הדיגיטלי שלנו 🤖")
    u_msg = st.chat_input("איך אפשר לעזור?")
    if u_msg:
        st.chat_message("user").write(u_msg)
        r = client.chat.completions.create(model="llama-3.3-70b-versatile", 
                                          messages=[{"role":"user","content":f"Biz info: {st.session_state.biz_info}. User: {u_msg}. Hebrew."}])
        st.chat_message("assistant").write(r.choices[0].message.content)
    
    st.divider()
    st.subheader("קביעת תור מהירה 📅")
    c1, c2 = st.columns(2)
    with c1: st.date_input("יום", key="cust_d")
    with c2: st.time_input("שעה", key="cust_t")
    if st.button("תזמינו לי מקום! 🚀", key="cust_btn"):
        st.balloons()
        st.success("הבקשה נשלחה!")
    st.stop()

# --- 👑 דף המנכ"לית (ניהול) ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>כניסת הנהלה</h3>", unsafe_allow_html=True)
    l_email = st.text_input("אימייל", key="m_user")
    l_pass = st.text_input("סיסמה", type="password", key="m_pass")
    if st.button("התחברות למערכת 🚀", key="m_btn"):
        if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("פרטים שגויים")

elif st.session_state.plan is None:
    st.markdown("<div class='magic-title'>בחרי מסלול</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("Basic (250₪)", key="b1"): st.session_state.plan = "Basic"; st.rerun()
    if c2.button("Pro (750₪)", key="b2"): st.session_state.plan = "Pro"; st.rerun()
    if c3.button("Enterprise (2500₪)", key="b3"): st.session_state.plan = "Enterprise"; st.rerun()

else:
    with st.sidebar:
        st.markdown(f"### מנכ\"לית מיי 👑\n**חבילה:** {st.session_state.plan}")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.session_state.plan = None
            st.rerun()
        st.divider()
        page = st.radio("ניווט:", ["✨ דף הבית", "🏢 הגדרות עסק", "📅 יומן פגישות", "🔗 קישור ללקוחות"])

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write("הכל עובד פיקס. המפתחות בכספת והעיצוב חזר!")
    
    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות עסק 🏢")
        st.session_state.biz_info = st.text_area("מה לספר ללקוחות?", value=st.session_state.biz_info)
        if st.button("שמור ✅", key="save_biz"): st.success("נשמר!")

    elif page == "📅 יומן פגישות":
        st.header("ניהול תורים 📅")
        st.write("כאן תראי את כל מי שקבע תור דרך דף הלקוח.")

    elif page == "🔗 קישור ללקוחות":
        st.header("הקישור הסודי שלך 🌐")
        st.info("זה הלינק שאת שולחת ללקוחות. הם יראו רק את הדף הנקי.")
        st.code("https://YOUR-APP.streamlit.app/?view=customer")
