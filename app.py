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

# --- עיצוב יוקרתי ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #fdfbff; }
    .stButton>button { 
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
        color: white; border-radius: 20px; border: none; padding: 15px;
        font-weight: bold; font-size: 18px; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(124,58,237,0.3); }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-radius: 15px; border: 1px solid #e2e8f0; }
    .main-title { color: #7c3aed; font-size: 45px; font-weight: 800; margin-bottom: 0px; }
</style>
""", unsafe_allow_html=True)

# --- דפים ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 class='main-title'>MEIROM MAGIC AI 🧚‍♀️</h1>", unsafe_allow_html=True)
    st.image("fairy_logo.png", width=350)
    st.write("### הופכים את העסק שלך לקסם אוטומטי")
    if st.button("בואי נתחיל את הקסם ✨"): go('options')

elif st.session_state.page == 'options':
    st.header("בחרי את עוצמת הקסם")
    c1, c2, c3 = st.columns(3)
    for i, (p, pr) in enumerate([("Basic", "250"), ("Pro ⭐", "750"), ("Enterprise", "2500")]):
        with [c1, c2, c3][i]:
            st.markdown(f"<div style='background:white; padding:20px; border-radius:20px; border:1px solid #eee; text-align:center;'><h3>{p}</h3><h2>₪{pr}</h2></div>", unsafe_allow_html=True)
            if st.button(f"בחר {p}", key=f"p{i}"):
                st.session_state.plan, st.session_state.price = p, pr
                go('payment')

elif st.session_state.page == 'payment':
    st.header("💳 תשלום מאובטח")
    with st.container(border=True):
        st.write(f"מסלול נבחר: **{st.session_state.plan}** | סכום: **₪{st.session_state.price}**")
        st.text_input("מספר כרטיס אשראי")
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
                    # בינה מלאכותית - זמן וסיכום
                    res_time = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Extract date from '{task}' as YYYYMMDDTHHMMSSZ. Return only code."}]).choices[0].message.content.strip()
                    report = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Short summary in Hebrew for {biz}: {task}."}]).choices[0].message.content
                    
                    # שליחת מייל אוטומטי
                    msg = EmailMessage()
                    msg['Subject'] = f"אישור הטמעה: {biz}"; msg['From'] = MY_EMAIL; msg['To'] = em
                    msg.set_content(report, charset='utf-8')
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as sm:
                        sm.login(MY_EMAIL, APP_PASSWORD); sm.send_message(msg)
                    
                    st.success("הקסם בוצע! הדו''ח נשלח למייל.")
                    
                    # הצגת כפתורי פעולה יפים
                    if g_on:
                        u = f"https://www.google.com/calendar/render?action=TEMPLATE&text={urllib.parse.quote(biz)}&dates={res_time}/{res_time}"
                        st.markdown(f'<a href="{u}" target="_blank" style="display:block;padding:12px;background:#7c3aed;color:white;text-align:center;border-radius:15px;text-decoration:none;font-weight:bold;">לחצי כאן להוספה ליומן בטלפון 📅</a>', unsafe_allow_html=True)
                    
                    if w_on:
                        wa_txt = urllib.parse.quote(f"היי {biz}, הפגישה תואמה בהצלחה! ✨")
                        st.markdown(f'<a href="https://wa.me/?text={wa_txt}" target="_blank" style="display:block;padding:12px;background:#25D366;color:white;text-align:center;border-radius:15px;text-decoration:none;font-weight:bold;margin-top:10px;">שלחי אישור בוואטסאפ ללקוח 📱</a>', unsafe_allow_html=True)
                    
                    s.update(label="בוצע בהצלחה!", state="complete")
                    st.balloons()
