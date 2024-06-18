import streamlit as st

def prediction_log_page():
    if 'prediction_log' not in st.session_state:
        st.session_state['prediction_log'] = []

    st.subheader("Prediction Log")

    # Initialize totals
    total_calories = 0
    total_carbohydrates = 0
    total_protein = 0
    total_fat = 0

    # Calculate totals
    for entry in st.session_state['prediction_log']:
        nutrition = entry['Nutrition Facts']
        total_calories += nutrition['Calories']
        total_carbohydrates += nutrition['Carbohydrate (g)']
        total_protein += nutrition['Protein (g)']
        total_fat += nutrition['Fat (g)']

    # Checkbox to toggle visibility of logs
    show_logs = st.checkbox("Show Prediction Logs")

    if show_logs:
        if st.session_state['prediction_log']:
            for entry in st.session_state['prediction_log']:
                st.write(f"**Timestamp:** {entry['Timestamp']}")
                st.write(f"**Predicted Class:** {entry['Predicted Class']}")
                servings = entry.get('Servings', 'N/A')  # Handle missing 'Servings' key
                st.write(f"**Servings:** {servings}")
                st.write(f"**Nutrition Facts:**")
                st.write(entry['Nutrition Facts'])
                st.write("---")
        else:
            st.write("No predictions logged yet.")

    # Display totals
    st.subheader("Total Nutritional Intake")
    st.write(f"**Total Calories:** {total_calories} kcal")
    st.write(f"**Total Carbohydrates:** {total_carbohydrates} g")
    st.write(f"**Total Protein:** {total_protein} g")
    st.write(f"**Total Fat:** {total_fat} g")
