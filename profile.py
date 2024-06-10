import streamlit as st
from database import load_profile, save_profile

def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def calculate_daily_needs(bmi, lifestyle):
    lifestyle_factors = {
        "Idle": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Athletic": 1.9
    }
    factor = lifestyle_factors[lifestyle]
    base_calories = 2000
    calories = base_calories * factor

    protein = (calories * 0.15) / 4
    carbs = (calories * 0.55) / 4
    fat = (calories * 0.30) / 9

    return calories, protein, carbs, fat

def profile_page(conn):
    st.subheader("User Profile")
    username = st.session_state["username"]
    
    profile_data = load_profile(conn, username)
    if profile_data:
        weight, height, lifestyle = profile_data
    else:
        weight, height, lifestyle = None, None, "Idle"

    weight = st.number_input("Weight (kg)", value=weight if weight else 0.0)
    height = st.number_input("Height (cm)", value=height if height else 0.0)
    lifestyle = st.radio("Lifestyle", ("Idle", "Light", "Moderate", "Active", "Athletic"), index=["Idle", "Light", "Moderate", "Active", "Athletic"].index(lifestyle))

    if st.button("Save Profile"):
        bmi = calculate_bmi(weight, height)
        calories, protein, carbs, fat = calculate_daily_needs(bmi, lifestyle)
        save_profile(conn, username, weight, height, lifestyle, bmi, calories, protein, carbs, fat)
        st.success("Profile saved successfully!")
    
    st.subheader("Profile Summary")
    if weight and height:
        bmi = calculate_bmi(weight, height)
        calories, protein, carbs, fat = calculate_daily_needs(bmi, lifestyle)
        st.write(f"BMI: {bmi:.2f}")
        st.write(f"Calories per day: {calories:.2f}")
        st.write(f"Protein per day: {protein:.2f} grams")
        st.write(f"Carbohydrates per day: {carbs:.2f} grams")
        st.write(f"Fat per day: {fat:.2f} grams")
    else:
        st.write("Please complete your profile to see the summary.")
