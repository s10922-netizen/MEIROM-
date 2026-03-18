import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. Apple Page Setup ---
st.set_page_config(page_title="Magic OS", page_icon="🍏", layout="centered")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key Missing")
    st.stop()

# --- 2. APPLE MINIMALIST CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: right;
        background-color: #ffffff;
    }

    /* כותרת אפל קלאסית */
    .apple-header {
        font-size: 34px; font-weight: 600; color: #1d1d1f;
        text-align: center; padding-top: 50px; margin-bottom: 10px;
    }
    
    .apple-sub {
        font-size: 18px; color: #86868b; text-align: center; margin-bottom: 40px;
    }

    /* תיבות זכוכית נקיות */
    .apple-box {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid #d2d2d7;
        margin-bottom: 20px;
    }

    /* כפתור כחול אפל */
    .stButton>button {
        background-color: #0071e3;
        color: white; border-radius: 12px; border: none;
        height: 50px; font-size: 17px; font-weight: 400; width: 100%;
    }
    .stButton>button:hover { background-color: #0077ed; }

    /* הסתרת אלמנטים מיותרים */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
def get_clean_df():
    try:
        url = f"{SHEET_CSV_URL}&t={pd.Timestamp.now().timestamp()}"
        df = pd.read_csv(url)
        # ניקוי כל הטבלה מרווחים ואותיות גדולות
        return df.astype(str).apply(lambda x: x.str.strip().str.lower())
    except:
        return pd.DataFrame()

# --- 4. NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""

if st.session_state.page == "auth":
    st.markdown("<div class='apple-header'>Magic OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='apple-sub'>הכניסה לעסק שלך.</div>", unsafe_allow_html=True)
    
    tab_in, tab_up = st.tabs(["כניסה", "הרשמה"])
    
    with tab_in:
        st.markdown("<div class='apple-box'>", unsafe_allow_html=True)
        m = st.text_input("אימייל", key="m_in").strip().lower()
        if st.button("התחברי"):
            df = get_clean_df()
            if not df.empty:
                # בדיקה האם המייל מופיע איפשהו בשורות
                found = df.apply(lambda row: m in row.values, axis=1).any()
                if found:
                    st.session_state.user_email = m
                    st.session_state.page = "dashboard"
                    st.rerun()
                else: st.error("לא מצאנו את המייל בטבלה.")
            else: st.error("שגיאה בחיבור לנתונים.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_up:
        st.markdown("<div class='apple-box'>", unsafe_allow_html=True)
        rm = st.text_input("מייל לעסק", key="m_up")
        rp = st.text_input("סיסמה", type="password", key="p_up")
        if st.button("התחלת הקמה"):
            st.session_state.temp_m, st.session_state.temp_p = rm, rp
            st.session_state.page = "onboarding"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "onboarding":
    st.markdown("<div class='apple-header'>פרטי העסק</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='apple-box'>", unsafe_allow_html=True)
        name = st.text_input("שם המותג")
        desc = st.text_area("מה העסק עושה?")
        if st.button("שמור"):
            st.session_state.biz_data = {"name": name, "desc": desc}
            st.session_state.page = "dashboard" # כניסה ישירה
            st.session_state.user_email = st.session_state.temp_m
            # שליחה לגוגל
            url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
            requests.post(url, data={"entry.855862094": st.session_state.temp_m, "entry.1847739029": f"Pass: {st.session_state.temp_p} | Biz: {name}"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='apple-header'>Welcome</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='apple-sub'>{st.session_state.user_email}</div>", unsafe_allow_html=True)
    
    menu = st.selectbox("", ["🏠 בית", "✍️ סוכן תוכן", "💬 צ'אט שירות"])
    
    st.markdown("<div class='apple-box'>", unsafe_allow_html=True)
    if menu == "🏠 בית":
        st.write("כל המערכות פועלות. ה-AI מסונכרן.")
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()
            
    elif menu == "✍️ סוכן תוכן":
        goal = st.text_input("מה נכתוב היום?")
        if st.button("ייצור פוסט"):
            biz = st.session_state.get('biz_data', {})
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"כתוב פוסט ל{biz.get('name')}: {goal}"}])
            st.info(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות":
        q = st.chat_input("שאלת לקוח...")
        if q:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"ענה רק על שאלות עסקית."}, {"role":"user","content":q}])
            st.markdown(f"<div style='background:#f5f5f7; padding:15px; border-radius:15px;'>{res.choices[0].message.content}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
