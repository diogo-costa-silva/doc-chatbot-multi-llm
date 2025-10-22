"""
GenAI Document Chatbot

A multi-LLM chatbot for document analysis supporting Google Gemini, Groq, and Ollama.
"""

__version__ = "0.6.0"
__author__ = "GenAI Document Chatbot Contributors"

# Core components
from .llm_manager import LLMManager
from .document_processor import DocumentProcessor
from .chat_handler import ChatHandler
from .platform_utils import is_huggingface_space, is_ollama_supported, get_platform_name

__all__ = [
    "LLMManager",
    "DocumentProcessor",
    "ChatHandler",
    "is_huggingface_space",
    "is_ollama_supported",
    "get_platform_name",
]
