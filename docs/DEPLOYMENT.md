# Deployment Guide: GitHub → Hugging Face Spaces

This guide explains how to deploy the Multi-LLM Document Chatbot to Hugging Face Spaces with automatic synchronization from GitHub.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [One-Time Setup](#one-time-setup)
- [Daily Workflow](#daily-workflow)
- [Configuration Details](#configuration-details)
- [Troubleshooting](#troubleshooting)
- [Alternative Platforms](#alternative-platforms)

---

## 🎯 Architecture Overview

```
GitHub Repository (single source of truth)
    ↓ (push to main)
GitHub Actions Workflow
    ↓ (automatic deployment)
Hugging Face Spaces (production)
```

**Benefits:**
- ✅ Single codebase in GitHub
- ✅ Automatic deployment on every commit
- ✅ Works locally (with Ollama) and on HF (without Ollama)
- ✅ Zero maintenance of duplicate repositories

---

## 🔑 Prerequisites

Before starting, ensure you have:

1. **GitHub Account** with a repository for this project
2. **Hugging Face Account** ([sign up here](https://huggingface.co/join))
3. **GitHub CLI** (optional but recommended): `brew install gh`
4. **API Keys** (for testing):
   - Google Gemini: [Get free key](https://makersuite.google.com/app/apikey)
   - Groq: [Get free key](https://console.groq.com)

---

## 🚀 One-Time Setup

### Step 1: Create Hugging Face Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the details:
   - **Space name**: `doc-chatbot-multi-llm` (or your preferred name)
   - **License**: MIT
   - **SDK**: **Streamlit**
   - **Hardware**: **CPU basic** (free tier)
   - **Visibility**: Public or Private

3. Click **Create Space**

> **⚠️ Important**: HF will create template files automatically (README.md, app.py, etc.). This is normal! The GitHub Actions workflow will overwrite these with your code on the first deployment.

### Step 2: Get Hugging Face Token

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **New token**
3. Configure:
   - **Name**: `github-actions-deploy`
   - **Type**: **Write** ⚠️ (required for pushing code)
4. Copy the token (starts with `hf_...`)

### Step 3: Configure GitHub Secrets

You need to add 3 secrets to your GitHub repository:

#### Option A: Via GitHub Web Interface

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these three secrets:
   - **Name**: `HF_TOKEN` | **Value**: Your Hugging Face token from Step 2
   - **Name**: `HF_USERNAME` | **Value**: Your Hugging Face username
   - **Name**: `HF_SPACE_NAME` | **Value**: The space name (e.g., `doc-chatbot-multi-llm`)

#### Option B: Via GitHub CLI (Recommended)

```bash
# Navigate to your project directory
cd /path/to/doc-chatbot-multi-llm

# Set HF_TOKEN
gh secret set HF_TOKEN
# Paste the token when prompted

# Set HF_USERNAME
gh secret set HF_USERNAME -b "your-huggingface-username"

# Set HF_SPACE_NAME
gh secret set HF_SPACE_NAME -b "doc-chatbot-multi-llm"

# Verify secrets were created
gh secret list
```

### Step 4: Push to GitHub

If you haven't already, push your code to GitHub:

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Multi-LLM Document Chatbot"

# Add remote and push
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/doc-chatbot-multi-llm.git
git branch -M main
git push -u origin main
```

The GitHub Actions workflow will automatically trigger and deploy to Hugging Face!

### Step 5: Configure API Keys on Hugging Face

After the first deployment completes (~2-5 minutes):

1. Go to your Space: `https://huggingface.co/spaces/<YOUR_HF_USERNAME>/doc-chatbot-multi-llm`
2. Navigate to **Settings** → **Repository secrets**
3. Add your API keys:
   - **Name**: `GEMINI_API_KEY` | **Value**: Your Gemini key
   - **Name**: `GROQ_API_KEY` | **Value**: Your Groq key

4. The Space will automatically restart with the new secrets

### Step 6: Test Your Deployment

1. Open your Space URL: `https://huggingface.co/spaces/<YOUR_HF_USERNAME>/doc-chatbot-multi-llm`
2. Wait for the build to complete (~2-5 minutes on first run)
3. Test the application:
   - Configure an LLM (Gemini or Groq)
   - Upload a test document
   - Ask a question

---

## 🔄 Daily Workflow

After the initial setup, deploying updates is simple:

```bash
# 1. Make changes to your code
vim streamlit_app.py

# 2. Commit and push
git add .
git commit -m "Add new feature: XYZ"
git push

# 3. Automatic deployment! 🎉
# Check progress at: github.com/<YOUR_GITHUB_USERNAME>/doc-chatbot-multi-llm/actions
```

That's it! Every push to the `main` branch triggers an automatic deployment to Hugging Face.

---

## ⚙️ Configuration Details

### GitHub Actions Workflow

The workflow file `.github/workflows/deploy-to-huggingface.yml` contains:

```yaml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches: [main]
  workflow_dispatch:  # Manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Push to Hugging Face
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git clone https://huggingface.co/spaces/${{ secrets.HF_USERNAME }}/${{ secrets.HF_SPACE_NAME }}
          cd ${{ secrets.HF_SPACE_NAME }}
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          # Copy files and push
```

### Files Deployed to Hugging Face

The workflow deploys:
- `streamlit_app.py`
- `src/` directory (all Python modules)
- `requirements.txt`
- `README.md` (with HF YAML frontmatter)
- `.streamlit/config.toml`
- `examples/` directory

**Not deployed:**
- `.env` file (use HF Secrets instead)
- `pyproject.toml` (UV not needed on HF)
- `uv.lock`
- Development docs

### Platform Differences

The code automatically adapts:

| Feature | Local Development | Hugging Face Spaces |
|---------|-------------------|---------------------|
| **Ollama** | ✅ Available | ❌ Hidden (not available) |
| **Gemini** | ✅ Available | ✅ Available |
| **Groq** | ✅ Available | ✅ Available |
| **Environment Detection** | `SPACE_ID` = None | `SPACE_ID` = set by HF |

See `src/platform_utils.py` for implementation details.

---

## 🐛 Troubleshooting

### Issue: Deployment fails with "Invalid credentials"

**Solution:**
```bash
# Regenerate HF token with WRITE permissions
# Then update the GitHub secret:
gh secret set HF_TOKEN
```

### Issue: Space shows template files instead of my code

**Cause**: First deployment may take 2-5 minutes to complete and replace template.

**Solution:**
1. Check GitHub Actions status: `gh run list`
2. Wait for workflow to complete
3. If persists after 10 minutes, force rebuild on HF: **Settings** → **Factory reboot**

### Issue: Space not updating after push

**Solution:**
1. Check GitHub Actions completed successfully
2. View HF Space logs: Go to **Settings** → **Logs**
3. Force rebuild if needed: **Settings** → **Factory reboot**

### Issue: Ollama appears on Hugging Face (it shouldn't)

**Cause**: Platform detection not working.

**Solution:**
- Verify `src/platform_utils.py` was committed
- Check that `src/llm_manager.py` imports `platform_utils`
- HF automatically sets `SPACE_ID` environment variable

### Issue: README.md not displaying correctly on HF

**Cause**: YAML frontmatter issue.

**Solution:**
- Ensure YAML is at the very top of README.md (lines 1-11)
- Must start with `---` and include `sdk: streamlit`
- GitHub will show it as text/hide it, but HF needs it for configuration

### Monitor Deployment

**Via GitHub:**
```bash
# List recent workflow runs
gh run list

# Watch live logs
gh run watch

# View specific run
gh run view <run-id> --log
```

**Via Hugging Face:**
- Space → **Logs** tab shows build and runtime logs
- Check for Python errors or missing dependencies

---

## 🔧 Manual Deployment

To deploy without making a commit:

```bash
# Trigger workflow manually
gh workflow run deploy-to-huggingface.yml

# Or via GitHub web interface:
# Actions → Deploy to Hugging Face Spaces → Run workflow
```

---

## 🌐 Alternative Platforms

### Streamlit Community Cloud

**Pros:**
- Direct GitHub integration (no GitHub Actions needed)
- Easy setup
- Free tier

**Cons:**
- Limited to 3 apps on free tier

**How to deploy:**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub repository
3. Select `streamlit_app.py`
4. Add secrets in Streamlit dashboard

### Railway / Render

**Pros:**
- More resources than free tiers
- Support for Docker

**Cons:**
- Requires Docker configuration
- May have costs

---

## 📚 Additional Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

---

## ✅ Deployment Checklist

Before going live, ensure:

- [ ] All code is committed and pushed to GitHub
- [ ] GitHub secrets configured (HF_TOKEN, HF_USERNAME, HF_SPACE_NAME)
- [ ] HF Space created with Streamlit SDK
- [ ] API keys added to HF Space secrets (GEMINI_API_KEY, GROQ_API_KEY)
- [ ] GitHub Actions workflow completed successfully
- [ ] Space is accessible and working
- [ ] Tested with both Gemini and Groq
- [ ] Tested document upload and processing
- [ ] Dark/light theme toggle works

---

**Questions?** Open an issue on GitHub or check the [main README](../README.md).
