import streamlit as st
import tensorflow as tf
import os
import random
from PIL import Image
import numpy as np
import numpy as np
from keras.utils import to_categorical

from sklearn.preprocessing import LabelEncoder

# Load the TensorFlow model
model = tf.keras.models.load_model('exported_model')
arrKey = np.array(["ayam", "daging_rendang", "dendeng_batokok", "gulai_ikan", "gulai_tambusu", "telur_bbalado", "telur_dadar", "tahu", "daun_singkong", "perkedel", "nasi", "tempe", "telur_mata_sapi", "mie", "udang"])
le2 = LabelEncoder()
arrKey = le2.fit_transform(arrKey)
arrKey = to_categorical(arrKey, num_classes=len(np.unique(arrKey)))
#ini buat revert dari array ke label asli


# Function to load a random image from the dataset folder
# def load_random_image(folder_path):
#     image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
#     files = [f for f in os.listdir(folder_path) if any(f.endswith(ext) for ext in image_extensions)]
    
#     if not files:
#         raise ValueError("No image files found in the specified directory.")
    
#     random_file = random.choice(files)
#     image_path = os.path.join(folder_path, random_file)
    
#     return Image.open(image_path)

# dataset_folder = "D:\\AOL_ML\\fitter\\datasets"
# random_image = load_random_image(dataset_folder)
# random_image.show()  # This will open the image using the default image viewer

try:
    random_image = load_random_image(dataset_folder)
    random_image.show()
except Exception as e:
    print(f"An error occurred: {e}")

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

    prediction = model.predict(image_array)
    prediction = le2.inverse_transform([np.argmax(prediction)])
    return prediction

# Set up the Streamlit app
def main ():
    st.title('TensorFlow Model Prediction from Random Image Sample')

# Folder path for the dataset
    dataset_folder = r'D:\AOL_ML\fitter\dataset'

# Button to load a random sample
    if st.button('Load Random Sample'):
        if random_image is not None:
            st.image(random_image, caption='Random Sample Image', use_column_width=True)
            target_size = (101,101) 
            prediction = make_prediction(image_array)
            # Display the prediction
            st.write('Prediction:')
            st.write(prediction)

if __name__ == '__main__':
    main()
