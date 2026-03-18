import streamlit as st
from groq import Groq
import urllib.parse
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets!")
    st.stop()

# --- בדיקה: האם זה לקוח חיצוני? ---
# אם הכתובת מכילה ?view=customer, נציג דף נקי לגמרי
query_params = st.query_params
is_customer_view = query_params.get("view") == "customer"

# --- זיכרון המערכת ---
if 'biz_info' not in st.session_state:
    st.session_state.biz_info = "ברוכים הבאים לעסק שלנו! אנחנו כאן לכל שאלה."
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}

# --- 🌐 דף לקוח חיצוני (נפרד לגמרי) ---
if is_customer_view:
    st.markdown(f"<h1 style='text-align:center; color:#7c3aed;'>✨ ברוכים הבאים ✨</h1>", unsafe_allow_html=True)
    st.write(st.session_state.biz_info)
    st.divider()
    
    st.subheader("צ'אט עם הנציג הדיגיטלי שלנו 🤖")
    u_msg = st.chat_input("איך אפשר לעזור?")
    if u_msg:
        st.chat_message("user").write(u_msg)
        r = client.chat.completions.create(model="llama-3.3-70b-versatile", 
                                          messages=[{"role":"user","content":f"Biz info: {st.session_state.biz_info}. User: {u_msg}. Hebrew."}])
        st.chat_message("assistant").write(r.choices[0].message.content)
    st.stop() # עוצר כאן כדי שלא יראו את שאר האתר

# --- 👑 מכאן והלאה: דף המנכ"לית והניהול (דורש התחברות) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'plan' not in st.session_state: st.session_state.plan = None

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>Meirom Magic AI - כניסת מנהלים</h1>", unsafe_allow_html=True)
    l_email = st.text_input("אימייל", key="l_user")
    l_pass = st.text_input("סיסמה", type="password", key="l_pass")
    if st.button("התחברות 🚀"):
        if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
            st.session_state.logged_in = True
            st.rerun()

elif st.session_state.plan is None:
    st.header("בחרי מסלול")
    if st.button("Enterprise (2500₪)"): st.session_state.plan = "Enterprise"; st.rerun()

else:
    with st.sidebar:
        st.write(f"חבילה: {st.session_state.plan}")
        page = st.radio("ניווט:", ["✨ דף הבית", "🏢 הגדרות עסק", "🔗 קישור ללקוחות"])

    if page == "✨ דף הבית":
        st.title("מרכז שליחה")
    
    elif page == "🏢 הגדרות עסק":
        st.header("הגדרות עסק")
        st.session_state.biz_info = st.text_area("מה לספר ללקוחות?", value=st.session_state.biz_info)
        st.button("שמור ✅")

    elif page == "🔗 קישור ללקוחות":
        st.header("הקישור שלך להפצה 🌐")
        st.write("שלחי את הקישור הזה ללקוחות שלך. הם יראו דף נקי בלי צורך בסיסמה!")
        # יצירת הלינק האוטומטי
        base_url = "https://your-app-name.streamlit.app/" # תחליפי בכתובת האמיתית שלך
        customer_link = f"{base_url}?view=customer"
        st.code(customer_link)
        st.info("הלקוחות שייכנסו ללינק הזה יראו רק את הצ'אטבוט!")
