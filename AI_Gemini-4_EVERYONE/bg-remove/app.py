import streamlit as st
import requests

from io import BytesIO

from PIL import Image

# Define remove.bg API endpoint and API key
API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"
API_KEY = "ru3dcXbAyjp8NEd7zjxztghM"  # Replace 'YOUR_API_KEY' with your actual API key

# Streamlit app title
st.title("Background Remover")

# Function to remove background using remove.bg API
def remove_background(image):
    # Open image file
    img = Image.open(image)

    # Create byte buffer to hold image data
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Request headers
    headers = {"X-Api-Key": API_KEY}

    # Request payload
    files = {"image_file": img_buffer}

    # Send POST request to remove.bg API
    response = requests.post(API_ENDPOINT, headers=headers, files=files)

    # Check if request was successful
    if response.status_code == 200:
        # Display the processed image
        st.image(BytesIO(response.content), use_column_width=True)
    else:
        # Display error message
        st.error("Failed to remove background. Please try again.")

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Check if an image is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Check if the 'Remove Background' button is clicked
    if st.button("Remove Background"):
        # Call remove_background function
        remove_background(uploaded_file)