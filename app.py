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

# --- 3. עיצוב CSS (החזרתי את הקסם) ---
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
</style>
""", unsafe_allow_html=True)

# --- 4. לוגיקה וזיכרון ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'biz_info' not in st.session_state: st.session_state.biz_info = "ברוכים הבאים לעסק!"

# דף לקוח חיצוני
if st.query_params.get("view") == "customer":
    st.markdown("<div class='magic-title'>ברוכים הבאים</div>", unsafe_allow_html=True)
    st.write(st.session_state.biz_info)
    st.stop()

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
        st.subheader("הצטרפי למהפכה ✨")
        new_mail = st.text_input("מייל להרשמה", key="r_e")
        new_pass = st.text_input("בחרי סיסמה", type="password", key="r_p")
        
        if st.button("צרי חשבון חינם"):
            # הקישור לטופס שלך (מעובד לשליחה אוטומטית)
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            
            # ה-IDs שהוצאנו מהלינק שלך
            payload = {
                "entry.855862094": new_mail, # שדה האימייל
                "entry.1847739029": new_pass  # שדה הסיסמה
            }
            
            try:
                requests.post(form_url, data=payload)
                st.balloons()
                st.success(f"מנכ\"לית, {new_mail} נרשם בטבלה שלך בהצלחה!")
            except:
                st.error("הייתה בעיה קטנה בשליחה לטבלה.")

# --- 6. מרכז הבקרה (אחרי התחברות) ---
else:
    with st.sidebar:
        st.markdown("### מנכ\"לית מיי 👑")
        page = st.radio("ניווט:", ["✨ דף הבית", "🚀 סוכן שיווק", "🏢 הגדרות עסק", "🔗 קישור ללקוחות"])
        if st.button("התנתקות"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write("המערכת מחוברת ומוכנה לעבודה!")
        
    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק AI")
        task = st.text_area("על מה לכתוב פוסט?")
        if st.button("צור תוכן ⚡"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Write marketing for: {task} in Hebrew"}])
            st.write(res.choices[0].message.content)

    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות עסק")
        st.session_state.biz_info = st.text_area("מידע שהצ'אטבוט יכיר:", value=st.session_state.biz_info)
        st.button("שמור ✅")

    elif page == "🔗 קישור ללקוחות":
        st.header("הקישור שלך 🌐")
        st.code("https://YOUR-APP.streamlit.app/?view=customer")
