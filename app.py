import streamlit as st
import requests
import urllib.parse
import time
from groq import Groq

# --- 1. הגדרות בסיסיות ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב LUXE (זהב ושחור) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: center; background-color: #fff; color: #000; }
    .brand-title { font-size: 50px; font-weight: 700; margin-top: 50px; letter-spacing: 5px; background: linear-gradient(45deg, #000, #d4af37, #000); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .brand-tagline { font-size: 14px; letter-spacing: 5px; color: #d4af37; margin-bottom: 50px; text-transform: uppercase; }
    .stButton>button { background-color: #000 !important; color: #fff !important; border-radius: 0px !important; height: 60px !important; width: 100% !important; border: none !important; font-size: 17px; margin-top: 20px; transition: 0.3s; }
    .stButton>button:hover { background-color: #d4af37 !important; }
    input { background-color: transparent !important; border: none !important; border-bottom: 2px solid #eee !important; text-align: center !important; font-size: 20px !important; padding: 10px 0 !important; }
</style>
""", unsafe_allow_html=True)

# אתחול משתנים
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- 3. דף כניסה והרשמה ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>AI BUSINESS AGENCY</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["כניסה", "הרשמה"])
    
    with tab1:
        email = st.text_input("EMAIL", key="log_e").strip().lower()
        pwd = st.text_input("PASSWORD", key="log_p", type="password")
        if st.button("LOG IN"):
            if email and pwd:
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
                
    with tab2:
        re = st.text_input("NEW EMAIL", key="reg_e").strip().lower()
        rb = st.text_input("BIZ NAME", key="reg_b")
        if st.button("CREATE ACCOUNT"):
            if re:
                requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse", 
                              data={"entry.855862094": re, "entry.1847739029": rb})
                st.success("SUCCESS! GO TO LOGIN.")

# --- 4. דף העבודה (Dashboard) ---
elif st.session_state.page == "dashboard":
    st.markdown("<div class='brand-title' style='font-size:30px;'>DASHBOARD</div>", unsafe_allow_html=True)
    st.write(f"WELCOME, {st.session_state.user_email.upper()}")
    
    topic = st.text_area("מה המשימה של הסוכנות היום?", placeholder="למשל: סוודר שחור יוקרתי...")
    
    if st.button("GENERATE MAGIC ✨"):
        if topic:
            with st.spinner("סוכנות AI מייצרת תוכן..."):
                # א. יצירת הטקסט
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":"אתה סוכן AI לעסקים. כתוב פוסט יוקרתי קצר בעברית."},
                              {"role":"user","content":topic}]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # ב. יצירת התמונה (השיטה הכי בטוחה - חיפוש ישיר)
                clean_topic = urllib.parse.quote(topic)
                # אנחנו משתמשים ב-Pollinations עם מילות מפתח קבועות ליוקרה
                st.session_state.last_image_url = f"https://image.pollinations.ai/prompt/luxury,professional,fashion,{clean_topic}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
                st.session_state.magic_done = True
        else:
            st.warning("אנא הכניסי נושא")

    if st.session_state.magic_done:
        # הצגת התמונה
        st.image(st.session_state.last_image_url, use_container_width=True)
        # הצגת הטקסט
        st.info(st.session_state.last_text)
        # וואטסאפ
        wa_txt = urllib.parse.quote(st.session_state.last_text)
        st.markdown(f'<a href="https://wa.me/?text={wa_txt}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:50px; cursor:pointer;">SEND TO WHATSAPP 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
