import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות וחיבורים ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets!")
    st.stop()

# --- 2. פונקציות עזר ---
def get_users_df():
    try:
        # קורא את הטבלה עם "מזהה רענון" כדי לא לקבל נתונים ישנים מהזיכרון
        refresh_url = f"{SHEET_CSV_URL}&refresh={pd.Timestamp.now().timestamp()}"
        df = pd.read_csv(refresh_url)
        return df
    except:
        return pd.DataFrame()

def send_to_google(email, password, plan):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    payload = {"entry.855862094": email, "entry.1847739029": f"Pass: {password} | Plan: {plan}"}
    requests.post(url, data=payload)

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
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבי עמוד ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "auth"

# --- 5. דפי המערכת ---

if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])

    with t1:
        st.subheader("ברוכה השבה!")
        l_mail = st.text_input("אימייל", key="login_user").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="login_password")
        
        if st.button("כניסה למערכת 🚀"):
            df = get_users_df()
            if not df.empty:
                # מנרמלים עמודות למציאה קלה
                df.columns = [c.lower() for c in df.columns]
                email_col = [c for c in df.columns if 'email' in c or 'מייל' in c][0]
                
                # חיפוש משתמש
                match = df[df[email_col].astype(str).str.lower().str.strip() == l_mail]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_email = l_mail
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("לא מצאנו אותך בטבלה. וודאי שנרשמת קודם.")
            else: st.error("הטבלה לא נגישה כרגע.")

    with t2:
        st.subheader("יצירת חשבון חדש")
        r_mail = st.text_input("מייל להרשמה", key="reg_user")
        r_pass = st.text_input("בחרי סיסמה", type="password", key="reg_password")
        if st.button("המשך לבחירת חבילה ➡️"):
            if r_mail and r_pass:
                st.session_state.temp_mail, st.session_state.temp_pass = r_mail, r_pass
                st.session_state.page = "packages"
                st.rerun()

elif st.session_state.page == "packages":
    st.subheader("בחרי את המסלול שלך ✨")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("בחרתי VIP 🌟"):
            send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "VIP")
            st.session_state.page = "success"
            st.rerun()
    with col2:
        if st.button("בחרתי צמיחה 🚀"):
            send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "Growth")
            st.session_state.page = "success"
            st.rerun()

elif st.session_state.page == "success":
    st.balloons()
    st.success("נרשמת בהצלחה!")
    if st.button("כניסה למרכז הבקרה"):
        st.session_state.logged_in = True
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "dashboard":
    st.sidebar.write(f"שלום, {st.session_state.user_email}")
    if st.sidebar.button("התנתקות"):
        st.session_state.logged_in = False
        st.session_state.page = "auth"
        st.rerun()
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    prompt = st.text_area("מה נכתוב היום?")
    if st.button("הפעל AI"):
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
        st.write(res.choices[0].message.content)
