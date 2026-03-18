import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- הגדרות ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY")
    st.stop()

# --- פונקציות ---
def get_users_df():
    try:
        # קורא את הטבלה ומוודא שהיא לא נשמרת בזיכרון ישן (Cache)
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache_bust={st.session_state.get('refresh_count', 0)}")
        return df
    except:
        return pd.DataFrame()

# --- עיצוב ---
st.markdown("<style> .magic-title { background: linear-gradient(90deg, #7c3aed, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: bold; text-align: center; } </style>", unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "auth"

# --- דף כניסה/הרשמה ---
if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 כניסה", "📝 הרשמה"])

    with t1:
        l_email = st.text_input("אימייל").strip().lower()
        l_pwd = st.text_input("סיסמה", type="password")
        
        if st.button("כניסה למערכת 🚀"):
            df = get_users_df()
            if not df.empty:
                # הופך את כל הטבלה לטקסט קטן כדי למנוע בעיות של אותיות גדולות/קטנות
                df.columns = [c.lower() for c in df.columns]
                
                # מוצא את העמודה של המייל (זאת שמכילה את המילה email או מייל)
                email_col = [c for c in df.columns if 'email' in c or 'מייל' in c]
                
                if email_col:
                    col_name = email_col[0]
                    # מחפש את המשתמש
                    user_exists = df[df[col_name].astype(str).str.lower().str.strip() == l_email]
                    
                    if not user_exists.empty:
                        st.session_state.logged_in = True
                        st.session_state.user_email = l_email
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("המייל לא נמצא בטבלה. וודאי שנרשמת קודם!")
                        st.info("טיפ: גוגל מעדכנת את הטבלה הציבורית כל 5 דקות. אם נרשמת עכשיו, חכי דקה.")
                else:
                    st.error("לא מצאתי עמודת אימייל בטבלה שלך.")
            else:
                st.error("הטבלה ריקה או לא מפורסמת נכון.")

    with t2:
        st.subheader("הרשמה")
        r_email = st.text_input("מייל")
        r_pwd = st.text_input("סיסמה", type="password")
        if st.button("המשך לחבילות"):
            st.session_state.temp_mail, st.session_state.temp_pass = r_email, r_pwd
            st.session_state.page = "packages"
            st.rerun()

elif st.session_state.page == "dashboard":
    st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
    st.write(f"ברוכה הבאה, {st.session_state.user_email}!")
    if st.sidebar.button("התנתקות"):
        st.session_state.logged_in = False
        st.session_state.page = "auth"
        st.rerun()

# (המשך הלוגיקה של החבילות נשאר זהה...)
