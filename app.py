import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# משיכת המפתח מהכספת הסודית של Streamlit
GROQ_API_KEY = "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"
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

# --- עיצוב האתר ---
st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")
st.title("🚀 Meiron AI Solutions")

with st.form("main_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה?")
    target_email = st.text_input("מייל למשלוח")
    submit = st.form_submit_button("שלח פתרון AI")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("מנתח..."):
            try:
                completion = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[
                        {"role": "system", "content": "אתה יועץ עסקי. תן 3 פתרונות פשוטים בעברית בלבד."},
                        {"role": "user", "content": f"העסק: {biz_name}. הבעיה: {problem}."}
                    ],
                    temperature=0.4
                )
                ai_solution = completion.choices[0].message.content
                msg = EmailMessage()
                msg.set_content(f"שלום!\n\nהנה הפתרונות עבור {biz_name}:\n\n{ai_solution}\n\nמירום.")
                msg['Subject'] = f"פתרון עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                st.success("נשלח!")
                st.balloons()
            except Exception as e:
                st.error(f"שגיאה: {e}")
