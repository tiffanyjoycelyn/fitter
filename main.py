import streamlit as st
import base64
import time
from auth import login_user, register_user, logout, splash_screen
from database import connect_db, create_tables
from profile import profile_page
from prediction import prediction_page

def main():
    conn = connect_db()
    create_tables(conn)

    if st.session_state["show_splash"]:
        splash_screen()
    else:
        if not st.session_state["login_status"]:
            if st.session_state["page"] == "login":
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    if login_user(conn, username, password):
                        st.session_state["login_status"] = True
                        st.session_state["username"] = username
                        st.success(f"Logged in as {username}")
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")
                if st.button("New user? Register here"):
                    st.session_state["page"] = "register"
                    st.experimental_rerun()
            elif st.session_state["page"] == "register":
                st.subheader("Register")
                with st.form("registration_form"):
                    reg_username = st.text_input("Register Username")
                    reg_password = st.text_input("Register Password", type="password")
                    submitted = st.form_submit_button("Register")
                    if submitted:
                        register_user(conn, reg_username, reg_password)
                        st.success("User registered successfully!")
                        st.experimental_rerun()
                if st.button("Already have an account? Login here"):
                    st.session_state["page"] = "login"
                    st.experimental_rerun()
        else:
            st.sidebar.title(f"HI! Welcome, {st.session_state['username']}")
            if st.sidebar.button("Profile"):
                st.session_state["page"] = "profile"
                st.experimental_rerun()
            
            if st.sidebar.button('Predict - Upload Image'):
                st.session_state["page"] = "predict"
                st.experimental_rerun()

            if st.session_state["page"] == "profile":
                profile_page(conn)
            elif st.session_state["page"] == "predict":
                prediction_page()

            if st.sidebar.button("Log Out"):
                conn.commit()
                conn.close()
                logout()

if __name__ == '__main__':
    if "login_status" not in st.session_state:
        st.session_state["login_status"] = False

    if "show_splash" not in st.session_state:
        st.session_state["show_splash"] = True

    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    with open("fitter_logo.png", "rb") as image_file:
        st.session_state["logo_base64"] = base64.b64encode(image_file.read()).decode("utf-8")

    main()
