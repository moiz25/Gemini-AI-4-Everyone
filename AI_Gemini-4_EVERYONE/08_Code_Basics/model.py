import os
import streamlit as st
from openai import OpenAI
from apikey import apikey

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
# OpenAI Audio to Text
############################################

def generate_text_from_audio_openai(client, audio_file,
                                    model="whisper-1", response_format="text"):
    response = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        response_format=response_format
    )
    return response

if __name__ == '__main__':
    st.title("Audio Transcription using OpenAI API")
    audio_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])
    
    if audio_file:
        if st.button("Transcribe"):
            st.audio(audio_file, format='audio/wav')
            with st.spinner('Transcribing audio...'):
                # Assuming `client` is initialized somewhere in your script
                client = setup_openai(apikey)
                result = generate_text_from_audio_openai(client, audio_file)
                st.write(result)
