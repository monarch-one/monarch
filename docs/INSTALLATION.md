# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **Terminal**: Any modern terminal emulator with Unicode support
- **Memory**: 50MB RAM minimum
- **Storage**: 10MB free disk space

### Recommended Requirements
- **Terminal Size**: 120x30 characters or larger
- **Python**: Version 3.9+ for best performance
- **Internet**: Stable connection for RSS feed updates

## Installation Methods

### Method 1: Standard Installation

1. **Download the repository:**
   ```bash
   git clone https://github.com/monarch-one/monarch.git
   cd monarch
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration:**
   ```bash
   cp custom_feeds.example.json custom_feeds.json
   ```

5. **Run the application:**
   ```bash
   python ancap_rss.py
   ```

### Method 2: One-Click Setup (Windows)

1. **Download and run the setup script:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
   ```

### Method 3: Docker Installation

1. **Build and run with Docker:**
   ```bash
   docker build -t ancap-rss .
   docker run -it ancap-rss
   ```

## Platform-Specific Instructions

### Windows

**Prerequisites:**
- Install Python from [python.org](https://python.org) or Microsoft Store
- Ensure pip is included (usually automatic)

**Terminal Recommendations:**
- Windows Terminal (recommended)
- PowerShell 7+
- WSL2 with your preferred Linux distribution

**Troubleshooting:**
- If you get "python not found", try `py` instead of `python`
- Enable UTF-8 support in your terminal settings

### macOS

**Prerequisites:**
- Python 3 (install via Homebrew recommended):
  ```bash
  brew install python
  ```

**Terminal Recommendations:**
- iTerm2 (recommended)
- Default Terminal.app works fine

### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora/CentOS:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

## Verification

After installation, verify everything works:

```bash
python ancap_rss.py --version
python ancap_rss.py --test-feeds
```

## Uninstallation

To completely remove ANCAP RSS Reader:

1. **Deactivate virtual environment (if used):**
   ```bash
   deactivate
   ```

2. **Remove the project directory:**
   ```bash
   rm -rf monarch/  # Linux/macOS
   rmdir /s monarch  # Windows
   ```

3. **Remove any global configurations (optional):**
   - Windows: `%APPDATA%\ancap-rss\`
   - macOS: `~/Library/Application Support/ancap-rss/`
   - Linux: `~/.config/ancap-rss/`

## Next Steps

- [Configuration Guide](CONFIGURATION.md) - Customize your RSS feeds
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Repository](https://github.com/monarch-one/monarch) - Latest updates and community
