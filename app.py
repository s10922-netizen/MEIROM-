import streamlit as st
import requests
import urllib.parse
import time
import base64
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC AI", page_icon="💎", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing Groq API Key in Secrets")
    st.stop()

# --- 2. עיצוב סוכנות AI LUXE (זהב ושחור) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: center; background-color: #000; color: #fff; }
    .brand-title { font-size: 55px; font-weight: 700; margin-top: 50px; letter-spacing: 7px; color: #d4af37; text-transform: uppercase; }
    .brand-tagline { font-size: 14px; letter-spacing: 5px; color: #ffffff; margin-bottom: 50px; opacity: 0.8; }
    .stButton>button { background: linear-gradient(45deg, #d4af37, #fdfaf0) !important; color: #000 !important; border-radius: 0px !important; height: 65px !important; width: 100% !important; border: none !important; font-size: 18px; font-weight: bold; margin-top: 20px; cursor: pointer; }
    input, textarea { background-color: #111 !important; border: 1px solid #d4af37 !important; color: #fff !important; text-align: right !important; border-radius: 0px !important; }
    .status-box { border: 1px solid #d4af37; padding: 20px; margin-top: 20px; background: #0a0a0a; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- 3. דף כניסה ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>PREMIUM AI AUTO-AGENCY</div>", unsafe_allow_html=True)
    e = st.text_input("ENTER EMAIL", key="log_e")
    p = st.text_input("ENTER PASSWORD", key="log_p", type="password")
    if st.button("ACTIVATE AGENCY 🔑"):
        if e and p:
            st.session_state.user_email = e
            st.session_state.page = "dashboard"
            st.rerun()

# --- 4. דף עבודה (המוח של הסוכנות) ---
elif st.session_state.page == "dashboard":
    st.markdown("<div class='brand-title' style='font-size:30px;'>AGENCY TERMINAL</div>", unsafe_allow_html=True)
    
    topic = st.text_area("תארי את המשימה ל-AI (למשל: קולקציית שעוני זהב חדשה)", height=150)
    
    if st.button("EXECUTE FULL AUTO-POST 🚀"):
        if topic:
            with st.spinner("מייצר תוכן, מעבד תמונה ומכין שידור לרשתות..."):
                # א. יצירת הטקסט השיווקי
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":"אתה סוכן AI יוקרתי לעסקים. כתוב פוסט אינסטגרם מנצח בעברית."},
                              {"role":"user","content":topic}]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # ב. תרגום וייצור תמונה (הזרקת Base64 למניעת חסימות)
                # שימוש במודל יצירה מתקדם (Flux) דרך Pollinations
                img_url = f"https://pollinations.ai/p/high-end-product-photography,luxury,elegant,{urllib.parse.quote(topic)}?width=1024&height=1024&nologo=true&model=flux"
                
                try:
                    img_data = requests.get(img_url).content
                    b64_img = base64.b64encode(img_data).decode()
                    st.session_state.img_html = f'<img src="data:image/jpeg;base64,{b64_img}" style="width:100%; border: 2px solid #d4af37;">'
                    st.session_state.magic_done = True
                    
                    # ג. כאן בעתיד תבוא פונקציית ה-API לפרסום אוטומטי
                    # publish_to_instagram(st.session_state.last_text, img_url)
                    
                except:
                    st.error("Server Timeout. Try again in 5 seconds.")
        else:
            st.warning("אנא הכניסי תיאור משימה")

    if st.session_state.magic_done:
        st.markdown('<div class="status-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.img_html, unsafe_allow_html=True)
        st.write("### 📝 תוכן הפוסט:")
        st.write(st.session_state.last_text)
        st.success("✅ המערכת מוכנה לשידור. ברגע שנקבל אישורי API מ-Meta, הלחיצה תפרסם ישירות.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # גיבוי לוואטסאפ שתמיד עובד
        wa_txt = urllib.parse.quote(st.session_state.last_text)
        st.markdown(f'<a href="https://wa.me/?text={wa_txt}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:50px; cursor:pointer; margin-top:10px;">שלחי כגיבוי לוואטסאפ 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
