# Audio Transcription and Note-Taking App

## Overview

This Streamlit-based application transcribes audio files and generates detailed notes from the transcription. It uses OpenAI's Whisper model for audio transcription and GPT-4 for creating comprehensive notes.

## Features

- **Audio File Upload**: Supports mp3, mp4, wav, ogg formats.
- **Audio Transcription**: Utilizes OpenAI's Whisper for transcribing audio.
- **Detailed Note Generation**: Employs OpenAI's GPT-4 to create comprehensive notes from transcriptions.
- **Organized Storage**: Saves notes in date-based directories for easy access.
- **User-Friendly Interface**: Built with Streamlit for an intuitive user experience.
- **Progress Updates**: Provides real-time feedback during processing.
- **Downloadable Outputs**: Allows users to download the generated Markdown notes.

## Prerequisites

- **Python 3.7+**
- **FFmpeg**
- **OpenAI API Key**

## Installation

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/yourusername/audio-transcription-notes-app.git
   cd audio-transcription-notes-app
   ```

2. **Install Required Python Packages**
   
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   
   - **On Ubuntu**:
     ```bash
     sudo apt-get install ffmpeg
     ```
   - **On macOS with Homebrew**:
     ```bash
     brew install ffmpeg
     ```
   - **For Windows**:
     Download and install FFmpeg from the [official website](https://ffmpeg.org/download.html).

4. **Configure Environment Variables**
   
   The application requires an OpenAI API key for transcription and note generation. You can set this up using either a `.env` file or Streamlit's `secrets.toml` file.

   ### a. Using a `.env` File

   1. **Create a `.env` File**
      
      In the root directory of the project, create a file named `.env`:
      
      ```bash
      touch .env
      ```

   2. **Add Your OpenAI API Key**
      
      Open the `.env` file in a text editor and add the following line:
      
      ```env
      OPENAI_API_KEY=your_openai_api_key_here
      ```

      **Example:**
      
      ```env
      OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      ```

      **Important Notes:**
      - **Security**: Ensure that `.env` is included in your `.gitignore` file to prevent sensitive information from being pushed to version control.
      - **Consistency**: Maintain the exact key name `OPENAI_API_KEY` as referenced in the application code.

   ### b. Using Streamlit's `secrets.toml` File

   1. **Locate the `.streamlit` Directory**
      
      Streamlit reads secrets from a `secrets.toml` file located within a `.streamlit` directory in the project's root. If the `.streamlit` directory doesn't exist, create it:
      
      ```bash
      mkdir .streamlit
      ```

   2. **Create or Edit the `secrets.toml` File**
      
      Inside the `.streamlit` directory, create or modify the `secrets.toml` file:
      
      ```bash
      touch .streamlit/secrets.toml
      ```

      Open `secrets.toml` in a text editor and add your OpenAI API key:
      
      ```toml
      OPENAI_API_KEY = "your_openai_api_key_here"
      ```

      **Example:**
      
      ```toml
      OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      ```

      **Important Notes:**
      - **Security**: Do not share the `secrets.toml` file publicly. It contains sensitive information.
      - **Deployment**: When deploying on platforms like Streamlit Community Cloud, you can add secrets directly through the platform's interface, which securely handles the `secrets.toml` configuration.

## Usage

1. **Run the Streamlit App**
   
   ```bash
   streamlit run main.py
   ```

2. **Access the App**
   
   Open the provided local URL in your web browser.

3. **Upload an Audio File**
   
   Use the file uploader to select an audio file (mp3, mp4, wav, ogg) up to **3 GB** in size.

4. **Process the Audio**
   
   Click the "Transcribe and Create Notes" button to start processing. Monitor the progress through real-time updates and progress bars.

5. **View and Download Notes**
   
   Once processing is complete, view the generated notes within the app and download the Markdown file using the provided download button. The notes are also saved in the `notes/YYYY-MM-DD/` directory.

## File Structure

```
audio-transcription-notes-app/
│
├── main.py                # Main application script
├── .env                   # Environment file for API key (create this)
├── .streamlit/
│   └── secrets.toml       # Streamlit secrets file for API key
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── notes/                 # Directory where notes are saved
    └── YYYY-MM-DD/        # Date-based subdirectories for notes
        └── filename_notes.md
```

## Contributing

Contributions to improve the app are welcome. Please follow these steps:

1. **Fork the Repository**
   
   ```bash
   git clone https://github.com/yourusername/audio-transcription-notes-app.git
   cd audio-transcription-notes-app
   ```

2. **Create a New Branch**
   
   ```bash
   git checkout -b feature-branch
   ```

3. **Make Your Changes and Commit**
   
   ```bash
   git commit -am 'Add some feature'
   ```

4. **Push to the Branch**
   
   ```bash
   git push origin feature-branch
   ```

5. **Create a New Pull Request**
   
   Open a pull request with a detailed description of your changes.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgments

- **OpenAI** for providing powerful models like Whisper and GPT-4.
- **Streamlit** for enabling the creation of interactive web applications with ease.
- Community contributors and all who have supported the development of this app.

## Additional Information

### Environment Variables Configuration

You can configure environment variables to manage sensitive information securely. Below are the methods to set them up:

#### Using a `.env` File

1. **Create the `.env` File**:
   
   ```bash
   touch .env
   ```

2. **Add Environment Variables**:
   
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Ensure Security**:
   
   Make sure to add `.env` to your `.gitignore` to prevent it from being committed to version control.

#### Using `secrets.toml` File in Streamlit

1. **Navigate to `.streamlit` Directory**:
   
   ```bash
   mkdir -p .streamlit
   ```

2. **Create or Edit `secrets.toml`**:
   
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

3. **Leveraging Streamlit's Secret Management**:
   
   When deploying to platforms like Streamlit Community Cloud, you can add secrets directly through the platform's interface, which ensures that your keys are stored securely and not exposed in your codebase.

## Troubleshooting

- **File Upload Limits**:
  
  If you encounter issues with file upload limits, ensure that the `maxUploadSize` parameter in your `.streamlit/config.toml` is correctly set. Refer to the [Streamlit Configuration Documentation](https://docs.streamlit.io/library/advanced-features/configuration) for more details.

- **Environment Variable Issues**:
  
  Verify that your `.env` or `secrets.toml` files are correctly formatted and placed in the appropriate directories. Ensure that the key names match those referenced in your application code.

- **Dependency Problems**:
  
  Make sure all required Python packages are installed. You can reinstall dependencies using:
  
  ```bash
  pip install --upgrade -r requirements.txt
  ```

## Contact

For further assistance, feel free to reach out or open an issue on the [GitHub repository](https://github.com/yourusername/audio-transcription-notes-app/issues).

---

*Feel free to reach out if you need further assistance!*
