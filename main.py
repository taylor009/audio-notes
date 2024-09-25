import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
from stqdm import stqdm  # Optional: For advanced progress bars

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_detailed_notes(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using the latest GPT-4 model for better performance
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that creates very detailed notes from transcriptions."
            },
            {
                "role": "user",
                "content": f"""Create very detailed notes from the following transcription, including:

1. A comprehensive overview
2. Key points and main ideas discussed
3. Detailed breakdown of each major topic
4. Any action items or decisions mentioned
5. Questions raised and answers provided
6. Notable quotes with speaker attribution (if possible)
7. Overall tone and sentiment of the discussion

Format the output in markdown. Here's the transcription:

{text}"""
            }
        ],
        # max_tokens=12000  # Adjust this value based on your needs and model limits
    )
    return response.choices[0].message.content.strip()

def process_audio(audio_file, progress_bar, status_text, log_placeholder):
    total_steps = 6
    current_step = 0

    steps = [
        "Saving uploaded file...",
        "Converting audio format...",
        "Transcribing audio...",
        "Generating detailed notes...",
        "Saving notes to file...",
        "Cleaning up temporary files..."
    ]

    def log_step(message):
        with log_placeholder.container():
            st.write(f"- {message}")

    # Step 1: Save the uploaded file
    status_text.text(steps[current_step])
    progress_bar.progress(current_step / total_steps)
    log_step("Saving uploaded file...")
    audio_file_name = os.path.basename(audio_file.name)
    base_name = os.path.splitext(audio_file_name)[0]

    temp_dir = "temp_processing"
    os.makedirs(temp_dir, exist_ok=True)

    temp_audio_path = os.path.join(temp_dir, audio_file_name)
    with open(temp_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
    current_step += 1
    progress_bar.progress(current_step / total_steps)

    # Step 2: Convert the file using ffmpeg
    status_text.text(steps[current_step])
    progress_bar.progress(current_step / total_steps)
    log_step("Converting audio format...")
    output_name = f"{base_name}.ogg"
    output_path = os.path.join(temp_dir, output_name)

    ffmpeg_command = [
        'ffmpeg', '-y', '-i', temp_audio_path, '-vn', '-map_metadata', '-1',
        '-ac', '1', '-c:a', 'libopus', '-b:a', '12k', '-application', 'voip', output_path
    ]

    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    current_step += 1
    progress_bar.progress(current_step / total_steps)

    # Step 3: Transcribe the audio
    status_text.text(steps[current_step])
    progress_bar.progress(current_step / total_steps)
    log_step("Transcribing audio...")
    with open(output_path, "rb") as audio_converted:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_converted)
    current_step += 1
    progress_bar.progress(current_step / total_steps)

    # Step 4: Generate detailed notes
    status_text.text(steps[current_step])
    progress_bar.progress(current_step / total_steps)
    log_step("Generating detailed notes...")
    notes = create_detailed_notes(transcript.text)
    current_step += 1
    progress_bar.progress(current_step / total_steps)

    # Step 5: Save notes to a file
    status_text.text(steps[current_step])
    progress_bar.progress(current_step / total_steps)
    log_step("Saving notes to file...")
    current_date = datetime.now().strftime("%Y-%m-%d")
    notes_dir = os.path.join("notes", current_date)
    os.makedirs(notes_dir, exist_ok=True)

    md_file_name = f"{base_name}_notes.md"
    full_path = os.path.join(notes_dir, md_file_name)
    with open(full_path, 'w') as file:
        file.write(notes)
    current_step += 1
    progress_bar.progress(current_step / total_steps)

    # Step 6: Clean up temporary files
    status_text.text(steps[current_step])
    progress_bar.progress(current_step / total_steps)
    log_step("Cleaning up temporary files...")
    os.remove(temp_audio_path)
    os.remove(output_path)
    os.rmdir(temp_dir)
    current_step += 1
    progress_bar.progress(current_step / total_steps)

    status_text.text("Processing complete!")
    return full_path, notes

# Streamlit UI
st.title("AI Audio Transcripts with Markdown Notes")

# Initialize placeholders for progress bar, status text, and logs
progress_bar = st.progress(0, text="Starting process...")
status_text = st.empty()
log_placeholder = st.empty()

uploaded_file = st.file_uploader(
    "Choose an audio file to transcribe and create notes from (Max size: 3 GB)",
    type=['mp3', 'mp4', 'wav', 'ogg']
)

if uploaded_file is not None:
    # Display the audio player
    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    # Display file size
    file_size_mb = len(audio_bytes) / (1024 ** 2)
    st.write(f"**File size:** {file_size_mb:.2f} MB")

    if file_size_mb > 3072:
        st.error("The uploaded file exceeds the 3 GB size limit. Please upload a smaller file.")
    else:
        if st.button('Transcribe and Create Notes'):
            try:
                file_path, notes = process_audio(uploaded_file, progress_bar, status_text, log_placeholder)
                st.success(f"Audio transcribed and notes created successfully! Notes saved to `{file_path}`")
                st.markdown(notes)
                
                # Read the markdown file content
                with open(file_path, 'r') as md_file:
                    md_content = md_file.read()
                
                # Provide a download button for the markdown file
                st.download_button(
                    label="Download Notes as Markdown",
                    data=md_content,
                    file_name=os.path.basename(file_path),
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")

st.sidebar.markdown("## About")
st.sidebar.info(
    "This app transcribes audio files and creates detailed notes using OpenAI's Whisper for transcription "
    "and GPT-4 for note creation."
)

# Display current max upload size
current_max = st.get_option('server.maxUploadSize')
st.sidebar.write(f"**Configured Max Upload Size:** {current_max} MB")