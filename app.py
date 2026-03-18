import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
from datetime import datetime

# --- 1. הגדרות דף וחיבורים ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"שגיאת חיבור (Secrets/Requirements): {e}")
    st.stop()

# --- 2. עיצוב CSS (הקסם הסגול) ---
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
        font-size: 60px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white; border: none; border-radius: 20px; padding: 10px 25px; transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. לוגיקה וזיכרון ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'plan' not in st.session_state: st.session_state.plan = None
if 'biz_info' not in st.session_state: st.session_state.biz_info = ""

# --- 4. פונקציות גוגל שיטס ---
def get_all_users():
    try:
        df = conn.read(spreadsheet=st.secrets["GSHEET_URL"])
        return df
    except:
        return pd.DataFrame(columns=["Email", "Password"])

def save_new_user(email, password):
    df = get_all_users()
    new_user = pd.DataFrame([{"Email": email, "Password": password}])
    updated_df = pd.concat([df, new_user], ignore_index=True)
    conn.update(spreadsheet=st.secrets["GSHEET_URL"], data=updated_df)

# --- 5. ניווט דפים ---

# א. דף לקוח חיצוני
if st.query_params.get("view") == "customer":
    st.markdown("<div class='magic-title'>ברוכים הבאים</div>", unsafe_allow_html=True)
    st.write(st.session_state.biz_info)
    customer_msg = st.chat_input("איך אפשר לעזור?")
    if customer_msg:
        st.chat_message("user").write(customer_msg)
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Biz: {st.session_state.biz_info}. User: {customer_msg}. Hebrew."}])
        st.chat_message("assistant").write(res.choices[0].message.content)
    st.stop()

# ב. דף כניסה והרשמה (עם חיבור לשיטס)
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    
    with tab1:
        le = st.text_input("אימייל", key="l_e")
        lp = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה 🚀", key="l_b"):
            all_users = get_all_users()
            if not all_users.empty and le in all_users['Email'].values:
                correct_pass = all_users[all_users['Email'] == le]['Password'].values[0]
                if str(lp) == str(correct_pass):
                    st.session_state.logged_in = True
                    st.rerun()
            st.error("פרטים לא נכונים או משתמש לא קיים")
            
    with tab2:
        ne = st.text_input("מייל חדש", key="r_e")
        np = st.text_input("סיסמה", type="password", key="r_p")
        if st.button("צרי חשבון ✨", key="r_b"):
            save_new_user(ne, np)
            st.balloons()
            st.success("נרשמת בטבלה! עכשיו אפשר להתחבר.")

# ג. דף ניהול (אחרי התחברות)
else:
    if st.session_state.plan is None:
        st.header("בחרי מסלול")
        if st.button("Enterprise (2500₪)"): st.session_state.plan = "Enterprise"; st.rerun()
    else:
        with st.sidebar:
            st.write(f"חבילה: {st.session_state.plan}")
            page = st.radio("ניווט:", ["✨ דף הבית", "🚀 סוכן שיווק", "🏢 הגדרות עסק", "🔗 קישור ללקוחות"])
            if st.button("התנתקות"): st.session_state.logged_in = False; st.rerun()

        if page == "✨ דף הבית":
            st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        
        elif page == "🏢 הגדרות עסק":
            st.header("הגדרות עסק")
            st.session_state.biz_info = st.text_area("מידע ללקוחות:", value=st.session_state.biz_info)
            st.button("שמור ✅")

        elif page == "🔗 קישור ללקוחות":
            st.header("הקישור שלך 🌐")
            st.code("https://YOUR-APP.streamlit.app/?view=customer")
