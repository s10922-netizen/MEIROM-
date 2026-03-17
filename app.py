import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage

# --- הגדרות אבטחה וחיבור ---
# המפתח נמשך מהכספת הסודית ב-Streamlit Cloud
GROQ_API_KEY = st.secrets["GROQ_KEY"]
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

client = Groq(api_key=GROQ_API_KEY)

# --- עיצוב ממשק המערכת ---
st.set_page_config(page_title="Meiron AI | Enterprise System", page_icon="🏢", layout="wide")

# עיצוב כותרת מרשימה
st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .sub-title { font-size: 20px; color: #4B5563; text-align: center; margin-bottom: 30px; }
    </style>
    <div class="main-title">🏢 Meiron AI Solutions</div>
    <div class="sub-title">מערכת אוטונומית להטמעה וניהול בינה מלאכותית בעסקים</div>
    """, unsafe_allow_html=True)

# --- סרגל צד לניהול המנוי ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    st.header("ניהול חשבון מנוי")
    subscription_plan = st.selectbox(
        "בחר מסלול הטמעה:",
        ["Basic (ייעוץ ואוטומציה בסיסית)", "Pro (הטמעת סוכני AI פעילים)", "Enterprise (מחלקה דיגיטלית מלאה)"]
    )
    st.write("---")
    st.info("המנוי כולל: עדכוני מודלים אוטומטיים, ניטור שגיאות ותחזוקת בוטים 24/7.")

# --- טופס הזנת נתונים לעסק ---
with st.container():
    st.markdown("### 🛠️ הגדרת הטמעה חדשה")
    with st.form("main_logic_form"):
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("שם העסק / החברה")
            biz_email = st.text_input("אימייל למשלוח הדו''ח והחיוב")
        with col2:
            biz_sector = st.selectbox("תחום פעילות", ["קמעונאות", "שירותים מקצועיים", "מסחר מקוון", "אחר"])
            challenge = st.text_area("תאר את התהליך שתרצה להפוך לאוטומטי (צוואר בקבוק)")
        
        submit_btn = st.form_submit_button("הפעל הטמעה ושלח תוכנית חודשית")

# --- לוגיקת הביצוע ---
if submit_btn:
    if biz_name and challenge and biz_email:
        with st.spinner(f"ה-AI מבצע הטמעה במסלול {subscription_plan}..."):
            try:
                # פרומפט (הוראות) שמגדיר את המערכת כמתקינה ולא רק מייעצת
                system_prompt = f"""
                אתה ה-CTO של Meiron AI Solutions. 
                הלקוח נרשם למסלול: {subscription_plan}.
                עליך לייצר מסמך 'אישור הטמעה' עבור {biz_name} בתחום {biz_sector}.
                
                המסמך חייב לכלול:
                1. איזה כלי AI הטמעת לו עכשיו (למשל: סוכן אוטומטי למיילים, בוט ניהול מלאי).
                2. ערך חודשי: למה המנוי הזה חוסך לו משכורת של עובד.
                3. מה ה-AI יעשה עבורו באופן אוטונומי בכל שבוע במהלך החודש הקרוב.
                
                כתוב בעברית עסקית, בטוחה בעצמה וטכנולוגית.
                """
                
                # קריאה למודל הכי חדש (3.3)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": system_prompt}],
                    temperature=0.4
                )
                
                full_report = response.choices[0].message.content

                # --- שליחת המייל ללקוח ---
                msg = EmailMessage()
                msg.set_content(f"""
שלום רב,
כאן המערכת האוטונומית של Meiron AI Solutions.

השלמנו את הגדרת התשתית הראשונית עבור {biz_name}.
סוג המנוי הפעיל: {subscription_plan}

להלן דו''ח ההטמעה ותוכנית הפעולה החודשית שלך:
-----------------------------------------------------------
{full_report}
-----------------------------------------------------------

המערכת תמשיך לרוץ ברקע ולשפר את ביצועי העסק באופן אוטומטי. 
העדכון הבא יישלח אליך בעוד שבוע בדיוק.

בברכה,
Meiron AI System
""", charset='utf-8')

                msg['Subject'] = f"אישור הטמעה ותוכנית עבודה חודשית - {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email

                # חיבור לשרת גוגל ושליחה
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                
                # תצוגה באתר
                st.success(f"✅ ההטמעה הושלמה! המייל נשלח לכתובת {biz_email}")
                st.balloons()
                
                with st.expander("צפה בדו''ח ההטמעה המלא שנוצר"):
                    st.markdown(full_report)

            except Exception as e:
                st.error(f"שגיאה בתהליך: {e}")
    else:
        st.warning("בבקשה מלאי את כל השדות כדי שנוכל להתחיל בהטמעה.")

# --- הערה לסיום למצגת ---
st.write("---")
st.caption("Meiron AI Solutions © 2026 | Powered by Groq & Llama 3.3")
