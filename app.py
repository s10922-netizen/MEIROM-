import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# --- ניהול זיכרון (Session State) ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin@magic.com": "1234"}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'plan' not in st.session_state:
    st.session_state.plan = None

# --- פונקציית חיפוש באינטרנט ---
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"Source: {r['title']}\nContent: {r['body']}" for r in results])
    except:
        return "לא נמצא מידע עדכני כרגע."

# --- עיצוב CSS מתקדם ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    /* כותרת מנצנצת */
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 60px; font-weight: bold; text-align: center;
        margin-bottom: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* עיצוב סרגל צד */
    [data-testid="stSidebar"] { background-color: #f3f0ff; border-left: 2px solid #7c3aed; }
    
    /* כפתורי חבילות */
    .stButton>button {
        border-radius: 15px; border: none; transition: 0.3s;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- לוגיקת דפי האתר ---

# 1. דף כניסה והרשמה (אם לא מחוברים)
if not st.session_state.logged_in:
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>הכניסה למורשים בלבד ✨</h2>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔑 התחברות", "📝 הרשמה"])
    
    with tab_login:
        l_email = st.text_input("אימייל")
        l_pass = st.text_input("סיסמה", type="password")
        if st.button("כניסה למערכת 🚀", use_container_width=True):
            if l_email in st.session_state.users and st.session_state.users[l_email] == l_pass:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("מייל או סיסמה לא נכונים")

    with tab_signup:
        s_email = st.text_input("בחרי אימייל להרשמה")
        s_pass = st.text_input("בחרי סיסמה חזקה", type="password")
        if st.button("צור חשבון חדש 🧚‍♀️", use_container_width=True):
            if s_email in st.session_state.users:
                st.warning("את כבר רשומה!")
            else:
                st.session_state.users[s_email] = s_pass
                st.success("נרשמת בהצלחה! עברי ללשונית התחברות.")

# 2. דף בחירת חבילה (אם מחוברים אבל לא בחרו חבילה)
elif st.session_state.logged_in and st.session_state.plan is None:
    st.markdown("<div class='magic-title'>בחרי את המסלול שלך</div>", unsafe_allow_html=True)
    st.write("### כדי להתחיל להשתמש בסוכנים, עליך לבחור חבילת מנוי:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### Basic 🧚‍♀️")
        st.write("סוכן שיווק בסיסי\n\nללא חיפוש באינטרנט\n\n**250 ש\"ח לחודש**")
        if st.button("בחר Basic"):
            st.session_state.plan = "Basic"
            st.rerun()

    with col2:
        st.success("### Pro ⭐")
        st.write("סוכן שיווק + חיפוש אינטרנט\n\nחיבור לוואטסאפ\n\n**750 ש\"ח לחודש**")
        if st.button("בחר Pro (מומלץ!)"):
            st.session_state.plan = "Pro"
            st.rerun()

    with col3:
        st.warning("### Enterprise 👑")
        st.write("כל הפיצ'רים פתוחים\n\nמנקה הספאם של סבתא\n\n**2,500 ש\"ח לחודש**")
        if st.button("בחר Enterprise"):
            st.session_state.plan = "Enterprise"
            st.rerun()

# 3. דף האפליקציה המלא (אחרי התחברות ובחירת חבילה)
else:
    with st.sidebar:
        st.markdown(f"### מנכ\"לית מיי 👑\n**חבילה:** {st.session_state.plan}")
        if st.button("התנתקות 🔒"):
            st.session_state.logged_in = False
            st.session_state.plan = None
            st.rerun()
        st.divider()
        page = st.radio("תפריט ניווט:", ["✨ דף הבית", "🚀 סוכן שיווק", "🧹 מנקה הבלגן"])

    if page == "✨ דף הבית":
        st.markdown("<div class='magic-title'>מרכז הבקרה</div>", unsafe_allow_html=True)
        st.write(f"### ברוכה הבאה! החבילה שלך ({st.session_state.plan}) פעילה.")
        col1, col2 = st.columns(2)
        col1.metric("סטטוס", "מחוברת ✅")
        col2.metric("חיסכון חודשי משוער", "₪12,500")

    elif page == "🚀 סוכן שיווק":
        st.header("סוכן שיווק חכם")
        biz = st.text_input("שם העסק")
        task = st.text_area("מה לכתוב היום?")
        
        # הגבלת פיצ'ר לפי חבילה
        use_search = False
        if st.session_state.plan in ["Pro", "Enterprise"]:
            use_search = st.toggle("הפעל סריקה באינטרנט 🌐", value=True)
        else:
            st.warning("סריקה באינטרנט פתוחה למנויי Pro בלבד.")

        if st.button("הפעל קסם ⚡", use_container_width=True):
            with st.status("הפיה בעבודה..."):
                context = web_search(biz) if use_search else "No internet access."
                prompt = f"Context: {context}\nWrite a marketing post for {biz}: {task}. Language: Hebrew. Finish with 'Meirom Magic AI'."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                ans = res.choices[0].message.content
                st.write(ans)
                
                # כפתור וואטסאפ (פתוח לכולם חוץ מ-Basic)
                if st.session_state.plan != "Basic":
                    whatsapp_text = urllib.parse.quote(ans)
                    st.markdown(f"""
                        <a href="https://wa.me/?text={whatsapp_text}" target="_blank">
                            <button style="width: 100%; background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 15px; font-weight: bold; cursor: pointer;">
                                שלחי בוואטסאפ! 📱✨
                            </button>
                        </a>
                    """, unsafe_allow_html=True)
                else:
                    st.info("כדי לשלוח ישירות לוואטסאפ, שדרגי ל-Pro.")

    elif page == "🧹 מנקה הבלגן":
        if st.session_state.plan == "Enterprise":
            st.header("מנקה הבלגן של סבתא 👵")
            st.write("הפיצ'ר פעיל בחשבון ה-Enterprise שלך!")
        else:
            st.error("הפיצ'ר הזה פתוח למנויי Enterprise בלבד.")
