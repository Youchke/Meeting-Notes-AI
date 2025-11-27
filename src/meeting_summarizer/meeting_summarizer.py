import google.generativeai as genai
from gemini_api_interaction import GeminiCompletionAPI

def summarize_transcription(
        transcriptions: str,
        config: GeminiCompletionAPI,
) -> str:
    """
    Summarizes the meeting transcription using Google's Gemini model.

    Parameters
    ----------
    transcriptions : str
        The meeting transcription.
    config : GeminiCompletionAPI
        The configuration for the Gemini Completion API.

    Returns
    -------
    str
        The generated meeting summary.
    """
    genai.configure(api_key=config.api_key)
    
    model = genai.GenerativeModel(
        model_name=config.model,
        generation_config={
            "temperature": config.temperature,
            "top_p": config.top_p,
            "top_k": config.top_k,
            "max_output_tokens": config.max_tokens,
        }
    )

    # Gemini 1.5 Flash has a 1M token context window, so we can usually process 
    # the entire transcription in one go without complex chunking.
    
    prompt = f"You are a helpful assistant. Please summarize the following meeting points:\n\n{transcriptions}"
    
    import time
    retry_count = 0
    max_retries = 5
    base_delay = 2

    while retry_count < max_retries:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                retry_count += 1
                wait_time = base_delay * (2 ** (retry_count - 1))
                print(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"Error generating summary: {e}")
                return ""
    return ""
