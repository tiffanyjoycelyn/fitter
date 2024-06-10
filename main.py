import streamlit as st
import tensorflow as tf
import os
from PIL import Image
import numpy as np
import keras.utils as utils
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import io
import pandas as pd
import time
import base64
import bcrypt
import sqlite3

def connect_db():
    conn = sqlite3.connect('user_data.db', check_same_thread=False)
    return conn

def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()

def login_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    return False

def register_user(conn, username, password):
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")

def logout():
    st.session_state["login_status"] = False
    st.session_state.pop("username", None)
    st.experimental_rerun()

def splash_screen():
    st.markdown(
        f"""
        <style>
        .reportview-container .main .block-container{{
            padding-top: 0px;
            padding-right: 0px;
            padding-left: 0px;
            padding-bottom: 0px;
        }}
        .splash-screen {{
            background-color: black;
            color: white;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 9999;
        }}
        .splash-screen h1 {{
            font-size: 3em;
        }}
        .splash-screen img {{
            width: 200px;
        }}
        .splash-screen p {{
            font-size: 1.2em;
        }}
        </style>
        <div class="splash-screen">
            <img src="data:image/png;base64,{st.session_state["logo_base64"]}" alt="fitter logo">
            <h1>Welcome to fitter!</h1>
            <p>Track Your Nutrition</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)
    st.session_state["show_splash"] = False
    st.experimental_rerun()

def make_prediction(image_array):
    prediction = model.predict(image_array)
    predicted_class = le2.inverse_transform([np.argmax(prediction)])[0]
    return predicted_class

def load_image(uploaded_file):
    return io.BytesIO(uploaded_file.read())

def main():
    conn = connect_db()
    create_users_table(conn)

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
            st.title('TensorFlow Model Prediction from Random Image Sample')

            uploadFile = st.sidebar.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png', 'webp'])
            if uploadFile is not None:
                st.session_state["uploaded_file"] = uploadFile

            if "uploaded_file" in st.session_state:
                if st.button('Test Prediction'):
                    image = load_image(st.session_state["uploaded_file"])
                    x = utils.load_img(image, target_size=(110, 110))
                    x = utils.img_to_array(x)
                    x = x.reshape(1, 110, 110, 3) / 255

                    prediction = make_prediction(x)
                    st.image(Image.open(image))
                    st.write(f"Prediction: {prediction}")

                    confidence_score = np.max(model.predict(x))
                    st.write(f"Confidence Score: {confidence_score:.2f}")

                    if confidence_score < 0.85:
                        st.warning("The model's prediction has a low confidence score (below 85%) and may not be reliable.")

                    if prediction in nutrition_facts:
                        st.subheader("Nutrition Facts per 100 gram:")
                        nutrition_df = pd.DataFrame(nutrition_facts[prediction], index=[prediction])
                        st.dataframe(nutrition_df)
                    else:
                        st.write("Nutrition facts not available for this predicted class.")

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

    model = tf.keras.models.load_model('exported_model')
    arrKey = ["ayam", "daging_rendang", "dendeng_batokok", "gulai_ikan", "gulai_tambusu", "telur_balado",
              "telur_dadar", "tahu", "daun_singkong", "perkedel", "nasi", "tempe", "telur_mata_sapi",
              "mie", "udang"]
    le2 = LabelEncoder()
    le2.fit(arrKey)

    nutrition_facts = {
        "ayam": {"Protein (g)": 20, "Fat (g)": 10, "Carbohydrate (g)": 5, "Calories": 250},
        "daging_rendang": {"Protein (g)": 18, "Fat (g)": 15, "Carbohydrate (g)": 3, "Calories": 300},
        "dendeng_batokok": {"Protein (g)": 25, "Fat (g)": 12, "Carbohydrate (g)": 8, "Calories": 280},
        "gulai_ikan": {"Protein (g)": 22, "Fat (g)": 14, "Carbohydrate (g)": 6, "Calories": 270},
        "gulai_tambusu": {"Protein (g)": 19, "Fat (g)": 13, "Carbohydrate (g)": 7, "Calories": 280},
        "telur_balado": {"Protein (g)": 12, "Fat (g)": 9, "Carbohydrate (g)": 4, "Calories": 200},
        "telur_dadar": {"Protein (g)": 15, "Fat (g)": 11, "Carbohydrate (g)": 5, "Calories": 220},
        "tahu": {"Protein (g)": 10, "Fat (g)": 8, "Carbohydrate (g)": 3, "Calories": 180},
        "daun_singkong": {"Protein (g)": 5, "Fat (g)": 3, "Carbohydrate (g)": 2, "Calories": 100},
        "perkedel": {"Protein (g)": 8, "Fat (g)": 6, "Carbohydrate (g)": 4, "Calories": 150},
        "nasi": {"Protein (g)": 2, "Fat (g)": 1, "Carbohydrate (g)": 20, "Calories": 150},
        "tempe": {"Protein (g)": 15, "Fat (g)": 10, "Carbohydrate (g)": 5, "Calories": 250},
        "telur_mata_sapi": {"Protein (g)": 14, "Fat (g)": 9, "Carbohydrate (g)": 6, "Calories": 210},
        "mie": {"Protein (g)": 5, "Fat (g)": 3, "Carbohydrate (g)": 20, "Calories": 200},
        "udang": {"Protein (g)": 20, "Fat (g)": 10, "Carbohydrate (g)": 3, "Calories": 220}
    }

    main()
