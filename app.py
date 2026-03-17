# --- עמוד 2: בחירת אופציות, מחירים ותשלום ---
elif st.session_state.page == 'options':
    st.markdown("<h2 style='text-align: center;'>💳 בחירת מסלול מנוי חודשי</h2>", unsafe_allow_html=True)
    st.write("כל מסלול כולל הטמעה מלאה ותחזוקה שוטפת של מערכות ה-AI בעסק שלך.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### Basic")
        st.markdown("**250₪ / לחודש**")
        st.write("* ייעוץ אסטרטגי חודשי")
        st.write("* אוטומציית מיילים בסיסית")
        if st.button("בחר Basic 💳"):
            st.session_state.plan = "Basic"
            st.session_state.price = "250"
            go_to('payment') # עובר לעמוד תשלום דמה
            
    with col2:
        st.success("### Pro ⭐")
        st.markdown("**750₪ / לחודש**")
        st.write("* 3 סוכני AI פעילים")
        st.write("* ניתוח נתונים שבועי")
        if st.button("בחר Pro 💳"):
            st.session_state.plan = "Pro"
            st.session_state.price = "750"
            go_to('payment')
            
    with col3:
        st.warning("### Enterprise")
        st.markdown("**2,500₪ / לחודש**")
        st.write("* ניהול AI מלא לעסק")
        st.write("* פיתוח כלים מותאמים אישית")
        if st.button("בחר Enterprise 💳"):
            st.session_state.plan = "Enterprise"
            st.session_state.price = "2,500"
            go_to('payment')
