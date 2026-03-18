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
    # שומרים את כל פרטי העסק והחבילה בשדה המידע
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
        animation: shine 3s linear infinite; font-size: 50px; font-weight: bold; text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .package-card { border: 2px solid #7c3aed; border-radius: 15px; padding: 20px; text-align: center; background: white; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(45deg, #7c3aed, #ec4899); color: white; border-radius: 20px; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. ניהול מצבי עמוד ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- 5. ניווט דפים ---

# דף כניסה והרשמה
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Business OS</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה למערכת", "📝 הקמת עסק חדש"])
    
    with t1:
        l_mail = st.text_input("אימייל", key="login_m").strip().lower()
        if st.button("כניסה 🚀"):
            df = get_users_df()
            if not df.empty and l_mail in df.astype(str).values:
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("משתמש לא נמצא. הירשמי קודם!")

    with t2:
        r_mail = st.text_input("מייל לעסק", key="reg_m")
        r_pass = st.text_input("סיסמה", type="password", key="reg_p")
        if st.button("המשך להגדרת העסק"):
            st.session_state.temp_mail = r_mail
            st.session_state.page = "onboarding"
            st.rerun()

# דף הגדרת עסק (Onboarding)
elif st.session_state.page == "onboarding":
    st.header("ספרי ל-AI על העסק שלך 🖋️")
    b_name = st.text_input("שם העסק", placeholder="למשל: מיירום מג'יק")
    b_desc = st.text_area("מה העסק עושה?", placeholder="למשל: סוכנות שיווק שמתמחה ב...")
    b_target = st.text_input("מי קהל היעד?", placeholder="למשל: בעלות עסקים קטנים")
    
    if st.button("שמור והמשך לבחירת חבילה"):
        st.session_state.biz_data = {"name": b_name, "desc": b_desc, "target": b_target}
        st.session_state.page = "packages"
        st.rerun()

# דף חבילות
elif st.session_state.page == "packages":
    st.header("בחרי מסלול")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='package-card'><h3>🌟 VIP</h3><p>AI ללא הגבלה</p></div>", unsafe_allow_html=True)
        if st.button("בחרתי VIP"):
            save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "VIP"})
            st.session_state.page = "dashboard"
            st.session_state.user_email = st.session_state.temp_mail
            st.rerun()
    with c2:
        st.markdown("<div class='package-card'><h3>🚀 Basic</h3><p>כלים בסיסיים</p></div>", unsafe_allow_html=True)
        if st.button("בחרתי בסיסי"):
            save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "Basic"})
            st.session_state.page = "dashboard"
            st.session_state.user_email = st.session_state.temp_mail
            st.rerun()

# מרכז הבקרה (הפורטל)
elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.title("Control Center")
        menu = st.radio("תפריט", ["🏠 דף הבית", "✍️ סוכן תוכן שיווקי", "💬 צ'אט שירות", "👥 ניהול לקוחות (למנהלת)"])
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 דף הבית":
        st.markdown(f"## ברוך הבא, {st.session_state.user_email}")
        st.info("כאן תוכל לנהל את העסק שלך בעזרת הכלים החכמים שלנו.")
        
    elif menu == "✍️ סוכן תוכן שיווקי":
        st.header("יצירת פוסטים מותאמים אישית")
        goal = st.text_input("מה המטרה של הפוסט?")
        if st.button("צור תוכן"):
            biz = st.session_state.get('biz_data', {})
            prompt = f"כתוב פוסט לעסק בשם {biz.get('name')}. העסק עוסק ב: {biz.get('desc')}. קהל היעד הוא: {biz.get('target')}. מטרה: {goal}."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.write(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        st.header("צ'אטבוט שירות לקוחות")
        user_q = st.chat_input("שאל משהו...")
        if user_q:
            st.chat_message("user").write(user_q)
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"אתה נציג שירות אדיב."}, {"role":"user","content":user_q}])
            st.chat_message("assistant").write(res.choices[0].message.content)

    elif menu == "👥 ניהול לקוחות (למנהלת)":
        st.header("דאטה של כל המערכת")
        df = get_users_df()
        st.dataframe(df)
