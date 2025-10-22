# Changelog

## Version 0.6.0 - Production Readiness (2025-10-22)

### 🔴 Critical Fixes

**Legal & Licensing:**
- ✅ **Added MIT LICENSE file** - Repository now has proper open-source licensing
  - Includes copyright notice and full MIT license text
  - Aligns with README.md license declaration

**Documentation Accuracy:**
- ✅ **Fixed URL placeholders** - Replaced hardcoded "your-username" with clear `<YOUR_GITHUB_USERNAME>` variable
  - Updated README.md, DEPLOYMENT.md, CONTRIBUTING.md
  - Added explanatory notes for users to replace placeholders
- ✅ **Removed broken references** - Fixed documentation pointing to non-existent files
  - CLAUDE.md: Updated reference from `README_HUGGINGFACE.md` to `README.md`
  - CLAUDE.md: Updated reference from `README_DEPLOY.md` to `DEPLOYMENT.md`

**Dependency Management:**
- ✅ **Clarified multi-LLM dependency strategy** - Documented local vs cloud approach
  - `pyproject.toml`: Includes ALL LLMs (Gemini, Groq, Ollama) for full local development
  - `requirements.txt`: Cloud-only LLMs (Gemini, Groq) for HF Spaces deployment
  - Added inline comments explaining separation strategy
  - Maintains true "Multi-LLM" promise: `uv sync` gives full offline capabilities

**Security & Robustness:**
- ✅ **Added file size validation** - Prevents crashes from oversized uploads
  - `document_processor.py`: Validates file size before processing
  - TXT files: 10MB limit
  - PDF files: 50MB limit
  - Clear error messages with size limits displayed to users

**Version Control:**
- ✅ **Updated .gitignore for uv.lock** - Prevents version lock conflicts
  - Uncommented `uv.lock` exclusion
  - Added explanatory comment about cross-environment compatibility

---

### 🟡 Quality Improvements

**Code Quality:**
- ✅ **Replaced print() with structured logging** - Professional error handling
  - Added `logging` module to `llm_manager.py`
  - Replaced 8 print statements with appropriate log levels (error, warning, info)
  - Improves debugging and production monitoring

**Configuration Management:**
- ✅ **Created centralized config module** - Eliminated magic numbers
  - New file: `src/config.py` with all constants
  - Extracted: `CHUNK_SIZE=1000`, `CHUNK_OVERLAP=200`, `MAX_CHUNKS_FOR_QUERY=3`
  - Added: `MAX_FILE_SIZE_TXT=10MB`, `MAX_FILE_SIZE_PDF=50MB`
  - Added: `DEFAULT_LLM_TEMPERATURE=0.7`, `DEFAULT_MAX_TOKENS=2000`
  - Updated all modules to import from config

**Internationalization:**
- ✅ **Translated example document to English** - Consistency with codebase
  - `examples/exemplo_documento.txt` → `examples/example_document.txt`
  - Content about Gen AI fully translated
  - Maintains educational quality

**Frontend Architecture:**
- ✅ **Moved inline CSS to separate file** - Better code organization
  - Created `.streamlit/style.css` with all custom styles
  - `streamlit_app.py`: Loads CSS from file with graceful fallback
  - Easier to maintain and customize UI

**Module Structure:**
- ✅ **Improved src/__init__.py** - Better package interface
  - Added `__version__ = "0.6.0"` and `__author__`
  - Exported main classes: `LLMManager`, `DocumentProcessor`, `ChatHandler`
  - Exported utility functions: `is_huggingface_space`, `is_ollama_supported`
  - Added `__all__` for explicit public API
  - Enables cleaner imports: `from src import LLMManager`

**Documentation:**
- ✅ **Enhanced packages.txt documentation** - Clear usage guidelines
  - Comprehensive comments explaining purpose
  - Examples of when system packages are needed
  - Format instructions and common package examples
  - Explains why file is currently empty

- ✅ **Reorganized requirements.txt** - Professional dependency management
  - Added clear header and section organization
  - Inline comments for each package explaining purpose
  - Notes section explaining Ollama exclusion
  - Instructions for local development vs HF Spaces

---

### 📊 Impact Summary

| Category | Changes |
|----------|---------|
| **Files Created** | 3 (LICENSE, src/config.py, .streamlit/style.css) |
| **Files Modified** | 11 (README, DEPLOYMENT, CONTRIBUTING, CLAUDE, pyproject.toml, .gitignore, streamlit_app, llm_manager, document_processor, __init__, packages.txt, requirements.txt) |
| **Files Renamed** | 1 (exemplo_documento.txt → example_document.txt) |
| **Lines Changed** | ~400 |
| **Critical Issues Fixed** | 6 |
| **Quality Improvements** | 7 |

