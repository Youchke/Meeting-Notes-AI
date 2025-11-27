import os
import time
import google.generativeai as genai
from gemini_api_interaction import GeminiAudioAPI

def transcribe_audio(config: GeminiAudioAPI) -> str:
    """
    Transcribes the audio using Google's Gemini model.

    Parameters
    ----------
    config : GeminiAudioAPI
        The configuration for the Gemini Audio API.
    Returns
    -------
    str
        The transcription of the audio.
    """
    # Configure the API
    genai.configure(api_key=config.api_key)

    # Upload the file
    print(f"Uploading file {config.file_path} to Gemini...")
    audio_file = genai.upload_file(path=config.file_path)

    # Wait for processing
    print("Waiting for audio processing...")
    while audio_file.state.name == "PROCESSING":
        time.sleep(2)
        audio_file = genai.get_file(audio_file.name)

    if audio_file.state.name == "FAILED":
        raise ValueError("Audio file processing failed.")

    print("Generating transcription...")
    model = genai.GenerativeModel(model_name=config.model)
    
    prompt = "Please transcribe this audio file verbatim. Do not add any other text."
    if config.prompt:
        prompt = config.prompt

    retry_count = 0
    max_retries = 5
    base_delay = 2

    while retry_count < max_retries:
        try:
            response = model.generate_content(
                [audio_file, prompt],
                request_options={"timeout": 600}
            )
            break
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                retry_count += 1
                wait_time = base_delay * (2 ** (retry_count - 1))
                print(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise e
    else:
        raise RuntimeError("Max retries exceeded for audio transcription.")

    # Clean up (optional, but good practice to delete files from cloud storage)
    try:
        genai.delete_file(audio_file.name)
    except Exception as e:
        print(f"Warning: Failed to delete file {audio_file.name}: {e}")

    return response.text
