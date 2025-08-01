# ANCAP RSS Reader

[![Docker Build](https://github.com/monarch-one/monarch/actions/workflows/docker.yml/badge.svg)](https://github.com/monarch-one/monarch/actions/workflows/docker.yml)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue?logo=docker)](https://ghcr.io/monarch-one/monarch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy: 100%](https://img.shields.io/badge/Privacy-100%25-green)](https://github.com/monarch-one/monarch#-100-privacy-guaranteed)

A powerful, terminal-based RSS reader with a distinctive ANCAP (Anarcho-Capitalist) theme, built in Python using curses for a smooth TUI experience.

```
▄▀█ █▄ █ █▀▀ ▄▀█ █▀█
█▀█ █ ▀█ █▄▄ █▀█ █▀▀
» A LIBERTARIAN RSS READER «
```

## 🔒 **100% Privacy Guaranteed**

**ANCAP RSS Reader is completely private and respects your digital sovereignty:**

- 🚫 **No data collection** - Zero telemetry, analytics, or tracking
- 🏠 **Runs entirely locally** - All data stays on your machine
- 🔐 **No external connections** - Only fetches RSS feeds you configure
- 🚀 **No cloud dependencies** - Works offline with cached content
- 🛡️ **No user profiling** - Your reading habits remain private
- 💾 **Local storage only** - All preferences saved to your local files
- 🌐 **Open source** - Complete transparency, inspect every line of code

*Built by libertarians, for libertarians - your privacy is non-negotiable.*

## ✨ Features

- **📰 Multi-feed RSS aggregation** - Load from unlimited RSS/Atom feeds
- **🎯 Real-time updates** - Automatic feed refreshing with progress indicators
- **⭐ Favorites system** - Save and organize your most important articles
- **📖 Read/Unread tracking** - Persistent article state management
- **🎨 Beautiful ASCII art branding** - Distinctive ANCAP visual identity
- **⌨️ Powerful keyboard shortcuts** - Efficient navigation and control
- **🖱️ Mouse support** - Click to read, scroll with mouse wheel
- **🔍 Smart content parsing** - Clean HTML content display
- **💾 Persistent data** - Your preferences and read articles are saved
- **🌐 Browser integration** - Open articles in your default browser

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- **OR** Docker (for containerized deployment)

### Installation

#### Option 1: Docker (Recommended) 🐳

**Pre-built Images (No Build Required):**
```bash
# Run directly from GitHub Container Registry
docker run -it --rm ghcr.io/monarch-one/monarch:latest

# With data persistence
docker run -it --rm \
  -v ancap-rss-data:/app/data \
  -v ancap-rss-logs:/app/logs \
  ghcr.io/monarch-one/monarch:latest
```

**Quick Start (Build from Source):**
```bash
# Clone and run with Docker
git clone https://github.com/monarch-one/monarch.git
cd monarch

# Windows
docker-run.bat

# Linux/macOS
./docker-run.sh

# PowerShell (Cross-platform)
.\docker-run.ps1
```

**Manual Docker:**
```bash
# Build and run
docker build -t ancap-rss .
docker run -it --rm ancap-rss

# Or use Docker Compose
docker-compose up ancap-rss
```

**Available Docker Tags:**
- `latest` - Latest stable release
- `main` - Latest main branch build
- `v1.0.0` - Specific version tags

[📖 **Full Docker Guide**](docs/DOCKER.md) | [🐳 **Docker Installation**](docs/DOCKER-INSTALL.md)

#### Option 2: Python Native

1. **Clone the repository:**
   ```bash
   git clone https://github.com/monarch-one/monarch.git
   cd monarch/ANCAP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your RSS feeds:**
   ```bash
   cp ../custom_feeds.example.json custom_feeds.json
   # Edit custom_feeds.json with your preferred feeds
   ```

4. **Run the application:**
   ```bash
   python ancap_rss.py
   
   # Or use the provided scripts:
   # Windows: run_ancap_rss.bat or run_ancap_rss.ps1
   # Linux/Mac: ./run_ancap_rss.sh
   ```

## ⚙️ Configuration

### Adding RSS Feeds

Edit the `custom_feeds.json` file to add your preferred RSS feeds:

```json
[
  ["BBC News", "http://feeds.bbci.co.uk/news/rss.xml"],
  ["Reuters", "https://feeds.reuters.com/reuters/topNews"],
  ["Hacker News", "https://hnrss.org/frontpage"],
  ["Mises Institute", "https://mises.org/feeds/rss"]
]
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `j` / `↓` | Navigate down |
| `k` / `↑` | Navigate up |
| `Space` | Read selected article |
| `o` | Open article in browser |
| `f` | Toggle favorites mode |
| `l` / `s` | Toggle favorite (save/unsave) |
| `u` | Mark article as unread |
| `m` | Toggle all articles read/unread |
| `PgUp` / `PgDn` | Scroll by page |
| `q` / `Esc` | Quit application |

### Mouse Controls

- **Click** on any article to read it
- **Mouse wheel** to scroll through articles
- **Click and drag** for smooth navigation

## 📁 Project Structure

```
monarch/
├── ancap_rss.py              # Main application
├── requirements.txt          # Python dependencies
├── custom_feeds.json         # Your RSS feed configuration
├── custom_feeds.example.json # Example feed configuration
├── data/                     # User data directory
│   ├── favorites.json        # Saved favorite articles
│   └── read_articles.json    # Read article tracking
├── logs/                     # Application logs
│   └── ancap_rss.log        # Debug and error logs
├── docs/                     # Documentation
│   ├── INSTALLATION.md      # Detailed installation guide
│   ├── CONFIGURATION.md     # Advanced configuration
│   └── TROUBLESHOOTING.md   # Common issues and solutions
├── scripts/                  # Utility scripts
│   ├── setup.py            # Installation helper
│   └── backup_data.py       # Data backup utility
└── LICENSE                   # MIT License
```

## 🛠️ Development

### Setting up Development Environment

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Issue: Terminal too small**
- Minimum recommended terminal size: 80x24
- For best experience: 120x30 or larger

**Issue: Unicode characters not displaying**
- Ensure your terminal supports UTF-8
- Try a different terminal emulator if issues persist

**Issue: Mouse not working**
- Ensure your terminal supports mouse events
- Try using keyboard shortcuts instead

**Issue: Feeds not loading**
- Check internet connection
- Verify feed URLs in `custom_feeds.json`
- Check logs in `logs/ancap_rss.log`

### Debug Mode

Run with debug logging:
```bash
python ancap_rss.py --debug
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Built with [feedparser](https://pypi.org/project/feedparser/) for RSS parsing
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) for HTML content cleaning
- [curses](https://docs.python.org/3/library/curses.html) for the terminal interface
- Inspired by the principles of individual liberty and free markets

## 📧 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/monarch-one/monarch/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/monarch-one/monarch/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/monarch-one/monarch/wiki)

---

**Made with ❤️ by the liberty-loving community**

> "The curious task of economics is to demonstrate to men how little they really know about what they imagine they can design." - F.A. Hayek
