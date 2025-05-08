import streamlit as st
import requests
from PIL import Image
import io

st.title("Brain Tumor Classification")
st.write("Upload MRI images for model to classify the tumor.")
uploaded_files = st.file_uploader("Select the file", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    files = [("files", (file.name, file, file.type)) for file in uploaded_files]
    if st.button("Send"):
        with st.spinner("Model is processing..."):
            response = requests.post("http://localhost:8000/predict", files=files)
            result = response.json()

        st.success("Finish!")
        for file, pred in zip(uploaded_files, result["results"]):
            st.image(file, caption=f"Prediction: {pred['prediction']}", use_column_width=True)