---

### 🎯 Deployment Status

**Before v0.6.0:**
- ❌ No LICENSE file
- ❌ Broken documentation references
- ❌ Hardcoded placeholders in docs
- ❌ No file upload size limits (crash risk)
- ❌ Print statements instead of logging
- ❌ Magic numbers scattered in code
- ❌ Inline CSS mixed with Python
- ⚠️ Conflicting Ollama dependencies

**After v0.6.0:**
- ✅ **Production-ready for GitHub**
- ✅ **Production-ready for Hugging Face Spaces**
- ✅ **Professional code quality**
- ✅ **Complete documentation**
- ✅ **Robust error handling**
- ✅ **Maintainable architecture**

---

## Version 0.5.0 - Pre-Deployment Preparation (2025-10-21)

### 📚 Documentation Overhaul

**Complete English Translation:**
- ✅ All Python source files translated to English (docstrings, comments)
- ✅ Streamlit UI fully translated to English (buttons, labels, messages)
- ✅ `.env.example` comments translated

**New Comprehensive Documentation:**
- ✅ **README.md**: Complete rewrite with clear structure
  - Quick start guide for HF Spaces users
  - Local development setup instructions
  - Project structure and architecture
  - Multi-platform support table
  - Use cases and features overview
- ✅ **docs/DEPLOYMENT.md**: Consolidated deployment guide
  - One-time setup instructions
  - GitHub Actions workflow details
  - Secrets configuration (GitHub & HF)
  - Troubleshooting section
  - Platform differences explained
- ✅ **docs/CONTRIBUTING.md**: Contribution guidelines
  - Code of conduct
  - Development setup
  - Code style guidelines (PEP 8, docstrings, type hints)
  - Commit message format
  - Pull request process
  - Testing checklist

**Documentation Cleanup:**
- ❌ Removed duplicate/outdated docs:
  - `docs/PROXIMOS_PASSOS.md`
  - `docs/PROXIMOS_PASSOS_GH_HF.md`
  - `docs/GUIA_RAPIDO.md`
  - `docs/README_DEPLOY.md` (consolidated into DEPLOYMENT.md)
  - `docs/prompt.md`
  - `.github/SETUP_SECRETS.md` (consolidated into DEPLOYMENT.md)
- ❌ Removed test file: `txt.txt`
- ✅ Kept: `docs/PARA_CANDIDATURA.md` (user will manage), `docs/prompt_2.md`

### 💻 Code Improvements

**Translation to English:**
- All module docstrings and comments
- All function/class documentation
- All UI strings (Streamlit interface)
- Error messages and user feedback
- Configuration helpers and tooltips

**Files Translated:**
- `src/llm_manager.py`
- `src/document_processor.py`
- `src/chat_handler.py`
- `src/platform_utils.py`
- `streamlit_app.py`

**Code Quality:**
- Following Python/Streamlit conventions
- Clear, descriptive variable names
- Comprehensive docstrings with Args/Returns
- Type hints for function signatures

### 📝 Dependency Management

**requirements.txt:**
- Added clear section comments
- Organized by category (Web Framework, LLM Providers, etc.)
- Added inline comments for each package
- Noted Ollama exclusion (local-only)

**packages.txt:**
- Clarified purpose (HF Spaces system packages)
- Explained why currently empty
- Added examples for future reference
- Clear English documentation

### 🗑️ Project Cleanup

**Removed Files:**
- `txt.txt` - test file
- `docs/prompt.md` - no longer needed
- `docs/PROXIMOS_PASSOS.md` - superseded
- `docs/PROXIMOS_PASSOS_GH_HF.md` - superseded
- `docs/GUIA_RAPIDO.md` - content integrated into README
- `docs/README_DEPLOY.md` - consolidated into DEPLOYMENT.md
- `.github/SETUP_SECRETS.md` - consolidated into DEPLOYMENT.md

### 🎯 Deployment Readiness

**Ready for:**
- ✅ Public GitHub repository
- ✅ Hugging Face Spaces deployment
- ✅ Open-source contributions
- ✅ Global audience (English documentation)
- ✅ Professional presentation

