import streamlit as st
import tensorflow as tf
import os
import random
from PIL import Image
import numpy as np

# Load the TensorFlow model
model = tf.keras.models.load_model('exported_model')

# Function to load a random image from the dataset folder
def load_random_image(folder_path):
    # List all image files in the dataset folder (e.g., JPEG, PNG)
    image_extensions = ['.png', '.jpg', '.jpeg']
    files = [f for f in os.listdir(folder_path) if any(f.endswith(ext) for ext in image_extensions)]
    if not files:
        st.error("No image files found in the dataset folder.")
        return None
    # Select a random file
    random_file = random.choice(files)
    # Load the image
    image = Image.open(os.path.join(folder_path, random_file))
    return image

# Function to preprocess the image for the model
def preprocess_image(image, target_size):
    # Resize the image to the target size
    image = image.resize(target_size)
    # Convert the image to a numpy array
    image_array = np.array(image)
    # Normalize the image array
    image_array = image_array / 255.0
    # Expand dimensions to match the model input shape
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# Function to make predictions
def make_prediction(image_array):
    # Use the model to make a prediction
    prediction = model.predict(image_array)
    return prediction

# Set up the Streamlit app
st.title('TensorFlow Model Prediction from Random Image Sample')

# Folder path for the dataset
dataset_folder = r'D:\AOL_ML\fitter\mi'

# Button to load a random sample
if st.button('Load Random Sample'):
    # Load a random image from the dataset folder
    random_image = load_random_image(dataset_folder)
    if random_image is not None:
        # Display the image
        st.image(random_image, caption='Random Sample Image', use_column_width=True)
        # Preprocess the image
        target_size = (101,101)  # Adjust this to match your model's input size
        image_array = preprocess_image(random_image, target_size)
        # Make a prediction using the image
        prediction = make_prediction(image_array)
        # Display the prediction
        st.write('Prediction:')
        st.write(prediction)
