import streamlit as st

def prediction_log_page():
    if 'prediction_log' not in st.session_state:
        st.session_state['prediction_log'] = []

    st.subheader("Prediction Log")
    if st.session_state['prediction_log']:
        for entry in st.session_state['prediction_log']:
            st.write(f"**Timestamp:** {entry['Timestamp']}")
            st.write(f"**Predicted Class:** {entry['Predicted Class']}")
            st.write(f"**Nutrition Facts:**")
            st.write(entry['Nutrition Facts'])
            st.write("---")
    else:
        st.write("No predictions logged yet.")
