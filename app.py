import streamlit as st
import requests

# עיצוב בסיסי
st.markdown("<h1 style='text-align:center; color:#7c3aed;'>Meirom Magic AI 🚀</h1>", unsafe_allow_html=True)

# קלט
mail = st.text_input("אימייל להרשמה")
pwd = st.text_input("בחרי סיסמה", type="password")

if st.button("צרי חשבון ✨"):
    if mail and pwd:
        # הקישור הישיר של הטופס שלך
        url = "https://docs.google.com/forms/d/e/1FAIpQLSdWPISX09Kj4Z2oQFSC6smC5KtXm1iVvSrc_5nxvvsFx6hX7Q/formResponse"
        
        # נתונים לשליחה
        payload = {
            "entry.855862094": mail,
            "entry.1847739029": pwd
        }
        
        try:
            # שליחה
            response = requests.post(url, data=payload)
            
            # בגלל שזה גוגל פורמס, גם אם הוא מחזיר דף אישור זה נחשב הצלחה
            st.balloons()
            st.success("זה עבד! הנתונים נשלחו.")
            st.info("מנכ\"לית, בדקי עכשיו את ה-Google Sheet שלך - השורה שם!")
            
        except Exception as e:
            st.error(f"תקלה קטנה: {e}")
    else:
        st.warning("נא למלא את כל השדות")
