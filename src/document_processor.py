"""
TXT and PDF Document Processor
"""
from typing import Optional
import tempfile
from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_CHUNKS_FOR_QUERY,
    DOCUMENT_SUMMARY_LENGTH,
    MAX_FILE_SIZE_TXT,
    MAX_FILE_SIZE_PDF,
    TEXT_SPLITTER_SEPARATORS
)


class DocumentProcessor:
    """Processes and extracts text from TXT and PDF documents"""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initializes the processor

        Args:
            chunk_size: Maximum size of each text chunk (default from config)
            chunk_overlap: Overlap between consecutive chunks (default from config)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=TEXT_SPLITTER_SEPARATORS
        )

    def process_file(self, file_path: str) -> tuple[str, dict]:
        """
        Processes a file and extracts its content

        Args:
            file_path: Path to the file

        Returns:
            Tuple with (full_text, metadata)
        """
        file_extension = Path(file_path).suffix.lower()

        if file_extension == '.txt':
            return self._process_txt(file_path)
        elif file_extension == '.pdf':
            return self._process_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def process_uploaded_file(self, uploaded_file) -> tuple[str, dict]:
        """
        Processes a file uploaded via Streamlit

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            Tuple with (full_text, metadata)

        Raises:
            ValueError: If file size exceeds limits
        """
        # Validate file size based on type
        file_extension = Path(uploaded_file.name).suffix.lower()
        file_size = uploaded_file.size

        if file_extension == '.txt' and file_size > MAX_FILE_SIZE_TXT:
            max_mb = MAX_FILE_SIZE_TXT / (1024 * 1024)
            raise ValueError(f"TXT file too large. Maximum size: {max_mb:.0f}MB")
        elif file_extension == '.pdf' and file_size > MAX_FILE_SIZE_PDF:
            max_mb = MAX_FILE_SIZE_PDF / (1024 * 1024)
            raise ValueError(f"PDF file too large. Maximum size: {max_mb:.0f}MB")

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            text, metadata = self.process_file(tmp_path)
            metadata['filename'] = uploaded_file.name
            metadata['size'] = uploaded_file.size
            return text, metadata
        finally:
            # Remove temporary file
            Path(tmp_path).unlink(missing_ok=True)

    def _process_txt(self, file_path: str) -> tuple[str, dict]:
        """
        Processes TXT file

        Args:
            file_path: Path to TXT file

        Returns:
            Tuple with (text, metadata)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            metadata = {
                'type': 'txt',
                'chars': len(text),
                'words': len(text.split()),
                'lines': text.count('\n') + 1
            }

            return text, metadata

        except Exception as e:
            raise ValueError(f"Error processing TXT file: {str(e)}")

    def _process_pdf(self, file_path: str) -> tuple[str, dict]:
        """
        Processes PDF file

        Args:
            file_path: Path to PDF file

        Returns:
            Tuple with (text, metadata)
        """
        try:
            reader = PdfReader(file_path)

            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            metadata = {
                'type': 'pdf',
                'pages': len(reader.pages),
                'chars': len(text),
                'words': len(text.split())
            }

            # Add PDF metadata if available
            if reader.metadata:
                if reader.metadata.title:
                    metadata['title'] = reader.metadata.title
                if reader.metadata.author:
                    metadata['author'] = reader.metadata.author

            return text, metadata

        except Exception as e:
            raise ValueError(f"Error processing PDF file: {str(e)}")

    def chunk_text(self, text: str) -> list[str]:
        """
        Splits text into smaller chunks

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        return self.text_splitter.split_text(text)

    def get_relevant_chunks(self, text: str, query: str, max_chunks: int = MAX_CHUNKS_FOR_QUERY) -> str:
        """
        Returns the most relevant chunks for a query
        (Simple keyword-based implementation)

        Args:
            text: Full text
            query: User query
            max_chunks: Maximum number of chunks to return

        Returns:
            Text with the most relevant chunks
        """
        chunks = self.chunk_text(text)

        # If text is small, return everything
        if len(chunks) <= max_chunks:
            return text

        # Simple implementation: returns chunks containing query words
        query_words = set(query.lower().split())
        scored_chunks = []

        for chunk in chunks:
            chunk_words = set(chunk.lower().split())
            # Score based on number of query words present in chunk
            score = len(query_words.intersection(chunk_words))
            scored_chunks.append((score, chunk))

        # Sort by score and return top chunks
        scored_chunks.sort(reverse=True, key=lambda x: x[0])
        relevant_chunks = [chunk for _, chunk in scored_chunks[:max_chunks]]

        return "\n\n".join(relevant_chunks)

    def summarize_document(self, text: str, max_length: int = DOCUMENT_SUMMARY_LENGTH) -> str:
        """
        Creates a summary of the document
        (Returns first characters as simple preview)

        Args:
            text: Full text
            max_length: Maximum summary length

        Returns:
            Document summary
        """
        if len(text) <= max_length:
            return text

        # Try to cut at a complete sentence
        truncated = text[:max_length]
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.8:  # If found a period in the last 20%
            return truncated[:last_period + 1]

        return truncated + "..."
