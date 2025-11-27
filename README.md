# Meeting Summary Generator

The Meeting Summary Generator is a Python-based tool that extracts audio from an MP4 video of a virtual meeting, transcribes the audio using OpenAI's Whisper model, and generates a summary of the meeting using OpenAI's GPT models. You can also start the process from an audio file or a text file.

## Features

- Extract audio from video files (MP4 format)
- Transcribe audio using Google Gemini
- Summarize transcriptions using Google Gemini
- Save generated meeting summaries as text files

## Requirements

- [Download Python](https://www.python.org/downloads/) 3.10 or higher (required for compatibility with certain libraries and features)
- Get a [Google Gemini](https://aistudio.google.com/app/apikey) API key (keep this key secure and do not commit it to version control)
- [Docker](https://www.docker.com/) (optional, for running in a container)

## Installation

### Using Docker (Recommended)

1.  Clone this repository:
    ```bash
    git clone https://github.com/samimhidia1/meeting-summary-generator.git
    cd meeting-summary-generator
    ```

    *   Create a `.env` file in the project root:
        ```bash
        echo "GEMINI_API_KEY=your-gemini-api-key" > .env
        ```
    *   **OR** ensure you have `gemini_apikey.txt` present.

3.  Run with Docker Compose:
    ```bash
    docker-compose run --rm meeting-summarizer
    ```

### Manual Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/samimhidia1/meeting-summary-generator.git
    ```
2. Change to the project directory:

    ```bash
    cd meeting-summary-generator
    ```
3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    * if you are using Windows:

    ```bash
    venv\Scripts\activate
    ```
    * if you are using Linux or macOS:

    ```bash
    source venv/bin/activate
    ```

5. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

Alternatively, you can use the provided setup script to automate the creation of the virtual environment and installation of dependencies:

```bash
./setup.sh
```

## Usage

### Quick Start Guide

1. **Set up the Gemini API key:**
   Create a file named `gemini_apikey.txt` in the root directory of the project and add your Gemini API key to this file. The `main.py` script will read the API key from this file.

   ```bash
   echo "your-gemini-api-key" > gemini_apikey.txt
   ```

2. **Run the script for the first time:**
   Run the `main.py` script in your terminal:

   ```bash
   python main.py
   ```

   The script will prompt you to enter the name of the project you want to generate a summary for. Enter the name of the project and press `Enter`.

   e.g. `Project MK-Ultra`

   If the project does not exist, the script will create a new project directory with the name you entered. The project directory will be created in the `projects` directory.

### Detailed Usage Instructions

#### Adding a video file to an existing project

1. Place the video file you want to process in the `videos` directory of the project directory.
2. The script will extract the audio from the video file and save it in the `audios` directory of the project directory.
3. The script will transcribe the audio and save the transcription in the `transcriptions` directory of the project directory.
4. Finally, the script will generate a summary of the transcription and save it in the `summaries` directory of the project directory.

#### Adding an audio file to an existing project

1. Place the audio file you want to process in the `audios` directory of the project directory.
2. The script will transcribe the audio and save the transcription in the `transcriptions` directory of the project directory.
3. Finally, the script will generate a summary of the transcription and a structured meeting summary from it and save both text files in the `summaries` directory of the project directory.

#### Adding a text file to an existing project

1. Place the text file you want to process in the `transcriptions` directory of the project directory.
2. The script will generate a summary of the transcription and a structured meeting summary from it and save both text files in the `summaries` directory of the project directory.

### Running the script for an existing project after adding a video file, audio file, or text file

1. Once you have placed the video file, audio file, or text file in the appropriate directory, re-run the `main.py` script in your terminal:

   ```bash
   python main.py
   ```

2. Select the name of the project you want to generate a summary for and press `Enter`.

3. The script will then prompt you to choose between the following options:

   - `1`: Start from video file
   - `2`: Start from an audio file
   - `3`: Start from a text file
   - `4`: Exit

4. Choose the option that best suits your needs and press `Enter.

#### Option 1: Start from video file
If you choose option 1, the script will prompt you to enter the name of the video file you want to extract the audio from. Enter the name of the video file with the extension and press `Enter`.

e.g. `meeting.mp4`

#### Option 2: Start from an audio file
If you choose option 2, the script will prompt you to enter the name of the audio file you want to transcribe. Enter the name of the audio file with the extension and press `Enter`.

e.g. `meeting.wav`

#### Option 3: Start from a text file
If you choose option 3, the script will prompt you to enter the name of the text file you want to summarize. Enter the name of the text file with the extension and press `Enter`.

e.g. `meeting.txt`

#### Option 4: Exit
If you choose option 4, the script will exit.

## Structure of the generated summary

The generated summary is structured as follows:

```
STRUCTURE:
1. Meeting Objectives:
    a. Objective 1: [Brief description]
    b. Objective 2:
    .
    .
    .
    c. Objective n:
2. Key Discussion Points:
    a. Topic 1: [Brief summary of discussion]
        Main point 1
        Main point 2
        ...
        Main point n
    b. Topic 2:
        Main point 1
        Main point 2
        ...
        Main point n
    .
    .
    .
    n. Topic n:
        Main point 1
        Main point 2
        ...
        Main point n
3. Important Decisions:
    a. Decision 1: [Decision made and rationale]
    b. Decision 2:
    .
    .
    .
    n. Decision n:
4. Action Items:
    a. Action Item 1: [Task description] - [Deadline]
    b. Action Item 2:
    .
    .
    .
    n. Action Item n:
5. Meeting Outcomes:
    a. Objective 1: [Status - Achieved/Partially Achieved/Not Achieved]
        [Key takeaways, insights, or progress made]
    b. Objective 2:
    .
    .
    .
    n. Objective n:
6. Next Steps:
    a. Next Meeting Date: [Next Meeting Date]
    b. Agenda Items for Next Meeting: [List of Agenda Items]
    c. Additional Follow-up: [Any other relevant information or follow-up tasks]
```

You can change the structure of the summary by editing the `summary_structure.txt` file in the `generate_meeting_summary/prompts` directory and the line 111 of the pipelines.py script.

## Project Structure

The project is structured as follows:

```
meeting_summary_generator/
├── audio_extractor
│   └── audio_extractor.py
├── generate_meeting_summary
│   ├── generate_meeting_summary.py
│   └── prompts
│       ├── summary_structure_2.txt
│       └── summary_structure.txt
├── main.py
├── meeting_summarizer
│   ├── meeting_summarizer.py
│   ├── prompts
│   │   └── summarize_transcript.txt
│   └── utils.py
├── openai_api_interaction
│   └── openai_api_interaction.py
├── pipelines.py
├── projects
│   └── MK-Monarch
│       ├── audios
│       ├── summaries
│       ├── transcriptions
│       └── videos
├── README.md
├── requirements.txt
├── speech_transcriber
│   └── speech_transcriber.py
├── temp
└── tests
    ├── test_audio_extractor.py
    ├── test_meeting_summarizer.py
    └── test_speech_transcriber.py
```

## Testing

You can run the unit tests with the following command:

```bash
python -m unittest discover  tests
```

**Note:** Running the tests for `speech_transcriber` and `meeting_summarizer` will consume tokens from your OpenAI API quota, so use it judiciously to avoid running out of your allocated tokens.

## Setup Script

The `setup.sh` script automates the creation of the virtual environment and installation of dependencies. To use the script, run the following command:

```bash
./setup.sh
```

The script will create a virtual environment, activate it, and install the required dependencies from the `requirements.txt` file.

## TODO

- [ ] Add support for other video formats
- [ ] Add support for other audio formats
- [ ] Rewrite the tests to use mocks instead of the actual OpenAI API
- [ ] Add support for other Transformers models
- [ ] Add support for other prompts and summary structures
- [ ] Add support for other languages and automatic language detection
- [ ] Make the text in the terminal more user-friendly
- [ ] Test for other operating systems

## Acknowledgements

- [OpenAI](https://openai.com)
- [MoviePy](https://zulko.github.io/moviepy)
- [Pydub](https://github.com/jiaaro/pydub)

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Sami Mhidia - sami.mhidia@jarvisator.com
