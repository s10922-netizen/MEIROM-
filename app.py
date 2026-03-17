import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# משיכת המפתח מה-Secrets של Streamlit
# (ודאי שהכנסת אותו ב-Settings -> Secrets כפי שהסברתי קודם)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

# --- עיצוב האתר ---
st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")
st.title("🚀 Meiron AI Solutions")
st.markdown("### פתרונות AI חכמים לעסקים")

with st.form("main_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה?")
    target_email = st.text_input("מייל למשלוח")
    submit = st.form_submit_button("שלח פתרון AI")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("מנתח נתונים במודל החדש..."):
            try:
                # המודל המעודכן ביותר ל-2026 - יציב וחכם
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "אתה יועץ עסקי מקצועי. תן 3 פתרונות AI פשוטים, קצרים וברורים בעברית בלבד. כתוב פסקאות קצרות."},
                        {"role": "user", "content": f"העסק: {biz_name}. הבעיה: {problem}."}
                    ],
                    temperature=0.3
                )
                
                ai_solution = completion.choices[0].message.content

                msg = EmailMessage()
                msg.set_content(f"שלום!\n\nהנה הפתרונות המעודכנים עבור {biz_name}:\n\n{ai_solution}\n\nבברכה,\nמירום.")
                msg['Subject'] = f"פתרון מותאם אישית עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                st.success("נשלח בהצלחה מהמערכת החדשה!")
                st.balloons()
            except Exception as e:
                st.error(f"שגיאה: {e}")
