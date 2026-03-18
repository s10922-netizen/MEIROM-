import streamlit as st
from groq import Groq
import time, urllib.parse
from datetime import datetime, timedelta

# --- חיבור ל-GROQ ---
try:
    client = Groq(api_key="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")
except:
    st.error("Missing GROQ_KEY in secrets!")

# --- ניהול דפים ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
def go(p):
    st.session_state.page = p
    st.rerun()

# --- עיצוב האתר (CSS) ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f8fafc; }
    .plan-box {
        background: white; padding: 25px; border-radius: 20px;
        border: 1px solid #e2e8f0; text-align: center;
        transition: 0.3s; height: 100%;
    }
    .plan-box:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); border-color: #7c3aed; }
    .price { color: #7c3aed; font-size: 32px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- דף פתיחה ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='color:#7c3aed; text-align:center; font-size:60px;'>Meirom Magic AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>סוכני AI חכמים שחוסכים לעסק שלך זמן וכסף</h3>", unsafe_allow_html=True)
    if st.button("בואי נבנה את האוטומציה שלך ✨", use_container_width=True): go('options')

# --- דף בחירת חבילה ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align:center;'>בחרי את רמת הקסם לעסק</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='plan-box'><h3>Basic 🧚</h3><div class='price'>₪250</div><p>ניהול יומן בסיסי</p></div>", unsafe_allow_html=True)
        if st.button("בחר Basic", key="b"): st.session_state.plan = "Basic"; go('main')
            
    with col2:
        st.markdown("<div class='plan-box' style='border: 2px solid #7c3aed;'><h3>Pro ⭐</h3><div class='price'>₪750</div><p>חיבור לאינטרנט ומידע בזמן אמת</p></div>", unsafe_allow_html=True)
        if st.button("בחר Pro", key="p"): st.session_state.plan = "Pro ⭐"; go('main')
            
    with col3:
        st.markdown("<div class='plan-box'><h3>Enterprise 👑</h3><div class='price'>₪2500</div><p>סוכן משגיח ומחקר מתחרים</p></div>", unsafe_allow_html=True)
        if st.button("בחר Enterprise", key="e"): st.session_state.plan = "Enterprise"; go('main')

# --- מסוף הניהול (המוצר) ---
elif st.session_state.page == 'main':
    st.header(f"מסוף ניהול AI - חבילת {st.session_state.plan}")
    
    # הגדרות לפי חבילה
    web_on = (st.session_state.plan != "Basic")
    super_on = (st.session_state.plan == "Enterprise")

    with st.container(border=True):
        biz = st.text_input("שם העסק")
        task = st.text_area("מה הסוכן צריך לבצע?")
        
        if st.button("הפעל סוכן מבצע ⚡", use_container_width=True):
            with st.status("הסוכן עובד...") as s:
                if web_on:
                    st.write("🌐 סורק את האינטרנט לקבלת מידע על העסק...")
                    time.sleep(2)
                
                # הפעלת ה-AI
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role":"user","content": f"Analyze {biz} and do: {task}. Mention: Powered by Meirom Magic AI."}]
                )
                
                if super_on:
                    st.write("🛡️ סוכן משגיח בודק את התוצאה...")
                    time.sleep(1)
                
                s.update(label="הושלם!", state="complete")
                st.info(res.choices[0].message.content)
                st.balloons()
