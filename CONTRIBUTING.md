# Contributing to ANCAP RSS Reader

Thank you for your interest in contributing to ANCAP RSS Reader! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Operating system and version
   - Python version
   - Terminal emulator used
   - Steps to reproduce
   - Expected vs actual behavior
   - Log files (`logs/ancap_rss.log`)

### Suggesting Features

1. **Check the roadmap** in [CHANGELOG.md](CHANGELOG.md)
2. **Open a discussion** for major features first
3. **Use the feature request template**
4. **Describe the use case** and benefits

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/monarch.git
   cd monarch
   ```
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

#### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes**
3. **Test your changes**:
   ```bash
   # Run the application
   python ancap_rss.py
   
   # Check code style
   black ancap_rss.py
   flake8 ancap_rss.py
   ```
4. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add search functionality"
   ```
5. **Push and create a Pull Request**

#### Code Style Guidelines

- **Follow PEP 8** for Python code style
- **Use meaningful variable names**
- **Add comments** for complex logic
- **Keep functions focused** and reasonably sized
- **Use type hints** where appropriate
- **Maintain the ASCII art branding** in new interfaces

#### Commit Message Format

Use conventional commits format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
- `feat: add article search functionality`
- `fix: resolve feed loading timeout issue`
- `docs: update installation instructions`

## 🧪 Testing

### Manual Testing

1. **Test basic functionality**:
   - Feed loading and display
   - Article reading and navigation
   - Favorites management
   - Keyboard shortcuts

2. **Test edge cases**:
   - Empty feed list
   - Network connectivity issues
   - Invalid RSS feeds
   - Terminal resizing

3. **Cross-platform testing**:
   - Windows (cmd, PowerShell, Windows Terminal)
   - macOS (Terminal, iTerm2)
   - Linux (various terminal emulators)

### Automated Testing

```bash
# Run code quality checks
black --check ancap_rss.py
flake8 ancap_rss.py
mypy ancap_rss.py

# Test imports
python -c "import feedparser, bs4, requests, curses"

# Validate configuration
python -c "import json; json.load(open('custom_feeds.example.json'))"
```

## 📋 Project Structure

Understanding the codebase:

```
ancap_rss.py
├── Global Configuration      # BASE_DIR, DATA_DIR, file paths
├── Data Management          # Load/save functions for feeds, articles, favorites
├── Background Feed Loading  # Concurrent RSS feed fetching
├── Display Functions        # safe_addstr, draw_entry, format_html_content
├── Main Interfaces         # draw_feed, read_article, favorites_mode
└── Main Application        # main() function, event loop
```

### Key Functions

- **`fetch_entries_background()`**: Concurrent RSS feed loading
- **`draw_feed()`**: Main article list interface
- **`read_article()`**: Article reading interface
- **`favorites_mode()`**: Favorites management interface
- **`safe_addstr()`**: Safe terminal text rendering

## 🎨 Design Principles

### ANCAP Branding

- **Maintain the ASCII logo** across all interfaces
- **Use yellow/gold colors** for primary elements
- **Keep the libertarian theme** in messaging and examples
- **Preserve the professional appearance**

### User Experience

- **Keyboard-first navigation** with mouse support
- **Consistent interface patterns** across screens
- **Clear visual hierarchy** with proper spacing
- **Responsive design** for different terminal sizes

### Code Quality

- **Readable and maintainable** code structure
- **Robust error handling** with helpful messages
- **Efficient performance** for large feed lists
- **Cross-platform compatibility**

## 🌟 Areas for Contribution

### High Priority

1. **Search functionality** - Full-text article search
2. **Performance optimization** - Faster feed loading
3. **Mobile support** - Better small screen experience
4. **Configuration UI** - In-app feed management

### Medium Priority

1. **Plugin system** - Extensible architecture
2. **Themes** - Customizable color schemes
3. **Export features** - OPML, PDF export
4. **Analytics** - Reading statistics

### Documentation

1. **Video tutorials** - Setup and usage guides
2. **API documentation** - For future plugin system
3. **Localization** - Multi-language support
4. **Wiki articles** - Advanced use cases

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** to all contributors
- **Welcome newcomers** and help them get started
- **Focus on the code**, not personal attacks
- **Assume good intentions** in discussions
- **Follow libertarian principles** of voluntary cooperation

### Communication

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Pull Request reviews** - Constructive feedback only
- **Wiki** - Collaborative documentation

## 🏷️ Labels and Milestones

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Documentation updates
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority-high` - Critical issues
- `platform-specific` - OS-specific issues

### Pull Request Labels

- `ready for review` - Ready for maintainer review
- `work in progress` - Not ready for merge
- `needs testing` - Requires additional testing
- `breaking change` - Changes that break compatibility

## 📞 Getting Help

### For Contributors

- **Development questions**: Open a GitHub Discussion
- **Stuck on an issue**: Comment on the issue for help
- **Want to collaborate**: Reach out on relevant issues

### For Users

- **Usage questions**: Check documentation first, then GitHub Discussions
- **Bug reports**: Use GitHub Issues with detailed information
- **Feature requests**: Start with GitHub Discussions

## 🎉 Recognition

Contributors will be:
- **Listed in README.md** acknowledgments
- **Mentioned in release notes** for significant contributions
- **Invited as collaborators** for ongoing contributors

---

**Thank you for contributing to ANCAP RSS Reader!** 

Your contributions help build better tools for the liberty-loving community. Every bug report, feature suggestion, and code contribution makes the project stronger.

*"The curious task of economics is to demonstrate to men how little they really know about what they imagine they can design."* - F.A. Hayek
