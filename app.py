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
        url = f"{SHEET_CSV_URL}&refresh={pd.Timestamp.now().timestamp()}"
        return pd.read_csv(url)
    except: return pd.DataFrame()

def save_to_google(email, data_dict):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    info = " | ".join([f"{k}: {v}" for k, v in data_dict.items()])
    payload = {"entry.855862094": email, "entry.1847739029": info}
    requests.post(url, data=payload)

# --- 3. עיצוב CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite; font-size: 45px; font-weight: bold; text-align: center;
    }
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבי עמוד ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- 5. ניווט דפים ---

if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Business OS</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])
    
    with t1:
        l_mail = st.text_input("אימייל", key="lin_m").strip().lower()
        l_pass = st.text_input("סיסמה", type="password", key="lin_p")
        if st.button("כניסה למערכת 🚀"):
            df = get_users_df()
            all_text = df.astype(str).apply(lambda x: x.str.lower()).to_string().lower()
            if l_mail in all_text:
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("משתמש לא נמצא.")

    with t2:
        r_mail = st.text_input("מייל לעסק", key="rin_m").strip().lower()
        r_pass = st.text_input("סיסמה חדשה", type="password", key="rin_p")
        if st.button("המשך להקמת העסק ✨"):
            if r_mail and r_pass:
                st.session_state.temp_mail, st.session_state.temp_pass = r_mail, r_pass
                st.session_state.page = "onboarding"
                st.rerun()

elif st.session_state.page == "onboarding":
    st.header("ספרי לנו על העסק שלך 🖋️")
    name = st.text_input("שם העסק")
    desc = st.text_area("מה העסק עושה?")
    target = st.text_input("מי הקהל?")
    if st.button("שמור והמשך"):
        st.session_state.biz_data = {"name": name, "desc": desc, "target": target}
        st.session_state.page = "packages"
        st.rerun()

elif st.session_state.page == "packages":
    st.header("בחרי מסלול")
    if st.button("מסלול פרימיום 🌟"):
        save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "Premium", "pass": st.session_state.temp_pass})
        st.session_state.user_email = st.session_state.temp_mail
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.write(f"שלום, **{st.session_state.user_email}**")
        
        # --- הגדרת התפריט לפי סוג המשתמש ---
        menu_options = ["🏠 בית", "✍️ סוכן תוכן AI", "💬 צ'אט שירות"]
        
        # 🔑 אם המייל הוא המייל שלך, תוסיפי את כפתור הניהול הסודי!
        if st.session_state.user_email == "admin@magic.com":
            menu_options.append("👑 ניהול לקוחות")
            
        menu = st.radio("תפריט ניהול", menu_options)
        
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 בית":
        st.markdown(f"## ברוך הבא לפורטל הניהול")
        st.info("כאן תוכלו להשתמש בכלי ה-AI שלכם.")
        
    elif menu == "✍️ סוכן תוכן AI":
        st.header("יצירת תוכן מותאם")
        goal = st.text_input("מה המטרה?")
        if st.button("צור פוסט"):
            biz = st.session_state.biz_data
            prompt = f"כתוב פוסט לעסק {biz.get('name')} שעושה {biz.get('desc')} לקהל {biz.get('target')}. מטרה: {goal}."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.write(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        st.header("צ'אט שירות לקוחות")
        q = st.chat_input("שאל...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"נציג שירות אדיב."}, {"role":"user","content":q}])
            st.write(res.choices[0].message.content)

    # 🔒 החלק הזה יוצג רק לך!
    elif menu == "👑 ניהול לקוחות":
        st.header("מנכ\"לית, הנה הדאטה שלך:")
        st.dataframe(get_users_df())
