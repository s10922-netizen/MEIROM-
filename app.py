import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# משיכת המפתח מהכספת הסודית של Streamlit
GROQ_API_KEY = st.secrets["GROQ_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")
st.title("🚀 Meiron AI Solutions")

with st.form("main_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה?")
    target_email = st.text_input("מייל למשלוח")
    submit = st.form_submit_button("שלח פתרון")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("ה-AI בונה פתרון..."):
            try:
                prompt = f"Business: {biz_name}. Problem: {problem}. Give 3 business tips in Hebrew."
                completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile", # המודל המעודכן
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                ai_solution = completion.choices[0].message.content

                msg = EmailMessage()
                msg.set_content(f"שלום!\n\nהנה הפתרון עבור {biz_name}:\n\n{ai_solution}\n\nבברכה, מירום.", charset='utf-8')
                msg['Subject'] = f"ייעוץ AI עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                st.success("✅ המייל נשלח בהצלחה!")
                st.balloons()
            except Exception as e:
                st.error(f"שגיאה: {e}")
