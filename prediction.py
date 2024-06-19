import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
import io
from datetime import datetime
from database import connect_db, save_prediction_log_db

def load_image(uploaded_file):
    return io.BytesIO(uploaded_file.read())

def prediction_page():
    st.subheader("Upload Image for Prediction")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        img_array = np.array(image.resize((110, 110))) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        with st.spinner('Predicting...'):
            model = tf.keras.models.load_model('exported_model')
            arrKey = ["ayam", "daging_rendang", "dendeng_batokok", "gulai_ikan", "gulai_tambusu", "telur_balado",
                      "telur_dadar", "tahu", "daun_singkong", "perkedel", "nasi", "tempe", "telur_mata_sapi",
                      "mie", "udang"]
            le2 = LabelEncoder()
            le2.fit(arrKey)

            predictions = model.predict(img_array)
            predicted_class = le2.inverse_transform([np.argmax(predictions)])[0]

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

        st.write(f"**Predicted Class:** {predicted_class}")
        st.write("**Nutritional Facts per 100 grams:**")
        st.write(nutrition_facts[predicted_class])

        servings = st.number_input("Number of servings (1 serving = 100 grams)", min_value=1, step=1)
        
        nutrition_per_serving = nutrition_facts[predicted_class]
        nutrition_total = {
            "Calories": nutrition_per_serving["Calories"] * servings,
            "Carbohydrate (g)": nutrition_per_serving["Carbohydrate (g)"] * servings,
            "Protein (g)": nutrition_per_serving["Protein (g)"] * servings,
            "Fat (g)": nutrition_per_serving["Fat (g)"] * servings
        }

        st.write(f"**Nutritional Facts for {servings} serving(s):**")
        st.write(nutrition_total)

        save_to_log = st.button("Save Prediction to Log")

        if save_to_log:
            log_entry = {
                "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Predicted Class": predicted_class,
                "Servings": servings,
                "Nutrition Facts": nutrition_total
            }
            if 'prediction_log' not in st.session_state:
                st.session_state.prediction_log = []
            st.session_state.prediction_log.append(log_entry)
            st.write("Prediction saved to log.")

            # Save to database
            log_entry_db = {
                "username": st.session_state['username'],
                "timestamp": log_entry['Timestamp'],
                "predicted_class": log_entry['Predicted Class'],
                "servings": log_entry['Servings'],
                "calories": nutrition_total['Calories'],
                "protein": nutrition_total['Protein (g)'],
                "carbohydrates": nutrition_total['Carbohydrate (g)'],
                "fat": nutrition_total['Fat (g)']
            }
            conn = connect_db()
            save_prediction_log_db(conn, log_entry_db)
            conn.close()
