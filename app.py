import streamlit as st
from groq import Groq
import smtplib, time, urllib.parse
from email.message import EmailMessage

# --- SETUP ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing Key!")

def go(p):
    st.session_state.page = p
    st.rerun()

if 'page' not in st.session_state: st.session_state.page = 'welcome'

st.set_page_config(page_title="Magic AI", page_icon="🧚‍♀️")
st.markdown("<style>.stApp{direction:rtl; text-align:right;} button{width:100% !important;}</style>", unsafe_allow_html=True)

# --- PAGES ---
if st.session_state.page == 'welcome':
    st.header("MEIROM MAGIC AI 🧚‍♀️")
    st.image("fairy_logo.png", width=300)
    if st.button("בואי נתחיל ✨"): go('options')

elif st.session_state.page == 'options':
    st.header("בחרי חבילה")
    for p, pr in [("Basic", "250"), ("Pro", "750"), ("Enterprise", "2500")]:
        if st.button(f"{p} - {pr} ILS"):
            st.session_state.plan, st.session_state.price = p, pr
            go('payment')

elif st.session_state.page == 'payment':
    st.header("תשלום מאובטח 💳")
    st.write(f"חבילה: {st.session_state.plan}")
    st.text_input("מספר כרטיס")
    if st.button("שלמי עכשיו"):
        with st.spinner("מעבד..."): time.sleep(1)
        go('main')

elif st.session_state.page == 'main':
    st.header(f"מסוף: {st.session_state.plan}")
    with st.sidebar:
        st.image("fairy_logo.png", width=100)
        g_on = st.toggle("יומן גוגל", True)
        w_on = st.toggle("וואטסאפ", True)
    
    with st.form("m"):
        biz = st.text_input("שם העסק")
        em = st.text_input("אימייל")
        task = st.text_area("משימה")
        if st.form_submit_button("הפעל סוכן ⚡"):
            with st.status("הפייה עובדת...") as s:
                # Time
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Extract date from '{task}' as YYYYMMDDTHHMMSSZ. Only the code."}])
                tm = res.choices[0].message.content.strip()
                # Report
                rep = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Summary in Hebrew for {biz}: {task}."}]).choices[0].message.content
                
                if g_on:
                    url = f"https://www.google.com/calendar/render?action=TEMPLATE&text={urllib.parse.quote(biz)}&dates={tm}/{tm}"
                    st.markdown(f'<a href="{url}" target="_blank" style="display:block;padding:10px;background:#7c3aed;color:white;text-align:center;border-radius:10px;text-decoration:none;">הוספה ליומן 📅</a>', unsafe_allow_html=True)
                
                if w_on:
                    wa = f"https://wa.me/?text={urllib.parse.quote('הפגישה תואמה!')}"
                    st.markdown(f'<a href="{wa}" target="_blank" style="display:block;padding:10px;background:#25D366;color:white;text-align:center;border-radius:10px;text-decoration:none;margin-top:5px;">שלחי וואטסאפ 📱</a>', unsafe_allow_html=True)
                
                s.update(label="בוצע!", state="complete")
                st.info(rep)
                st.balloons()