**Repository Structure:**
```
genai-doc-chatbot/
├── README.md                    ✨ NEW (comprehensive English)
├── CHANGELOG.md                 📝 UPDATED (this entry)
├── CLAUDE.md                    ✅ (unchanged)
├── .env.example                 🌍 (English)
├── requirements.txt             ✅ (validated, commented)
├── packages.txt                 ✅ (validated, documented)
├── streamlit_app.py             🌍 (English)
├── src/                         🌍 (all English)
├── docs/
│   ├── DEPLOYMENT.md            ✨ NEW (consolidated guide)
│   ├── CONTRIBUTING.md          ✨ NEW (guidelines)
│   ├── PARA_CANDIDATURA.md      ✅ (kept, Portuguese)
│   └── prompt_2.md              ✅ (kept, user manages)
└── .github/workflows/           ✅ (unchanged)
```

### 📊 Impact Summary

| Category | Before | After |
|----------|--------|-------|
| **Language** | Mixed PT/EN | ✅ Fully English |
| **Documentation** | 7+ scattered files | ✅ 3 clear, focused docs |
| **Code comments** | Portuguese | ✅ English |
| **UI strings** | Portuguese | ✅ English |
| **Dependencies** | Uncommented list | ✅ Organized with comments |
| **Project structure** | Cluttered | ✅ Clean, professional |

### 🚀 Next Steps

After this version:
1. Push to GitHub repository
2. Configure GitHub secrets for HF deployment
3. Create Hugging Face Space
4. Test automatic deployment workflow
5. Verify application works on HF Spaces
6. Share with global audience

---

## Version 0.4.0 - Toggle de Tema Dark/Light (2025-10-21)

### ✨ Nova Funcionalidade: Alternância de Tema Visível

#### Motivação
- App estava em modo claro por padrão (cansativo para a vista)
- Menu nativo do Streamlit (⚙️ > Settings > Theme) não é intuitivo
- Necessidade de toggle visível e acessível no frontend

#### Solução Implementada

**Toggle Visual no Header:**
- Botão no canto superior direito da área principal
- 🌜 quando em modo escuro (representa "night mode")
- 🌞 quando em modo claro (representa "day mode")
- Tooltip: "Alternar tema claro/escuro"

**Comportamento:**
- Tema escuro como padrão inicial
- Clique alterna instantaneamente entre temas
- Preferência persiste durante a sessão
- Auto-rerun para aplicar mudanças

#### Decisões de UX

**Posicionamento:**
- Header principal (não na sidebar)
- Separado das configurações do chatbot (LLM/documentos)
- Máxima visibilidade, sempre acessível

**Lógica do Ícone:**
- ✅ Ícone representa o **tema atual** (não o destino)
- Segue convenções de apps modernas (GitHub, VS Code, Twitter)
- Intuitivo: vê lua → está escuro, vê sol → está claro

#### Implementação Técnica

**Ficheiros modificados:**

1. **`.streamlit/config.toml`:**
   - Tema escuro como base padrão
   - Cores: `backgroundColor: #0E1117`, `textColor: #FAFAFA`

2. **`streamlit_app.py`:**
   - `initialize_session_state()`: Dicionários com configs dos 2 temas
   - `toggle_theme()`: Aplica tema via `st._config.set_option()` + rerun
   - `main_chat()`: Layout com `st.columns([0.85, 0.15])` para header + toggle

**Estado em `session_state`:**
```python
theme = {
    "current": "dark",  # ou "light"
    "refreshed": True,
    "dark": {...},      # config tema escuro
    "light": {...}      # config tema claro
}
```

#### Correção de Lógica
- **Versão inicial (incorreta)**: Modo escuro mostrava 🌞
- **Corrigido**: Modo escuro mostra 🌜 (representa estado atual)

### 📊 Resultado

| Aspeto | Antes | Agora |
|--------|-------|-------|
| **Tema padrão** | Claro (cansativo) | ✅ Escuro (confortável) |
| **Alternar tema** | Menu escondido ⚙️ | ✅ Toggle visível no header |
| **UX** | Não intuitivo | ✅ Ícone representa estado atual |
| **Localização** | Misturado com configs | ✅ Separado (header principal) |
| **Persistência** | Browser | ✅ Sessão (session_state) |

## Versão 0.3.1 - Correção Lógica API Keys (2025-10-21)

### 🐛 Bug Corrigido: Listagem sem API Key

#### Problema
App mostrava lista de modelos Gemini/Groq mesmo sem API key configurada, mas não conseguia usá-los. Criava falsa expectativa.

