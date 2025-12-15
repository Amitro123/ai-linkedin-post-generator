# 🚀 AI-Powered LinkedIn Post Generator

![Architecture](./assets/architecture_diagram.png)


> A sophisticated multi-agent system that generates viral LinkedIn posts in Hebrew using CrewAI, OpenAI GPT-4, and Reflex UI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/joaomdmoura/crewAI)
[![Reflex](https://img.shields.io/badge/Reflex-0.8.16-purple.svg)](https://reflex.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Keys Setup](#api-keys-setup)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project demonstrates advanced AI agent orchestration using **CrewAI** to create a production-ready LinkedIn content generation system. The system employs 5 specialized AI agents working in sequence to research, analyze, write, validate, and optimize viral LinkedIn posts tailored to your personal writing style.

### Why This Project?

- **Multi-Agent AI System**: Showcases expertise in orchestrating multiple AI agents with distinct roles
- **Production-Ready UI**: Beautiful, responsive Reflex web interface with real-time progress tracking
- **Personalized Content**: Learns from your writing style to maintain authenticity
- **Enterprise Architecture**: Modular, scalable, and maintainable codebase
- **Full-Stack AI Application**: Combines backend AI processing with modern frontend

## ✨ Features

### 🤖 AI Agent System

- **Content Researcher**: Analyzes topics, tools, and trends using web scraping and search
- **Style Analyzer**: Learns your unique writing style from example posts
- **Viral Writer**: Generates engaging posts following your style guidelines
- **Viral Validator**: Ensures posts have emojis, hashtags, CTAs, code examples, and metrics
- **Engagement Optimizer**: Final polish for maximum engagement

### 🎨 Modern Web Interface

- **Real-time Progress Tracking**: Watch agents work with live status updates
- **Post History**: Save and manage all generated posts
- **Statistics Dashboard**: Track generation time, success rate, and productivity
- **Copy to Clipboard**: One-click post copying
- **Responsive Design**: Works on desktop and mobile

### 🔧 Technical Features

- **Caching System**: Reduces API calls and speeds up generation
- **Error Handling**: Robust fallback mechanisms
- **Async Processing**: Non-blocking UI during generation
- **Modular Architecture**: Easy to extend and customize
- **YAML Configuration**: Simple agent and task management

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Reflex Web UI                        │
│  (Real-time progress, history, stats dashboard)         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CrewAI Orchestration Layer                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│   Agents     │          │    Tasks     │
│  (5 agents)  │◄────────►│  (5 tasks)   │
└──────────────┘          └──────────────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  OpenAI API  │          │  Web Tools   │
│  (GPT-4o)    │          │  (Scraping)  │
└──────────────┘          └──────────────┘
```

### Agent Workflow

```
1. Content Researcher
   ↓ (researches topic/URL)
2. Style Analyzer
   ↓ (analyzes your writing style)
3. Viral Writer
   ↓ (writes initial post)
4. Viral Validator
   ↓ (checks emojis, hashtags, CTA, code, metrics)
5. Engagement Optimizer
   ↓ (final polish)
✅ Ready-to-post content
```

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Node.js 16+ (for Reflex frontend)
- OpenAI API key
- (Optional) Serper API key for web search

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/linkedin-post-generator.git
cd linkedin-post-generator
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Configure your writing style** (optional)
```bash
python style_trainer.py
```

6. **Run the application**
```bash
reflex run
```

7. **Open your browser**
```
http://localhost:3000
```

## 🎮 Usage

### Web Interface

1. **Enter a topic or URL** in the text area
2. **Click "צור פוסט"** (Create Post)
3. **Watch the agents work** with real-time progress updates
4. **Copy your generated post** and publish to LinkedIn!

### Command Line

```python
from agents import generate_post

# Generate a post
result = generate_post(
    content_input="AI agents and automation trends in 2025",
    use_existing_style=True
)

print(result)
```

### Training Your Writing Style

```bash
python style_trainer.py
```

Follow the prompts to input 3-5 of your best LinkedIn posts. The system will learn your:
- Tone and voice
- Sentence structure
- Emoji usage
- Call-to-action style
- Technical depth

## 📁 Project Structure

```
linkedin-post-generator/
├── linkedin_post_generator/    # Reflex web application
│   ├── __init__.py
│   └── linkedin_post_generator.py
├── config/                     # Configuration files
│   ├── agents.yaml            # Agent definitions
│   ├── tasks.yaml             # Task definitions
│   └── writing_style.json     # Your learned writing style
├── cache/                      # Cached research results
├── data/                       # Post history database
├── agents.py                   # Core agent orchestration
├── style_trainer.py           # Writing style learning tool
├── linkedin_poster.py         # LinkedIn API integration
├── requirements.txt           # Python dependencies
├── rxconfig.py               # Reflex configuration
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## ⚙️ Configuration

### Agent Configuration (`config/agents.yaml`)

```yaml
content_researcher:
  role: "חוקר תוכן מקצועי"
  goal: "לחקור ולאסוף מידע מדויק על כלים, טכנולוגיות ומגמות בתחום ה-AI"
  backstory: "אתה חוקר AI מנוסה..."

viral_writer:
  role: "כותב תוכן ויראלי"
  goal: "לכתוב פוסטים מרתקים..."
  backstory: "אתה כותב תוכן מנוסה..."
```

### Task Configuration (`config/tasks.yaml`)

```yaml
research_task:
  description: "חקור כלי, מוצר או טכנולוגיית AI..."
  expected_output: "סיכום תמציתי..."

writer_task:
  description: "כתוב פוסט לינקדאין..."
  expected_output: "פוסט מקצועי..."
```

## 🔑 API Keys Setup

### Required

1. **OpenAI API Key**
   - Sign up at [platform.openai.com](https://platform.openai.com)
   - Create an API key
   - Add to `.env`: `OPENAI_API_KEY=sk-...`

### Optional

2. **Serper API Key** (for web search)
   - Sign up at [serper.dev](https://serper.dev)
   - Get your API key
   - Add to `.env`: `SERPER_API_KEY=...`

3. **Groq API Key** (alternative LLM)
   - Sign up at [groq.com](https://groq.com)
   - Get your API key
   - Add to `.env`: `GROQ_API_KEY=...`

See [API_SETUP.md](API_SETUP.md) for detailed instructions.

## 📸 Screenshots

### Main Dashboard
![Dashboard](docs/images/dashboard.png)

### Post Generation in Progress
![Generation](docs/images/generation.png)

### Generated Post
![Result](docs/images/result.png)

## 🛠️ Technologies Used

- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Multi-agent orchestration framework
- **[OpenAI GPT-4](https://openai.com)**: Large language model
- **[Reflex](https://reflex.dev)**: Pure Python web framework
- **[LangChain](https://langchain.com)**: LLM application framework
- **[Pydantic](https://pydantic.dev)**: Data validation
- **[YAML](https://yaml.org)**: Configuration management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Dana** - AI Engineer & Full-Stack Developer

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- CrewAI team for the amazing multi-agent framework
- OpenAI for GPT-4
- Reflex team for the Python web framework
- The open-source community

## 📈 Future Enhancements

- [ ] LinkedIn direct posting integration
- [ ] Multi-language support
- [ ] A/B testing for post variations
- [ ] Analytics dashboard with engagement predictions
- [ ] Image generation for posts
- [ ] Scheduling system
- [ ] Team collaboration features
- [ ] Chrome extension

---

⭐ If you find this project useful, please consider giving it a star!

Made with ❤️ and 🤖 by Dana