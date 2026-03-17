import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import urllib.parse
import time # הוספת ספרייית זמן

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
        with st.spinner("הסוכן מייצר פתרון ומעצב תמונה..."):
            try:
                # 1. יצירת הטקסט
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "תן פתרון עסקי קצר בעברית."},
                              {"role": "user", "content": f"עסק: {biz_name}, בעיה: {problem}"}]
                )
                ai_response = completion.choices[0].message.content

                # 2. יצירת קישור לתמונה וניקוי שלו
                # הוספנו מילות מפתח באנגלית כדי שהתמונה תצא מקצועית
                clean_name = urllib.parse.quote(biz_name)
                image_url = f"https://pollinations.ai/p/professional_business_marketing_for_{clean_name}?width=1080&height=1080&nologo=true&seed={int(time.time())}"

                # המתנה קלה כדי לוודא שהתמונה נוצרה בשרת
                time.sleep(2)

                # 3. שליחת המייל כ-HTML
                msg = EmailMessage()
                msg['Subject'] = f"✅ פתרון ועיצוב עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email
                
                # עיצוב המייל ב-HTML
                email_content = f"""
                <div dir="rtl" style="font-family: sans-serif; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #2e7d32;">שלום! כאן הסוכן של Meiron AI</h2>
                    <p>ניתחנו את הבעיה עבור <strong>{biz_name}</strong>:</p>
                    <p style="background: #f9f9f9; padding: 10px; border-right: 5px solid #2e7d32;">{ai_response}</p>
                    <hr>
                    <h3>העיצוב השיווקי שלך מוכן:</h3>
                    <p>אם התמונה לא מופיעה, לחץ על "הצג תמונות" במייל או בקישור למטה.</p>
                    <img src="{image_url}" width="500" style="border-radius: 10px; display: block; margin: 0 auto;">
                    <br>
                    <div style="text-align: center;">
                        <a href="{image_url}" style="background: #2e7d32; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">הורד תמונה ברזולוציה גבוהה</a>
                    </div>
                </div>
                """
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content.encode('utf-8'))

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)

                # 4. הצגה באתר
                st.success("הסוכן סיים! בדוק את המייל.")
                st.image(image_url, caption=f"עיצוב עבור {biz_name}")
                st.info(ai_response)
                st.balloons()

            except Exception as e:
                st.error(f"שגיאה: {e}")
