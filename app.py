import streamlit as st
import requests
import urllib.parse
import time
from groq import Groq

# --- הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing Groq API Key")
    st.stop()

# --- עיצוב ZARA LUXE (מוגן ושמור) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: center; background-color: #ffffff; color: #000; }
    .brand-title { font-size: 55px; font-weight: 700; margin-top: 40px; letter-spacing: 5px; background: linear-gradient(45deg, #000, #b59410, #000); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .brand-tagline { font-size: 14px; letter-spacing: 6px; color: #b59410; margin-bottom: 50px; text-transform: uppercase; font-weight: 200; }
    .stButton>button { background-color: #000 !important; color: #fff !important; border-radius: 0px !important; height: 60px !important; width: 100% !important; border: none !important; font-size: 17px !important; letter-spacing: 2px !important; margin-top: 25px !important; transition: 0.3s; }
    .stButton>button:hover { background-color: #b59410 !important; }
    input { background-color: transparent !important; border: none !important; border-bottom: 2px solid #eee !important; text-align: center !important; font-size: 20px !important; border-radius: 0px !important; padding: 15px 0 !important; color: #000 !important; }
    input:focus { border-bottom: 2px solid #b59410 !important; box-shadow: none !important; }
    textarea { border: 1px solid #eee !important; text-align: right !important; border-radius: 0px !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- דף כניסה והרשמה (שמירה על הפיצ'רים) ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>Creative AI Solutions</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["כניסה", "הרשמה"])
    
    with t1:
        login_email = st.text_input("EMAIL", key="log_m").strip().lower()
        login_pass = st.text_input("PASSWORD", key="log_p", type="password")
        if st.button("LOG IN"):
            if login_email and login_pass:
                st.session_state.user_email = login_email
                st.session_state.page = "dashboard"
                st.rerun()
    
    with t2:
        reg_email = st.text_input("NEW EMAIL", key="reg_m").strip().lower()
        reg_biz = st.text_input("BUSINESS NAME", key="reg_b")
        reg_pass = st.text_input("PASSWORD", key="reg_p", type="password")
        if st.button("CREATE ACCOUNT"):
            if reg_email and reg_pass:
                requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse", 
                              data={"entry.855862094": reg_email, "entry.1847739029": reg_biz})
                st.success("SUCCESS! GO TO LOG IN.")

# --- דף עבודה (Dashboard) ---
elif st.session_state.page == "dashboard":
    st.markdown("<div class='brand-title' style='font-size:35px;'>DASHBOARD</div>", unsafe_allow_html=True)
    st.write(f"WELCOME, {st.session_state.user_email.upper()}")
    
    topic = st.text_area("מה ה-AI ייצר עבור העסק היום?")
    
    if st.button("GENERATE MAGIC ✨"):
        if topic:
            with st.spinner("CREATING..."):
                # 1. טקסט
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":"אתה סוכן תוכן יוקרתי בסטייל ZARA. ענה בעברית."}, {"role":"user","content":topic}]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # 2. תמונה (תיקון הכתובת ושימוש ב-seed רענן)
                safe_topic = urllib.parse.quote(topic)
                st.session_state.last_image_url = f"https://image.pollinations.ai/prompt/luxury,fashion,minimalist,high-quality,{safe_topic}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
                st.session_state.magic_done = True
        else:
            st.warning("אנא כתבי נושא")

    if st.session_state.magic_done:
        # הצגת תמונה בשיטה יציבה
        st.image(st.session_state.last_image_url, use_container_width=True)
        st.info(st.session_state.last_text)
        
        # כפתור וואטסאפ (נשמר!)
        wa_url = f"https://wa.me/?text={urllib.parse.quote(st.session_state.last_text)}"
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366 !important; border-color:#25D366 !important;">SEND TO WHATSAPP 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
