import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# --- הגדרות ---
GROQ_API_KEY = "gsk_jUtWaZ7q2YzI98BNVkWGdyb3FY8eSMyzhQL3irkSdWRuLFfWn" # ודאי שהמפתח תקין
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")
st.title("🚀 Meiron AI Solutions")

with st.form("main_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה?")
    target_email = st.text_input("מייל למשלוח")
    submit = st.form_submit_button("צור פתרון עכשיו")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("מייצר פתרון מקצועי..."):
            try:
                # הנחיה שמכריחה אותו לכתוב עברית נקייה
                prompt = f"Business: {biz_name}. Problem: {problem}. Give 3 professional business tips in Hebrew. Keep it simple and clear. No special characters."
                
                completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                ai_solution = completion.choices[0].message.content

                # --- התיקון לשגיאת ה-ASCII ---
                msg = EmailMessage()
                msg.set_content(f"שלום!\n\nהנה הפתרונות עבור {biz_name}:\n\n{ai_solution}\n\nבברכה, מירום.", charset='utf-8') # כאן הוספנו תמיכה בעברית!
                msg['Subject'] = f"ייעוץ AI עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                st.success("✅ הצלחה! הפתרון נשלח למייל בעברית תקינה.")
                st.balloons()
                
            except Exception as e:
                st.error(f"שגיאה: {e}")
