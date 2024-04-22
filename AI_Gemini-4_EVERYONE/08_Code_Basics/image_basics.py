import os
from io import BytesIO
 
import requests
import streamlit as st
from PIL import Image
from openai import OpenAI
 
# from apikey import apikey
 
 
############################################
# OpenAI API setup
############################################
 
def setup_openai(apikey):
    # Set up OpenAI API key
    os.environ['OPENAI_API_KEY'] = apikey
    OpenAI.api_key = apikey
    client = OpenAI()
    return client

############################################
# OpenAI Image Generation
############################################
def generate_image_openai(client, prompt, model="dall-e-2", size="1024x1024", n=1):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        n=n,
    )
    image_url = response.data[0].url
    image = requests.get(image_url)
    image = Image.open(BytesIO(image.content))
    return image

def main():
    pass

apikey = "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"  # Replace "your_api_key_here" with your actual API key
client = setup_openai(apikey)
# Image Generation ####
st.title("Image Generation using OpenAI API")
prompt = st.text_input("Enter your prompt", value="A cute cat jumping over a fence, cartoon, colorful")
if st.button("Generate Image"):
    with st.spinner('Generating image...'):
        image = generate_image_openai( client , prompt)
        st.image(image)