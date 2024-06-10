import streamlit as st
import tensorflow as tf
import os
from PIL import Image
import numpy as np
import  keras.utils as utils
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import io
import pandas as  pd

USER_DATA = {
    "tes": "tes",
    "alin": "alin"
}

if "login_status" not in st.session_state:
    st.session_state["login_status"] = False

def login(username, password):
    if USER_DATA.get(username) == password:
        st.session_state["login_status"] = True
        st.session_state["username"] = username
        st.experimental_rerun()
        return True
    else:
        st.session_state["login_status"] = False
        st.experimental_rerun()
        return False

def logout():
    st.session_state["login_status"] = False
    st.session_state.pop("username", None)

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

def make_prediction(image_array):
    prediction = model.predict(image_array)
    predicted_class = le2.inverse_transform([np.argmax(prediction)])[0]
    return predicted_class

def load_image(uploaded_file):
    return io.BytesIO(uploaded_file.read())

def main():
    if not st.session_state["login_status"]:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password")
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()
            st.experimental_rerun()
        st.title('TensorFlow Model Prediction from Random Image Sample')
        uploadFile = st.file_uploader(label="Upload Image", type=['jpg', 'jpeg', 'png', 'webp'])

        if uploadFile is not None:
            if st.button('Test Prediction'):
                image = load_image(uploadFile)
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

if __name__ == '__main__':
    main()
