"""
Chat conversation and history manager
"""
from typing import Optional
from datetime import datetime


class ChatHandler:
    """Manages conversation history and context"""

    def __init__(self):
        self.messages = []
        self.document_context = None
        self.document_metadata = None

    def add_message(self, role: str, content: str):
        """
        Adds message to history

        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })

    def get_messages(self) -> list:
        """
        Returns all messages

        Returns:
            List of messages
        """
        return self.messages

    def clear_messages(self):
        """Clears message history"""
        self.messages = []

    def set_document_context(self, text: str, metadata: dict):
        """
        Sets the current document context

        Args:
            text: Full document text
            metadata: Document metadata
        """
        self.document_context = text
        self.document_metadata = metadata

    def get_document_context(self) -> Optional[str]:
        """
        Returns document context

        Returns:
            Document text or None
        """
        return self.document_context

    def get_document_metadata(self) -> Optional[dict]:
        """
        Returns document metadata

        Returns:
            Dictionary with metadata or None
        """
        return self.document_metadata

    def has_document(self) -> bool:
        """
        Checks if a document is loaded

        Returns:
            True if document exists, False otherwise
        """
        return self.document_context is not None

    def clear_document(self):
        """Removes current document"""
        self.document_context = None
        self.document_metadata = None

    def get_conversation_summary(self) -> str:
        """
        Generates conversation summary

        Returns:
            String with conversation summary
        """
        if not self.messages:
            return "No messages yet."

        user_messages = sum(1 for m in self.messages if m['role'] == 'user')
        assistant_messages = sum(1 for m in self.messages if m['role'] == 'assistant')

        summary = f"Conversation with {user_messages} question(s) and {assistant_messages} answer(s)"

        if self.has_document():
            doc_type = self.document_metadata.get('type', 'document').upper()
            filename = self.document_metadata.get('filename', 'document')
            summary += f"\nDocument: {filename} ({doc_type})"

        return summary

    def export_conversation(self) -> str:
        """
        Exports conversation in text format

        Returns:
            String with entire formatted conversation
        """
        export = []

        # Header
        export.append("=" * 60)
        export.append("CONVERSATION EXPORT")
        export.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        export.append("=" * 60)
        export.append("")

        # Document information
        if self.has_document():
            export.append("DOCUMENT:")
            for key, value in self.document_metadata.items():
                export.append(f"  {key}: {value}")
            export.append("")

        # Messages
        export.append("CONVERSATION:")
        export.append("-" * 60)
        for msg in self.messages:
            role = "YOU" if msg['role'] == 'user' else "ASSISTANT"
            timestamp = msg['timestamp']
            export.append(f"\n[{timestamp}] {role}:")
            export.append(msg['content'])
            export.append("-" * 60)

        return "\n".join(export)

    def get_context_for_llm(self, include_history: bool = False) -> Optional[str]:
        """
        Returns formatted context for LLM

        Args:
            include_history: Whether to include message history

        Returns:
            Formatted context or None
        """
        if not self.has_document():
            return None

        context_parts = [self.document_context]

        if include_history and self.messages:
            # Add recent messages as additional context
            recent_messages = self.messages[-6:]  # Last 3 interactions
            history = "\n\nRecent conversation history:\n"
            for msg in recent_messages:
                role = "User" if msg['role'] == 'user' else "Assistant"
                history += f"{role}: {msg['content']}\n"
            context_parts.append(history)

        return "\n\n".join(context_parts)
