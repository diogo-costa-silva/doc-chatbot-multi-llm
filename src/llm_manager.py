"""
Multi-LLM Manager (Gemini, Groq, Ollama)
"""
import os
import logging
from typing import Optional, Generator
import google.generativeai as genai
from groq import Groq
from .platform_utils import is_ollama_supported
from .config import DEFAULT_LLM_TEMPERATURE, DEFAULT_MAX_TOKENS

logger = logging.getLogger(__name__)

# Ollama is optional (not available in some environments like HF Spaces)
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ollama = None


class LLMManager:
    """Manages multiple LLM providers"""

    def __init__(self):
        self.provider = None
        self.model_name = None
        self.client = None

    def configure(self, provider: str, model_name: str, api_key: Optional[str] = None) -> bool:
        """
        Configures the LLM provider

        Args:
            provider: 'gemini', 'groq', or 'ollama'
            model_name: Model name to use
            api_key: API key (not required for Ollama)

        Returns:
            True if configured successfully, False otherwise
        """
        try:
            self.provider = provider.lower()
            self.model_name = model_name

            if self.provider == "gemini":
                if not api_key:
                    return False
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel(model_name)

            elif self.provider == "groq":
                if not api_key:
                    return False
                self.client = Groq(api_key=api_key)

            elif self.provider == "ollama":
                # Ollama doesn't need API key, but needs to be available
                if not OLLAMA_AVAILABLE:
                    logger.error("Ollama is not available in this environment")
                    return False

                self.client = ollama
                # Check if model is available
                try:
                    ollama.show(model_name)
                except Exception:
                    # Try to pull the model
                    try:
                        ollama.pull(model_name)
                    except Exception as e:
                        logger.error(f"Error pulling Ollama model {model_name}: {e}")
                        return False
            else:
                return False

            return True

        except Exception as e:
            logger.error(f"Error configuring {provider}: {e}")
            return False

    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generates response using the configured LLM

        Args:
            prompt: User question
            context: Additional context (document content)

        Returns:
            LLM response
        """
        if not self.client:
            return "Error: LLM not configured. Please select a model first."

        # Combine context and prompt
        full_prompt = prompt
        if context:
            full_prompt = f"""Document context:
{context}

---

User question: {prompt}

Please answer based on the context provided above."""

        try:
            if self.provider == "gemini":
                response = self.client.generate_content(full_prompt)
                return response.text

            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=DEFAULT_LLM_TEMPERATURE,
                    max_tokens=DEFAULT_MAX_TOKENS
                )
                return response.choices[0].message.content

            elif self.provider == "ollama":
                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                return response['message']['content']

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def stream_response(self, prompt: str, context: Optional[str] = None) -> Generator[str, None, None]:
        """
        Generates streaming response

        Args:
            prompt: User question
            context: Additional context (document content)

        Yields:
            Response chunks
        """
        if not self.client:
            yield "Error: LLM not configured. Please select a model first."
            return

        # Combine context and prompt
        full_prompt = prompt
        if context:
            full_prompt = f"""Document context:
{context}

---

User question: {prompt}

Please answer based on the context provided above."""

        try:
            if self.provider == "gemini":
                response = self.client.generate_content(full_prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text

            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=DEFAULT_LLM_TEMPERATURE,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            elif self.provider == "ollama":
                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
                        {"role": "user", "content": full_prompt}
                    ],
                    stream=True
                )
                for chunk in response:
                    if 'message' in chunk and 'content' in chunk['message']:
                        yield chunk['message']['content']

        except Exception as e:
            yield f"Error generating response: {str(e)}"

    @staticmethod
    def is_ollama_available() -> bool:
        """
        Checks if Ollama is available in this environment

        Returns:
            True if Ollama can be used, False otherwise
        """
        return OLLAMA_AVAILABLE and is_ollama_supported()

    @staticmethod
    def get_available_models() -> dict:
        """
        Returns available models by provider (fallback/defaults)

        Returns:
            Dictionary with providers and their default models
        """
        models = {
            "gemini": [
                # Updated models for 2025 (1.5 deprecated)
                "gemini-2.5-flash-lite",  # Fast, low cost
                "gemini-2.5-flash",       # Stable Flash 2.5
                "gemini-2.5-pro",         # Stable Pro with thinking
                "gemini-2.0-flash-exp",   # Flash 2.0 experimental
            ],
            "groq": [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ]
        }

        # Only include Ollama if available
        if LLMManager.is_ollama_available():
            models["ollama"] = [
                "llama3.2",
                "llama3.1",
                "mistral",
                "phi3",
                "qwen2.5"
            ]

        return models

    @staticmethod
    def get_ollama_models() -> tuple[list, bool]:
        """
        Returns locally installed Ollama models

        Returns:
            Tuple with (list of installed models, service is active)
        """
        # If Ollama is not available, return empty list
        if not OLLAMA_AVAILABLE:
            return [], False

        try:
            result = ollama.list()
            # The returned object has a .models attribute which is a list of Model objects
            # Each Model object has .name or .model attributes
            installed = []
            for model in result.models:
                # Use .model if available, otherwise .name
                model_name = model.model if hasattr(model, 'model') else model.name
                # Remove tag (e.g., "llama3.2:latest" -> "llama3.2")
                base_name = model_name.split(':')[0]
                if base_name not in installed:  # Avoid duplicates
                    installed.append(base_name)
            return installed, True
        except Exception as e:
            # If it fails, return empty list and indicate service is not active
            logger.warning(f"Error connecting to Ollama: {e}")
            return [], False

    @staticmethod
    def check_ollama_status() -> bool:
        """
        Checks if Ollama service is active

        Returns:
            True if service is running, False otherwise
        """
        # If Ollama is not available, return False
        if not OLLAMA_AVAILABLE:
            return False

        try:
            ollama.list()
            return True
        except Exception:
            return False

    @staticmethod
    def get_gemini_models_dynamic(api_key: str) -> tuple[list, bool]:
        """
        Fetches available Gemini models directly from the API

        Args:
            api_key: Gemini API key

        Returns:
            Tuple with (list of available models, success)
        """
        if not api_key:
            return LLMManager.get_available_models()['gemini'], False

        try:
            genai.configure(api_key=api_key)
            models_list = list(genai.list_models())

            # Filter only models that support generateContent
            available = []
            for model in models_list:
                if 'generateContent' in model.supported_generation_methods:
                    # Remove "models/" prefix if present
                    model_name = model.name.replace('models/', '')
                    available.append(model_name)

            # If models found, return; otherwise use fallback
            if available:
                return available, True
            else:
                return LLMManager.get_available_models()['gemini'], False

        except Exception as e:
            logger.warning(f"Error fetching Gemini models from API: {e}")
            # Fallback to default list
            return LLMManager.get_available_models()['gemini'], False

    @staticmethod
    def get_groq_models_dynamic(api_key: str) -> tuple[list, bool]:
        """
        Fetches available Groq models directly from the API

        Args:
            api_key: Groq API key

        Returns:
            Tuple with (list of available models, success)
        """
        if not api_key:
            return LLMManager.get_available_models()['groq'], False

        try:
            client = Groq(api_key=api_key)
            models_response = client.models.list()

            # Extract model names
            available = []
            for model in models_response.data:
                # Filter only chat/text models
                if hasattr(model, 'id'):
                    available.append(model.id)

            # If models found, return; otherwise use fallback
            if available:
                return available, True
            else:
                return LLMManager.get_available_models()['groq'], False

        except Exception as e:
            logger.warning(f"Error fetching Groq models from API: {e}")
            # Fallback to default list
            return LLMManager.get_available_models()['groq'], False
