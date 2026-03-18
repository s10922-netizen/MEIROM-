# ... (כל הקוד הקודם נשאר אותו דבר, הוספתי רק את החלק הזה בתפריט הניווט)

    elif page == "🤖 צ'אטבוט לקוחות":
        st.header("🤖 סימולציית צ'אט (לבעל העסק)")
        # (הקוד של הצ'אט שכבר יש לך...)

    elif page == "🌐 תצוגת לקוח סופית (דף חיצוני)":
        # דף נקי לגמרי בלי סרגל צד ובלי בלאגן
        st.markdown(f"<h1 style='text-align:center; color:#7c3aed;'>{st.session_state.get('biz_name', 'העסק שלי')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>{st.session_state.biz_info}</p>", unsafe_allow_html=True)
        st.divider()
        
        st.subheader("צ'אט עם העוזר האישי שלנו ✨")
        customer_input = st.chat_input("שלום! במה אפשר לעזור?")
        if customer_input:
            st.chat_message("user").write(customer_input)
            prompt = f"Assistant for: {st.session_state.biz_info}. Answer: {customer_input}. Hebrew."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.chat_message("assistant").write(res.choices[0].message.content)
            
        st.divider()
        st.subheader("קביעת תור מהירה 📅")
        col1, col2 = st.columns(2)
        with col1: st.date_input("בחר יום", key="cust_date")
        with col2: st.time_input("בחר שעה", key="cust_time")
        if st.button("תזמינו לי מקום! 🚀"):
            st.balloons()
            st.success("הבקשה נשלחה לבעל העסק! נשלח לך אישור בוואטסאפ בקרוב.")
