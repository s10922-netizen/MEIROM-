import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבור ל-AI ---
client = Groq(api_key="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")

# --- עיצוב מתקדם (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    /* עיצוב סרגל הצד */
    [data-testid="stSidebar"] { background-color: #f3f0ff; border-left: 1px solid #ddd; }
    
    /* כותרת מנצנצת */
    .magic-title {
        background: linear-gradient(90deg, #7c3aed, #ec4899, #7c3aed);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 50px; font-weight: bold; text-align: center;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* כפתורים מעוצבים */
    .stButton>button {
        border-radius: 12px; border: none; padding: 10px 20px;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.3); }
</style>
""", unsafe_allow_html=True)

# --- סרגל צד (תפריט הפיצ'רים) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🧚‍♀️ תפריט קסם</h2>", unsafe_allow_html=True)
    menu = st.radio("לאן נלך היום?", 
                    ["דף הבית ✨", "סוכן שיווק 🚀", "מנקה ספאם (בקרוב) 🧹", "חיבורים (WhatsApp/Mail) 🔗"])
    st.divider()
    st.info("Meirom Magic AI v2.0")

# --- לוגיקה של הדפים ---

# 1. דף הבית
if menu == "דף הבית ✨":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    st.write("### ברוכה הבאה, מנכ"לית! איזה קסם נחולל היום?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ המערכת מחוברת ל-AI")
    with col2:
        st.info("📈 0 לקוחות פעילים (בינתיים!)")

# 2. סוכן שיווק
elif menu == "סוכן שיווק 🚀":
    st.header("סוכן שיווק חכם")
    biz_name = st.text_input("שם העסק שלך")
    task = st.text_area("מה לכתוב עבורך?")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        use_web = st.checkbox("סרוק אינטרנט למידע מעודכן 🌐")
    
    if st.button("הפעל קסם שיווקי ✨", use_container_width=True):
        with st.status("הפיה חושבת...") as s:
            prompt = f"Write a professional marketing post for {biz_name}: {task}. Language: Hebrew."
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            result_text = res.choices[0].message.content
            st.write(result_text)
            st.balloons()
            
            # כפתורי פעולה מהירים
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.button("שלח למייל 📧")
            c2.button("שלח לוואטסאפ 📱")
