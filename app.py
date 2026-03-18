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
    st.error("Missing API Key")
    st.stop()

# --- 2. פונקציות חכמות ---
def get_users_df():
    try:
        # רענון נתונים מהטבלה
        url = f"{SHEET_CSV_URL}&t={pd.Timestamp.now().timestamp()}"
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
        text-align: center; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבים ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

# --- 5. ניווט דפים ---

# דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה למערכת", "📝 הרשמה VIP"])

    with t1:
        l_mail = st.text_input("אימייל", key="in_m").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="in_p")
        if st.button("כניסה 🚀"):
            df = get_users_df()
            if not df.empty:
                df.columns = [c.lower() for c in df.columns]
                # מחפשים את המייל בעמודה השנייה (אינדקס 1)
                match = df[df.iloc[:, 1].astype(str).str.lower().str.strip() == l_mail]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_email = l_mail
                    st.session_state.page = "dashboard"
                    st.rerun()
                else: st.error("המייל לא נמצא בטבלה. הירשמי קודם!")
            else: st.error("טעינת נתונים נכשלה.")

    with t2:
        r_mail = st.text_input("מייל חדש", key="reg_m")
        r_pass = st.text_input("סיסמה", type="password", key="reg_p")
        if st.button("המשך לבחירת חבילה ✨"):
            if r_mail and r_pass:
                st.session_state.temp_mail, st.session_state.temp_pass = r_mail, r_pass
                st.session_state.page = "packages"
                st.rerun()

# דף חבילות מעוצב
elif st.session_state.page == "packages":
    st.markdown("<h2 style='text-align:center;'>בחרי את עתיד העסק שלך ✨</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='package-card'><h3>🌟 VIP Magic</h3><p>בינה מלאכותית ללא הגבלה</p><h2>₪199</h2></div>", unsafe_allow_html=True)
        if st.button("רכישת VIP 💎"):
            send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "VIP")
            st.session_state.page = "success"
            st.rerun()
    with c2:
        st.markdown("<div class='package-card'><h3>🚀 Growth Pack</h3><p>סוכן שיווק וניהול תוכן</p><h2>₪99</h2></div>", unsafe_allow_html=True)
        if st.button("רכישת צמיחה 🚀"):
            send_to_google(st.session_state.temp_mail, st.session_state.temp_pass, "Growth")
            st.session_state.page = "success"
            st.rerun()

# דף הצלחה
elif st.session_state.page == "success":
    st.balloons()
    st.markdown("<div class='magic-title'>ברוכה הבאה למשפחה!</div>", unsafe_allow_html=True)
    if st.button("כניסה למרכז הבקרה 🎬"):
        st.session_state.logged_in = True
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

# מרכז הבקרה המלא
elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.markdown(f"### שלום, {st.session_state.user_email} 👑")
        menu = st.radio("תפריט ניהול", ["🏠 דף הבית", "✍️ סוכן תוכן שיווקי", "📈 ניתוח נתונים AI"])
        if st.button("התנתקות"):
            st.session_state.logged_in = False
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 דף הבית":
        st.markdown(f"<div class='magic-title'>ברוכה השבה, {st.session_state.user_email.split('@')[0]}!</div>", unsafe_allow_html=True)
        st.info("המערכת מחוברת לטבלה שלך ומוכנה לעבודה.")
        
    elif menu == "✍️ סוכן תוכן שיווקי":
        st.header("מחולל תוכן קריאטיבי 🤖")
        topic = st.text_input("מה הנושא של הפוסט?")
        platform = st.selectbox("לאיזו פלטפורמה?", ["אינסטגרם", "טיקטוק", "פייסבוק"])
        if st.button("צור קסם ✨"):
            with st.spinner("ה-AI כותב עבורך..."):
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט שיווקי ל{platform} בנושא {topic}. השתמש באימוג'ים ושפה מושכת."}])
                st.write(res.choices[0].message.content)
