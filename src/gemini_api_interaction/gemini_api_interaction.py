from dataclasses import dataclass
from typing import Optional

@dataclass
class GeminiAudioAPI:
    """
    A dataclass to store the configuration for the Gemini Audio API.
    """
    api_key: str
    file_path: str
    model: str = "gemini-2.0-flash"
    prompt: Optional[str] = None

@dataclass
class GeminiCompletionAPI:
    """
    A dataclass to store the configuration for the Gemini Completion API.
    """
    api_key: str
    model: str = "gemini-2.0-flash"
    max_tokens: Optional[int] = 8192
    temperature: Optional[float] = 0.5
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 64
