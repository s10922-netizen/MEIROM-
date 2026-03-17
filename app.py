import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# --- הגדרות אבטחה ---
GROQ_API_KEY = "gsk_jUtWaZ7q2YzI98BNVkWGdyb3FY8eSMyzhQL3irkSdWRuLFfWn"
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

# --- עיצוב האתר ---
st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")

st.title("🚀 Meiron AI Solutions")
st.markdown("### פתרונות AI חכמים לעסקים קיימים")

with st.form("main_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה בעסק?")
    target_email = st.text_input("מייל למשלוח הפתרון")
    submit = st.form_submit_button("צור פתרון עכשיו")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("מנתח נתונים..."):
            try:
                # שינוי למודל Mixtral - הרבה יותר יציב בעברית!
                completion = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[
                        {
                            "role": "system", 
                            "content": "אתה עוזר עסקי חכם. כתוב 3 פתרונות AI קצרים, ברורים ומעשיים בעברית בלבד. אל תכתוב מספרים מוזרים, אל תכתוב על 5G או AR. כתוב רק דברים פשוטים שבעל עסק יכול להבין."
                        },
                        {
                            "role": "user", 
                            "content": f"העסק: {biz_name}. הבעיה: {problem}. תן 3 פתרונות פשוטים בעברית."
                        }
                    ],
                    temperature=0.3, # הורדתי עוד יותר את היצירתיות כדי שלא ימציא שטויות
                    max_tokens=500
                )
                
                ai_solution = completion.choices[0].message.content

                # הכנת המייל
                msg = EmailMessage()
                msg.set_content(f"שלום!\n\nהנה הפתרונות עבור {biz_name}:\n\n{ai_solution}\n\nבברכה,\nמירום - פתרונות AI")
                msg['Subject'] = f"ייעוץ AI עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                st.success("נשלח בהצלחה!")
                st.balloons()
                
            except Exception as e:
                st.error(f"שגיאה: {e}")
