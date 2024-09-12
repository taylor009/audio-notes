# Audio Transcription and Note-Taking App

## Overview

This Streamlit-based application transcribes audio files and generates detailed notes from the transcription. It uses OpenAI's Whisper model for audio transcription and GPT-4 for creating comprehensive notes.

## Features

- Audio file upload (supports mp3, mp4, wav, ogg)
- Audio transcription using OpenAI's Whisper
- Detailed note generation using OpenAI's GPT-4
- Organized storage of notes in date-based directories
- User-friendly interface with Streamlit

## Prerequisites

- Python 3.7+
- FFmpeg
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/audio-transcription-notes-app.git
   cd audio-transcription-notes-app
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On macOS with Homebrew: `brew install ffmpeg`
   - For Windows, download from the official FFmpeg website

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

1. Run the Streamlit app:
   ```
   streamlit run audio.py
   ```

2. Open the provided URL in your web browser

3. Upload an audio file using the file uploader

4. Click "Transcribe and Create Notes" to process the audio

5. View the generated notes in the app and find the saved markdown file in the `notes/YYYY-MM-DD/` directory

## File Structure

```
audio-transcription-notes-app/
│
├── audio.py            # Main application script
├── .env                # Environment file for API key (create this)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── notes/              # Directory where notes are saved
    └── YYYY-MM-DD/     # Date-based subdirectories for notes
        └── filename_notes.md
```

## Contributing

Contributions to improve the app are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgments
