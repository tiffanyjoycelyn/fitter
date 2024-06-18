import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
from database import connect_db, save_prediction_log_db  # Import the database functions

def save_prediction_log(session_state, conn, predicted_class, nutrition_facts, servings):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session_state['username']
    log_entry = {
        'username': username,
        'timestamp': timestamp,
        'predicted_class': predicted_class,
        'servings': servings,
        'calories': nutrition_facts['Calories'],
        'protein': nutrition_facts['Protein (g)'],
        'carbohydrates': nutrition_facts['Carbohydrate (g)'],
        'fat': nutrition_facts['Fat (g)'],
        'nutrition_facts': nutrition_facts  # Store the entire nutrition facts dictionary
    }
    st.session_state['prediction_log'].append(log_entry)
    save_prediction_log_db(conn, log_entry)  # Save to the database

def prediction_page():
    conn = connect_db()  # Connect to the database
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

        st.write(f'Prediction: {predicted_class}')
        st.write('Nutrition facts (per 100 grams):')
        st.write(nutrition_facts[predicted_class])

        servings = st.number_input("Enter the number of servings (1 serving = 100 grams):", min_value=1, step=1)

        if servings > 0:
            # Adjust nutrition facts based on servings
            nutrition_facts_servings = {k: v * servings for k, v in nutrition_facts[predicted_class].items()}
            st.write('Adjusted Nutrition facts:')
            st.write(nutrition_facts_servings)

            if st.button("Save Prediction to Log"):
                save_prediction_log(st.session_state, conn, predicted_class, nutrition_facts_servings, servings)
                st.success("Prediction saved to log.")
