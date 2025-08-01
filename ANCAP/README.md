# ANCAP RSS Reader

A powerful, terminal-based RSS reader with a distinctive ANCAP (Anarcho-Capitalist) theme.

```
▄▀█ █▄ █ █▀▀ ▄▀█ █▀█
█▀█ █ ▀█ █▄▄ █▀█ █▀▀
» A LIBERTARIAN RSS READER «
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your RSS feeds:**
   ```bash
   # Copy the example file from the parent directory
   cp ../custom_feeds.example.json custom_feeds.json
   # Edit custom_feeds.json with your preferred feeds
   ```

3. **Run the application:**
   ```bash
   python ancap_rss.py
   
   # Or use the provided scripts:
   # Windows: run_ancap_rss.bat or run_ancap_rss.ps1
   # Linux/Mac: ./run_ancap_rss.sh
   ```

## 📁 Project Structure

```
ANCAP/
├── ancap_rss.py          # Main application
├── custom_feeds.json     # Your RSS feed configuration
├── requirements.txt      # Python dependencies
├── run_ancap_rss.*      # Platform-specific run scripts
├── data/                # Application data
│   ├── favorites.json   # Saved favorite articles
│   └── read_articles.json # Read article tracking
└── logs/                # Application logs
    └── ancap_rss.log   # Debug and error logs
```

## 🔒 Privacy

This application is 100% private:
- ✅ No data collection or telemetry
- ✅ Runs entirely locally on your machine
- ✅ Only connects to RSS feeds you configure
- ✅ All data stored locally in JSON files

## ⚙️ Configuration

Edit `custom_feeds.json` to add your RSS feeds:

```json
[
  ["Feed Name", "https://example.com/rss.xml"],
  ["Another Feed", "https://another-site.com/feed.xml"]
]
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `j` / `↓` | Navigate down |
| `k` / `↑` | Navigate up |
| `Space` | Read selected article |
| `o` | Open article in browser |
| `f` | Toggle favorites mode |
| `l` / `s` | Toggle favorite |
| `u` | Mark as unread |
| `m` | Toggle all read/unread |
| `q` / `Esc` | Quit |

---

**Made with ❤️ by the liberty-loving community**
