# Contributing to Multi-LLM Document Chatbot

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for everyone, regardless of:
- Level of experience
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race, ethnicity, or nationality
- Age
- Religion

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment, trolling, or insulting comments
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could be considered inappropriate in a professional setting

---

## 🚀 How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
1. **Check existing issues** to avoid duplicates
2. **Use the latest version** of the project
3. **Test locally** to confirm the bug

**When reporting bugs, include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

**Example:**
```markdown
**Bug**: Ollama models not detected on macOS

**Steps to reproduce:**
1. Install Ollama via `brew install ollama`
2. Run `ollama pull llama3.2`
3. Start app with `streamlit run streamlit_app.py`
4. Select Ollama provider

**Expected:** Models should be listed
**Actual:** Shows "No models installed"

**Environment:**
- macOS 14.0
- Python 3.11
- Ollama 0.1.0
```

### Suggesting Features

Before suggesting a feature:
1. Check if it's already implemented
2. Review open/closed feature requests
3. Consider if it fits the project's scope

**When suggesting features, include:**
- Clear description of the feature
- Use case / problem it solves
- Possible implementation approach
- Alternative solutions you've considered

### Contributing Code

Areas where contributions are especially welcome:

**High Priority:**
- Additional document formats (DOCX, CSV, Markdown)
- Embedding-based semantic search
- Vector database integration (Chroma, FAISS, Pinecone)
- Improved chunking strategies
- Additional LLM providers (Anthropic, OpenAI, Cohere)

**Medium Priority:**
- UI/UX improvements
- Performance optimizations
- Better error handling
- Internationalization (i18n)
- Mobile responsiveness

**Nice to Have:**
- Additional export formats (JSON, Markdown)
- Document comparison features
- Batch document processing
- Custom prompt templates
- Usage analytics dashboard

---

## 💻 Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- [UV](https://github.com/astral-sh/uv) (recommended) or pip
- (Optional) Ollama for local testing

### Setup Instructions

1. **Fork the repository**

Click "Fork" on GitHub to create your own copy.

2. **Clone your fork**

```bash
git clone https://github.com/your-username/genai-doc-chatbot.git
cd genai-doc-chatbot
```

3. **Add upstream remote**

```bash
git remote add upstream https://github.com/original-owner/genai-doc-chatbot.git
```

4. **Install dependencies**

```bash
# Using UV (recommended)
uv sync

# OR using pip
pip install -r requirements.txt
```

5. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your API keys
```

6. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

7. **Run the application**

```bash
uv run streamlit run streamlit_app.py
```

---

## 📝 Code Style Guidelines

### Python Code Style

We follow **PEP 8** with some modifications:

**General Rules:**
- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)
- Use descriptive variable names
- Add docstrings to all functions and classes

**Docstring Format:**
```python
def process_document(file_path: str, chunk_size: int = 1000) -> tuple[str, dict]:
    """
    Processes a document and extracts its content.

    Args:
        file_path: Path to the document file
        chunk_size: Maximum size of text chunks (default: 1000)

    Returns:
        Tuple containing (full_text, metadata_dict)

    Raises:
        ValueError: If file format is not supported
    """
    # Implementation
```

**Imports:**
```python
# Standard library
import os
from typing import Optional, Generator

# Third-party
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Local
from src.llm_manager import LLMManager
from src.document_processor import DocumentProcessor
```

**Type Hints:**
- Use type hints for function parameters and return values
- Use `Optional[T]` for nullable types
- Use `tuple[str, dict]` for Python 3.10+ (not `Tuple`)

### Streamlit Code Style

**Structure:**
```python
def main():
    """Main application entry point"""
    initialize_session_state()
    render_sidebar()
    render_main_content()

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'llm_manager' not in st.session_state:
        st.session_state.llm_manager = LLMManager()

def render_sidebar():
    """Render sidebar with settings"""
    with st.sidebar:
        st.title("Settings")
        # Sidebar content
```

**Session State:**
- Always check if key exists before accessing
- Use descriptive key names
- Group related state together

### File Organization

```
src/
├── __init__.py           # Package initialization
├── llm_manager.py        # LLM abstraction layer
├── document_processor.py # Document handling
├── chat_handler.py       # Chat logic
└── platform_utils.py     # Platform detection
```

**Each module should:**
- Have a single, clear responsibility
- Include comprehensive docstrings
- Handle errors gracefully
- Be testable independently

---

## 💬 Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**Good:**
```
feat(llm): add support for Anthropic Claude

- Implement ClaudeProvider class
- Add API key configuration
- Update UI to show Claude option

Closes #42
```

```
fix(document): handle PDF extraction errors gracefully

- Add try-catch for corrupted PDFs
- Display user-friendly error message
- Log detailed error for debugging

Fixes #38
```

**Bad:**
```
Update stuff
```

```
Fixed bug
```

### Rules

- Use imperative mood ("add" not "added")
- First line max 72 characters
- Separate subject from body with blank line
- Reference issues in footer

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update from upstream**

```bash
git fetch upstream
git rebase upstream/main
```

2. **Test your changes**

- Run the app locally
- Test with different LLM providers
- Test document upload/processing
- Check for console errors

3. **Check code style**

```bash
# Format code (if using black)
black src/ streamlit_app.py

# Check style (if using flake8)
flake8 src/ streamlit_app.py
```

4. **Update documentation**

- Update README.md if adding features
- Add/update docstrings
- Update CHANGELOG.md

### Submitting

1. **Push to your fork**

```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request on GitHub**

- Use a clear, descriptive title
- Reference related issues
- Describe what changed and why
- Include screenshots for UI changes

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Tested with Gemini
- [ ] Tested with Groq
- [ ] Tested with Ollama
- [ ] Tested document upload

## Screenshots (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Added/updated docstrings
- [ ] Updated README.md (if needed)
- [ ] Updated CHANGELOG.md
```

3. **Respond to feedback**

- Address review comments
- Make requested changes
- Update the PR

### After Merge

1. **Delete your branch**

```bash
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

2. **Update your fork**

```bash
git checkout main
git pull upstream main
git push origin main
```

---

## 🧪 Testing

### Manual Testing Checklist

Before submitting:

**LLM Configuration:**
- [ ] Gemini provider works
- [ ] Groq provider works
- [ ] Ollama provider works (local only)
- [ ] API key validation works
- [ ] Error messages are clear

**Document Processing:**
- [ ] TXT files upload correctly
- [ ] PDF files upload correctly
- [ ] Large files handled properly
- [ ] Invalid files show errors
- [ ] Document metadata displays correctly

**Chat Functionality:**
- [ ] Messages send successfully
- [ ] Streaming responses work
- [ ] Context is maintained
- [ ] Chat can be cleared
- [ ] Conversation export works

**UI/UX:**
- [ ] Dark theme works
- [ ] Light theme works
- [ ] Layout is responsive
- [ ] No console errors
- [ ] Buttons provide feedback

### Future: Automated Testing

We plan to add:
- Unit tests for core modules
- Integration tests for LLM providers
- End-to-end tests for workflows

---

## ❓ Questions?

- **General questions**: Open a [Discussion](https://github.com/<YOUR_GITHUB_USERNAME>/genai-doc-chatbot/discussions)
- **Bug reports**: Open an [Issue](https://github.com/<YOUR_GITHUB_USERNAME>/genai-doc-chatbot/issues)
- **Feature requests**: Open an [Issue](https://github.com/<YOUR_GITHUB_USERNAME>/genai-doc-chatbot/issues) with [Feature Request] tag

---

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

**Happy coding! 🚀**
