import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות בסיסיות ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# הקישור שנתת לי (CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

# חיבור ל-AI
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets!")
    st.stop()

# --- 2. פונקציות עזר ---

def get_users_df():
    """קורא את הטבלה מגוגל ומחזיר אותה כטבלה של פייתון"""
    try:
        # הוספת פרמטר למניעת שמירה במטמון (Cache) כדי שהנתונים יהיו טריים
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception as e:
        return pd.DataFrame()

def send_to_google_form(email, password, plan):
    """שולח רישום חדש לטופס גוגל"""
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

# --- 4. ניהול מצבי עמוד (Session State) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'page' not in st.session_state: st.session_state.page = "auth"

# --- 5. ניווט דפים ---

# דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])

    with tab1:
        st.subheader("שלום מנכ\"לית, היכנסי למערכת")
        l_email = st.text_input("אימייל", key="login_email")
        l_pwd = st.text_input("סיסמה", type="password", key="login_pwd")
        
        if st.button("כניסה 🚀"):
            with st.spinner("בודק בטבלה..."):
                df = get_users_df()
                if not df.empty:
                    # בודק אם המייל והסיסמה מופיעים באותה שורה
                    # הערה: העמודות ב-CSV של גוגל הן בד"כ 'Email Address' וכו'
                    # כאן אנחנו בודקים לפי המיקום של העמודה (עמודה 2 למייל)
                    valid_user = df[(df.iloc[:, 1].astype(str).str.strip() == l_email.strip())]
                    
                    if not valid_user.empty:
                        st.session_state.logged_in = True
                        st.session_state.user_email = l_email
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("מייל לא נמצא בטבלה. וודאי שנרשמת קודם.")
                else:
                    st.error("לא ניתן לקרוא את הטבלה כרגע.")

    with tab2:
        st.subheader("יצירת חשבון חדש")
        r_email = st.text_input("מייל להרשמה", key="reg_email")
        r_pwd = st.text_input("בחרי סיסמה", type="password", key="reg_pwd")
        if st.button("המשך לבחירת חבילה ⬅️"):
            if r_email and r_pwd:
                st.session_state.temp_email = r_email
                st.session_state.temp_pass = r_pwd
                st.session_state.page = "packages"
                st.rerun()

# דף חבילות
elif st.session_state.page == "packages":
    st.subheader("בחרי את המסלול שלך ✨")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.info("🌟 מסלול VIP - 199₪")
        if st.button("בחרתי VIP"):
            send_to_google_form(st.session_state.temp_email, st.session_state.temp_pass, "VIP")
            st.session_state.page = "success"
            st.rerun()
    with p_col2:
        st.info("🚀 מסלול צמיחה - 99₪")
        if st.button("בחרתי צמיחה"):
            send_to_google_form(st.session_state.temp_email, st.session_state.temp_pass, "Growth")
            st.session_state.page = "success"
            st.rerun()

# דף הצלחה
elif st.session_state.page == "success":
    st.balloons()
    st.success(f"נרשמת בהצלחה עם המייל: {st.session_state.temp_mail}")
    if st.button("מעבר למרכז הבקרה"):
        st.session_state.logged_in = True
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

# מרכז הבקרה (Dashboard)
elif st.session_state.page == "dashboard":
    st.sidebar.write(f"שלום, {st.session_state.user_email}")
    if st.sidebar.button("התנתקות"):
        st.session_state.logged_in = False
        st.session_state.page = "auth"
        st.rerun()
        
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    prompt = st.text_area("מה סוכן ה-AI יעשה בשבילך היום?")
    if st.button("הפעל קסם ⚡"):
        with st.spinner("ה-AI חושב..."):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"ענה בעברית: {prompt}"}])
            st.write(res.choices[0].message.content)
