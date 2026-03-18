import streamlit as st
import pandas as pd
import requests
import time
from groq import Groq

# --- הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

# קישורים לטבלה ולטופס
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"

MY_ADMIN_EMAIL = "Meiromp10@gmail.com" 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key in Secrets")
    st.stop()

# --- עיצוב ZARA המקורי (השארתי בדיוק את מה שהיה לך) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl; text-align: center;
        background-color: #ffffff; color: #000;
    }
    .brand-title { font-size: 45px; font-weight: 700; margin-top: 50px; color: #000; text-transform: uppercase; }
    .brand-tagline { font-size: 13px; letter-spacing: 3px; color: #888; margin-bottom: 50px; }
    .stButton>button {
        background-color: #000; color: #fff; border-radius: 0px; 
        height: 55px; font-size: 16px; width: 100%; border: none; margin-top: 20px;
    }
    input {
        background-color: transparent !important; border: none !important;
        border-bottom: 1px solid #ddd !important; text-align: center !important;
        font-size: 18px !important; padding: 10px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- לוגיקה ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'tool' not in st.session_state: st.session_state.tool = "home"

if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>Creative AI Systems</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["כניסה", "הרשמה"])
    with t1:
        m = st.text_input("מייל", key="log_m").strip().lower()
        if st.button("כניסה למערכת"):
            st.session_state.user_email = m
            st.session_state.page = "dashboard"
            st.rerun()
    with t2:
        rm = st.text_input("אימייל חדש", key="reg_m")
        rb = st.text_input("שם העסק", key="reg_b")
        if st.button("פתיחת חשבון"):
            requests.post(FORM_URL, data={"entry.855862094": rm, "entry.1847739029": f"Biz: {rb}"})
            st.session_state.user_email = rm
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='brand-title' style='font-size:30px;'>MEIROM MAGIC</div>", unsafe_allow_html=True)
    
    if st.session_state.tool == "home":
        if st.button("סוכן תוכן AI ✨"): st.session_state.tool = "ai"; st.rerun()
        if st.button("צ'אט שירות"): st.session_state.tool = "chat"; st.rerun()
        if st.button("התנתקות"): st.session_state.page = "auth"; st.rerun()
    
    elif st.session_state.tool == "ai":
        topic = st.text_area("על מה נעבוד היום?")
        
        if st.button("ייצור קסם (טקסט + תמונה) 🪄"):
            with st.spinner("מייצר..."):
                # 1. טקסט
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":"אתה סוכן תוכן יוקרתי."}, {"role":"user","content":topic}]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # 2. תמונה חינמית
                clean_topic = topic.replace(" ", "%20")
                st.session_state.last_image_url = f"https://image.pollinations.ai/prompt/{clean_topic}?width=1024&height=1024&nologo=true"
                st.session_state.magic_done = True
        
        if st.session_state.get('magic_done'):
            st.image(st.session_state.last_image_url)
            st.info(st.session_state.last_text)

        if st.button("חזרה לתפריט 🏠"):
            st.session_state.tool = "home"
            st.rerun()
