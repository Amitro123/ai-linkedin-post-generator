# 🚀 Complete Setup Guide

This guide will walk you through setting up the LinkedIn Post Generator from scratch.

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.11+** installed ([Download](https://www.python.org/downloads/))
- **Node.js 16+** installed ([Download](https://nodejs.org/))
- **Git** installed ([Download](https://git-scm.com/))
- An **OpenAI API key** ([Get one](https://platform.openai.com/api-keys))

## 🔧 Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-linkedin-post-generator.git
cd ai-linkedin-post-generator
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- CrewAI (multi-agent framework)
- Reflex (web framework)
- OpenAI SDK
- And all other required packages

### 4. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
# Add your OpenAI API key
```

Your `.env` should look like:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 5. Configure Your Writing Style (Optional but Recommended)

Run the style trainer to teach the AI your writing style:

```bash
python style_trainer.py
```

Follow the prompts to:
1. Paste 3-5 of your best LinkedIn posts
2. Add any specific style guidelines
3. The system will save your style to `config/writing_style.json`

### 6. Initialize Reflex

```bash
reflex init
```

This sets up the frontend components.

### 7. Run the Application

```bash
reflex run
```

The application will start:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000

### 8. Open Your Browser

Navigate to `http://localhost:3000` and start generating posts!

## 🎯 First Post Generation

1. **Enter a topic or URL** in the text area
   - Example: "AI automation trends 2025"
   - Or: "https://github.com/openai/gpt-4"

2. **Click "צור פוסט"** (Create Post)

3. **Watch the magic happen!** You'll see:
   - Content Researcher analyzing the topic
   - Style Analyzer applying your style
   - Viral Writer creating the post
   - Viral Validator checking quality
   - Engagement Optimizer polishing

4. **Copy and use!** Click the copy button and paste to LinkedIn

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'crewai'"

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "OpenAI API key not found"

**Solution:**
- Check that `.env` file exists in the project root
- Verify `OPENAI_API_KEY=sk-...` is set correctly
- Restart the application after adding the key

### Issue: "Reflex command not found"

**Solution:**
```bash
pip install reflex --upgrade
```

### Issue: Port 3000 already in use

**Solution:**
Edit `rxconfig.py` and change the port:
```python
config = rx.Config(
    app_name="linkedin_post_generator",
    port=3001,  # Change this
)
```

### Issue: Slow post generation

**Solution:**
- Check your internet connection
- Verify OpenAI API is accessible
- Consider using cached results (automatic)
- Try a different topic/URL

## 🎨 Customization

### Change Agent Behavior

Edit `config/agents.yaml` to modify:
- Agent roles
- Goals
- Backstories

### Modify Task Descriptions

Edit `config/tasks.yaml` to change:
- Task descriptions
- Expected outputs
- Task flow

### Adjust UI Theme

Edit `linkedin_post_generator/linkedin_post_generator.py`:
```python
app = rx.App(
    theme=rx.theme(
        appearance="dark",  # Change to "dark"
        accent_color="purple"  # Change color
    )
)
```

## 📊 Understanding the Workflow

```
User Input
    ↓
Content Researcher (gathers info)
    ↓
Style Analyzer (learns your style)
    ↓
Viral Writer (creates draft)
    ↓
Viral Validator (checks quality)
    ↓
Engagement Optimizer (final polish)
    ↓
Ready-to-Post Content!
```

## 🔐 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` by default
2. **Rotate API keys regularly** - Update them every 90 days
3. **Use environment variables** - Never hardcode secrets
4. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Reflex Documentation](https://reflex.dev/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

## 💡 Tips for Best Results

1. **Train with quality posts** - Use your best-performing content
2. **Be specific with topics** - Better input = better output
3. **Review and edit** - AI is a tool, add your personal touch
4. **Experiment** - Try different topics and styles
5. **Track performance** - Use the stats dashboard

## 🆘 Need Help?

- 📖 Check the [README.md](README.md)
- 🐛 [Open an issue](https://github.com/YOUR_USERNAME/ai-linkedin-post-generator/issues)
- 💬 [Start a discussion](https://github.com/YOUR_USERNAME/ai-linkedin-post-generator/discussions)

---

Happy posting! 🚀
