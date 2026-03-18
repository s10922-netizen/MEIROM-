import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות וחיבורים ---
st.set_page_config(page_title="Business OS", page_icon="💼", layout="wide")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. פונקציות ליבה ---
def get_users_df():
    try:
        # הוספת פרמטר זמן כדי למנוע טעינת נתונים ישנים מהדפדפן
        url = f"{SHEET_CSV_URL}&refresh={pd.Timestamp.now().timestamp()}"
        return pd.read_csv(url)
    except: return pd.DataFrame()

def save_to_google(email, data_dict):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    # שמירת כל המידע בשורה אחת
    info = " | ".join([f"{k}: {v}" for k, v in data_dict.items()])
    payload = {"entry.855862094": email, "entry.1847739029": info}
    try:
        requests.post(url, data=payload)
    except: pass

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
    @keyframes shine { to { background-position: 200% center; } }
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; width: 100%; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבי עמוד ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- 5. ניווט דפים ---

# דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Business OS</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])
    
    with t1:
        l_mail = st.text_input("אימייל", key="l_m").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה למערכת 🚀"):
            df = get_users_df()
            # מחפש את המייל והסיסמה בטקסט הגולמי של הטבלה
            all_text = df.astype(str).apply(lambda x: x.str.lower()).values.flatten()
            if l_mail in all_text and l_pass in all_text:
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("הפרטים לא נמצאו. אם נרשמת הרגע - המתיני 5 דקות לעדכון גוגל.")

    with t2:
        r_mail = st.text_input("מייל לעסק", key="r_m").strip().lower()
        r_pass = st.text_input("סיסמה חדשה", type="password", key="r_p")
        if st.button("המשך להקמת העסק ✨"):
            if r_mail and r_pass:
                st.session_state.temp_mail = r_mail
                st.session_state.temp_pass = r_pass
                st.session_state.page = "onboarding"
                st.rerun()

# דף אונבורדינג (פירוט העסק)
elif st.session_state.page == "onboarding":
    st.header("ספרי ל-AI על העסק שלך 🖋️")
    name = st.text_input("שם העסק")
    desc = st.text_area("מה העסק עושה? (פירוט עבור ה-AI)")
    target = st.text_input("מי הלקוחות?")
    if st.button("שמור והמשך"):
        st.session_state.biz_data = {"name": name, "desc": desc, "target": target}
        st.session_state.page = "packages"
        st.rerun()

# דף חבילות
elif st.session_state.page == "packages":
    st.header("בחרי מסלול")
    if st.button("מסלול פרימיום 🌟"):
        # שליחה לגוגל
        final_data = {**st.session_state.biz_data, "plan": "Premium", "pass": st.session_state.temp_pass}
        save_to_google(st.session_state.temp_mail, final_data)
        # כניסה מיידית בלי לחכות לטבלה!
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

# מרכז הבקרה (הפורטל)
elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.write(f"שלום, {st.session_state.user_email}")
        menu = st.radio("תפריט", ["🏠 בית", "✍️ סוכן תוכן AI", "💬 צ'אט שירות", "📊 ניהול (מנהלת)"])
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 בית":
        st.markdown(f"## ברוך הבא לפורטל הניהול של {st.session_state.biz_data.get('name', 'העסק שלך')}")
        st.success("המערכת פעילה!")
        
    elif menu == "✍️ סוכן תוכן AI":
        st.header("יצירת תוכן שיווקי")
        goal = st.text_input("מה המטרה היום?")
        if st.button("צור פוסט"):
            biz = st.session_state.biz_data
            prompt = f"כתוב פוסט לעסק {biz.get('name')} שעושה {biz.get('desc')} לקהל {biz.get('target')}. מטרה: {goal}."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.write(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        st.header("נציג שירות AI")
        q = st.chat_input("שאלת לקוח...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"אתה נציג שירות אדיב."}, {"role":"user","content":q}])
            st.write(res.choices[0].message.content)

    elif menu == "📊 ניהול (מנהלת)":
        st.header("כל הלקוחות בטבלה")
        st.dataframe(get_users_df())
