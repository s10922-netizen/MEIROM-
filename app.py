import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# --- הגדרות אבטחה (המפתחות שלך) ---
GROQ_API_KEY = "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"
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# חיבור ל-AI
client = Groq(api_key=GROQ_API_KEY)

# --- עיצוב האתר ---
st.set_page_config(page_title="Meiron AI Solutions", page_icon="🚀")

st.title("🚀 Meiron AI Solutions")
st.write("הופכים את העסק שלכם לחכם יותר בעזרת בינה מלאכותית")

# טופס המילוי
with st.form("my_form"):
    st.subheader("ספרו לנו על העסק שלכם")
    biz_name = st.text_input("שם העסק ומה אתם עושים?")
    problem = st.text_area("מה הבעיה או הקושי הכי גדול בעסק כרגע?")
    target_email = st.text_input("לאיזה מייל לשלוח את פתרון ה-AI?")
    
    submit_button = st.form_submit_button(label="צור פתרון AI מותאם אישית")

if submit_button:
    if not biz_name or not problem or not target_email:
        st.error("בבקשה תמלאו את כל השדות כדי שאוכל לעזור!")
    else:
        with st.spinner("ה-AI של מירום מנתח את העסק שלכם..."):
            try:
                # פנייה ל-AI עם הנחיות של מומחה טכנולוגי
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "אתה מומחה טכנולוגי בכיר להטמעת בינה מלאכותית בעסקים. התפקיד שלך הוא לנתח בעיה של עסק ולתת 3 פתרונות AI מעשיים, יצירתיים וחסכוניים שיפתרו את הבעיה הספציפית שהועלתה. כתוב בעברית מקצועית ומדרבנת."},
                        {"role": "user", "content": f"העסק: {biz_name}. הבעיה: {problem}."}
                    ]
                )
                ai_solution = completion.choices[0].message.content

                # שליחת המייל עם הפתרון
                msg = EmailMessage()
                msg.set_content(f"שלום!\n\nתודה שהשתמשת ב-Meiron AI Solutions.\n\nניתחנו את העסק שלך ({biz_name}) ואת הבעיה שהצגת: '{problem}'.\n\nהנה פתרונות ה-AI שהכנו עבורך:\n\n{ai_solution}\n\nבהצלחה!\nמירום - פתרונות AI")
                msg['Subject'] = f"פתרון AI מותאם אישית עבור {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = target_email

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                st.success(f"✅ הקסם קרה! הפתרון נשלח למייל: {target_email}")
                st.balloons() # חגיגה קטנה על המסך
                
            except Exception as e:
                st.error(f"אופס, קרתה שגיאה: {e}")

# קרדיט קטן בתחתית
st.markdown("---")
st.caption("Powered by Meiron AI • Built with Python & Groq")
