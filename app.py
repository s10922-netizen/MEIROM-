import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# --- זיכרון המערכת (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- עיצוב (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    /* עיצוב כללי */
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* דף כניסה */
    .login-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #7c3aed;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- פונקציות עזר ---
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"Source: {r['title']}\nContent: {r['body']}" for r in results])
    except: return "לא נמצא מידע עדכני."

# --- לוגיקת דפים ---

# דף כניסה (יוצג רק אם לא מחוברים)
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>ברוכה הבאה לממלכת האוטומציה ✨</h2>", unsafe_allow_html=True)
    
    col_empty1, col_login, col_empty2 = st.columns([1, 2, 1])
    
    with col_login:
        st.write("---")
        email = st.text_input("אימייל")
        password = st.text_input("סיסמה", type="password")
        
        c1, c2 = st.columns(2)
        if c1.button("התחברות 🚀", use_container_width=True):
            if email == "admin@magic.com" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("המייל או הסיסמה לא נכונים")
        
        if c2.button("הרשמה (בקרוב) 🧚‍♀️", use_container_width=True):
            st.toast("מערכת ההרשמה בבנייה!")

# דף האפליקציה (יוצג רק אחרי התחברות)
else:
    with st.sidebar:
        st.markdown("### מחוברת: מנכ\"לית מיי 👑")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        page = st.radio("תפריט:", ["✨ דף הבית", "🚀 סוכן שיווק", "🧹 מנקה הבלגן"])
        st.write("V 2.2 - Security Enabled")

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write(f"### שלום {st.session_state.get('user_name', 'מיי')}, איזה קסם נחולל היום?")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("מנוי", "Enterprise 👑")
        col2.metric("בקשות AI", "פעיל")
        col3.metric("חסכון היום", "4.5 שעות")

    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק חכם")
        biz = st.text_input("שם העסק")
        task = st.text_area("מה לכתוב?")
        
        if st.button("הפעל קסם ⚡", use_container_width=True):
            with st.status("יוצר תוכן...") as s:
                context = web_search(f"מידע על {biz}")
                prompt = f"Write a marketing post for {biz}: {task}. Language: Hebrew. Finish with 'Meirom Magic AI'."
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                ans = res.choices[0].message.content
                st.success("הנה התוצאה:")
                st.write(ans)
                
                whatsapp_text = urllib.parse.quote(ans)
                st.markdown(f"""
                    <a href="https://wa.me/?text={whatsapp_text}" target="_blank">
                        <button style="width: 100%; background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 18px;">
                            שלחי בוואטסאפ! 📱✨
                        </button>
                    </a>
                """, unsafe_allow_html=True)

    elif page == "🧹 מנקה הבלגן":
        st.header("מנקה הבלגן של סבתא 👵")
        st.write("כאן יהיה הפיצ'ר לניקוי ספאם ותמונות כפולות.")
