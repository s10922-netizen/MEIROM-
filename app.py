import streamlit as st
import requests
import urllib.parse
import time
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב סוכנות AI יוקרתית ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: center; background-color: #fff; color: #000; }
    .brand-title { font-size: 50px; font-weight: 700; margin-top: 50px; letter-spacing: 5px; background: linear-gradient(45deg, #000, #d4af37, #000); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .brand-tagline { font-size: 14px; letter-spacing: 5px; color: #d4af37; margin-bottom: 50px; text-transform: uppercase; }
    .stButton>button { background-color: #000 !important; color: #fff !important; border-radius: 0px !important; height: 60px !important; width: 100% !important; border: none !important; font-size: 17px; margin-top: 20px; transition: 0.3s; }
    .stButton>button:hover { background-color: #d4af37 !important; }
    input { background-color: transparent !important; border: none !important; border-bottom: 2px solid #eee !important; text-align: center !important; font-size: 20px !important; padding: 10px 0 !important; }
    textarea { text-align: right !important; border: 1px solid #eee !important; border-radius: 0px !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- 3. דף כניסה והרשמה ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>AI BUSINESS AGENCY</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["כניסה", "הרשמה"])
    with t1:
        e = st.text_input("EMAIL", key="log_e").strip().lower()
        p = st.text_input("PASSWORD", key="log_p", type="password")
        if st.button("LOG IN"):
            if e and p:
                st.session_state.user_email = e
                st.session_state.page = "dashboard"
                st.rerun()
    with t2:
        re = st.text_input("NEW EMAIL", key="reg_e").strip().lower()
        rb = st.text_input("BIZ NAME", key="reg_b")
        if st.button("CREATE ACCOUNT"):
            if re:
                requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse", 
                              data={"entry.855862094": re, "entry.1847739029": rb})
                st.success("SUCCESS! GO TO LOGIN.")

# --- 4. דף עבודה ---
elif st.session_state.page == "dashboard":
    st.markdown("<div class='brand-title' style='font-size:30px;'>DASHBOARD</div>", unsafe_allow_html=True)
    st.write(f"WELCOME, {st.session_state.user_email.upper()}")
    
    topic = st.text_area("על מה הסוכנות תעבוד היום?", placeholder="תארי את המוצר (למשל: בושם יוקרתי, שעון זהב)...")
    
    if st.button("GENERATE MAGIC ✨"):
        if topic:
            with st.spinner("סוכנות AI מייצרת תוכן ותמונה..."):
                # א. יצירת הטקסט
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":"אתה סוכן AI יוקרתי לעסקים. כתוב פוסט שיווקי קצר בעברית."},
                              {"role":"user","content":topic}]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # ב. תרגום שקט לאנגלית כדי שה-AI יצייר מדויק
                trans = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role":"system","content":"Translate the topic to English keywords for AI image generation. Only keywords."},
                              {"role":"user","content":topic}]
                )
                en_kw = trans.choices[0].message.content.strip().replace(" ", ",")
                
                # ג. יצירת התמונה (השיטה המנצחת)
                seed = int(time.time())
                # הוספנו מילות מפתח שמבטיחות מראה של צילום מוצר מקצועי
                prompt = f"professional-product-photography,luxury,highly-detailed,{en_kw}"
                st.session_state.last_image_url = f"https://pollinations.ai/p/{urllib.parse.quote(prompt)}?width=1024&height=1024&seed={seed}&model=flux"
                
                st.session_state.magic_done = True
        else:
            st.warning("PLEASE ENTER A TOPIC")

    if st.session_state.magic_done:
        # הצגת התמונה - השתמשתי בפורמט HTML כדי לעקוף חסימות
        st.markdown(f'''
            <div style="border: 2px solid #eee; padding: 5px; background: #fff;">
                <img src="{st.session_state.last_image_url}" style="width:100%; display:block;">
            </div>
        ''', unsafe_allow_html=True)
        
        st.info(st.session_state.last_text)
        
        wa_txt = urllib.parse.quote(st.session_state.last_text)
        st.markdown(f'<a href="https://wa.me/?text={wa_txt}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:50px; cursor:pointer; margin-top:10px;">SEND TO WHATSAPP 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
