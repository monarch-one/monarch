# Changelog

All notable changes to ANCAP RSS Reader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-01

### Added
- 🎉 **Initial Release**: Complete RSS reader with ANCAP branding
- 📰 **Multi-feed RSS aggregation**: Support for unlimited RSS/Atom feeds
- ⭐ **Favorites system**: Save and organize important articles
- 📖 **Read/Unread tracking**: Persistent article state management
- 🎨 **ASCII art branding**: Distinctive ANCAP visual identity throughout
- ⌨️ **Comprehensive keyboard shortcuts**: Efficient navigation and control
- 🖱️ **Full mouse support**: Click to read, scroll with mouse wheel
- 🔍 **Smart content parsing**: Clean HTML content display with BeautifulSoup
- 💾 **Persistent data storage**: User preferences and read articles saved
- 🌐 **Browser integration**: Open articles in default browser
- 🚀 **Professional project structure**: Organized codebase with documentation
- 📚 **Complete documentation**: Installation, configuration, and troubleshooting guides
- 🛠️ **Setup automation**: Automated installation scripts for all platforms
- 🐳 **Docker support**: Containerized deployment option
- 🔄 **Real-time updates**: Automatic feed refreshing with progress indicators
- 📊 **Live statistics**: Real-time article counts and feed status
- 🎯 **Toggle functionality**: Bulk mark all articles as read/unread
- 🌈 **Color-coded interface**: Visual distinction between read/unread/favorite articles

### Technical Features
- **Python 3.7+ compatibility**: Modern Python with full backward compatibility
- **Curses TUI**: Terminal-based user interface with full feature support
- **Concurrent feed loading**: Multi-threaded RSS feed fetching for performance
- **Error handling**: Robust error handling and logging system
- **Cross-platform**: Windows, macOS, and Linux support
- **Unicode support**: Full UTF-8 character support for international content
- **Responsive design**: Adaptive layout for different terminal sizes
- **Memory efficient**: Optimized for low resource usage

### Keyboard Shortcuts
- `j/k` or `↓/↑`: Navigate articles
- `Space`: Read selected article
- `o`: Open article in browser
- `f`: Toggle favorites mode
- `l/s`: Toggle favorite status
- `u`: Mark article as unread
- `m`: Toggle all articles read/unread
- `PgUp/PgDn`: Scroll by page
- `q/Esc`: Quit application

### Project Structure
```
monarch/
├── ancap_rss.py              # Main application
├── requirements.txt          # Python dependencies
├── custom_feeds.json         # RSS feed configuration
├── data/                     # User data directory
├── logs/                     # Application logs
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
└── LICENSE                   # MIT License
```

### Documentation
- **README.md**: Complete project overview and quick start guide
- **docs/INSTALLATION.md**: Detailed installation instructions for all platforms
- **docs/CONFIGURATION.md**: Advanced configuration and customization guide
- **docs/TROUBLESHOOTING.md**: Common issues and comprehensive solutions

### Automation & DevOps
- **scripts/setup.py**: Cross-platform automated setup script
- **scripts/backup_data.py**: Data backup and restore utility
- **Dockerfile**: Container deployment support
- **GitHub Actions**: Automated CI/CD pipeline
- **Platform launchers**: Convenient startup scripts for Windows/Unix

### Default RSS Feeds
Curated selection of libertarian and general news sources:
- BBC News, Reuters, Hacker News
- Mises Institute, Foundation for Economic Education
- Reason Magazine, Cato Institute
- Zero Hedge, The Austrian
- And more quality sources

### 🎨 Visual Identity
- **Prominent ANCAP ASCII logo**: Distinctive branding across all screens
- **Yellow color scheme**: ANCAP-themed color palette
- **Professional layout**: Clean, organized interface design
- **Right-aligned status elements**: Consistent visual hierarchy
- **Readable typography**: Optimized for terminal display

## [Unreleased]

### Planned Features
- 🔍 **Search functionality**: Full-text search across articles
- 🏷️ **Tagging system**: Custom article organization
- 📱 **Mobile support**: Terminal-based mobile interface
- 🌍 **Internationalization**: Multi-language support
- 📊 **Analytics**: Reading statistics and trends
- 🔄 **Auto-refresh**: Configurable automatic feed updates
- 💬 **Comments integration**: Support for article comments
- 📧 **Email integration**: Send articles via email
- 🎨 **Theme system**: Customizable color themes
- 🔌 **Plugin system**: Extensible architecture

---

**Legend:**
- 🎉 Major feature
- 📰 Content/Feed related
- ⭐ User experience
- 🎨 Visual/UI
- 🛠️ Technical/Dev
- 📚 Documentation
- 🐛 Bug fix
- 🔧 Maintenance
