import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MagicOS", page_icon="🪄", layout="centered") # Centered מתאים יותר למובייל

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב UI/UX מובייל יוקרתי ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #F7F9FC;
    }

    /* כותרת דקה ויוקרתית */
    .app-header {
        background: linear-gradient(135deg, #6D28D9 0%, #D946EF 100%);
        padding: 40px 20px;
        border-radius: 0 0 40px 40px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(109, 40, 217, 0.2);
    }

    /* כרטיסיות 'ווידג'ט' */
    .card {
        background: white;
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* כפתורים מעוגלים */
    .stButton>button {
        background: #6D28D9;
        color: white;
        border-radius: 50px;
        border: none;
        height: 55px;
        font-size: 18px;
        font-weight: 700;
        width: 100%;
        margin-top: 10px;
    }

    /* בועות צ'אט */
    .user-bubble { background-color: #6D28D9; color: white; padding: 15px; border-radius: 20px 20px 0 20px; margin: 10px 0; display: inline-block; }
    .ai-bubble { background-color: #F1F5F9; color: #1E293B; padding: 15px; border-radius: 20px 20px 20px 0; margin: 10px 0; display: inline-block; border: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# --- 3. פונקציות ליבה ---
def get_users_df():
    try:
        url = f"{SHEET_CSV_URL}&cachebust={pd.Timestamp.now().timestamp()}"
        return pd.read_csv(url)
    except: return pd.DataFrame()

def save_to_google(email, data_dict):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    info = " | ".join([f"{k}: {v}" for k, v in data_dict.items()])
    requests.post(url, data={"entry.855862094": email, "entry.1847739029": info})

# --- 4. לוגיקת ניווט ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- א. דף כניסה ---
if st.session_state.page == "auth":
    st.markdown("<div class='app-header'><h1>MagicOS</h1><p>המרכז העסקי שלך</p></div>", unsafe_allow_html=True)
    
    mode = st.radio("", ["כניסה", "הרשמה"], horizontal=True)
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        u_email = st.text_input("אימייל").strip().lower()
        if mode == "כניסה":
            u_pass = st.text_input("סיסמה", type="password")
            if st.button("כניסה למערכת 🚀"):
                df = get_users_df()
                # חיפוש חסין: בודק אם המייל מופיע איפשהו בשורות
                if not df.empty and any(df.astype(str).apply(lambda x: u_email in x.values, axis=1)):
                    st.session_state.user_email = u_email
                    st.session_state.page = "dashboard"
                    st.rerun()
                else: st.error("לא מצאנו אותך. ודאי שנרשמת.")
        else:
            u_pass = st.text_input("סיסמה חדשה", type="password")
            if st.button("התחלת עבודה ✨"):
                st.session_state.temp_mail, st.session_state.temp_pass = u_email, u_pass
                st.session_state.page = "onboarding"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- ב. דף אונבורדינג ---
elif st.session_state.page == "onboarding":
    st.markdown("<div class='app-header'><h1>הגדרת עסק</h1></div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        b_name = st.text_input("שם המותג")
        b_desc = st.text_area("מה אתם מוכרים?")
        b_target = st.text_input("מי הקהל?")
        if st.button("המשך לחבילות ⬅️"):
            st.session_state.biz_data = {"name": b_name, "desc": b_desc, "target": b_target}
            st.session_state.page = "packages"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- ג. דף חבילות ---
elif st.session_state.page == "packages":
    st.markdown("<div class='app-header'><h1>בחירת חבילה</h1></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card' style='text-align:center;'><h3>VIP</h3><h2>₪199</h2></div>", unsafe_allow_html=True)
        if st.button("בחרתי VIP"):
            save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "VIP", "pass": st.session_state.temp_pass})
            st.session_state.user_email = st.session_state.temp_mail
            st.session_state.page = "dashboard"
            st.rerun()

# --- ד. מרכז הבקרה (Dashboard) ---
elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='app-header'><h3>שלום, {st.session_state.user_email.split('@')[0]}</h3></div>", unsafe_allow_html=True)
    
    menu = st.selectbox("תפריט מהיר", ["🏠 דף הבית", "✍️ סוכן תוכן AI", "💬 צ'אט שירות לקוחות"])
    
    if menu == "🏠 דף הבית":
        st.markdown("<div class='card'><h4>סטטוס מערכת</h4><p>הכל פועל כשורה. ה-AI מסונכרן לעסק שלך.</p></div>", unsafe_allow_html=True)
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    elif menu == "✍️ סוכן תוכן AI":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        goal = st.text_input("מה המטרה היום?")
        if st.button("ייצור פוסט ✨"):
            biz = st.session_state.biz_data
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט לעסק {biz.get('name')} שעושה {biz.get('desc')}. מטרה: {goal}"}])
            st.info(res.choices[0].message.content)
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "💬 צ'אט שירות לקוחות":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        q = st.chat_input("שאלת לקוח...")
        if q:
            # הוראות קשוחות לצ'אטבוט
            sys_msg = f"אתה נציג שירות של {st.session_state.biz_data.get('name')}. ענה רק על שאלות מקצועיות הקשורות לעסק. אל תנהל שיחות חולין."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":sys_msg}, {"role":"user","content":q}])
            st.markdown(f"<div class='ai-bubble'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
