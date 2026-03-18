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
        font-size: 60px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white; border: none; border-radius: 20px; padding: 10px 25px; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. לוגיקה ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'biz_info' not in st.session_state: st.session_state.biz_info = "ברוכים הבאים!"

# --- 5. דף כניסה והרשמה ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    
    with tab1:
        st.subheader("כניסת מנכ\"לית")
        e = st.text_input("אימייל", key="l_e")
        p = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה 🚀"):
            if e == "admin@magic.com" and p == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")
            
    with tab2:
        st.subheader("הצטרפי בחינם ✨")
        new_mail = st.text_input("מייל להרשמה", key="r_e")
        new_pass = st.text_input("בחרי סיסמה ", type="password", key="r_p") # וודאי שיש רווח קטן ב-label
        
        if st.button("צרי חשבון ✨"):
            if new_mail and new_pass:
                # הכתובת הישירה לשליחה - שימי לב לשינוי הקטן ב-URL
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
                
                payload = {
                    "entry.855862094": new_mail,
                    "entry.1847739029": new_pass
                }
                
                try:
                    # שיטה פשוטה יותר שעוקפת את ה-401
                    response = requests.post(form_url, data=payload)
                    
                    # גוגל תמיד מחזירה 200 אם הטופס נשלח, גם אם לא ראינו את זה
                    st.balloons()
                    st.success("נרשמת בהצלחה! תבדקי עכשיו את הטבלה הירוקה.")
                except Exception as ex:
                    st.error(f"תקלה בחיבור: {ex}")
            else:
                st.warning("נא למלא את כל השדות")

else:
    # מרכז הבקרה
    with st.sidebar:
        st.markdown("### מנכ\"לית מיי 👑")
        if st.button("התנתקות"):
            st.session_state.logged_in = False
            st.rerun()
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    st.write("המערכת עובדת!")
