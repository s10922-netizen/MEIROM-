import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# הגדרות
GROQ_API_KEY = "gsk_jUtWaZ7q2YzI98BNVkWGdyb3FY8eSMyzhQL3irkSdWRuLFfWn"
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

st.title("🚀 Meiron AI Solutions")

with st.form("main"):
    biz = st.text_input("שם העסק")
    prob = st.text_area("בעיה")
    mail = st.text_input("מייל")
    btn = st.form_submit_button("שלח")

if btn and biz and prob and mail:
    with st.spinner("עובד..."):
        try:
            chat = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a business consultant. Respond in Hebrew only. Be short and simple. 3 bullet points max."},
                    {"role": "user", "content": f"עסק: {biz}, בעיה: {prob}. תן 3 פתרונות קצרים בעברית."}
                ],
                temperature=0.1 # כמעט אפס יצירתיות כדי למנוע שטויות
            )
            res = chat.choices[0].message.content

            msg = EmailMessage()
            msg.set_content(f"היי,\n\nהפתרונות עבור {biz}:\n{res}")
            msg['Subject'] = f"ייעוץ עבור {biz}"
            msg['From'] = MY_EMAIL
            msg['To'] = mail

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(MY_EMAIL, APP_PASSWORD)
                smtp.send_message(msg)
            st.success("נשלח!")
            st.balloons()
        except Exception as e:
            st.error(f"שגיאה: {e}")
