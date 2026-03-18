import streamlit as st
import requests
import urllib.parse
from groq import Groq

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב סוכנות LUXE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: center; background-color: #fff; color: #000; }
    .brand-title { font-size: 50px; font-weight: 700; margin-top: 50px; letter-spacing: 5px; background: linear-gradient(45deg, #000, #d4af37, #000); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }
    .brand-tagline { font-size: 14px; letter-spacing: 5px; color: #d4af37; margin-bottom: 50px; text-transform: uppercase; }
    .stButton>button { background-color: #000 !important; color: #fff !important; border-radius: 0px !important; height: 60px !important; width: 100% !important; border: none !important; font-size: 17px; margin-top: 20px; }
    .stButton>button:hover { background-color: #d4af37 !important; }
    input { background-color: transparent !important; border: none !important; border-bottom: 2px solid #eee !important; text-align: center !important; font-size: 20px !important; padding: 10px 0 !important; }
    /* עיצוב ה"תמונה" החדשה */
    .icon-box { 
        width: 150px; height: 150px; background: #fdfaf0; border: 2px solid #d4af37; 
        border-radius: 50%; margin: 20px auto; display: flex; align-items: center; 
        justify-content: center; font-size: 70px; box-shadow: 0 10px 20px rgba(212,175,55,0.1);
    }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- 3. דף כניסה והרשמה (כל הפיצ'רים שלך נשמרים) ---
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
    
    topic = st.text_area("על מה הסוכנות תעבוד היום?", placeholder="למשל: סוודר, בושם, נעליים...")
    
    if st.button("GENERATE MAGIC ✨"):
        if topic:
            with st.spinner("סוכנות AI מייצרת תוכן..."):
                # א. יצירת הטקסט ב-Groq
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":"אתה סוכן AI יוקרתי לעסקים. כתוב פוסט שיווקי קצר בעברית."},
                              {"role":"user","content":topic}]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # ב. בחירת אייקון מתאים (הפתרון החינמי והחסין)
                icon = "✨" # ברירת מחדל
                if "סוודר" in topic or "בגד" in topic: icon = "🧶"
                elif "בושם" in topic: icon = "🧴"
                elif "שעון" in topic: icon = "⌚"
                elif "נעל" in topic: icon = "👠"
                elif "תכשיט" in topic or "זהב" in topic: icon = "💎"
                
                st.session_state.last_icon = icon
                st.session_state.magic_done = True
        else:
            st.warning("אנא הכניסי נושא")

    if st.session_state.magic_done:
        # הצגת ה"תמונה" (האייקון המעוצב)
        st.markdown(f'<div class="icon-box">{st.session_state.last_icon}</div>', unsafe_allow_html=True)
        
        st.info(st.session_state.last_text)
        
        wa_txt = urllib.parse.quote(st.session_state.last_text)
        st.markdown(f'<a href="https://wa.me/?text={wa_txt}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:50px; cursor:pointer;">SEND TO WHATSAPP 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
