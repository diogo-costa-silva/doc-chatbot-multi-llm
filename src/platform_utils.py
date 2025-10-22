"""
Platform and environment detection utilities
"""
import os


def is_huggingface_space() -> bool:
    """
    Detects if application is running on Hugging Face Spaces

    Returns:
        True if running on HF Spaces, False otherwise
    """
    # HF Spaces defines SPACE_ID variable
    return os.getenv("SPACE_ID") is not None or os.getenv("SPACE_AUTHOR_NAME") is not None


def get_platform_name() -> str:
    """
    Returns current platform name

    Returns:
        Platform name: 'huggingface', 'local', etc.
    """
    if is_huggingface_space():
        return "huggingface"
    return "local"


def is_ollama_supported() -> bool:
    """
    Checks if Ollama is supported on current platform

    Returns:
        True if Ollama can be used, False otherwise
    """
    # Ollama only works in local environment
    return not is_huggingface_space()
