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
        color: white; border: none; border-radius: 20px; width: 100%; height: 50px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. לוגיקה ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 5. דף כניסה והרשמה ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])
    
    with tab1:
        e = st.text_input("מייל", key="l_e")
        p = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה 🚀"):
            if e == "admin@magic.com" and p == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")
            
    with tab2:
        st.subheader("הרשמה מהירה לטבלה")
        new_mail = st.text_input("מייל חדש", key="r_e")
        new_pass = st.text_input("סיסמה חדשה ", type="password", key="r_p")
        
        if st.button("צרי חשבון ✨"):
            if new_mail and new_pass:
                # הכתובת לשליחה "שקטה"
                form_base_url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
                
                # בניית הקישור עם הנתונים בפנים
                params = {
                    "entry.855862094": new_mail,
                    "entry.1847739029": new_pass,
                    "submit": "Submit"
                }
                
                try:
                    # שליחה שקטה - גוגל חושב שמישהו פשוט גלש ללינק
                    requests.get(form_base_url, params=params)
                    st.balloons()
                    st.success("זה הצליח! המידע נשלח. בדקי את הטבלה הירוקה בעוד כמה שניות.")
                except Exception as ex:
                    st.error(f"תקלה בחיבור: {ex}")
            else:
                st.warning("נא למלא את כל השדות")

else:
    st.sidebar.button("התנתקות", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    st.write("המערכת שלך חיה ובועטת!")
