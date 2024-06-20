import streamlit as st
import time
from database import load_profile, save_profile, connect_db, calculate_remaining_nutrition

def profile_page(conn):
    st.subheader("User Profile")
    
    if 'username' not in st.session_state or st.session_state['username'] is None:
        st.write("Please log in to view and edit your profile.")
        return

    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = load_profile(conn, st.session_state['username'])
        st.write("Loaded profile data:", st.session_state.profile_data)

    if st.session_state.profile_data is None:
        st.write("Please fill out your profile information.")
        name = st.text_input("Name")
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        lifestyle = st.radio("Lifestyle", ("Idle", "Light", "Moderate", "Active", "Athletic"))
        bmi = weight / ((height / 100) ** 2)
        bmi_classification = classify_bmi(bmi)

        lifestyle_factor = {
            "Idle": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Athletic": 1.9
        }[lifestyle]

        bmr = 10 * weight + 6.25 * height - 5 * 25 + 5
        calories_per_day = bmr * lifestyle_factor
        protein_per_day = weight * 1.2
        carbs_per_day = calories_per_day * 0.55 / 4
        fat_per_day = calories_per_day * 0.3 / 9

        if st.button("Save Profile"):
            with st.spinner("Updating profile..."):
                st.session_state.profile_data = {
                    "username": st.session_state['username'],
                    "name": name,
                    "weight": weight,
                    "height": height,
                    "lifestyle": lifestyle,
                    "bmi": bmi,
                    "calories": calories_per_day,
                    "protein": protein_per_day,
                    "carbs": carbs_per_day,
                    "fat": fat_per_day,
                    "bmi_classification": bmi_classification,
                }
                save_profile(conn, st.session_state.profile_data)
                st.write("Saved profile data:", st.session_state.profile_data)
                time.sleep(2)
            st.success("Profile saved successfully!")
            st.experimental_rerun()
    else:
        profile_data = st.session_state.profile_data
        profile_data.setdefault("name", "")
        profile_data.setdefault("weight", 0)
        profile_data.setdefault("height", 0)
        profile_data.setdefault("lifestyle", "Idle")
        profile_data.setdefault("bmi", 0)
        profile_data.setdefault("calories", 0)
        profile_data.setdefault("protein", 0)
        profile_data.setdefault("carbs", 0)
        profile_data.setdefault("fat", 0)
        profile_data.setdefault("bmi_classification", "Normal weight")
        if st.checkbox("Show profile information"):
            show_profile_info(profile_data)

        if st.checkbox("Edit profile information"):
            name = st.text_input("Name", value=profile_data["username"])
            weight = st.number_input("Weight (kg)", min_value=1.0, value=profile_data["weight"], step=0.1)
            height = st.number_input("Height (cm)", min_value=1.0, value=profile_data["height"], step=0.1)
            lifestyle = st.radio("Lifestyle", ("Idle", "Light", "Moderate", "Active", "Athletic"), index=["Idle", "Light", "Moderate", "Active", "Athletic"].index(profile_data["lifestyle"]))
            bmi = weight / ((height / 100) ** 2)
            bmi_classification = classify_bmi(bmi)

            lifestyle_factor = {
                "Idle": 1.2,
                "Light": 1.375,
                "Moderate": 1.55,
                "Active": 1.725,
                "Athletic": 1.9
            }[lifestyle]

            bmr = 10 * weight + 6.25 * height - 5 * 25 + 5
            calories_per_day = bmr * lifestyle_factor
            protein_per_day = weight * 1.2
            carbs_per_day = calories_per_day * 0.55 / 4
            fat_per_day = calories_per_day * 0.3 / 9

            if st.button("Save Profile"):
                with st.spinner("Updating profile..."):
                    st.session_state.profile_data = {
                        "username": st.session_state['username'],
                        "name": name,
                        "weight": weight,
                        "height": height,
                        "lifestyle": lifestyle,
                        "bmi": bmi,
                        "calories": calories_per_day,
                        "protein": protein_per_day,
                        "carbs": carbs_per_day,
                        "fat": fat_per_day,
                        "bmi_classification": bmi_classification,
                    }
                    save_profile(conn, st.session_state.profile_data)
                    st.write("Saved profile data:", st.session_state.profile_data)
                    time.sleep(2)
                st.success("Profile updated successfully!")
                st.experimental_rerun()

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def show_profile_info(profile_data):
    st.subheader(f"Profile Summary for {profile_data['username']}")
    st.markdown(f"**BMI**: {profile_data['bmi']:.2f}")
    st.markdown(f"**Calories per day**: {profile_data['calories']:.2f}")
    st.markdown(f"**Protein per day**: {profile_data['protein']:.2f} grams")
    st.markdown(f"**Carbohydrates per day**: {profile_data['carbs']:.2f} grams")
    st.markdown(f"**Fat per day**: {profile_data['fat']:.2f} grams")

    st.subheader("Health Classification")
    if profile_data['bmi_classification'] == "Underweight":
        st.write("You are considered underweight. It is important to eat a balanced diet and maintain a healthy lifestyle.")
    elif profile_data['bmi_classification'] == "Normal weight":
        st.write("You are considered to have a normal weight. Keep up the good work maintaining a healthy lifestyle!")
    elif profile_data['bmi_classification'] == "Overweight":
        st.write("You are considered overweight. It is important to watch your diet and exercise regularly.")
    else:
        st.write("You are considered obese. It is important to seek advice from healthcare professionals to manage your weight.")
