import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="wide")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"

MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. THE ZARA EXECUTIVE DESIGN (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: center;
        background-color: #ffffff; color: #000000;
    }

    .brand-header {
        font-size: 50px; font-weight: 700; letter-spacing: -1px;
        margin-top: 40px; color: #000; border-bottom: 1px solid #000;
        display: inline-block; padding-bottom: 10px; margin-bottom: 10px;
    }
    
    .brand-sub {
        font-size: 14px; letter-spacing: 5px; color: #888;
        text-transform: uppercase; margin-bottom: 50px;
    }

    /* כפתורים רחבים ויוקרתיים */
    .stButton>button {
        background-color: #000000;
        color: #ffffff; border-radius: 0px; 
        height: 60px; font-size: 18px; font-weight: 300;
        width: 100%; border: none; letter-spacing: 1px;
        transition: 0.3s; margin-bottom: 20px;
    }
    .stButton>button:hover { background-color: #333; transform: translateY(-2px); }

    /* שדות טקסט רחבים וברורים */
    input, textarea {
        background-color: #fafafa !important;
        color: #000 !important;
        border: 1px solid #eee !important;
        border-radius: 0px !important;
        text-align: right !important;
        font-size: 18px !important;
        padding: 15px !important;
    }
    
    /* בועות צ'אט מעוצבות */
    .chat-container {
        border: 1px solid #eee; padding: 20px; background: #fdfdfd; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. פונקציות ליבה ---
def check_user_status(email):
    email_clean = str(email).strip().lower()
    if email_clean == MY_ADMIN_EMAIL.lower():
        return "ADMIN", "מנכ\"לית מיי"
    try:
        url = f"{SHEET_CSV_URL}&t={time.time()}"
        df = pd.read_csv(url)
        for _, row in df.iterrows():
            if email_clean in " ".join(row.astype(str)).lower():
                # מנסה לחלץ שם עסק
                info = str(row.iloc[-1])
                biz = info.split('|')[-1].replace('Biz:', '').strip() if '|' in info else "העסק שלך"
                return "USER", biz
        return "NEW", None
    except: return "NEW", None

# --- 4. ניהול דפים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'tool' not in st.session_state: st.session_state.tool = "home"

# --- א. כניסה והרשמה ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-header'>MEIROM MAGIC</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-sub'>ARTIFICIAL INTELLIGENCE SYSTEMS</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### כניסה")
        l_m = st.text_input("אימייל משתמש", key="l_m")
        l_p = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה"):
            status, name = check_user_status(l_m)
            if status != "NEW" or l_m == MY_ADMIN_EMAIL:
                st.session_state.user_email = l_m
                st.session_state.biz_name = name if name else "העסק"
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("משתמש לא נמצא.")

    with col2:
        st.write("### הרשמה")
        r_m = st.text_input("אימייל חדש", key="r_m")
        r_b = st.text_input("שם העסק", key="r_b")
        r_p = st.text_input("סיסמה", type="password", key="r_p")
        if st.button("רישום משתמש"):
            if r_m and r_b:
                requests.post(FORM_URL, data={"entry.855862094": r_m, "entry.1847739029": f"Pass: {r_p} | Biz: {r_b}"})
                st.session_state.user_email = r_m
                st.session_state.biz_name = r_b
                st.session_state.page = "dashboard"
                st.rerun()

# --- ב. לוח בקרה (מרכז העבודה) ---
elif st.session_state.page == "dashboard":
    # זיהוי פנייה
    welcome = "ברוכה הבאה מנכ\"לית מיי" if st.session_state.user_email == MY_ADMIN_EMAIL else f"שלום, {st.session_state.biz_name}"
    
    st.markdown(f"<div class='brand-header'>{welcome}</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # תפריט ראשי רחב
    if st.session_state.tool == "home":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🤖 סוכן תוכן AI"):
                st.session_state.tool = "ai"
                st.rerun()
        with c2:
            if st.button("💬 צ'אט שירות לקוחות"):
                st.session_state.tool = "chat"
                st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    # --- כלי 1: סוכן תוכן ---
    elif st.session_state.tool == "ai":
        st.write("### סוכן תוכן שיווקי")
        topic = st.text_area("על מה נכתוב היום? (פרטי כמה שיותר)", height=150)
        if st.button("ייצור תוכן"):
            if topic:
                with st.spinner("ה-AI יוצר קסם..."):
                    res = client.chat.completions.create(model="llama-3.3-70b-versatile", 
                        messages=[{"role":"user","content":f"כתוב פוסט שיווקי מדהים עבור העסק {st.session_state.biz_name} בנושא: {topic}"}])
                    st.markdown("---")
                    st.write(res.choices[0].message.content)
            else: st.warning("אנא הזיני נושא.")
        
        if st.button("חזרה לתפריט"):
            st.session_state.tool = "home"
            st.rerun()

    # --- כלי 2: צ'אט בוט ---
    elif st.session_state.tool == "chat":
        st.write("### צ'אט שירות לקוחות חכם")
        st.write("הזיני את שאלת הלקוח וה-AI יענה בשמך:")
        
        user_query = st.text_input("שאלת הלקוח:")
        if st.button("קבלת תשובה"):
            if user_query:
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", 
                    messages=[{"role":"system","content":f"את נציגת שירות של {st.session_state.biz_name}"}, {"role":"user","content":user_query}])
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                st.write(res.choices[0].message.content)
                st.markdown("</div>", unsafe_allow_html=True)

        if st.button("חזרה לתפריט"):
            st.session_state.tool = "home"
            st.rerun()
