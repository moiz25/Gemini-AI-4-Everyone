

import streamlit as st
import requests
import os
import re
import random

# Define Hugging Face API endpoint and your API token
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_TOKEN = {"Authorization": "Bearer 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"}

# Function to query the model and get captions
def get_caption(image_file):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    # Save the uploaded image to a temporary location
    temp_image_path = "temp_image.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(image_file.read())
    
    # Query the model with the temporary image file
    with open(temp_image_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    
    # Delete the temporary image file
    os.remove(temp_image_path)
    
    if response.status_code == 200:
        result = response.json()
        caption = result[0].get("generated_text", "Caption not generated")
        return caption
    else:
        return f"Error generating caption. Status code: {response.status_code}. Response content: {response.content}"

# Function to generate hashtags randomly
def generate_random_hashtags():
    # List of predefined keywords or categories for hashtags
    keywords = ["nature", "travel", "food", "fitness", "art", "music", "technology", "fashion", "photography"]
    # Shuffle the keywords to randomize
    random.shuffle(keywords)
    # Select a random subset of keywords to generate hashtags
    num_hashtags = random.randint(2, 4)  # You can adjust the number of hashtags as needed
    hashtags = ['#' + keyword.lower() for keyword in keywords[:num_hashtags]]
    return hashtags

# Function to generate hashtags from the caption
def generate_hashtags(caption):
    # Extracting keywords from the caption (you can use more sophisticated NLP techniques here)
    keywords = re.findall(r'\b\w{4,}\b', caption)
    # Generating hashtags by adding '#' before each keyword
    hashtags = ['#' + keyword.lower() for keyword in keywords]
    return hashtags

# Streamlit app for image caption generation
def image_caption_app():
    st.title("Image Caption Generator")

    # File uploader for image
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)

        # Generate caption and hashtags on button click
        if st.button("Generate Caption"):
            with st.spinner("Generating caption..."):
                caption = get_caption(image_file)
                hashtags = generate_hashtags(caption)
                random_hashtags = generate_random_hashtags()
            st.success("Caption generated successfully!")
            st.write("Generated Caption:", caption)
            st.write("Generated Hashtags:", " ".join(hashtags + random_hashtags))
def main():
    image_caption_app()

if __name__ == "__main__":
    main()