#### Correção
- ❌ SEM API key: Não mostra modelos, exibe erro claro
- ✅ COM API key: Busca modelos dinamicamente via API
- ✅ Validação ocorre ANTES de mostrar opções
- ✅ Mensagem clara de como configurar

#### Interface Melhorada
**Quando SEM API key:**
```
❌ API key GEMINI necessária para usar este provider!

Como configurar:
1. Obtenha API key gratuita (ver links abaixo)
2. Adicione ao ficheiro .env: GEMINI_API_KEY=sua_chave_aqui
3. Reinicie a aplicação

Modelo: [⚠️ Configure GEMINI_API_KEY primeiro]
```

**Quando COM API key no .env:**
```
✅ GEMINI_API_KEY configurada no .env
Primeiros caracteres: AIzaSyA626z11CR...
☐ Usar outra API key temporariamente
```

## Versão 0.3.0 - Busca Dinâmica de Modelos (2025-10-21)

### ✨ Nova Funcionalidade: Listagem Dinâmica de Modelos

#### Problema Original
- Erro 404: `gemini-1.5-pro-latest is not found`
- Modelos hard-coded ficavam desatualizados
- Gemini 1.5 descontinuado, substituído por 2.0 e 2.5

#### Solução Implementada

**Busca Automática via API:**
- ✅ **Gemini**: `genai.list_models()` busca modelos disponíveis
- ✅ **Groq**: `client.models.list()` busca modelos disponíveis
- ✅ **Ollama**: Já funcionava (mantido)

**Funcionalidades:**
1. Busca modelos direto da API quando API key disponível
2. Cache de resultados para performance
3. Botão "🔄 Atualizar Lista" para refresh manual
4. Fallback para lista padrão se API falhar
5. Indicador visual: "✅ X modelo(s) disponível(is) via API"

**Modelos Atualizados (Gemini):**
- ❌ `gemini-1.5-pro-latest` (removido - descontinuado)
- ❌ `gemini-1.5-flash-latest` (removido - descontinuado)
- ✅ `gemini-2.5-flash-lite` (novo - rápido, baixo custo)
- ✅ `gemini-2.5-flash` (novo - estável)
- ✅ `gemini-2.5-pro` (novo - melhor qualidade)
- ✅ `gemini-2.0-flash-exp` (mantido - experimental)

### 📊 Benefícios

| Aspeto | Antes (v0.2.2) | Agora (v0.3.0) |
|--------|----------------|----------------|
| **Modelos** | Hard-coded, desatualizados | ✅ Busca dinâmica da API |
| **Erros 404** | ❌ Possível | ✅ Impossível |
| **Novos modelos** | Precisa atualizar código | ✅ Aparecem automaticamente |
| **Validação API Key** | Só no uso | ✅ Valida ao listar modelos |
| **Performance** | N/A | ✅ Cache de resultados |

### 🔧 Implementação Técnica

**Novas funções em `llm_manager.py`:**
```python
get_gemini_models_dynamic(api_key) -> (modelos, sucesso)
get_groq_models_dynamic(api_key) -> (modelos, sucesso)
```

**Atualização em `streamlit_app.py`:**
- Deteta API key do `.env` automaticamente
- Busca modelos com spinner de loading
- Cache em `session_state` para evitar chamadas repetidas
- Botão refresh por provider

## Versão 0.2.2 - Correção KeyError + Rename (2025-10-21)

### 🐛 Bug Corrigido: KeyError no Session State

#### Problema
```
KeyError: 'st.session_state has no key "$WIDGET_ID-..."'
```
- **Causa**: Validação contínua modificava `session_state` antes dos widgets renderizarem
- **Efeito**: App crashava ao carregar

#### Correção
- Uso de `st.session_state.get()` com defaults seguros
- Validação não causa side-effects antes dos widgets
- Flag `_needs_revalidation` para desconfigurar após widgets criados

### 📝 Renomeação: app.py → streamlit_app.py

#### Por que mudar?
- ✅ **Convenção oficial** do Streamlit
- ✅ **Hugging Face** reconhece automaticamente
- ✅ **Streamlit Cloud** detecta sem configuração
- ✅ Comando mais simples: `streamlit run .`

#### Ficheiros atualizados
- `app.py` → `streamlit_app.py`
- Toda a documentação (5 ficheiros .md)
- README, GUIA_RAPIDO, PROXIMOS_PASSOS, etc.

## Versão 0.2.1 - Correção Crítica Ollama (2025-10-21)

### 🐛 Bug Crítico Corrigido

