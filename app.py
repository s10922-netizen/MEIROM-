import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבורים ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"שגיאת חיבור: {e}")
    st.stop()

# --- לוגיקה ---
st.markdown("<h1 style='text-align:center;'>Meirom Magic AI</h1>", unsafe_allow_html=True)

# בדיקת לקוח חיצוני
query_params = st.query_params
if query_params.get("view") == "customer":
    st.write("ברוכים הבאים לעסק!")
    # כאן יבוא דף הלקוח הנקי
    st.stop()

# דף התחברות/הרשמה
tab1, tab2 = st.tabs(["🔑 התחברות", "📝 הרשמה"])

with tab2:
    st.subheader("יצירת חשבון חדש")
    new_email = st.text_input("מייל", key="reg_email")
    new_pass = st.text_input("סיסמה", type="password", key="reg_pass")
    if st.button("צרי חשבון ✨"):
        # כאן תבוא הפקודה שכותבת לטבלה
        st.success("נרשמת בהצלחה!")
