# Configuration Guide

## RSS Feed Configuration

### Basic Setup

The main configuration file is `custom_feeds.json` in the root directory. This file contains an array of RSS feed definitions.

**Format:**
```json
[
  ["Display Name", "RSS URL"],
  ["Another Feed", "https://example.com/feed.xml"]
]
```

### Example Configuration

```json
[
  ["BBC News", "http://feeds.bbci.co.uk/news/rss.xml"],
  ["Reuters World", "https://feeds.reuters.com/reuters/worldNews"],
  ["Hacker News", "https://hnrss.org/frontpage"],
  ["TechCrunch", "https://techcrunch.com/feed/"],
  ["Mises Institute", "https://mises.org/feeds/rss"]
]
```

### Popular RSS Feeds

#### News & General
- **BBC News**: `http://feeds.bbci.co.uk/news/rss.xml`
- **Reuters World**: `https://feeds.reuters.com/reuters/worldNews`
- **AP News**: `https://feeds.ap.org/ApNews/apf-topnews`
- **NPR**: `https://feeds.npr.org/1001/feed.json`

#### Technology
- **Hacker News**: `https://hnrss.org/frontpage`
- **TechCrunch**: `https://techcrunch.com/feed/`
- **Ars Technica**: `https://feeds.arstechnica.com/arstechnica/index`
- **The Verge**: `https://www.theverge.com/rss/index.xml`

#### Libertarian/Economic
- **Mises Institute**: `https://mises.org/feeds/rss`
- **Foundation for Economic Education**: `https://fee.org/feeds/rss`
- **Reason Magazine**: `https://reason.com/latest/feed/`
- **Cato Institute**: `https://www.cato.org/rss/libertarianism`
- **Zero Hedge**: `https://feeds.feedburner.com/zerohedge/feed`

## Application Settings

### Data Storage

User data is stored in the `data/` directory:

- **`data/read_articles.json`** - Tracks which articles you've read
- **`data/favorites.json`** - Stores your favorite articles

### Logging

Application logs are stored in `logs/ancap_rss.log`. You can adjust logging level by editing the script:

```python
# In ancap_rss.py, change logging level:
logging.basicConfig(level=logging.INFO)  # INFO, DEBUG, WARNING, ERROR
```

### Performance Tuning

#### Feed Loading
```python
# Adjust concurrent feed loading (default: 10)
max_workers = min(20, len(feed_list))  # Increase for faster loading
```

#### Refresh Rate
```python
# Adjust auto-refresh timeout (default: 30 seconds)
stdscr.timeout(60000)  # 60 seconds
```

## Advanced Configuration

### Custom Keyboard Shortcuts

You can modify keyboard shortcuts by editing the key handling sections in `ancap_rss.py`:

```python
# Example: Change 'f' to 'b' for favorites
elif key == ord('b'):  # Changed from 'f'
    favorites_mode(stdscr)
```

### Color Themes

Modify the color scheme in the `main()` function:

```python
# Custom color pairs
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green theme
curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan text
curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta accent
```

### ASCII Art Customization

To change the ANCAP logo, modify these lines in all display functions:

```python
ancap_line1 = "Your Custom ASCII Line 1"
ancap_line2 = "Your Custom ASCII Line 2"
subtitle = "» YOUR CUSTOM SUBTITLE «"
```

## Feed Validation

### Testing Your Feeds

Use the built-in feed tester:
```bash
python ancap_rss.py --test-feeds
```

### Common Feed Issues

1. **Invalid URL**: Ensure the URL is accessible and returns XML/JSON
2. **SSL Certificates**: Some feeds may have certificate issues
3. **Rate Limiting**: Some sites limit request frequency
4. **Redirects**: Ensure final URL points to actual feed

### Feed Format Support

Supported formats:
- **RSS 2.0** - Most common format
- **Atom 1.0** - Modern XML format
- **RSS 1.0/RDF** - RDF-based format
- **JSON Feed** - JSON-based format (limited support)

## Backup and Restore

### Backup Your Data
```bash
# Create backup
cp -r data/ backup-$(date +%Y%m%d)/
```

### Restore Data
```bash
# Restore from backup
cp -r backup-20231201/ data/
```

### Export Favorites
```python
# Custom script to export favorites as OPML
python scripts/export_favorites.py --format opml
```

## Environment Variables

Set these environment variables for additional configuration:

```bash
# Custom data directory
export ANCAP_RSS_DATA_DIR="/path/to/custom/data"

# Custom feed file
export ANCAP_RSS_FEEDS="/path/to/custom/feeds.json"

# Debug mode
export ANCAP_RSS_DEBUG=1
```

## Integration with Other Tools

### Shell Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias rss="cd /path/to/monarch && python ancap_rss.py"
alias rss-backup="cp -r /path/to/monarch/data/ ~/rss-backup-$(date +%Y%m%d)/"
```

### Systemd Service (Linux)
```ini
# /etc/systemd/user/ancap-rss.service
[Unit]
Description=ANCAP RSS Reader
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/monarch/ancap_rss.py
Restart=always

[Install]
WantedBy=default.target
```

## Troubleshooting Configuration

### Common Configuration Errors

1. **JSON Syntax Error**: Validate your `custom_feeds.json` with a JSON validator
2. **File Permissions**: Ensure the application can write to `data/` directory
3. **Network Issues**: Check firewall settings for RSS feed access

### Reset Configuration
```bash
# Reset to default configuration
rm custom_feeds.json
cp custom_feeds.example.json custom_feeds.json

# Clear all data
rm -rf data/
mkdir data/
```

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or visit our [GitHub Issues](https://github.com/monarch-one/monarch/issues).
