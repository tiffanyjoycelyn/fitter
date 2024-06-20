import streamlit as st
from database import connect_db, calculate_remaining_nutrition, load_profile

def prediction_log_page():
    if 'prediction_log' not in st.session_state:
        st.session_state['prediction_log'] = []

    if 'username' not in st.session_state or st.session_state['username'] is None:
        st.write("Please log in to view your prediction logs.")
        return

    conn = connect_db()
    profile_data = load_profile(conn, st.session_state['username'])
    st.write("Loaded profile data:", profile_data)

    if profile_data is None:
        st.write("Please complete your profile information first.")
        return

    st.subheader("Prediction Log")

    total_calories = 0
    total_carbohydrates = 0
    total_protein = 0
    total_fat = 0

    for entry in st.session_state['prediction_log']:
        nutrition = entry.get('Nutrition Facts', {}) 
        total_calories += nutrition.get('Calories', 0)
        total_carbohydrates += nutrition.get('Carbohydrate (g)', 0)
        total_protein += nutrition.get('Protein (g)', 0)
        total_fat += nutrition.get('Fat (g)', 0)

    show_logs = st.checkbox("Show Prediction Logs")

    if show_logs:
        if st.session_state['prediction_log']:
            for entry in st.session_state['prediction_log']:
                st.write(f"**Timestamp:** {entry['Timestamp']}")
                st.write(f"**Predicted Class:** {entry['Predicted Class']}")
                servings = entry.get('Servings', 'N/A')
                st.write(f"**Servings:** {servings}")
                st.write(f"**Nutrition Facts:**")
                st.write(entry['Nutrition Facts'])
                st.write("---")
        else:
            st.write("No predictions logged yet.")

    st.subheader("Total Nutritional Intake from Logs")
    st.write(f"**Total Calories:** {total_calories} kcal")
    st.write(f"**Total Carbohydrates:** {total_carbohydrates} g")
    st.write(f"**Total Protein:** {total_protein} g")
    st.write(f"**Total Fat:** {total_fat} g")
    
    remaining_calories, remaining_protein, remaining_carbs, remaining_fat = calculate_remaining_nutrition(conn, st.session_state['username'], profile_data)

    st.subheader("Remaining Nutritional Intake for Today")
    st.write(f"**Remaining Calories:** {profile_data['calories'] - total_calories:.2f} kcal")
    st.write(f"**Remaining Protein:** {profile_data['protein'] - total_protein:.2f} g")
    st.write(f"**Remaining Carbohydrates:** {profile_data['carbs'] - total_carbohydrates:.2f} g")
    st.write(f"**Remaining Fat:** {profile_data['fat'] - total_fat:.2f} g")

    exceeded_nutrients = []
    additional_info = []
    if total_calories > profile_data['calories']:
        exceeded_nutrients.append(f"Calories by {total_calories - profile_data['calories']:.2f} kcal")
    if total_carbohydrates > profile_data['carbs']:
        exceeded_nutrients.append(f"Carbohydrates by {total_carbohydrates - profile_data['carbs']:.2f} g")
        additional_info.append("Excessive carbohydrate intake can lead to weight gain, increased risk of diabetes, and heart disease.")
    if total_protein > profile_data['protein']:
        exceeded_nutrients.append(f"Protein by {total_protein - profile_data['protein']:.2f} g")
        additional_info.append("Excessive protein intake can cause kidney strain and other health issues.")
    if total_fat > profile_data['fat']:
        exceeded_nutrients.append(f"Fat by {total_fat - profile_data['fat']:.2f} g")
        additional_info.append("Too much fat can lead to weight gain and increase the risk of heart disease.")

    if exceeded_nutrients:
        st.warning("You have exceeded your daily nutritional limits for the following:\n" + "\n".join(exceeded_nutrients))
        st.subheader("Health Implications of Exceeding Nutrient Limits")
        for info in additional_info:
            st.write(f"- {info}")
    else:
        st.success("You are within your daily nutritional limits. Keep up the good work!")

