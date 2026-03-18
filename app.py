import streamlit as st
from groq import Groq
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- הגדרות דף ---
st.set_page_config(page_title="Meirom Magic AI", page_icon="🧚‍♀️", layout="wide")

# --- חיבורים (AI וטבלה) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
# חיבור ל-Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- פונקציה לקריאת משתמשים מהטבלה ---
def get_users():
    try:
        # קורא את הטבלה שהגדרת ב-Secrets
        df = conn.read(spreadsheet=st.secrets["GSHEET_URL"])
        return df.set_index('Email')['Password'].to_dict()
    except:
        return {"admin@magic.com": "1234"}

# --- פונקציה להוספת משתמש חדש לטבלה ---
def add_user(email, password):
    df = conn.read(spreadsheet=st.secrets["GSHEET_URL"])
    new_data = pd.DataFrame([{"Email": email, "Password": password}])
    updated_df = pd.concat([df, new_data], ignore_index=True)
    conn.update(spreadsheet=st.secrets["GSHEET_URL"], data=updated_df)

# --- לוגיקה של המערכת ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

users = get_users() # טוען את המשתמשים מהגוגל שיטס!

# --- (כאן מגיע כל שאר הקוד של העיצוב והדפים...) ---

# בקטע של ההרשמה (Tab 2), נשנה את הכפתור לזה:
# if st.button("צרי חשבון ✨"):
#     add_user(new_email, new_pass)
#     st.success("נרשמת בטבלה! עכשיו זה נשמר לתמיד.")
