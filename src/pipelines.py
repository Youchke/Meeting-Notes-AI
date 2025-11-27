import os
from audio_extractor import extract_audio_from_video
from generate_meeting_summary import generate_meeting_summary
from meeting_summarizer import summarize_transcription
from gemini_api_interaction import GeminiAudioAPI, GeminiCompletionAPI
from speech_transcriber import transcribe_audio


def save_text(text, output_path):
    with open(output_path, "w", encoding='utf-8') as transcription_file:
        transcription_file.write(text)


def video_to_summary(
        project: str,
        video_name: str,
        api_key: str,
        save_output: bool = True,
) -> None:
    """
    Extracts audio from a video, transcribes the audio, and summarizes the meeting.

    Parameters
    ----------
    project : str
        The name of the project.
    video_name : str
        The name of the input video file.
    api_key : str
        The Google Gemini API key.
    save_output : bool, optional
        Whether to save the outputs to disk, by default True.
    """
    # Step 1: Extract audio from the video

    print(f"Extracting audio from: {video_name} ...")
    if save_output:
        video_path = "projects/{}/videos/{}".format(project, video_name)
        audio_output_path = "projects/{}/audios/{}.wav".format(project, video_name.split(".")[0])
    else:
        # If not saving, we assume video_path is passed as video_name (absolute path)
        # and we create a temp file for audio
        import tempfile
        video_path = video_name
        temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio_output_path = temp_audio.name
        temp_audio.close()

    extract_audio_from_video(video_path, audio_output_path)
    print(f"Audio extracted and saved to: {audio_output_path}")

    # Step 2: Transcribe the audio and summarize the meeting
    audio_to_summary(project, audio_output_path, api_key, save_output=save_output)
    
    if not save_output:
        os.remove(audio_output_path)


def audio_to_summary(
        project: str,
        audio_path: str,
        api_key: str,
        save_output: bool = True,
) -> dict:
    """
    Transcribes the audio and summarizes the meeting.

    Parameters
    ----------
    project : str
        The name of the project.
    audio_path : str
        The path to the input audio file.
    api_key : str
        The Google Gemini API key.
    save_output : bool, optional
        Whether to save the outputs to disk, by default True.
    """
    # Step 1: Transcribe the audio
    print("Transcribing the audio file...")
    configAudio = GeminiAudioAPI(api_key=api_key, file_path=audio_path)
    transcription = transcribe_audio(configAudio)
    audio_name = os.path.basename(audio_path).split(".")[0]
    
    if save_output:
        output_transcription_path = "projects/{}/transcriptions/transcription_{}.txt".format(project, audio_name)
        save_text(transcription, output_transcription_path)
    
    print("Transcription from the audio completed.")

    # Step 2: Summarize the meeting transcription
    return text_to_summary(project, transcription, audio_name, api_key, save_output=save_output)


def text_to_summary(
        project: str,
        transcription: str,
        name: str,
        api_key: str,
        save_output: bool = True,
) -> dict:
    """
    Summarizes the meeting transcription.

    Parameters
    ----------
    project : str
        The name of the project.
    transcription : str
        The transcription of the meeting.
    name : str
        The name of the input text file.
    api_key : str
        The Google Gemini API key.
    save_output : bool, optional
        Whether to save the outputs to disk, by default True.
        
    Returns
    -------
    dict
        A dictionary containing the transcription, summary, and meeting summary.
    """
    # Step 1: Summarize the meeting transcription
    base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(base_dir, "meeting_summarizer/prompts/summarize_transcript.txt")
    
    try:
        prompt_template_summarize = open(prompt_path, "r", encoding='utf-8').read()
    except FileNotFoundError:
        print(f"Warning: Prompt file not found at {prompt_path}. Using default prompt.")
        prompt_template_summarize = "You are a helpful assistant. Please summarize the following meeting points:"

    print("Summarizing the meeting transcription...")
    
    # Using Gemini for summarization
    configSummary = GeminiCompletionAPI(
        api_key=api_key,
        max_tokens=8192,
        temperature=0.5
    )
    
    summary = summarize_transcription(transcriptions=transcription,
                                      config=configSummary)
    
    if save_output:
        text_name = name
        output_summary_path = "projects/{}/summaries/summary_{}.txt".format(project, text_name)
        save_text(summary, output_summary_path)
        print(f"Transcriptions summary saved to: {output_summary_path}")
    else:
        print("Summary of transcriptions completed.")

    # Step 2: Generate the meeting summary
    meeting_summary_prompt_path = os.path.join(base_dir, "generate_meeting_summary/prompts/summary_structure_2.txt")
    try:
        prompt_template_meeting_summary = open(meeting_summary_prompt_path, "r", encoding='utf-8').read()
    except FileNotFoundError:
        print(f"Warning: Prompt file not found at {meeting_summary_prompt_path}. Using default structure.")
        prompt_template_meeting_summary = "Please provide a structured summary of the meeting."

    print("Generating the meeting summary...")
    
    configMeetingSummary = GeminiCompletionAPI(
        api_key=api_key,
        max_tokens=8192
    )
    
    meeting_summary = generate_meeting_summary(summary=summary,
                                               config=configMeetingSummary,
                                               prompt_template=prompt_template_meeting_summary)
    
    if save_output:
        output_meeting_summary_path = "projects/{}/summaries/meeting_summary_{}.txt".format(project, name)
        save_text(meeting_summary, output_meeting_summary_path)
        print(f"Meeting summary saved to: {output_meeting_summary_path}")
    else:
        print("Meeting summary completed.")
    
    return {
        "transcription": transcription,
        "summary": summary,
        "meeting_summary": meeting_summary
    }
