import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# פונקציית חיפוש בחינם
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"Source: {r['title']}\nContent: {r['body']}" for r in results])
    except:
        return "לא נמצא מידע עדכני."

# --- עיצוב מתקדם (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    /* עיצוב סרגל הצד */
    [data-testid="stSidebar"] { background-color: #f3f0ff; border-left: 1px solid #7c3aed; }
    
    /* כותרת מנצנצת */
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 50px; font-weight: bold; text-align: center;
        margin-bottom: 20px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* כפתורים מעוגלים וצבעוניים */
    .stButton>button {
        border-radius: 20px; border: none; padding: 10px 25px;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- סרגל צד (ניווט נגיש) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🧚‍♀️ Meirom Menu</h2>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("לאן נלך היום?", 
                    ["✨ דף הבית", "🚀 סוכן שיווק", "🧹 מנקה הבלגן (לסבתא)", "🔗 חיבורים ואינטגרציות"])
    st.divider()
    st.write("V 2.0 - מנכ\"לית: מיי")

# --- דף הבית ---
if page == "✨ דף הבית":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    st.write("### ברוכה הבאה למרכז השליטה שלך!")
    st.info("השתמשי בתפריט מצד ימין כדי לעבור בין הכלים השונים.")
    
    col1, col2, col3 = st.columns(3)
col1.metric("סטטוס מערכת", "פעיל ✨")
    col2.metric("סוכנים רצים", "3")
    col3.metric("חיסכון בזמן", "95%")

# --- סוכן שיווק ---
elif page == "🚀 סוכן שיווק":
    st.header("סוכן שיווק ואסטרטגיה")
    biz = st.text_input("שם העסק")
    task = st.text_area("מה הסוכן צריך לבצע? (פוסט, תסריט, רעיון)")
    
    col_tools = st.columns(2)
    with col_tools[0]:
        use_search = st.toggle("סריקה באינטרנט 🌐", value=True)
    
    if st.button("הפעל קסם ⚡", use_container_width=True):
        with st.status("הפיה בעבודה...") as s:
            context = web_search(f"מידע על {biz}") if use_search else ""
            prompt = f"Context: {context}\nTask: {task} for {biz}. Language: Hebrew. Finish with 'Meirom Magic AI'."
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                ans = res.choices[0].message.content
                st.success("הנה התוצאה:")
                st.write(ans)
                st.balloons()
                
                # כפתורי נגישות סופיים
                st.divider()
                st.write("### מה לעשות עם התוצאה?")
                c1, c2, c3, c4 = st.columns(4)
                c1.button("שלח למייל 📧")
                c2.button("שלח לוואטסאפ 📱")
                c3.button("פרסם באינסטגרם 📸")
                c4.button("פרסם בטיקטוק 🎬")
            except Exception as e:
                st.error(f"תקלה בחיבור ל-AI: {e}")

# --- דף מנקה הבלגן (סבתא) ---
elif page == "🧹 מנקה הבלגן (לסבתא)":
    st.header("הפיצ'ר של סבתא: ניקוי ספאם ותמונות 👵")
    st.warning("הפיצ'ר הזה נמצא כרגע בפיתוח...")
    st.write("בקרוב: ה-AI יסרוק את הטלפון שלך וימחק הודעות ספאם ותמונות כפולות באופן אוטומטי!")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ4Z3R3eGZ4Z3R3eGZ4Z3R3eGZ4Z3R3eGZ4Z3R3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9iYmcmY3Q9Zw/3o7TKVUn7iM8FMEU24/giphy.gif")

# --- חיבורים ---
elif page == "🔗 חיבורים ואינטגרציות":
    st.header("ניהול חיבורים")
    st.write("חברי את העסק שלך לכל הפלטפורמות")
    st.checkbox("WhatsApp API")
    st.checkbox("Instagram Business")
    st.checkbox("Facebook Pages")
    st.checkbox("Google Mail")
    st.button("שמור הגדרות חיבור")
