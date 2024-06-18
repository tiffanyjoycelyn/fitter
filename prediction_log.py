import streamlit as st

def prediction_log_page():
    if 'prediction_log' not in st.session_state:
        st.session_state['prediction_log'] = []

    st.subheader("Prediction Log")

    total_calories = 0
    total_carbohydrates = 0
    total_protein = 0
    total_fat = 0

    for entry in st.session_state['prediction_log']:
        nutrition = entry['Nutrition Facts']
        total_calories += nutrition['Calories']
        total_carbohydrates += nutrition['Carbohydrate (g)']
        total_protein += nutrition['Protein (g)']
        total_fat += nutrition['Fat (g)']

    show_logs = st.checkbox("Show Prediction Logs")

    if show_logs:
        if st.session_state['prediction_log']:
            for entry in st.session_state['prediction_log']:
                st.write(f"**Timestamp:** {entry['Timestamp']}")
                st.write(f"**Predicted Class:** {entry['Predicted Class']}")
                st.write(f"**Nutrition Facts:**")
                st.write(entry['Nutrition Facts'])
                st.write("---")
        else:
            st.write("No predictions logged yet.")

    st.subheader("Total Nutritional Intake")
    st.write(f"**Total Calories:** {total_calories} kcal")
    st.write(f"**Total Carbohydrates:** {total_carbohydrates} g")
    st.write(f"**Total Protein:** {total_protein} g")
    st.write(f"**Total Fat:** {total_fat} g")

