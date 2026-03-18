import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות וחיבורים ---
st.set_page_config(page_title="Business OS", page_icon="💼", layout="wide")
# הקישור הציבורי שלך
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. פונקציות ליבה ---
def get_users_df():
    try:
        # שימוש בפרמטר רענון כדי לעקוף Cache של דפדפנים
        url = f"{SHEET_CSV_URL}&nocache={pd.Timestamp.now().timestamp()}"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame()

def save_to_google(email, data_dict):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    # איחוד כל המידע לשדה הנתונים בטבלה
    info = " | ".join([f"{k}: {v}" for k, v in data_dict.items()])
    payload = {"entry.855862094": email, "entry.1847739029": info}
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        pass

# --- 3. עיצוב CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite; font-size: 50px; font-weight: bold; text-align: center;
    }
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; width: 100%; font-weight: bold; height: 50px; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבי עמוד ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- 5. לוגיקת דפים ---

# א. דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Business OS</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])
    
    with t1:
        l_mail = st.text_input("אימייל", key="login_email_val").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="login_pass_val")
        if st.button("כניסה למערכת 🚀", key="login_btn_final"):
            with st.spinner("מאמת נתונים..."):
                df = get_users_df()
                if not df.empty:
                    # בדיקה האם המייל קיים איפשהו בטבלה
                    search_str = l_mail
                    # הופך את כל הטבלה לסטרינג אחד גדול ובודק אם המייל שם
                    table_as_string = df.astype(str).apply(lambda x: x.str.lower()).to_string().lower()
                    
                    if search_str in table_as_string:
                        st.session_state.user_email = l_mail
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("לא נמצא משתמש כזה. ודאי שנרשמת ושהטבלה מפורסמת.")
                else:
                    st.error("לא ניתן לגשת לנתוני המשתמשים כרגע.")

    with t2:
        r_mail = st.text_input("מייל לעסק", key="reg_email_val").strip().lower()
        r_pass = st.text_input("סיסמה חדשה", type="password", key="reg_pass_val")
        if st.button("המשך להקמת העסק ✨", key="reg_btn_final"):
            if r_mail and r_pass:
                st.session_state.temp_mail = r_mail
                st.session_state.temp_pass = r_pass
                st.session_state.page = "onboarding"
                st.rerun()

# ב. דף אונבורדינג
elif st.session_state.page == "onboarding":
    st.header("ספרי לנו על העסק שלך 🖋️")
    name = st.text_input("שם העסק", key="biz_name")
    desc = st.text_area("מה העסק עושה?", key="biz_desc")
    target = st.text_input("מי קהל היעד?", key="biz_target")
    if st.button("שמור והמשך לבחירת חבילה"):
        st.session_state.biz_data = {"name": name, "desc": desc, "target": target}
        st.session_state.page = "packages"
        st.rerun()

# ג. דף חבילות
elif st.session_state.page == "packages":
    st.header("בחרי מסלול")
    if st.button("רכישת מסלול פרימיום 🌟"):
        save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "Premium", "pass": st.session_state.temp_pass})
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

# ד. מרכז הבקרה (Dashboard)
elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.write(f"מחובר: **{st.session_state.user_email}**")
        menu = st.radio("תפריט", ["🏠 בית", "✍️ סוכן תוכן AI", "💬 צ'אט שירות", "👥 ניהול לקוחות"])
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 בית":
        st.markdown(f"## ברוך הבא לפורטל הניהול")
        st.success("המערכת פעילה ומחוברת.")
        
    elif menu == "✍️ סוכן תוכן AI":
        st.header("יצירת תוכן מותאם")
        goal = st.text_input("מה המטרה?")
        if st.button("צור פוסט"):
            biz = st.session_state.get('biz_data', {})
            prompt = f"כתוב פוסט לעסק בשם {biz.get('name')}. תיאור: {biz.get('desc')}. קהל: {biz.get('target')}. מטרה: {goal}."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.write(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        st.header("נציג שירות AI")
        q = st.chat_input("שאל את המערכת...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"אתה נציג שירות אדיב."}, {"role":"user","content":q}])
            st.write(res.choices[0].message.content)

    elif menu == "👥 ניהול לקוחות":
        st.header("רשימת לקוחות")
        st.dataframe(get_users_df())
