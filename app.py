import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import urllib.parse # כלי לניקוי כתובות אינטרנט

# --- הגדרות אבטחה ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Meiron AI - Super Agent", page_icon="🤖")
st.title("🤖 Meiron AI - Super Agent")

with st.form("super_agent_form"):
    biz_name = st.text_input("שם העסק")
    problem = st.text_area("מה הבעיה?")
    target_email = st.text_input("מייל למשלוח")
    submit = st.form_submit_button("הפעל סוכן ביצוע")

if submit:
    if biz_name and problem and target_email:
        with st.spinner("הסוכן מעצב עבורך את הפתרון..."):
            try:
                # 1. יצירת הטקסט
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "תן פתרון עסקי קצר בעברית."},
                              {"role": "user", "content": f"עסק: {biz_name}, בעיה: {problem}"}]
                )
                ai_response = completion.choices[0].message.content

                # 2. יצירת תמונה (ניקוי הכתובת כדי שתעבוד בטוח!)
                clean_name = urllib.parse.quote(biz_name)
                image_url = f"https://pollinations.ai/p/professional_marketing_banner_for_{clean_name}_style_modern_clean?width=1080&height=1080&seed=42"

                # 3. שליחת מייל מעוצב ב-HTML (כדי שיראו את התמונה במייל)
                msg = EmailMessage()
                msg['Subject'] = f"✅ המשימה הושלמה עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email
                
                # יצירת תוכן המייל כ-HTML
                email_content = f"""
                <html>
                <body dir="rtl" style="font-family: Arial, sans-serif;">
                    <h2>שלום! כאן סוכן ה-AI של מירום.</h2>
                    <p>ביצעתי את המשימה עבור <strong>{biz_name}</strong>.</p>
                    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 10px;">
                        <p>{ai_response}</p>
                    </div>
                    <h3>התמונה השיווקית שיצרתי עבורך:</h3>
                    <img src="{image_url}" alt="Marketing Image" style="width: 100%; max-width: 500px; border-radius: 10px;">
                    <p><a href="{image_url}">לחץ כאן להורדת התמונה במידה ולא רואים אותה</a></p>
                    <br>
                    <p>בברכה,<br><strong>Meiron AI Solutions</strong></p>
                </body>
                </html>
                """
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content.encode('utf-8'))

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)

                # 4. הצגה באתר
                st.success("המשימה הושלמה!")
                st.subheader("התמונה שהסוכן יצר:")
                st.image(image_url) # עכשיו זה יעבוד כי הכתובת נקייה
                st.info(ai_response)
                st.balloons()

            except Exception as e:
                st.error(f"שגיאה: {e}")
