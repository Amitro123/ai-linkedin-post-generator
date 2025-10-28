# Contributing to LinkedIn Post Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-linkedin-post-generator.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add: your feature description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## 💻 Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
reflex run
```

## 🧪 Testing

Before submitting a PR, ensure:
- [ ] Code follows Python PEP 8 style guidelines
- [ ] All existing tests pass
- [ ] New features include appropriate tests
- [ ] Documentation is updated

## 📋 Code Style

- Use Black for code formatting: `black .`
- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Keep functions focused and modular

## 🐛 Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## ✨ Feature Requests

Feature requests are welcome! Please:
- Check if the feature already exists
- Describe the use case
- Explain why it would be valuable
- Consider implementation complexity

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for updates to existing features
- `Refactor:` for code refactoring
- `Docs:` for documentation changes

Example: `Add: viral validator agent for post quality checks`

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 📞 Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing! 🎉
