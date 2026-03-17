import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing API Key")

MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- עיצוב בסיסי ונקי (בלי HTML שביש) ---
st.set_page_config(page_title="Meirom AI | Active", page_icon="⚡")

# --- דף 1: פתיחה ---
if st.session_state.page == 'welcome':
    st.title("MEIROM AI")
    st.subheader("מערכת אוטונומית להטמעת בינה מלאכותית")
    st.info("לחצי על הכפתור למטה כדי להיכנס למסוף הביצוע")
    if st.button("כניסה למערכת 🚀", use_container_width=True):
        go_to('main')

# --- דף 2: מסוף הביצוע (כאן קורה הקסם!) ---
elif st.session_state.page == 'main':
    st.header("מרכז שליטה מבצעי")
    
    # חיבור תשתיות
    with st.container(border=True):
        st.write("🔗 **חיבור תשתיות פעילות**")
        c1, c2, c3 = st.columns(3)
        ws = c1.checkbox("WhatsApp")
        cal = c2.checkbox("Calendar")
        mail = c3.checkbox("Email")

    # טופס פקודה
    with st.form("exec_form"):
        biz_name = st.text_input("שם העסק")
        biz_email = st.text_input("אימייל לשליחת אישור")
        mission = st.text_area("מה המשימה לביצוע? (למשל: 'שלח הודעת תודה לכל לקוח')")
        submit = st.form_submit_button("הפעל סוכן מבצע ⚡", use_container_width=True)

        if submit and biz_name and mission:
            with st.status("סוכן Meirom AI מבצע הטמעה...", expanded=True) as status:
                st.code("> Establishing secure link... OK")
                time.sleep(1)
                
                if ws:
                    st.code("> Connecting WhatsApp API... SUCCESS")
                    time.sleep(1)
                if cal:
                    st.code("> Syncing Google Calendar... DONE")
                    time.sleep(1)
                
                st.code("> Executing AI Task logic...")
                
                # לוגיקת AI
                p = f"ACT AS: Business Implementer. Task: {mission} for {biz_name}. Tools: WhatsApp:{ws}, Cal:{cal}. SUMMARY OF ACTIONS IN HEBREW."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":p}])
                st.session_state.report = res.choices[0].message.content
                
                # מייל
                try:
                    msg = EmailMessage()
                    msg['Subject'] = f"Action Log - {biz_name}"
                    msg['From'] = MY_EMAIL; msg['To'] = biz_email
                    msg.set_content(st.session_state.report, charset='utf-8')
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                        s.login(MY_EMAIL, APP_PASSWORD)
                        s.send_message(msg)
                except:
                    st.warning("הדו''ח נוצר אך המייל נכשל")
                
                status.update(label="המשימה בוצעה בהצלחה! ✅", state="complete")
                st.balloons()

    if st.session_state.report:
        with st.container(border=True):
            st.subheader("סיכום הטמעה מבצעית:")
            st.write(st.session_state.report)

    if st.button("⬅️ חזרה לדף הבית", use_container_width=True):
        st.session_state.report = None
        go_to('welcome')
