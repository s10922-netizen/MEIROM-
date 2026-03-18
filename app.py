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
    st.error("Missing API Key in Secrets!")
    st.stop()

# --- 2. פונקציות ליבה ---
def get_users_df():
    try:
        # רענון נתונים מהטבלה הציבורית
        url = f"{SHEET_CSV_URL}&refresh={pd.Timestamp.now().timestamp()}"
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

def send_to_google(email, password, plan):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    payload = {"entry.855862094": email, "entry.1847739029": f"Pass: {password} | Plan: {plan}"}
    requests.post(url, data=payload)

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
        font-size: 50px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .package-card {
        border: 2px solid #7c3aed; border-radius: 15px; padding: 20px; 
        text-align: center; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבי עמוד (Session State) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

# --- 5. ניווט דפים ---

# א. דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה למערכת", "📝 הרשמה VIP"])

    with t1:
        l_mail = st.text_input("אימייל", key="login_m").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="login_p")
        if st.button("כניסה 🚀", key="login_btn"):
            df = get_users_df()
            if not df.empty:
                # הופך את כל הטבלה לרשימה אחת לבדיקה מהירה
                all_data = df.astype(str).apply(lambda x: x.str.strip().str.lower()).values.flatten()
                if l_mail in all_data:
                    st.session_state.logged_in = True
                    st.session_state.user_email = l_mail
                    st.session_state.page = "dashboard"
                    st.rerun()
                else: st.error("המייל לא נמצא בטבלה. חכי 5 דקות לעדכון גוגל או הירשמי.")
            else: st.error("שגיאה בגישה לנתוני הטבלה.")

    with t2:
        r_mail = st.text_input("מייל חדש", key="reg_m").strip().lower()
        r_pass = st.text_input("סיסמה חדשה", type="password", key="reg_p")
        if st.button("המשך לבחירת חבילה ✨", key="reg_btn"):
            if r_mail and r_pass:
                st.session_state.temp_mail, st.session_state.temp_pass = r_mail, r_pass
                st.session_state.page = "packages"
                st.rerun()

# ב. דף חבילות
elif st.session_state.page == "packages":
    st.markdown("<h2 style='text-align:center;'>בחרי את המסלול שלך ✨</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='package-card'><h3>🌟 VIP Magic</h3><p>בינה מלאכותית ללא הגבלה</p><h2>₪199</h2></div>", unsafe_allow_html=True)
        if st.button("רכישת VIP 💎", key="vip_btn"):
            send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "VIP")
            st.session_state.page = "success"
            st.rerun()
    with c2:
        st.markdown("<div class='package-card'><h3>🚀 Growth Pack</h3><p>סוכן שיווק וניהול תוכן</p><h2>₪99</h2></div>", unsafe_allow_html=True)
        if st.button("רכישת צמיחה 🚀", key="growth_btn"):
            send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "Growth")
            st.session_state.page = "success"
            st.rerun()

# ג. דף הצלחה
elif st.session_state.page == "success":
    st.balloons()
    st.markdown("<div class='magic-title'>ברוכה הבאה למשפחה!</div>", unsafe_allow_html=True)
    st.info("שימי לב: לוקח לגוגל כ-5 דקות לעדכן את הטבלה. תוכלי להיכנס למערכת בעוד רגע.")
    if st.button("מעבר למסך הבקרה 🎬"):
        st.session_state.logged_in = True
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

# ד. מרכז הבקרה המלא (ה-Dashboard)
elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.markdown(f"### שלום, {st.session_state.user_email} 👑")
        menu = st.radio("תפריט ניהול", ["🏠 דף הבית", "✍️ סוכן תוכן AI", "👥 ניהול לקוחות", "💬 צ'אט שירות לקוחות"])
        if st.button("התנתקות"):
            st.session_state.logged_in = False
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 דף הבית":
        st.markdown(f"<div class='magic-title'>ברוכה השבה, {st.session_state.user_email.split('@')[0]}!</div>", unsafe_allow_html=True)
        st.success("המערכת מחוברת ומוכנה לעבודה.")
        st.write("כאן תמצאי את כל הכלים לניהול העסק שלך בעזרת בינה מלאכותית.")
        
    elif menu == "✍️ סוכן תוכן AI":
        st.header("מחולל תוכן קריאטיבי 🤖")
        topic = st.text_input("מה הנושא?")
        if st.button("צור תוכן ✨"):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט שיווקי על {topic}"}])
            st.write(res.choices[0].message.content)

    elif menu == "👥 ניהול לקוחות":
        st.header("רשימת הלקוחות שלך (מהטבלה) 📊")
        df = get_users_df()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("לא נמצאו נתונים בטבלה.")

    elif menu == "💬 צ'אט שירות לקוחות":
        st.header("צ'אטבוט שירות לקוחות חכם 👩‍💻")
        st.write("כאן תוכלי להתנסות באיך הצ'אטבוט שלך יענה ללקוחות:")
