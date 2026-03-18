import streamlit as st
from groq import Groq
import requests

# --- 1. הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- 2. חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets!")
    st.stop()

# --- 3. עיצוב CSS ---
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
        font-size: 50px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white; border-radius: 20px; border: none; padding: 10px 20px; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול זיכרון (Session State) ---
# כאן אנחנו מגדירים מה האתר "זוכר" בזמן שהגולש באתר
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login_screen"

# --- 5. פונקציית הרשמה לגוגל ---
def send_to_google(email, password, plan):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    payload = {
        "entry.855862094": email,
        "entry.1847739029": f"Pass: {password} | Plan: {plan}"
    }
    try:
        requests.post(url, data=payload)
        return True
    except:
        return False

# --- 6. ניווט בין דפים ---

# דף כניסה והרשמה
if st.session_state.page == "login_screen":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])
    
    with tab1:
        email = st.text_input("אימייל", key="l_email")
        pwd = st.text_input("סיסמה", type="password", key="l_pwd")
        if st.button("כניסה למערכת 🚀"):
            # כרגע הכניסה היא רק למנהלת, בהמשך נוכל לחבר בדיקה מול הטבלה
            if email == "admin@magic.com" and pwd == "1234":
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("פרטים שגויים. (כרגע רק המנהלת יכולה להיכנס)")

    with tab2:
        new_mail = st.text_input("מייל להרשמה", key="r_email")
        new_pass = st.text_input("בחרי סיסמה", type="password", key="r_pwd")
        if st.button("המשך לבחירת חבילה ⬅️"):
            if new_mail and new_pass:
                st.session_state.temp_mail = new_mail
                st.session_state.temp_pass = new_pass
                st.session_state.page = "packages"
                st.rerun()

# דף חבילות
elif st.session_state.page == "packages":
    st.subheader("בחרי את המסלול שלך ✨")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🌟 מסלול VIP - 199₪")
        if st.button("בחרתי VIP"):
            if send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "VIP"):
                st.session_state.page = "success"
                st.rerun()
    with col2:
        st.info("🚀 מסלול צמיחה - 99₪")
        if st.button("בחרתי צמיחה"):
            if send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "Growth"):
                st.session_state.page = "success"
                st.rerun()

# דף הצלחה
elif st.session_state.page == "success":
    st.balloons()
    st.success("נרשמת בהצלחה! הפרטים נשמרו בטבלה.")
    if st.button("כניסה למרכז הבקרה"):
        st.session_state.logged_in = True
        st.session_state.page = "dashboard"
        st.rerun()

# מרכז הבקרה (אחרי התחברות)
elif st.session_state.page == "dashboard":
    st.sidebar.title("מנכ\"לית מיי 👑")
    if st.sidebar.button("התנתקות"):
        st.session_state.logged_in = False
        st.session_state.page = "login_screen"
        st.rerun()
        
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    topic = st.text_area("על מה נכתוב היום עם ה-AI?")
    if st.button("צור תוכן"):
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט קצר על {topic}"}])
        st.write(res.choices[0].message.content)
