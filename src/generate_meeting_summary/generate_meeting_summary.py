import google.generativeai as genai
from gemini_api_interaction import GeminiCompletionAPI

def generate_meeting_summary(
        summary: str,
        config: GeminiCompletionAPI,
        prompt_template: str,
) -> str:
    """
    Generates a meeting summary using Google's Gemini model.
    Parameters
    ----------
    summary : str
        The meeting summary (or transcription).
    config : GeminiCompletionAPI
        The configuration for the Gemini Completion API.
    prompt_template : str
        The template for creating the summary prompt.

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

    # Combine the template and the content
    # The template likely contains instructions on how to structure the summary.
    final_prompt = f"{prompt_template}\n\nHere is the content to process:\n{summary}"

    import time
    retry_count = 0
    max_retries = 5
    base_delay = 2

    while retry_count < max_retries:
        try:
            response = model.generate_content(final_prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "Resource exhausted" in str(e):
                retry_count += 1
                wait_time = base_delay * (2 ** (retry_count - 1))
                print(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"Error generating meeting summary: {e}")
                return ""
    return ""
