import streamlit as st
from groq import Groq
import smtplib, time, urllib.parse
from email.message import EmailMessage

# --- חיבורים ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Key!")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

def go(p):
    st.session_state.page = p
    st.rerun()

if 'page' not in st.session_state: st.session_state.page = 'welcome'

# --- עיצוב יוקרתי (כולל כפתורי הקישור) ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #fdfbff; }
    
    /* כפתורי המערכת הסטנדרטיים */
    .stButton>button { 
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
        color: white !important; border-radius: 20px; border: none; padding: 15px;
        font-weight: bold; font-size: 18px; width: 100%; transition: 0.3s;
    }
    
    /* עיצוב כפתורי הקישור (יומן ווואטסאפ) */
    .magic-link-button {
        display: block;
        width: 100%;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
        color: white !important;
        text-decoration: none !important;
        border-radius: 20px;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(124,58,237,0.2);
        transition: 0.3s;
    }
    .magic-link-button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(124,58,237,0.4); }
    .wa-button { background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%); }
</style>
""", unsafe_allow_html=True)

# --- דפים ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='color:#7c3aed; font-size:45px; text-align:center;'>MEIROM MAGIC AI 🧚‍♀️</h1>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    st.write("### הופכים את העסק שלך לקסם אוטומטי")
    if st.button("בואי נתחיל את הקסם ✨"): go('options')

elif st.session_state.page == 'options':
    st.header("בחרי את עוצמת הקסם")
    c1, c2, c3 = st.columns(3)
    plans = [("Basic", "250"), ("Pro ⭐", "750"), ("Enterprise", "2500")]
    for i, (p, pr) in enumerate(plans):
        with [c1, c2, c3][i]:
            st.markdown(f"<div style='background:white; padding:20px; border-radius:20px; border:1px solid #eee; text-align:center;'><h3>{p}</h3><h2>₪{pr}</h2></div>", unsafe_allow_html=True)
            if st.button(f"בחר {p}", key=f"p{i}"):
                st.session_state.plan, st.session_state.price = p, pr
                go('payment')

elif st.session_state.page == 'payment':
    st.header("💳 תשלום מאובטח")
    with st.container(border=True):
        st.write(f"מסלול: **{st.session_state.plan}** | סכום: **₪{st.session_state.price}**")
        st.text_input("מספר כרטיס אשראי", placeholder="0000 0000 0000 0000")
        if st.button("אשר תשלום והמשך ✅"):
            with st.spinner("מאמת..."): time.sleep(1.5)
            go('main')
    if st.button("⬅️ חזור"): go('options')

elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        st.subheader("מערכות")
        g_on = st.toggle("סנכרון יומן", True)
        w_on = st.toggle("שליחת הודעה", True)
    
    with st.form("magic_form"):
        biz = st.text_input("שם הלקוח / העסק")
        em = st.text_input("אימייל לשליחת סיכום")
        task = st.text_area("מה לבצע? (למשל: תקבע פגישה למחר ב-10:00)")
        if st.form_submit_button("הפעל סוכן מבצע ⚡"):
            if task and biz:
                with st.status("הפייה בתהליך הטמעה...") as s:
                    # AI - זמן וסיכום
                    res_time = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Extract date from '{task}' as YYYYMMDDTHHMMSSZ. Return only code."}]).choices[0].message.content.strip()
                    report = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Short summary in Hebrew for {biz}: {task}."}]).choices[0].message.content
                    
                    #
