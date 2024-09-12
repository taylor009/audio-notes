import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_detailed_notes(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using the latest GPT-4 model for better performance
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates very detailed notes from transcriptions."},
            {"role": "user", "content": f"Create very detailed notes from the following transcription, including:\n\n"
                                        "1. A comprehensive overview\n"
                                        "2. Key points and main ideas discussed\n"
                                        "3. Detailed breakdown of each major topic\n"
                                        "4. Any action items or decisions mentioned\n"
                                        "5. Questions raised and answers provided\n"
                                        "6. Notable quotes with speaker attribution (if possible)\n"
                                        "7. Overall tone and sentiment of the discussion\n\n"
                                        f"Format the output in markdown. Here's the transcription:\n\n{text}"}
        ],
        # max_tokens=12000  # Adjust this value based on your needs and model limits
    )
    return response.choices[0].message.content.strip()

def process_audio(audio_file):
    # Get the original file name
    audio_file_name = os.path.basename(audio_file.name)
    base_name = os.path.splitext(audio_file_name)[0]

    # Save the uploaded file temporarily
    with open(audio_file_name, "wb") as f:
        f.write(audio_file.getbuffer())

    # Convert the file to a smaller format
    output_name = f"{base_name}.ogg"
    subprocess.run(['ffmpeg', '-y', '-i', audio_file_name, '-vn', '-map_metadata', '-1', '-ac', '1', '-c:a', 'libopus', '-b:a', '12k', '-application', 'voip', output_name])

    # Create the transcription
    with open(output_name, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    # Generate detailed notes
    notes = create_detailed_notes(transcript.text)

    # Create a directory structure for the notes
    current_date = datetime.now().strftime("%Y-%m-%d")
    notes_dir = os.path.join("notes", current_date)
    os.makedirs(notes_dir, exist_ok=True)

    # Save the notes to a file, overwriting if it exists
    md_file_name = f"{base_name}_notes.md"
    full_path = os.path.join(notes_dir, md_file_name)

    with open(full_path, 'w') as file:
        file.write(notes)

    # Clean up temporary files
    os.remove(audio_file_name)
    os.remove(output_name)

    return full_path, notes

# Streamlit UI
st.title("Audio Transcription and Detailed Note Taking")

uploaded_file = st.file_uploader("Choose an audio file to transcribe and create notes from", type=['mp3', 'mp4', 'wav', 'ogg'])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/ogg')
    if st.button('Transcribe and Create Notes'):
        with st.spinner('Processing audio and creating detailed notes...'):
            try:
                file_path, notes = process_audio(uploaded_file)
                st.success(f"Audio transcribed and notes created successfully! Notes saved to {file_path}")
                st.markdown(notes)
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")

st.sidebar.markdown("## About")
st.sidebar.info("This app transcribes audio files and creates detailed notes using OpenAI's Whisper for transcription and GPT for note creation.")