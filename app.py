import streamlit as st
import requests
from groq import Groq

# --- הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

# חיבור ל-Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing Groq API Key")
    st.stop()

# --- העיצוב המקורי והמדויק של MEIROM MAGIC ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: center;
        background-color: #ffffff;
        color: #000000;
    }
    
    .brand-title {
        font-size: 45px;
        font-weight: 700;
        margin-top: 50px;
        color: #000;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .brand-tagline {
        font-size: 13px;
        letter-spacing: 4px;
        color: #888;
        margin-bottom: 50px;
        text-transform: uppercase;
    }

    .stButton>button {
        background-color: #000 !important;
        color: #fff !important;
        border-radius: 0px !important;
        height: 55px !important;
        width: 100% !important;
        border: none !important;
        font-size: 16px !important;
        font-weight: 300 !important;
        letter-spacing: 1px !important;
        margin-top: 20px !important;
    }
    
    /* עיצוב שדות קלט */
    input, textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #eee !important;
        text-align: center !important;
        font-size: 18px !important;
        border-radius: 0px !important;
        color: #000 !important;
    }
    
    input:focus, textarea:focus {
        border-bottom: 1px solid #000 !important;
        box-shadow: none !important;
    }

    .stInfo {
        background-color: #f9f9f9 !important;
        border: none !important;
        color: #000 !important;
        border-radius: 0px !important;
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

# ניהול מצבי דפים
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- דף כניסה (העיצוב המקורי) ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>Creative AI Systems</div>", unsafe_allow_html=True)
    m = st.text_input("ENTER EMAIL", key="login_m").strip().lower()
    if st.button("LOG IN"):
        st.session_state.user_email = m
        st.session_state.page = "dashboard"
        st.rerun()

# --- דף עבודה (העיצוב המקורי) ---
elif st.session_state.page == "dashboard":
    st.markdown("<div class='brand-title' style='font-size:28px;'>DASHBOARD</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='letter-spacing:2px; color:#888; margin-bottom:30px;'>WELCOME, {st.session_state.user_email.upper()}</div>", unsafe_allow_html=True)
    
    topic = st.text_area("מה הנושא של הפוסט היום?", placeholder="כתבי כאן...")
    
    if st.button("GENERATE MAGIC ✨"):
        if topic:
            with st.spinner("CREATING..."):
                # 1. טקסט
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role":"system","content":"אתה סוכן תוכן יוקרתי. כתוב פוסט לאינסטגרם בעברית בסטייל ZARA. קצר וקולע."},
                        {"role":"user","content":topic}
                    ]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # 2. תמונה (Pollinations)
                clean_topic = topic.replace(" ", "%20")
                st.session_state.last_image_url = f"https://image.pollinations.ai/prompt/{clean_topic}?width=1024&height=1024&nologo=true"
                st.session_state.magic_done = True
        else:
            st.warning("PLEASE ENTER A TOPIC")

    if st.session_state.magic_done:
        st.image(st.session_state.last_image_url)
        st.info(st.session_state.last_text)
        
        # כפתור וואטסאפ (מעוצב כחלק מהמערכת)
        text_encoded = requests.utils.quote(st.session_state.last_text)
        wa_url = f"https://wa.me/?text={text_encoded}"
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:50px; cursor:pointer; margin-top:10px;">SEND TO WHATSAPP 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
