import streamlit as st
import requests
from groq import Groq

# --- הגדרות מערכת ---
st.set_page_config(page_title="MEIROM MAGIC", page_icon="🖤", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing Groq API Key")
    st.stop()

# --- עיצוב ZARA LUXE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: center; background-color: #fff; color: #000; }
    .brand-title { font-size: 40px; font-weight: 700; margin-top: 30px; text-transform: uppercase; }
    .stButton>button { background-color: #000; color: #fff; border-radius: 0px; height: 50px; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "auth"

if st.session_state.page == "auth":
    st.markdown("<div class='brand-title'>MEIROM MAGIC</div>", unsafe_allow_html=True)
    m = st.text_input("מייל כניסה", key="login_m").strip().lower()
    if st.button("כניסה למערכת"):
        st.session_state.user_email = m
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "dashboard":
    st.markdown(f"<div class='brand-title' style='font-size:25px;'>שלום {st.session_state.user_email}</div>", unsafe_allow_html=True)
    
    topic = st.text_area("על מה נעבוד היום? (ה-AI ייצר הכל)", placeholder="למשל: שמלת ערב יוקרתית לאירוע...")
    
    if st.button("ייצור קסם (טקסט + תמונה) בחינם ✨"):
        with st.spinner("מייצר פוסט ותמונה בחינם..."):
            # 1. ייצור טקסט ב-Groq
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"system","content":"אתה סוכן תוכן יוקרתי. כתוב פוסט לאינסטגרם בעברית בסטייל ZARA."},
                          {"role":"user","content":topic}]
            )
            st.session_state.last_text = res.choices[0].message.content
            
            # 2. ייצור תמונה בחינם (דרך Pollinations)
            # אנחנו שולחים את הנושא באנגלית למחולל התמונות
            prompt_for_img = topic.replace(" ", "%20")
            img_url = f"https://image.pollinations.ai/prompt/{prompt_for_img}?width=1024&height=1024&nologo=true"
            st.session_state.last_image_url = img_url
            st.session_state.magic_done = True

    if st.session_state.get('magic_done'):
        st.image(st.session_state.last_image_url, caption="התמונה שה-AI ייצר עבורך בחינם")
        st.info(st.session_state.last_text)
        
        # כפתור שליחה לוואטסאפ (חינמי לגמרי)
        text_encoded = requests.utils.quote(st.session_state.last_text)
        wa_url = f"https://wa.me/?text={text_encoded}"
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; height:45px; cursor:pointer;">שלח לוואטסאפ 📱</button></a>', unsafe_allow_html=True)

    if st.button("התנתקות"):
        st.session_state.page = "auth"
        st.rerun()
