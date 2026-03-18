import streamlit as st
import pandas as pd
import requests
from groq import Groq

# --- 1. הגדרות וחיבורים ---
st.set_page_config(page_title="Business OS Pro", page_icon="💎", layout="wide")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR5MK0_eAs57RI4cek-pDbL8wepCfZmZcMZhDqu374yzHWVjPnNyr_DZEnVkh8wGpmrRF1SwHUKgt2h/pub?gid=1413597206&single=true&output=csv"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing API Key")
    st.stop()

# --- 2. עיצוב CSS יוקרתי (SaaS Modern UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: #f8fafc;
    }
    
    /* כותרת מנצנצת */
    .magic-title {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 60px; font-weight: 800; text-align: center; padding: 30px;
        letter-spacing: -1px;
    }
    
    /* כרטיסיות חבילות ומידע */
    .st-emotion-cache-12w0qpk, .package-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
    }
    
    /* כפתורי פרימיום */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 30px;
        font-weight: 700;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar עיצוב */
    .stSidebar {
        background-color: #ffffff;
        border-left: 1px solid #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. פונקציות ליבה ---
def get_users_df():
    try:
        url = f"{SHEET_CSV_URL}&refresh={pd.Timestamp.now().timestamp()}"
        return pd.read_csv(url)
    except: return pd.DataFrame()

def save_to_google(email, data_dict):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
    info = " | ".join([f"{k}: {v}" for k, v in data_dict.items()])
    payload = {"entry.855862094": email, "entry.1847739029": info}
    requests.post(url, data=payload)

# --- 4. ניהול מצבים ---
if 'page' not in st.session_state: st.session_state.page = "auth"
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'biz_data' not in st.session_state: st.session_state.biz_data = {}

# --- 5. ניווט דפים ---

if st.session_state.page == "auth":
    st.markdown("<div class='magic-title'>Business OS</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 כניסת משתמש", "✨ הרשמה לפורטל"])
    
    with t1:
        l_mail = st.text_input("אימייל").strip().lower()
        l_pass = st.text_input("סיסמה", type="password")
        if st.button("התחברי עכשיו"):
            df = get_users_df()
            if not df.empty and l_mail in df.astype(str).values:
                st.session_state.user_email = l_mail
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("פרטים לא נמצאו.")

    with t2:
        r_mail = st.text_input("מייל לעסק", key="r_m")
        r_pass = st.text_input("סיסמה חדשה", type="password")
        if st.button("התחילי בבניית האימפריה"):
            st.session_state.temp_mail, st.session_state.temp_pass = r_mail, r_pass
            st.session_state.page = "onboarding"
            st.rerun()

elif st.session_state.page == "onboarding":
    st.markdown("<div class='magic-title'>הגדרת פרופיל עסקי</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='package-card'>", unsafe_allow_html=True)
        name = st.text_input("שם המותג")
        desc = st.text_area("מה העסק מוכר/מציע? (תיאור מפורט עבור ה-AI)")
        target = st.text_input("מי קהל היעד?")
        tone = st.selectbox("טון דיבור של ה-AI", ["מקצועי ורציני", "חברותי ושנון", "יוקרתי ומכובד", "אנרגטי ומכירתי"])
        if st.button("שמירה ומעבר לחבילות"):
            st.session_state.biz_data = {"name": name, "desc": desc, "target": target, "tone": tone}
            st.session_state.page = "packages"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "packages":
    st.markdown("<div class='magic-title'>בחירת מסלול צמיחה</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='package-card'><h3>💎 VIP Magic</h3><p>בינה מלאכותית ללא הגבלה<br>סוכן תוכן + צ'אט שירות</p><h2>₪199/mo</h2></div>", unsafe_allow_html=True)
        if st.button("בחירה במסלול VIP"):
            save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "VIP", "pass": st.session_state.temp_pass})
            st.session_state.user_email = st.session_state.temp_mail
            st.session_state.page = "dashboard"
            st.rerun()

    with col2:
        st.markdown("<div class='package-card'><h3>🚀 Growth</h3><p>סוכן שיווק חכם<br>ניהול תוכן שבועי</p><h2>₪99/mo</h2></div>", unsafe_allow_html=True)
        if st.button("בחירה במסלול צמיחה"):
            save_to_google(st.session_state.temp_mail, {**st.session_state.biz_data, "plan": "Growth", "pass": st.session_state.temp_pass})
            st.session_state.user_email = st.session_state.temp_mail
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.markdown(f"### 👑 {st.session_state.user_email}")
        menu = st.radio("תפריט ניהול", ["🏠 דף הבית", "✍️ סוכן תוכן AI", "💬 צ'אט שירות לקוחות"])
        
        # כפתור ניהול סודי למנהלת
        if st.session_state.user_email == "admin@magic.com":
            if st.button("📊 ניהול לקוחות"): st.session_state.show_admin = True
        
        if st.button("התנתקות"):
            st.session_state.page = "auth"
            st.rerun()

    if menu == "🏠 דף הבית":
        st.markdown(f"<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.success("המערכת פעילה. כל כלי ה-AI מסונכרנים לנתוני העסק שלך.")
        if st.session_state.get('show_admin'): st.dataframe(get_users_df())
        
    elif menu == "✍️ סוכן תוכן AI":
        st.header("מחולל פוסטים חכם 🤖")
        goal = st.text_input("מה המטרה של הפוסט היום?")
        if st.button("ייצור תוכן"):
            biz = st.session_state.biz_data
            prompt = f"אתה מומחה שיווק. כתוב פוסט לעסק {biz.get('name')} (תיאור: {biz.get('desc')}). קהל יעד: {biz.get('target')}. טון דיבור: {biz.get('tone')}. מטרה: {goal}."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.info(res.choices[0].message.content)

    elif menu == "💬 צ'אט שירות לקוחות":
        st.header("נציג שירות AI לעסק שלך 👩‍💻")
        st.write("כאן תוכלי לראות איך ה-AI יענה ללקוחות שלך.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("שאלת לקוח..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                biz = st.session_state.biz_data
                # הוראות קשוחות לצ'אטבוט
                system_instruction = f"""
                אתה נציג שירות לקוחות מקצועי של העסק '{biz.get('name')}'.
                תיאור העסק: {biz.get('desc')}.
                חוקים נוקשים:
                1. ענה רק על שאלות שקשורות לשירותים או למוצרים של העסק.
                2. אם שואלים שאלות חולין כמו 'מה קורה' או 'מי אתה', ענה בנימוס שאתה נציג השירות של העסק ושמחת לעזור בנושאים מקצועיים בלבד.
                3. אל תנהל שיחות אישיות.
                4. שמור על טון {biz.get('tone')}.
                """
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_instruction}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
