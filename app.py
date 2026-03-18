import streamlit as st
from groq import Groq
import requests

# --- 1. הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- 2. חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("חסר מפתח API ב-Secrets! (GROQ_API_KEY)")
    st.stop()

# --- 3. עיצוב CSS המנצנץ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    /* כותרת מנצנצת */
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center; padding: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* עיצוב כפתורים */
    .stButton>button {
        background: linear-gradient(45deg, #7c3aed, #ec4899);
        color: white; border: none; border-radius: 20px; padding: 10px 25px; 
        transition: 0.3s; width: 100%;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.3); }
</style>
""", unsafe_allow_html=True)

# --- 4. לוגיקה וזיכרון ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'biz_info' not in st.session_state: st.session_state.biz_info = "ברוכים הבאים לעסק שלנו!"

# בדיקת דף לקוח חיצוני (?view=customer)
if st.query_params.get("view") == "customer":
    st.markdown("<div class='magic-title'>ברוכים הבאים</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{st.session_state.biz_info}</h3>", unsafe_allow_html=True)
    customer_msg = st.chat_input("איך אפשר לעזור?")
    if customer_msg:
        st.chat_message("user").write(customer_msg)
        prompt = f"אתה עוזר חכם עבור העסק: {st.session_state.biz_info}. ענה על: {customer_msg} בעברית."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
        st.chat_message("assistant").write(res.choices[0].message.content)
    st.stop()

# --- 5. דף כניסה והרשמה ---
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה למערכת"])
    
    with tab1:
        st.subheader("כניסת מנהלת")
        e = st.text_input("אימייל", key="l_e")
        p = st.text_input("סיסמה", type="password", key="l_p")
        if st.button("כניסה לאימפריה 🚀"):
            if e == "admin@magic.com" and p == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("פרטים שגויים, מנכ\"לית.")
                
    with tab2:
        st.subheader("הצטרפי למהפכה ✨")
        st.write("מלאי פרטים והמידע יופיע בטבלה של מיי אוטומטית.")
        new_mail = st.text_input("מייל להרשמה", key="r_e")
        new_pass = st.text_input("בחרי סיסמה", type="password", key
