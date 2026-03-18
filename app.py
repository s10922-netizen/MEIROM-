import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import urllib.parse # כלי חדש לסידור הטקסט לוואטסאפ

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

# --- עיצוב (CSS) ---
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
    }
    @keyframes shine { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# --- סרגל צד ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🧚‍♀️ Meirom Menu</h2>", unsafe_allow_html=True)
    page = st.radio("ניווט:", ["✨ דף הבית", "🚀 סוכן שיווק", "🧹 מנקה הבלגן"])
    st.write("V 2.1 - WhatsApp Enabled")

# --- דף הבית ---
if page == "✨ דף הבית":
    st.markdown("<div class='magic-title'>Meirom Magic AI</div>", unsafe_allow_html=True)
    st.write("### ברוכה הבאה! היום האוטומציה שלך עוברת לשלב הבא.")

# --- סוכן שיווק (כאן הקסם של הוואטסאפ!) ---
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
            
            # --- כפתור הוואטסאפ האמיתי ---
            st.divider()
            # מכין את הטקסט לשליחה בקישור
            whatsapp_text = urllib.parse.quote(ans)
            whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
            
            st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank">
                    <button style="
                        width: 100%;
                        background-color: #25D366;
                        color: white;
                        padding: 15px;
                        border: none;
                        border-radius: 15px;
                        font-weight: bold;
                        cursor: pointer;
                        font-size: 18px;
                    ">
                        שלחי את זה בוואטסאפ עכשיו! 📱✨
                    </button>
                </a>
            """, unsafe_allow_html=True)
            st.balloons()

# --- דף סבתא ---
elif page == "🧹 מנקה הבלגן":
    st.header("מנקה הבלגן 👵")
    st.write("בפיתוח...")
