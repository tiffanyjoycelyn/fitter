import streamlit as st
import tensorflow as tf
import os
from PIL import Image
import numpy as np
import  keras.utils as utils
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import io

model = tf.keras.models.load_model('exported_model')
arrKey = np.array(["ayam", "daging_rendang", "dendeng_batokok", "gulai_ikan", "gulai_tambusu", "telur_balado", "telur_dadar", "tahu", "daun_singkong", "perkedel", "nasi", "tempe", "telur_mata_sapi", "mie", "udang"])
le2 = LabelEncoder()
arrKey = le2.fit_transform(arrKey)

def make_prediction(image_array):

    prediction = model.predict(image_array)
    prediction = le2.inverse_transform([np.argmax(prediction)])
    return prediction

def load_image(uploaded_file):
    return io.BytesIO(uploaded_file.read())

def main ():
    st.title('TensorFlow Model Prediction from Random Image Sample')
    uploadFile = st.file_uploader(label = "upload image", type = ['jpg', 'jpeg', 'png', 'webp'])

    if st.button('test prediction'):
        if uploadFile is not None:
            image = load_image(uploadFile)
            x = utils.load_img(image, target_size = (110, 110))
            x = utils.img_to_array(x)
            x = x.reshape(1, 110, 110, 3)/255
        prediction = make_prediction(x)
        st.image(Image.open(image))
        st.write(prediction)
        
if __name__ == '__main__':
    main()