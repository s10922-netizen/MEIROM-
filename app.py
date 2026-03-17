import streamlit as st
from groq import Groq
import smtplib
from email.message import EmailMessage
import time

# --- חיבור ל-AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_KEY"])
except:
    st.error("Missing GROQ_KEY in Secrets!")

# --- הגדרות אימייל ---
MY_EMAIL = "meiromp10@gmail.com"
APP_PASSWORD = "cyty rvau owas uaeg"

# --- ניהול ניווט ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'plan' not in st.session_state: st.session_state.plan = None
if 'price' not in st.session_state: st.session_state.price = "0"
if 'report' not in st.session_state: st.session_state.report = None

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- עיצוב CSS יוקרתי (Dark Mode & Glassmorphism) ---
st.set_page_config(page_title="Meirom AI | Enterprise", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* רקע כללי כהה */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* עיצוב כפתורים */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }

    /* כרטיסי מחיר עם אפקט זכוכית */
    .price-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .price-card:hover {
        transform: scale(1.05);
        border-color: #3b82f6;
    }

    /* תיבת תשלום */
    .payment-container {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid #3b82f6;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
    }
    
    /* כותרות */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* תיבות טקסט */
    input, textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- עמוד 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown("<div style='text-align: center; padding-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 4rem; font-weight: 900; letter-spacing: -1px;'>MEIROM <span style='color: #3b82f6;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.5rem; opacity: 0.8;'>Next-Gen Autonomous Business Integration</p>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/6159/6159448.png", width=220) # אייקון הייטקי יותר
    st.write("")
    if st.button("Get Started 🚀", use_container_width=True):
        go_to('options')
    st.markdown("</div>", unsafe_allow_html=True)

# --- עמוד 2: Options ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>Select Your Growth Plan</h2>", unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="price-card"><h4>Basic</h4><h2 style="color:#3b82f6;">₪250</h2><p>AI Consulting</p></div>', unsafe_allow_html=True)
        if st.button("Choose Basic"):
            st.session_state.plan = "Basic"; st.session_state.price = "250"; go_to('payment')
            
    with col2:
        st.markdown('<div class="price-card" style="border: 2px solid #3b82f6;"><h4>Pro ⭐</h4><h2 style="color:#3b82f6;">₪750</h2><p>Active AI Agents</p></div>', unsafe_allow_html=True)
        if st.button("Choose Pro"):
            st.session_state.plan = "Pro"; st.session_state.price = "750"; go_to('payment')
            
    with col3:
        st.markdown('<div class="price-card"><h4>Enterprise</h4><h2 style="color:#3b82f6;">₪2,500</h2><p>Full AI Management</p></div>', unsafe_allow_html=True)
        if st.button("Choose Enterprise"):
            st.session_state.plan = "Enterprise"; st.session_state.price = "2,500"; go_to('payment')

# --- עמוד 3: Payment ---
elif st.session_state.page == 'payment':
    st.markdown("<div class='payment-container'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Secure Checkout: {st.session_state.plan}</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; opacity:0.7;'>Total: ₪{st.session_state.price}/mo</p>", unsafe_allow_html=True)
    
    num = st.text_input("Card Number", placeholder="xxxx xxxx xxxx xxxx")
    c1, c2 = st.columns(2)
    with c1: st.text_input("Expiry", placeholder="MM/YY")
    with c2: st.text_input("CVV", placeholder="***")
    
    if st.button("Complete Purchase ✅"):
        with st.spinner("Processing..."):
            time.sleep(1.5)
        st.success("Authorized!")
        go_to('main')
    st.markdown("</div>", unsafe_allow_html=True)

# --- עמוד 4: Main & AI ---
elif st.session_state.page == 'main':
    st.markdown(f"<h1>System Terminal: <span style='color:#3b82f6;'>{st.session_state.plan}</span></h1>", unsafe_allow_html=True)
    
    with st.container():
        biz_name = st.text_input("Business Name")
        biz_email = st.text_input("Client Email")
        challenge = st.text_area("Operational Challenge")
        submit = st.form_submit_button("Execute AI Agent ⚡") if 'form' not in locals() else st.button("Execute AI Agent ⚡")

    if submit and biz_name and challenge and biz_email:
        with st.status("Analyzing business architecture...", expanded=True) as status:
            # AI Logic
            prompt = f"Write a high-level AI implementation report in HEBREW for {biz_name}. Plan: {st.session_state.plan}. Issue: {challenge}. Format with professional headers."
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            report = response.choices[0].message.content
            st.session_state.report = report
            
            # HTML Email Logic
            try:
                msg = EmailMessage()
                msg['Subject'] = f"Meirom AI | Official Report - {biz_name}"
                msg['From'] = MY_EMAIL
                msg['To'] = biz_email
                
                # יצירת מייל מעוצב ב-HTML
                html_content = f"""
                <div style="font-family: sans-serif; color: #1e293b; max-width: 600px; border: 1px solid #e2e8f0; padding: 20px; border-radius: 10px;">
                    <h1 style="color: #2563eb;">Meirom AI Solutions</h1>
                    <p>שלום <strong>{biz_name}</strong>,</p>
                    <p>הסוכנים שלנו השלימו את ניתוח המערכת עבורכם. להלן עיקרי הדו''ח:</p>
                    <div style="background: #f8fafc; padding: 15px; border-left: 4px solid #2563eb; white-space: pre-wrap;">
                        {report}
                    </div>
                    <p style="margin-top: 20px; font-size: 12px; color: #64748b;">נשלח אוטומטית על ידי Meirom AI Enterprise System</p>
                </div>
                """
                msg.add_alternative(html_content, subtype='html')
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                status.update(label="Analysis complete. Email dispatched. ✅", state="complete")
                st.balloons()
            except Exception as e:
                st.error(f"AI Success, Email Error: {e}")

    if st.session_state.report:
        st.markdown("<div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)
        st.subheader("System Output")
        st.write(st.session_state.report)
        st.download_button("Download Raw Data", data=st.session_state.report, file_name="Meirom_Report.txt")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Reset Terminal"):
        st.session_state.report = None
        go_to('welcome')