#### Problema: API Ollama mudou e parou de funcionar
- **Causa**: Módulo `ollama` Python mudou estrutura de retorno em versão recente
- **Sintoma**: `get_ollama_models()` falhava com `KeyError: 'name'`
- **Impacto**: App mostrava "Ollama não está a correr" mesmo com serviço ativo

#### Correção Implementada
```python
# ANTES (não funcionava):
models = ollama.list()
installed = [model['name'].split(':')[0] for model in models['models']]

# AGORA (corrigido):
result = ollama.list()  # Retorna objeto ListResponse
for model in result.models:  # .models é lista de objetos Model
    model_name = model.model  # Usar .model em vez de ['name']
```

### ✅ Validação Contínua de Estado

#### Problema: Estado inconsistente
- **Antes**: Badge dizia "Configurado" mas Ollama não conectava
- **Causa**: Estado `llm_configured` guardado mas nunca re-validado

#### Solução
- Validação automática em cada render para provider Ollama
- Auto-desconfigura se conexão for perdida
- Aviso específico: "⚠️ Conexão perdida! Verifique o serviço Ollama."

### 📊 Resultado

| Situação | Antes | Agora |
|----------|-------|-------|
| Ollama ativo | ❌ "não está a correr" | ✅ "ativo - 12 modelos" |
| Estado badge | ✅ verde (mas falso) | ✅ verde (validado) |
| Ollama cai | ✅ verde (inconsistente) | ⚠️ amarelo + aviso |
| Re-conecta | Manual reconfig | ✅ Auto-deteta |

## Versão 0.2.0 - Melhorias de UX (2025-10-21)

### 🎨 Melhorias de Interface

#### Indicador de Estado Sempre Visível
- **Antes**: Não era claro se o LLM estava configurado
- **Agora**: Badge verde "✅ LLM Configurado e Pronto!" no topo da sidebar
- **Benefício**: Utilizador sabe sempre o estado da aplicação

#### Botão "Configurar LLM" Melhorado
- **Antes**: Botão não dava feedback claro, confuso se funcionou
- **Agora**:
  - Muda para "🔄 Reconfigurar LLM" quando já configurado
  - Mostra balões animados quando sucesso
  - Mensagens de erro específicas por provider
  - Fica desativado se falta API key
- **Benefício**: Feedback visual claro e imediato

#### Deteção de Modelos Ollama
- **Antes**: Dizia "nenhum modelo instalado" mesmo com modelos presentes
- **Agora**:
  - Deteta corretamente se Ollama está a correr
  - Lista modelos instalados quando ativo
  - Mensagens específicas: "Ollama não está a correr" vs "Nenhum modelo instalado"
  - Botão "🔄 Atualizar Lista" para refresh manual
- **Benefício**: Diagnóstico claro de problemas

#### Informação de Configuração Atual
- **Novo**: Mostra provider e modelo em uso: "📡 Usando: OLLAMA - llama3.2"
- **Benefício**: Utilizador sabe exatamente qual LLM está a usar

### 🔧 Melhorias Técnicas

#### LLMManager
- Nova função `get_ollama_models()` retorna tupla `(modelos, está_ativo)`
- Nova função `check_ollama_status()` para verificar serviço
- Melhor error handling em todas as operações Ollama

#### App.py
- Estado da aplicação mais robusto
- Validação de API keys antes de permitir configuração
- Mensagens de erro contextualizadas por provider

### 📋 Problemas Corrigidos

1. ✅ Ollama não detetava modelos instalados
2. ✅ Botão "Configurar LLM" sem feedback
3. ✅ Não era claro quando LLM estava pronto
4. ✅ Erro genérico sem informação útil

### 🎯 Melhorias de UX em Resumo

| Aspeto | Antes | Agora |
|--------|-------|-------|
| **Estado do LLM** | Invisível | Badge sempre visível no topo |
| **Feedback ao configurar** | Nenhum | Balões + mensagem + rerun |
| **Deteção Ollama** | Falhava silenciosamente | Diagnóstico claro do problema |
| **Botão configurar** | Sempre "Configurar" | Muda para "Reconfigurar" |
| **Erro sem API key** | Permitia clicar | Botão desativado |
| **Info atual** | Nenhuma | Mostra provider/modelo em uso |

## Versão 0.1.0 - Release Inicial (2025-10-21)

### Funcionalidades
- Suporte multi-LLM (Gemini, Groq, Ollama)
- Processamento de documentos TXT/PDF
- Chat com streaming
- Interface Streamlit
- Exportação de conversas
- Documentação completa
