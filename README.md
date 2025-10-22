---
title: Multi-LLM Document Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.40.0"
app_file: streamlit_app.py
pinned: false
license: mit
---

# Multi-LLM Document Chatbot

[![Deploy to HF](https://github.com/diogo-costa-silva/genai-doc-chatbot/actions/workflows/deploy-to-huggingface.yml/badge.svg)](https://github.com/diogo-costa-silva/genai-doc-chatbot/actions/workflows/deploy-to-huggingface.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An intelligent chatbot that analyzes TXT and PDF documents using multiple Large Language Models (LLMs).

> **🚀 Automatic Deployment:** This project automatically syncs from GitHub to Hugging Face Spaces via GitHub Actions.

## ✨ Features

- **Multiple LLMs**: Support for Google Gemini, Groq, and Ollama (local)
- **Document Analysis**: Upload and process TXT and PDF files
- **Intuitive Interface**: Streamlit-based UI with sidebar configuration
- **Summaries & Q&A**: Ask questions about your documents
- **Real-time Streaming**: Streaming responses for better UX
- **Automatic Platform Detection**: Adapts automatically between local and cloud environments
- **Dark/Light Theme**: Toggle between themes with visual button

## 🚀 Quick Start

### Using on Hugging Face Spaces

If you're using this project on **Hugging Face Spaces**:

1. **Configure an LLM in the sidebar**:
   - Choose between Google Gemini or Groq
   - Select a model
   - Add your API key (or use pre-configured ones in Secrets)
   - Click "🚀 Configure LLM"

2. **Upload a document (optional)**:
   - Click "Browse files" in the sidebar
   - Select a TXT or PDF file
   - Click "📤 Process Document"

3. **Start chatting**:
   - Type your question in the chat
   - The chatbot will respond based on the document context

### 🔑 Get Free API Keys

- **Google Gemini**: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) (1M tokens/month free)
- **Groq**: [console.groq.com](https://console.groq.com) (Free with rate limits)

---

## 💻 Local Development Setup

### Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) package manager (recommended)
- (Optional) [Ollama](https://ollama.ai) for local LLMs

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/genai-doc-chatbot.git
cd genai-doc-chatbot
```

> **Note**: Replace `<YOUR_GITHUB_USERNAME>` with your actual GitHub username.

2. **Install dependencies**

```bash
# Using UV (recommended)
uv sync

# OR using pip
pip install -r requirements.txt
```

3. **Configure API Keys**

Copy the `.env.example` file to `.env` and add your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file:
```env
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Groq
GROQ_API_KEY=your_groq_api_key_here

# Ollama (no API key needed, install locally)
```

4. **Run the application**

```bash
# Using UV
uv run streamlit run streamlit_app.py

# OR if you activated the virtual environment
streamlit run streamlit_app.py
```

Access the app at `http://localhost:8501`

### Optional: Install Ollama (Local LLMs)

For completely private, offline LLMs:

```bash
# macOS
brew install ollama

# Download a model
ollama pull llama3.2

# Start Ollama service (if not running)
ollama serve
```

---

## 📚 Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)**: Complete guide for deploying to Hugging Face Spaces
- **[Contributing](docs/CONTRIBUTING.md)**: Guidelines for contributing to the project
- **[Changelog](CHANGELOG.md)**: Project version history and changes

---

## 🏗️ Project Structure

```
genai-doc-chatbot/
├── streamlit_app.py              # Main Streamlit application
├── src/
│   ├── llm_manager.py            # Multi-LLM management
│   ├── document_processor.py     # Document processing (TXT/PDF)
│   ├── chat_handler.py           # Chat logic and history
│   └── platform_utils.py         # Platform detection utilities
├── docs/                         # Documentation
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
├── examples/                     # Example documents
│   └── exemplo_documento.txt
├── .github/
│   └── workflows/
│       └── deploy-to-huggingface.yml  # Auto-deployment workflow
├── .streamlit/
│   ├── config.toml               # Streamlit configuration
│   └── secrets.toml.example      # API keys template for Streamlit Cloud
├── pyproject.toml                # UV project configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

---

## 🌐 Deployment

### Streamlit Community Cloud (Recommended)

The **easiest way** to deploy this project:

**Quick Deploy (3 steps):**

1. **Sign in to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository and branch (`main`)
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configure API Keys**
   - In your app's dashboard, go to "⚙️ Settings" → "Secrets"
   - Paste the following (replace with your actual keys):

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
GROQ_API_KEY = "your_groq_api_key_here"
```

**That's it!** Your app will be live at `https://<your-app-name>.streamlit.app`

> 💡 **Tip**: Use `.streamlit/secrets.toml.example` as a template for your secrets.

---

### Hugging Face Spaces (Alternative)

This project also supports **automatic deployment** to Hugging Face Spaces:

**One-time setup:**
1. Create a Space on Hugging Face
2. Configure GitHub secrets (HF_TOKEN, HF_USERNAME, HF_SPACE_NAME)
3. Push to `main` branch → automatic deployment!

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for detailed instructions.

---

### Other Platforms

- **Railway / Render**: Requires Docker configuration
- **Google Cloud Run**: Requires containerization
- **AWS / Azure**: Requires cloud platform setup

---

## 🔧 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **LLMs**: Google Gemini, Groq, Ollama
- **Document Processing**: [LangChain](https://python.langchain.com), [PyPDF](https://github.com/py-pdf/pypdf)
- **Package Management**: [UV](https://github.com/astral-sh/uv)
- **CI/CD**: GitHub Actions
- **Deployment**: Hugging Face Spaces

---

## 🤖 Multi-Platform Architecture

The project uses **automatic platform detection** to adapt between environments:

| Feature | Local | Hugging Face Spaces |
|---------|-------|---------------------|
| Google Gemini | ✅ | ✅ |
| Groq | ✅ | ✅ |
| Ollama (Local) | ✅ | ❌ (requires local install) |

The code automatically detects the platform (`src/platform_utils.py`) and adapts the interface:
- **Local**: Shows all 3 providers (Gemini, Groq, Ollama)
- **Hugging Face**: Shows only Gemini and Groq

> **📝 Note**: The local version supports Ollama for completely private LLMs, but this feature is not available on Hugging Face Spaces due to cloud platform limitations.

---

## 🎯 Use Cases

- **Document Analysis**: Upload contracts, reports, or research papers and ask questions
- **Summarization**: Get quick summaries of long documents
- **Information Extraction**: Find specific information in large texts
- **Multi-Model Comparison**: Compare responses from different LLMs
- **Privacy-First AI**: Use Ollama for completely offline, private document analysis

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](docs/CONTRIBUTING.md) before submitting a PR.

Key areas for contribution:
- Additional document formats (DOCX, CSV, etc.)
- Embedding-based semantic search
- Vector database integration (Chroma, FAISS)
- Additional LLM providers
- UI/UX improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [LangChain](https://python.langchain.com)
- Package management by [UV](https://github.com/astral-sh/uv)
- LLM providers: Google Gemini, Groq, Ollama

---

## 📞 Support

If you encounter any issues:

1. Check the [Deployment Guide](docs/DEPLOYMENT.md) for common problems
2. Review [Issues](https://github.com/<YOUR_GITHUB_USERNAME>/genai-doc-chatbot/issues) for similar problems
3. Open a new issue with detailed information

---

**Made with ❤️ using Claude Code**
