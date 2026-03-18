import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# פונקציית חיפוש
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
    
    [data-testid="stSidebar"] { background-color: #f3f0ff; border-left: 1px solid #7c3aed; }
    
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

    .stButton>button {
        border-radius: 20px; border: none; padding: 10px 25px;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- סרגל צד ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🧚‍♀️ Meirom Menu</h2>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("לאן נלך היום?", 
                    ["✨ דף הבית", "🚀 סוכן שיווק", "🧹 מנקה הבלגן (לסבתא)", "🔗 חיבורים"])
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
    task = st.text_area("מה הסוכן צריך לבצע?")
    
    if st.button("הפעל קסם ⚡", use_container_width=True):
        with st.status("הפיה בעבודה...") as s:
            context = web_search(f"מידע על {biz}")
            prompt = f"Context: {context}\nTask: {task} for {biz}. Language: Hebrew. Finish with 'Meirom Magic AI'."
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("הנה התוצאה:")
            st.write(res.choices[0].message.content)
            st.balloons()
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.button("שלח למייל 📧")
            c2.button("שלח לוואטסאפ 📱")
            c3.button("פרסם באינסטגרם 📸")

# --- דף סבתא ---
elif page == "🧹 מנקה הבלגן (לסבתא)":
    st.header("הפיצ'ר של סבתא 👵")
    st.write("בקרוב: ה-AI יסרוק את הטלפון שלך וימחק הודעות ספאם ותמונות כפולות!")

# --- חיבורים ---
elif page == "🔗 חיבורים":
    st.header("ניהול חיבורים")
    st.checkbox("WhatsApp API")
    st.checkbox("Instagram Business")
    st.checkbox("Google Mail")
