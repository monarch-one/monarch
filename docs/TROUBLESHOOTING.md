# Troubleshooting Guide

## Common Issues and Solutions

### Application Won't Start

#### Issue: "Python not found" error
**Solution:**
```bash
# Windows - try these alternatives:
py ancap_rss.py
python3 ancap_rss.py

# Verify Python installation:
python --version
```

#### Issue: "Module not found" errors
**Solution:**
```bash
# Install missing dependencies:
pip install -r requirements.txt

# Or install individually:
pip install feedparser beautifulsoup4 requests lxml
```

#### Issue: Permission denied errors
**Solution:**
```bash
# Ensure proper permissions:
chmod +x ancap_rss.py

# Or run with explicit Python:
python ancap_rss.py
```

### Display and Interface Issues

#### Issue: ASCII art not displaying correctly
**Symptoms:** Boxes, question marks, or garbled characters
**Solution:**
1. Ensure terminal supports UTF-8:
   ```bash
   # Check current locale:
   locale
   
   # Set UTF-8 (Linux/macOS):
   export LANG=en_US.UTF-8
   export LC_ALL=en_US.UTF-8
   ```

2. Try different terminal emulators:
   - **Windows**: Windows Terminal, ConEmu
   - **macOS**: iTerm2, Terminal.app
   - **Linux**: GNOME Terminal, Konsole, Alacritty

#### Issue: Terminal too small warning
**Solution:**
- Minimum size: 80x24 characters
- Recommended: 120x30 or larger
- Adjust terminal window size or font size

#### Issue: Colors not displaying
**Solution:**
```bash
# Check color support:
echo $TERM

# Common working values:
export TERM=xterm-256color
export TERM=screen-256color
```

#### Issue: Mouse not working
**Solution:**
1. Enable mouse support in terminal settings
2. Try different terminal emulator
3. Use keyboard shortcuts instead
4. Check if tmux/screen is interfering

### Network and Feed Issues

#### Issue: No feeds loading / "No feeds loaded" error
**Solutions:**
1. **Check internet connection**
2. **Verify feed URLs:**
   ```bash
   # Test individual feed:
   curl -I "https://feeds.reuters.com/reuters/topNews"
   ```
3. **Check custom_feeds.json syntax:**
   ```bash
   # Validate JSON:
   python -m json.tool custom_feeds.json
   ```

#### Issue: Some feeds fail to load
**Check logs:**
```bash
tail -f logs/ancap_rss.log
```

**Common causes:**
- **SSL certificate issues**: Use HTTP instead of HTTPS if available
- **Rate limiting**: Some sites limit requests per minute
- **Invalid feed format**: Ensure URL points to actual RSS/Atom feed
- **Firewall blocking**: Check corporate/personal firewall settings

#### Issue: Slow feed loading
**Solutions:**
1. **Reduce concurrent workers** (edit ancap_rss.py):
   ```python
   max_workers = min(5, len(feed_list))  # Reduce from 10 to 5
   ```
2. **Remove slow/problematic feeds**
3. **Check network speed**

### Data and Configuration Issues

#### Issue: Read articles not saving
**Solutions:**
1. **Check file permissions:**
   ```bash
   ls -la data/
   chmod 644 data/read_articles.json
   ```
2. **Verify data directory exists:**
   ```bash
   mkdir -p data/
   ```

#### Issue: Favorites not persisting
**Solutions:**
1. **Check favorites file:**
   ```bash
   cat data/favorites.json
   ```
2. **Reset favorites data:**
   ```bash
   rm data/favorites.json
   # Restart application to recreate
   ```

#### Issue: Configuration not loading
**Solutions:**
1. **Verify JSON syntax:**
   ```bash
   python -c "import json; print(json.load(open('custom_feeds.json')))"
   ```
2. **Reset to defaults:**
   ```bash
   cp custom_feeds.example.json custom_feeds.json
   ```

### Performance Issues

#### Issue: High memory usage
**Solutions:**
1. **Reduce number of feeds**
2. **Clear old data:**
   ```bash
   rm data/read_articles.json data/favorites.json
   ```
3. **Restart application periodically**

#### Issue: Application freezing
**Solutions:**
1. **Check for problematic feeds** in logs
2. **Reduce timeout values** (edit ancap_rss.py):
   ```python
   response = session.get(url, timeout=3)  # Reduce from 5 to 3
   ```
3. **Kill and restart:**
   ```bash
   # Kill if frozen:
   Ctrl+C
   
   # Or force kill:
   pkill -f ancap_rss.py
   ```

### Platform-Specific Issues

#### Windows Issues

**Issue: PowerShell execution policy**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue: Windows Terminal not showing colors**
- Update to latest Windows Terminal version
- Enable "Use acrylic material" in settings

#### macOS Issues

**Issue: Python not found after macOS update**
```bash
# Reinstall Python via Homebrew:
brew install python
```

**Issue: Certificate errors**
```bash
# Update certificates:
/Applications/Python\ 3.x/Install\ Certificates.command
```

#### Linux Issues

**Issue: Missing curses library**
```bash
# Ubuntu/Debian:
sudo apt install python3-dev

# Fedora:
sudo dnf install python3-devel ncurses-devel

# Arch:
sudo pacman -S python ncurses
```

## Debug Mode

Enable debug logging for detailed troubleshooting:

```python
# Edit ancap_rss.py, change logging level:
logging.basicConfig(level=logging.DEBUG, ...)
```

View debug output:
```bash
tail -f logs/ancap_rss.log
```

## Getting Help

### Self-Diagnosis Checklist

Before seeking help, try these steps:

1. ✅ **Check Python version**: `python --version` (needs 3.7+)
2. ✅ **Verify dependencies**: `pip list | grep -E "feedparser|beautifulsoup4|requests"`
3. ✅ **Test internet**: `ping google.com`
4. ✅ **Check terminal size**: Should be at least 80x24
5. ✅ **Validate feeds config**: `python -m json.tool custom_feeds.json`
6. ✅ **Review logs**: `cat logs/ancap_rss.log | tail -20`

### Log Collection

When reporting issues, include:

```bash
# System information:
python --version
pip list
echo $TERM
uname -a  # Linux/macOS
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"  # Windows

# Application logs:
tail -50 logs/ancap_rss.log

# Configuration:
cat custom_feeds.json
```

### Community Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/monarch-one/monarch/issues)
- 💬 **General Help**: [GitHub Discussions](https://github.com/monarch-one/monarch/discussions)
- 📚 **Documentation**: [Project Wiki](https://github.com/monarch-one/monarch/wiki)

### Quick Fixes

**Reset everything to defaults:**
```bash
# Backup first:
cp -r data/ data-backup/

# Reset:
rm -rf data/ logs/
rm custom_feeds.json
cp custom_feeds.example.json custom_feeds.json

# Restart application
python ancap_rss.py
```

**Emergency mode (minimal feeds):**
```json
[
  ["BBC News", "http://feeds.bbci.co.uk/news/rss.xml"],
  ["Reuters", "https://feeds.reuters.com/reuters/topNews"]
]
```

## Still Having Issues?

If none of these solutions work:

1. **Create a minimal test case**
2. **Gather system information** (as shown above)
3. **Open a GitHub issue** with detailed description
4. **Include error messages and logs**

Remember: The community is here to help! Don't hesitate to ask questions.
