import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import requests

# --- הגדרות אבטחה וחיבורים ---
# ודאי שהגדרת את GROQ_API_KEY בתוך ה-Secrets של Streamlit
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

# --- עיצוב ממשק האתר ---
st.set_page_config(page_title="Meiron AI - Super Agent", page_icon="🤖", layout="centered")

st.title("🤖 Meiron AI - Super Agent")
st.markdown("### המערכת שלא רק מייעצת, אלא ממש מבצעת")
st.write("בנית על ידי מירום - פתרונות טכנולוגיים חכמים בחינם")

# טופס קלט
with st.form("super_agent_form"):
    st.subheader("פרטי המשימה")
    biz_name = st.text_input("שם העסק (למשל: חנות הפרחים הגבעול)")
    problem = st.text_area("מה הבעיה? (למשל: אין לי פוסטים לאינסטגרם)")
    target_email = st.text_input("מייל למשלוח התוצר המוגמר")
    
    submit = st.form_submit_button("הפעל סוכן ביצוע")

# לוגיקה של הסוכן
if submit:
    if not biz_name or not problem or not target_email:
        st.warning("אנא מלאו את כל השדות כדי שהסוכן יוכל לעבוד.")
    else:
        with st.spinner("הסוכן מנתח, מעצב ושולח את התוצרים..."):
            try:
                # 1. יצירת האסטרטגיה (טקסט)
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "אתה סוכן AI ביצועי. תן פתרון אחד מעשי וקצר בעברית, וכתוב תיאור קצר לתמונה שיווקית שתתאים לעסק."},
                        {"role": "user", "content": f"עסק: {biz_name}, בעיה: {problem}"}
                    ],
                    temperature=0.4
                )
                ai_response = completion.choices[0].message.content

                # 2. יצירת תמונה שיווקית (ביצוע אוטומטי בחינם)
                # אנחנו יוצרים Prompt באנגלית עבור מחולל התמונות
                image_prompt = f"Professional business advertisement for {biz_name}, high quality, digital marketing style"
                image_url = f"https://pollinations.ai/p/{image_prompt.replace(' ', '_')}?width=1080&height=1080&seed=42"

                # 3. שליחת המייל עם כל התוצרים
                msg = EmailMessage()
                msg.set_content(f"""
שלום!
כאן סוכן ה-AI של מירום - Meiron AI Solutions.

ביצעתי עבור העסק שלך ({biz_name}) את המשימה.

הניתוח והפתרון שלי:
{ai_response}

יצרתי עבורך גם תמונה שיווקית מוכנה לפרסום!
תוכל להוריד אותה מכאן:
{image_url}

בהצלחה!
מירום - סוכני AI.
""")
                msg['Subject'] = f"✅ המשימה הושלמה עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)

                # 4. הצגת התוצאה באתר
                st.success("המשימה הושלמה בהצלחה! התוצרים נשלחו למייל.")
                st.balloons()
                st.snow()
                
                st.subheader("התמונה שהסוכן יצר עבורכם:")
                st.image(image_url, use_column_width=True)
                st.info(f"הפתרון הטקסטואלי: {ai_response}")

            except Exception as e:
                st.error(f"אירעה שגיאה טכנית: {e}")

# סיומת
st.markdown("---")
st.caption("Meiron AI Solutions © 2026 | Powered by Groq, Pollinations & Python")
