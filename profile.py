import streamlit as st
from database import load_profile, save_profile

def profile_page(conn):
    st.subheader("User Profile")
    
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
    
    if st.session_state.profile_data is None:
        st.write("Please fill out your profile information.")
        name = st.text_input("Name")
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        lifestyle = st.radio("Lifestyle", ("Idle", "Light", "Moderate", "Active", "Athletic"))
        
        if st.button("Save Profile"):
            st.session_state.profile_data = {
                "name": name,
                "weight": weight,
                "height": height,
                "lifestyle": lifestyle
            }
            st.success("Profile saved successfully!")
    else:
        profile_data = st.session_state.profile_data
        if st.checkbox("Show profile information"):
            st.write("You can edit your profile information below.")
            name = st.text_input("Name", value=profile_data["name"])
            weight = st.number_input("Weight (kg)", min_value=1.0, value=profile_data["weight"], step=0.1)
            height = st.number_input("Height (cm)", min_value=1.0, value=profile_data["height"], step=0.1)
            lifestyle = st.radio("Lifestyle", ("Idle", "Light", "Moderate", "Active", "Athletic"), index=["Idle", "Light", "Moderate", "Active", "Athletic"].index(profile_data["lifestyle"]))
            
            if st.button("Save Profile"):
                st.session_state.profile_data = {
                    "name": name,
                    "weight": weight,
                    "height": height,
                    "lifestyle": lifestyle
                }
                st.success("Profile updated successfully!")
        
        if st.session_state.profile_data:
            profile_summary()

def profile_summary():
    profile_data = st.session_state.profile_data
    weight = profile_data["weight"]
    height = profile_data["height"]
    bmi = weight / ((height / 100) ** 2)
    
    if bmi < 18.5:
        bmi_classification = "Underweight"
    elif 18.5 <= bmi < 24.9:
        bmi_classification = "Normal weight"
    elif 25 <= bmi < 29.9:
        bmi_classification = "Overweight"
    else:
        bmi_classification = "Obesity"
    
    lifestyle_factor = {
        "Idle": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Athletic": 1.9
    }[profile_data["lifestyle"]]
    
    bmr = 10 * weight + 6.25 * height - 5 * 25 + 5  # Simplified BMR for a 25-year-old male
    calories_per_day = bmr * lifestyle_factor
    protein_per_day = weight * 1.2
    carbs_per_day = calories_per_day * 0.55 / 4
    fat_per_day = calories_per_day * 0.3 / 9
    
    st.subheader(f"Profile Summary for {profile_data['name']}")
    st.markdown(f"**BMI**: {bmi:.2f} ({bmi_classification})")
    st.markdown(f"**Calories per day**: {calories_per_day:.2f}")
    st.markdown(f"**Protein per day**: {protein_per_day:.2f} grams")
    st.markdown(f"**Carbohydrates per day**: {carbs_per_day:.2f} grams")
    st.markdown(f"**Fat per day**: {fat_per_day:.2f} grams")
    
    st.subheader("Health Classification")
    if bmi_classification == "Underweight":
        st.write("You are considered underweight. It is important to eat a balanced diet and maintain a healthy lifestyle.")
    elif bmi_classification == "Normal weight":
        st.write("You are considered to have a normal weight. Keep up the good work maintaining a healthy lifestyle!")
    elif bmi_classification == "Overweight":
        st.write("You are considered overweight. It is important to watch your diet and exercise regularly.")
    else:
        st.write("You are considered obese. It is important to seek advice from healthcare professionals to manage your weight.")
