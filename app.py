import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# --- זיכרון משתמשים (Database זמני) ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- פונקציית חיפוש ---
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"Source: {r['title']}\nContent: {r['body']}" for r in results])
    except: return "לא נמצא מידע עדכני."

# --- עיצוב (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }
    [data-testid="stSidebar"] { background-color: #f3f0ff; border-left: 1px solid #7c3aed; }
</style>
""", unsafe_allow_html=True)

# --- לוגיקת דפים ---

if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה חדשה"])
    
    with tab1:
        email = st.text_input("אימייל", key="l_email")
        password = st.text_input("סיסמה", type="password", key="l_pass")
        if st.button("כניסה למערכת 🚀", use_container_width=True):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("פרטים שגויים")

    with tab2:
        new_email = st.text_input("מייל להרשמה")
        new_pass = st.text_input("סיסמה", type="password")
        if st.button("צור חשבון 🧚‍♀️", use_container_width=True):
            st.session_state.users[new_email] = new_pass
            st.success("נרשמת! עכשיו אפשר להתחבר.")

else:
    # תפריט צד (Sidebar) מופיע רק כשמחוברים
    with st.sidebar:
        st.markdown("### מחוברת: מנכ\"לית מיי 👑")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        page = st.radio("ניווט:", ["✨ דף הבית", "🚀 סוכן שיווק", "🧹 מנקה הבלגן"])

    # דפי האפליקציה
    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("סטטוס", "מחוברת ✅")
        col2.metric("חבילה", "Enterprise")
        col3.metric("חסכון", "95%")
        st.write("### ברוכה הבאה לסביבת העבודה שלך!")

    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק חכם")
        biz = st.text_input("שם העסק")
        task = st.text_area("מה לכתוב?")
        if st.button("הפעל קסם ⚡"):
            with st.status("חושבת..."):
                context = web_search(biz)
                prompt = f"Marketing post for {biz}: {task}. Hebrew."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                ans = res.choices[0].message.content
                st.write(ans)
                whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(ans)}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer;">שלחי בוואטסאפ 📱</button></a>', unsafe_allow_html=True)

    elif page == "🧹 מנקה הבלגן":
        st.header("מנקה הבלגן 👵")
        st.write("כאן יהיו הפיצ'רים של סבתא בקרוב!")
