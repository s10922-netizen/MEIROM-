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

# --- עיצוב יוקרתי ומתוקן ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #fdfbff; }
    
    /* תיקון הבלגן בסטטוס ובתיבות */
    [data-testid="stStatusWidget"] { direction: rtl; text-align: right; }
    .stAlert { direction: rtl; text-align: right; border-radius: 15px; }

    .stButton>button { 
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
        color: white !important; border-radius: 20px; border: none; padding: 15px;
        font-weight: bold; font-size: 18px; width: 100%; transition: 0.3s;
    }
    
    .magic-link-button {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        text-align: center; background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
        color: white !important; text-decoration: none !important; border-radius: 20px;
        font-weight: bold; font-size: 18px; box-shadow: 0 4px 15px rgba(124,58,237,0.2);
    }
    .wa-button { background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%); }
</style>
""", unsafe_allow_html=True)

# --- דף 1: ברוכים הבאים ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='color:#7c3aed; font-size:45px; text-align:center;'>MEIROM MAGIC AI 🧚‍♀️</h1>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    st.write("### הופכים את העסק שלך לקסם אוטומטי")
    if st.button("בואי נתחיל את הקסם ✨"): go('options')

# --- דף 2: בחירת מסלול ---
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

# --- דף 3: תשלום ---
elif st.session_state.page == 'payment':
    st.header("💳 תשלום מאובטח")
    with st.container(border=True):
        st.write(f"מסלול: **{st.session_state.plan}** | סכום: **₪{st.session_state.price}**")
        st.text_input("מספר כרטיס אשראי", placeholder="0000 0000 0000 0000")
        if st.button("אשר תשלום והמשך ✅"):
            with st.spinner("מאמת..."): time.sleep(1.5)
            go('main')
    if st.button("⬅️ חזור"): go('options')

# --- דף 4: מסוף הביצוע ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        g_on = st.toggle("סנכרון יומן", True)
        w_on = st.toggle("שליחת הודעה", True)
    
    with st.form("magic_form"):
        biz = st.text_input("שם הלקוח / העסק")
        em = st.text_input("אימייל לסיכום")
        task = st.text_area("מה לבצע? (למשל: פגישה למחר ב-10:00)")
        if st.form_submit_button("הפעל סוכן מבצע ⚡"):
            if task and biz:
                # הסטטוס המעודכן - בלי האייקון הבעייתי
                with st.status("הפייה בתהליך...", expanded=True) as s:
                    st.write("✨ מנתחת נתונים...")
                    res_time = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Extract date from '{task}' as YYYYMMDDTHHMMSSZ. Only code."}]).choices[0].message.content.strip()
                    report = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Short summary in Hebrew for {biz}: {task}."}]).choices[0].message.content
                    
                    st.write("📧 שולחת דיווח...")
                    msg = EmailMessage()
                    msg['Subject'] = f"אישור: {biz}"; msg['From'] = MY_EMAIL; msg['To'] = em
                    msg.set_content(report, charset='utf-8')
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as sm:
                        sm.login(MY_EMAIL, APP_PASSWORD); sm.send_message(msg)
                    
                    if g_on:
                        u = f"https://www.google.com/calendar/render?action=TEMPLATE&text={urllib.parse.quote(biz)}&dates={res_time}/{res_time}"
                        st.markdown(f'<a href="{u}" target="_blank" class="magic-link-button">הוספה ליומן 📅</a>', unsafe_allow_html=True)
                    
                    if w_on:
                        wa_txt = urllib.parse.quote(f"היי {biz}, הפגישה תואמה! ✨")
                        st.markdown(f'<a href="https://wa.me/?text={wa_txt}" target="_blank" class="magic-link-button wa-button">אישור בוואטסאפ 📱</a>', unsafe_allow_html=True)
                    
                    s.update(label="הטמעה הושלמה!", state="complete")
                    st.success("הקסם בוצע!")
                    st.balloons()

    if st.button("⬅️ יציאה"): go('welcome')
