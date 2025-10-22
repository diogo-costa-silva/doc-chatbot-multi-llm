"""
Configuration constants for the GenAI Document Chatbot
"""

# Document Processing
CHUNK_SIZE = 1000  # Maximum characters per text chunk
CHUNK_OVERLAP = 200  # Overlap between consecutive chunks
MAX_CHUNKS_FOR_QUERY = 3  # Maximum chunks to return for relevance queries
DOCUMENT_SUMMARY_LENGTH = 500  # Maximum length for document summaries

# File Upload Limits (in bytes)
MAX_FILE_SIZE_TXT = 10 * 1024 * 1024  # 10 MB for TXT files
MAX_FILE_SIZE_PDF = 50 * 1024 * 1024  # 50 MB for PDF files

# LLM Configuration
DEFAULT_LLM_TEMPERATURE = 0.7  # Temperature for LLM responses
DEFAULT_MAX_TOKENS = 2000  # Maximum tokens for LLM responses

# Text Splitter Configuration
TEXT_SPLITTER_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]  # Order matters: prefer paragraph > sentence > word

# Supported File Extensions
SUPPORTED_TEXT_EXTENSIONS = ['.txt']
SUPPORTED_PDF_EXTENSIONS = ['.pdf']
SUPPORTED_EXTENSIONS = SUPPORTED_TEXT_EXTENSIONS + SUPPORTED_PDF_EXTENSIONS
