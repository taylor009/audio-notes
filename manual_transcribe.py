import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio_file = 'dad-call-2024-09-18 11:45:35.mp4'
audio_file_name = os.path.basename(audio_file)
base_name = os.path.splitext(audio_file_name)[0]

# Convert the file to a smaller format
subprocess.run(['ffmpeg', '-y', '-i', audio_file, '-vn', '-map_metadata', '-1', '-ac', '1', '-c:a', 'libopus', '-b:a', '12k', '-application', 'voip', 'audio.ogg'])

# Open the converted file
audio_file = open('audio.ogg', 'rb')

# Create the transcription
transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
print(transcript.text)

# Close the file
audio_file.close()

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using the latest GPT-4 model for better performance
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes very detailed notes."},
            {"role": "user", "content": f"Write a very detailed document on the following text, including:\n\n"
                                        "1. A comprehensive summary\n"
                                        "2. Key points and main ideas\n"
                                        "3. Detailed notes on each major topic discussed\n"
                                        "4. Any action items or decisions made\n"
                                        "5. Questions raised and answers provided\n"
                                        "6. Notable quotes with speaker attribution (if possible)\n"
                                        "7. Overall tone and sentiment of the discussion\n\n"
                                        f"Format the output in markdown. Here's the text:\n\n{text}"}
        ],
        # max_tokens=12000  # Adjust this value based on your needs and model limits
    )
    return response.choices[0].message.content.strip()

# After generating the summary
transcription_text = transcript.text
summary = summarize_text(transcription_text)
print(summary)

# Save the summary to a file, overwriting if it exists
md_file_name = f"{base_name}_notes.md"
with open(md_file_name, 'w') as file:
    file.write(summary)

print(f"Detailed notes saved to {md_file_name}")