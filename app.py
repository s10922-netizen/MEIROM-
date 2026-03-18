import streamlit as st
import requests
import urllib.parse
from groq import Groq

# --- הגדרות מערכת בסיסיות ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

# חיבור ל-Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing Groq API Key")
    st.stop()

# --- עיצוב ZARA LUXE - שחור, לבן וזהב ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: center;
        background-color: #ffffff;
        color: #000000;
    }
    
    /* כותרות יוקרה */
    .brand-title {
        font-size: 50px;
        font-weight: 700;
        margin-top: 60px;
        color: #000;
        text-transform: uppercase;
        letter-spacing: 4px;
        background: linear-gradient(to right, #000, #b59410, #000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .brand-tagline {
        font-size: 14px;
        letter-spacing: 5px;
        color: #b59410; /* זהב יוקרתי */
        margin-bottom: 60px;
        text-transform: uppercase;
        font-weight: 200;
    }

    /* עיצוב כפתורים בסגנון זארה עם אנימציה */
    .stButton>button {
        background-color: #000 !important;
        color: #fff !important;
        border-radius: 0px !important;
        height: 60px !important;
        width: 100% !important;
        border: none !important;
        font-size: 17px !important;
        font-weight: 300 !important;
        letter-spacing: 2px !important;
        margin-top: 25px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background-color: #b59410 !important; /* זהב בריחופ */
        color: #fff !important;
        transform: translateY(-2px);
    }
    
    /* עיצוב שדות קלט (סיסמה, מייל) */
    input {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #eee !important;
        text-align: center !important;
        font-size: 20px !important;
        border-radius: 0px !important;
        color: #000 !important;
        padding: 15px 0 !important;
        transition: border-bottom 0.3s ease !important;
    }
    
    input:focus {
        border-bottom: 2px solid #b59410 !important; /* זהב בפוקוס */
        box-shadow: none !important;
    }

    /* עיצוב טאבים להתחברות/הרשמה */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-radius: 0px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888;
        font-weight: 400;
        letter-spacing: 1px;
    }
    .stTabs [aria-selected="true"] {
        color: #b59410; /* זהב בטאב נבחר */
        font-weight: 600;
        border-bottom-color: #b59410;
    }

    /* עיצוב תיבת טקסט לאיי */
    textarea {
        border: 1px solid #eee !important;
        text-align: right !important;
        border-radius: 0px !important;
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

# ניהול מצבי דפים ואתחול משתנים
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'magic_done' not in st.session_state: st.session_state.magic_done = False

# --- דף כניסה והרשמה (מלא ומעוצב) ---
if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div><div class='brand-tagline'>The Art of Creative AI</div>", unsafe_allow_html=True)
    
    # טאבים נקיים להתחברות והרשמה
    t1, t2 = st.tabs(["כניסה", "הרשמה"])
    
    with t1:
        # התחברות
        st.markdown("<br>", unsafe_allow_html=True)
        login_email = st.text_input("EMAIL", key="log_m").strip().lower()
        login_pass = st.text_input("PASSWORD", key="log_p", type="password") # שדה סיסמה секрет
        
        if st.button("SIGN IN"):
            # בדיקת התחברות פשוטה (אפשר לשדרג בהמשך עם בדיקה מול הטבלה)
            if login_email and login_pass:
                with st.spinner("AUTHENTICATING..."):
                    time.sleep(1) # הדמיית בדיקה
                    st.session_state.user_email = login_email
                    st.session_state.page = "dashboard"
                    st.rerun()
            else:
                st.warning("PLEASE ENTER EMAIL & PASSWORD")
                
    with t2:
        # הרשמה
        st.markdown("<br>", unsafe_allow_html=True)
        reg_email = st.text_input("NEW EMAIL", key="reg_m").strip().lower()
        reg_biz = st.text_input("BUSINESS NAME", key="reg_b")
        reg_pass = st.text_input("SET PASSWORD", key="reg_p", type="password") # שדה סיסמה סוד
        
        if st.button("CREATE ACCOUNT"):
            if reg_email and reg_pass:
                with st.spinner("REGISTERING..."):
                    # שליחת נתונים לטבלה (כמו קודם)
                    requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse", 
                                  data={"entry.855862094": reg_email, "entry.1847739029": f"Biz: {reg_biz}"})
                    st.success("ACCOUNT CREATED! PLEASE SIGN IN.")
            else:
                st.warning("PLEASE FILL IN ALL FIELDS")

# --- דף עבודה (Dashboard) ---
elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='brand-title' style='font-size:32px;'>DASHBOARD</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='letter-spacing:2px; color:#b59410; font-weight:200; margin-bottom:40px;'>WELCOME, {st.session_state.user_email.upper()}</div>", unsafe_allow_html=True)
    
    topic = st.text_area("על מה ה-AI יעבוד היום?", placeholder="למשל: סדרת פוסטים לאינסטגרם על קולקציית חורף...")
    
    if st.button("GENERATE MAGIC 🪄"):
        if topic:
            with st.spinner("CREATING YOUR CONTENT..."):
                # 1. טקסט
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role":"system","content":"אתה סוכן תוכן יוקרתי. כתוב פוסט לאינסטגרם בעברית בסטייל ZARA. קצר וקולע."},
                        {"role":"user","content":topic}
                    ]
                )
                st.session_state.last_text = res.choices[0].message.content
                
                # 2. תמונה (קישור מורחב ומדויק לשיפור הטעינה)
                prompt_for_img = urllib.parse.quote(topic)
                # הוספתי מילות מפתח קבועות (Luxury, High-End, Editorial, Minimalist)
                st.session_state.last_image_url = f"https://image.pollinations.ai/prompt/luxury,high-end,editorial,minimalist,high-fashion,photo,{prompt_for_img}?width=1024&height=1024&nologo=true&seed=42"
                st.session_state.magic_done = True
        else:
            st.warning("PLEASE ENTER A TOPIC")

    if st.session_state.magic_done:
        # הצגת התמונה בגדול ובאיכות
        st.image(st.session_state.last_image_url, use_container_width=True, caption="התמונה שה-AI ייצר עבור העסק")
        st.info(st.session_state.last_text)
        
        # כפתור וואטסאפ (מעוצב ירוק-ZARA)
        text_encoded = urllib.parse.quote(st.session_state.last_text)
        wa_url = f"https://wa.me/?text={text_encoded}"
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:50px; cursor:pointer; margin-top:10px;">SEND TO WHATSAPP 📱</button></a>', unsafe_allow_html=True)

    if st.button("LOG OUT"):
        st.session_state.page = "auth"
        st.session_state.magic_done = False
        st.rerun()
