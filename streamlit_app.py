"""
Multi-LLM ChatBot for Document Analysis
Streamlit Interface
"""
import streamlit as st
from dotenv import load_dotenv
import os
from src.llm_manager import LLMManager
from src.document_processor import DocumentProcessor
from src.chat_handler import ChatHandler

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ChatBot Multi-LLM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    with open('.streamlit/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    pass  # CSS file optional - app will work without it


def initialize_session_state():
    """Initializes session state"""
    if 'llm_manager' not in st.session_state:
        st.session_state.llm_manager = LLMManager()
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()
    if 'chat_handler' not in st.session_state:
        st.session_state.chat_handler = ChatHandler()
    if 'llm_configured' not in st.session_state:
        st.session_state.llm_configured = False

    # Initialize theme
    if 'theme' not in st.session_state:
        st.session_state.theme = {
            "current": "dark",
            "refreshed": True,
            "dark": {
                "theme.base": "dark",
                "theme.backgroundColor": "#0E1117",
                "theme.secondaryBackgroundColor": "#262730",
                "theme.primaryColor": "#FF4B4B",
                "theme.textColor": "#FAFAFA",
                "button_face": "🌜"
            },
            "light": {
                "theme.base": "light",
                "theme.backgroundColor": "#FFFFFF",
                "theme.secondaryBackgroundColor": "#F0F2F6",
                "theme.primaryColor": "#FF4B4B",
                "theme.textColor": "#262730",
                "button_face": "🌞"
            }
        }


def toggle_theme():
    """Toggles between light and dark theme"""
    current = st.session_state.theme["current"]
    new_theme = "light" if current == "dark" else "dark"

    # Apply new theme configuration
    theme_config = st.session_state.theme[new_theme]
    for key, value in theme_config.items():
        if key.startswith("theme"):
            st._config.set_option(key, value)

    # Update state
    st.session_state.theme["current"] = new_theme
    st.session_state.theme["refreshed"] = False


def sidebar():
    """Renders sidebar with settings"""
    with st.sidebar:
        st.title("⚙️ Settings")

        # LLM status indicator (always visible)
        # Safe validation: checks state but doesn't cause side-effects before widgets
        current_provider = st.session_state.get('current_provider', None)
        llm_is_valid = st.session_state.llm_configured

        # If configured with Ollama, validate connection (but don't modify state yet)
        if llm_is_valid and current_provider == "ollama":
            if not LLMManager.check_ollama_status():
                llm_is_valid = False
                # Mark for reconfiguration later (not now, to avoid KeyError)
                st.session_state.setdefault('_needs_revalidation', True)

        if llm_is_valid:
            st.success("✅ LLM Configured and Ready!")
        else:
            st.warning("⚠️ LLM not configured")
            # Reconfigure now that it's safe
            if st.session_state.get('_needs_revalidation', False):
                st.session_state.llm_configured = False
                st.session_state._needs_revalidation = False

        st.divider()

        # Provider Selection
        st.subheader("1. Choose LLM")
        available_models = LLMManager.get_available_models()

        provider = st.selectbox(
            "Provider",
            options=list(available_models.keys()),
            format_func=lambda x: x.upper(),
            key="provider_select"
        )

        # Model Selection - DYNAMIC FETCH when possible
        if provider == "ollama":
            # Always check Ollama status
            installed_models, ollama_running = LLMManager.get_ollama_models()

            if ollama_running and installed_models:
                model_options = installed_models
                st.success(f"✅ Ollama active - {len(installed_models)} model(s)")
            elif not ollama_running:
                model_options = available_models[provider]
                st.error("❌ Ollama is not running. Execute: `ollama serve`")
                # If it was configured but Ollama died, warn (safe use of .get())
                if st.session_state.llm_configured and st.session_state.get('current_provider') == "ollama":
                    st.warning("⚠️ Connection lost! Check Ollama service.")
            else:
                model_options = available_models[provider]
                st.warning("⚠️ No models installed. Execute: `ollama pull llama3.2`")

            # Refresh button
            if st.button("🔄 Refresh List", key="refresh_ollama"):
                st.rerun()

        elif provider in ["gemini", "groq"]:
            # For Gemini/Groq, REQUIRES API key to list models
            env_var = f"{provider.upper()}_API_KEY"
            temp_api_key = os.getenv(env_var, "")

            if not temp_api_key:
                # WITHOUT API KEY - DON'T show models (fixed logic!)
                st.error(f"❌ {provider.upper()} API key required to use this provider!")
                st.info(f"""
                    **How to configure:**
                    1. Get free API key (see links below)
                    2. Add to `.env` file: `{env_var}=your_key_here`
                    3. Restart the application
                """)
                # Non-functional placeholder
                model_options = [f"⚠️ Configure {env_var} first"]
            else:
                # WITH API KEY - dynamic fetch
                cache_key = f"{provider}_models_cache"
                if cache_key not in st.session_state or st.button(f"🔄 Refresh List {provider.upper()}", key=f"refresh_{provider}"):
                    with st.spinner(f"Fetching available {provider.upper()} models..."):
                        if provider == "gemini":
                            dynamic_models, success = LLMManager.get_gemini_models_dynamic(temp_api_key)
                        else:  # groq
                            dynamic_models, success = LLMManager.get_groq_models_dynamic(temp_api_key)

                        st.session_state[cache_key] = (dynamic_models, success)

                # Use cache if available
                if cache_key in st.session_state:
                    dynamic_models, success = st.session_state[cache_key]
                    if success:
                        model_options = dynamic_models
                        st.success(f"✅ {len(dynamic_models)} model(s) available via API")
                    else:
                        model_options = available_models[provider]
                        st.warning(f"⚠️ Failed to fetch models. Using default list ({len(model_options)} models)")
                else:
                    model_options = available_models[provider]
        else:
            model_options = available_models[provider]

        model = st.selectbox(
            "Model",
            options=model_options,
            key="model_select"
        )

        # API Key (if necessary)
        api_key = None
        if provider in ["gemini", "groq"]:
            st.subheader("2. API Key")
            env_var = f"{provider.upper()}_API_KEY"
            api_key = os.getenv(env_var, "")

            if api_key:
                # API key ALREADY configured in .env
                st.success(f"✅ {env_var} configured in .env")
                st.caption(f"First characters: {api_key[:15]}...")

                # Allow manual override if user wants
                if st.checkbox("Use another API key temporarily", key=f"override_{provider}"):
                    api_key_input = st.text_input(
                        f"API Key {provider.upper()} (temporary)",
                        type="password",
                        help=f"This key temporarily overrides the .env key"
                    )
                    if api_key_input:
                        api_key = api_key_input
            else:
                # WITHOUT API key in .env - request
                api_key_input = st.text_input(
                    f"API Key {provider.upper()}",
                    type="password",
                    help=f"Paste your {provider.upper()} API key here"
                )

                if api_key_input:
                    api_key = api_key_input

                # Warning if no API key
                if not api_key:
                    st.error("❌ API key required to continue!")

            # Useful links (always show)
            if provider == "gemini":
                st.markdown("[📝 Get Gemini API Key (free)](https://makersuite.google.com/app/apikey)")
            elif provider == "groq":
                st.markdown("[📝 Get Groq API Key (free)](https://console.groq.com)")

        # Button to configure
        st.subheader("3. Activate")

        # Determine if can configure
        can_configure = True
        if provider in ["gemini", "groq"] and not api_key:
            can_configure = False

        if st.button(
            "🚀 Configure LLM" if not st.session_state.llm_configured else "🔄 Reconfigure LLM",
            type="primary",
            use_container_width=True,
            disabled=not can_configure
        ):
            with st.spinner("Configuring..."):
                success = st.session_state.llm_manager.configure(provider, model, api_key)
                if success:
                    st.session_state.llm_configured = True
                    st.session_state.current_provider = provider
                    st.session_state.current_model = model
                    st.balloons()  # Visual celebration!
                    st.rerun()
                else:
                    st.session_state.llm_configured = False
                    if provider == "ollama":
                        st.error("❌ Error: Check if Ollama is running (`ollama serve`)")
                    else:
                        st.error("❌ Error: Check the API key")

        # Show current configuration
        if st.session_state.llm_configured:
            if hasattr(st.session_state, 'current_provider'):
                st.caption(f"📡 Using: {st.session_state.current_provider.upper()} - {st.session_state.current_model}")

        st.divider()

        # Document Upload
        st.subheader("📄 Document")
        uploaded_file = st.file_uploader(
            "Upload file",
            type=['txt', 'pdf'],
            help="Upload a TXT or PDF file for analysis"
        )

        if uploaded_file is not None:
            if st.button("📤 Process Document", use_container_width=True):
                with st.spinner("Processing document..."):
                    try:
                        text, metadata = st.session_state.doc_processor.process_uploaded_file(uploaded_file)
                        st.session_state.chat_handler.set_document_context(text, metadata)
                        st.success("✅ Document processed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        # Document information
        if st.session_state.chat_handler.has_document():
            metadata = st.session_state.chat_handler.get_document_metadata()
            st.info(f"""
                **Active Document:**
                - Name: {metadata.get('filename', 'N/A')}
                - Type: {metadata.get('type', 'N/A').upper()}
                - Words: {metadata.get('words', 'N/A')}
                {f"- Pages: {metadata.get('pages')}" if 'pages' in metadata else ''}
            """)

            if st.button("🗑️ Remove Document", use_container_width=True):
                st.session_state.chat_handler.clear_document()
                st.rerun()

        st.divider()

        # Additional actions
        st.subheader("🔧 Actions")

        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat_handler.clear_messages()
            st.rerun()

        if st.session_state.chat_handler.get_messages():
            if st.button("💾 Export Conversation", use_container_width=True):
                export = st.session_state.chat_handler.export_conversation()
                st.download_button(
                    label="⬇️ Download",
                    data=export,
                    file_name="conversation_export.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        st.divider()

        # Information
        with st.expander("ℹ️ About"):
            st.markdown("""
                **ChatBot Multi-LLM**

                Gen AI demonstration project that supports:
                - 🤖 Multiple LLMs (Gemini, Groq, Ollama)
                - 📄 TXT/PDF document analysis
                - 💬 Interactive chat

                Built with Streamlit, LangChain, and UV.
            """)


def main_chat():
    """Renders main chat area"""
    # Header with theme toggle
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.markdown('<div class="main-header">🤖 ChatBot Multi-LLM</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Analyze documents with AI</div>', unsafe_allow_html=True)
    with col2:
        # Theme toggle
        current_theme = st.session_state.theme["current"]
        button_emoji = st.session_state.theme[current_theme]["button_face"]
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing for alignment
        if st.button(button_emoji, key="theme_toggle", help="Toggle light/dark theme"):
            toggle_theme()

    # Check if rerun needed after theme change
    if not st.session_state.theme["refreshed"]:
        st.session_state.theme["refreshed"] = True
        st.rerun()

    # Check configuration
    if not st.session_state.llm_configured:
        st.warning("⚠️ Configure an LLM model in the sidebar to start.")
        st.info("""
            **How to use:**
            1. Select a provider (Gemini, Groq or Ollama) in the sidebar
            2. Choose a model
            3. Add your API key (if necessary)
            4. Click 'Configure LLM'
            5. (Optional) Upload a document for analysis
            6. Start chatting!
        """)
        return

    # Message history
    messages = st.session_state.chat_handler.get_messages()

    # Message container
    chat_container = st.container()

    with chat_container:
        if not messages:
            st.info("👋 Hello! How can I help you? Upload a document or ask a question.")
        else:
            for msg in messages:
                with st.chat_message(msg['role']):
                    st.markdown(msg['content'])

    # User input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.chat_handler.add_message('user', prompt)

        # Show user message
        with chat_container:
            with st.chat_message('user'):
                st.markdown(prompt)

        # Generate response
        with chat_container:
            with st.chat_message('assistant'):
                message_placeholder = st.empty()
                full_response = ""

                # Get document context if available
                context = st.session_state.chat_handler.get_document_context()

                # Stream response
                try:
                    for chunk in st.session_state.llm_manager.stream_response(prompt, context):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)

                except Exception as e:
                    full_response = f"❌ Error generating response: {str(e)}"
                    message_placeholder.markdown(full_response)

                # Add response to history
                st.session_state.chat_handler.add_message('assistant', full_response)


def main():
    """Main function"""
    initialize_session_state()
    sidebar()
    main_chat()


if __name__ == "__main__":
    main()
