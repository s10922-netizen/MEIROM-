import streamlit as st
from groq import Groq
import requests

# --- 1. הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- 2. חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

# --- 3. עיצוב CSS יוקרתי ---
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
        font-size: 55px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white; border-radius: 20px; border: none; padding: 10px 20px; width: 100%;
        font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4); }
    .package-card {
        border: 2px solid #7c3aed; border-radius: 15px; padding: 20px; text-align: center; background: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבים (State) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'step' not in st.session_state: st.session_state.step = "login"

# --- 5. לוגיקה של דפים ---

# דף כניסה והרשמה
if not st.session_state.logged_in and st.session_state.step == "login":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 כניסת מנכ\"לית", "📝 הרשמה חדשה"])
    
    with tab1:
        email = st.text_input("אימייל", key="login_email")
        pwd = st.text_input("סיסמה", type="password", key="login_pwd")
        if st.button("כניסה למערכת 🚀"):
            if email == "admin@magic.com" and pwd == "1234":
                st.session_state.logged_in = True
                st.session_state.step = "dashboard"
                st.rerun()
            else: st.error("פרטים לא נכונים")
            
    with tab2:
        st.subheader("הצטרפי למהפכה ✨")
        new_mail = st.text_input("מייל להרשמה", key="reg_mail")
        new_pass = st.text_input("בחרי סיסמה", type="password", key="reg_pass")
        if st.button("המשך לבחירת חבילה ⬅️"):
            if new_mail and new_pass:
                st.session_state.temp_mail = new_mail
                st.session_state.temp_pass = new_pass
                st.session_state.step = "package"
                st.rerun()
            else: st.warning("מלאי פרטים קודם")

# דף בחירת חבילה
elif st.session_state.step == "package":
    st.markdown("<h2 style='text-align:center;'>בחרי את המסלול שלך ✨</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='package-card'><h3>🌟 מסלול VIP</h3><p>כל כלי ה-AI ללא הגבלה</p><h4>₪199/חודש</h4></div>", unsafe_allow_html=True)
        if st.button("בחרתי VIP 💎", key="btn_vip"):
            st.session_state.selected_package = "VIP"
            st.session_state.step = "finalize"
            st.rerun()
            
    with col2:
        st.markdown("<div class='package-card'><h3>🚀 מסלול צמיחה</h3><p>סוכן שיווק וצ'אטבוט</p><h4>₪99/חודש</h4></div>", unsafe_allow_html=True)
        if st.button("בחרתי צמיחה 🚀", key="btn_growth"):
            st.session_state.selected_package = "Growth"
            st.session_state.step = "finalize"
            st.rerun()

# שלב סופי: שליחה לטבלה
elif st.session_state.step == "finalize":
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    payload = {
        "entry.855862094": st.session_state.temp_mail,
        "entry.1847739029": f"Pass: {st.session_state.temp_pass} | Plan: {st.session_state.selected_package}"
    }
    try:
        requests.post(form_url, data=payload)
        st.balloons()
        st.success("ההרשמה הושלמה! הפרטים נשמרו.")
        if st.button("מעבר למסך הבקרה 🎬"):
            st.session_state.logged_in = True
            st.session_state.step = "dashboard"
            st.rerun()
    except Exception:
        st.error("הייתה תקלה קטנה ברישום")

# מרכז הבקרה (Dashboard)
elif st.session_state.logged_in:
    with st.sidebar:
        st.markdown("### מנכ\"לית מיי 👑")
        choice = st.radio("לאן הולכים?", ["🏠 בית", "📝 סוכן תוכן AI"])
        if st.button("התנתקות"):
            st.session_state.logged_in = False
            st.session_state.step = "login"
            st.rerun()
            
    if choice == "🏠 בית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write("כל המערכות פועלות כשורה. את מוכנה לכבוש את העולם!")
        
    elif choice == "📝 סוכן תוכן AI":
        st.header("סוכן תוכן חכם 🤖")
        topic = st.text_area("על מה נכתוב היום?")
        if st.button("צור תוכן"):
            with st.spinner("ה-AI רוקח לך קסם..."):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role":"user","content":f"Write marketing text in Hebrew about: {topic}"}]
                )
                st.write(res.choices[0].message.content)
