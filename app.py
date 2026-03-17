import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import urllib.parse

# --- הגדרות ---
GROQ_API_KEY = "תדביקי_פה_מפתח_חדש_מ_GROQ"
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")
st.title("🚀 Meiron AI Solutions")

with st.form("main_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה?")
    target_email = st.text_input("מייל למשלוח")
    submit = st.form_submit_button("צור פתרון מנצח")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("ה-AI בונה לכם פתרון ותמונה..."):
            try:
                # בקשת פתרון בטקסט פשוט - בלי עיצובים מסובכים שמשבשים עברית
                prompt = f"Business: {biz_name}. Problem: {problem}. Give 3 simple tips in Hebrew. No numbers, no special symbols, just plain text."
                
                completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4
                )
                ai_solution = completion.choices[0].message.content

                # יצירת תמונה מ-Pollinations לפי שם העסק
                encoded_biz = urllib.parse.quote(biz_name)
                image_url = f"https://pollinations.ai/p/professional_business_logo_for_{encoded_biz}_modern_ai_style?width=1080&height=1080&seed=42&model=flux"

                # הצגת התמונה באתר
                st.image(image_url, caption=f"החזון החדש עבור {biz_name}")

                # שליחת המייל
                msg = EmailMessage()
                msg.set_content(f"היי!\nהנה הפתרונות עבור {biz_name}:\n\n{ai_solution}\n\nבברכה, מירום.")
                msg['Subject'] = f"ייעוץ AI עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                st.success("זה עבד! בדקו את המייל.")
                st.balloons()
                
            except Exception as e:
                st.error(f"שגיאה: {e}")
