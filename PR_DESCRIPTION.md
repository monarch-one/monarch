# 🏗️ Reorganize Project: Move ANCAP RSS Reader to dedicated ANCAP/ subfolder

## 📁 Project Reorganization

This PR reorganizes the project structure by moving the ANCAP RSS Reader application to a dedicated `ANCAP/` subfolder for better organization and distribution.

### 🔄 Changes Made:
- ✅ **Moved main application files** to `ANCAP/` directory
- ✅ **Created proper project structure** with `data/` and `logs/` subfolders
- ✅ **Updated README.md** installation instructions for new structure
- ✅ **Added ANCAP-specific README.md** with quick start guide
- ✅ **Maintained all functionality** and file relationships
- ✅ **Enhanced project organization** for easier distribution and development

### 📂 New Structure:
```
ANCAP/
├── ancap_rss.py          # Main application
├── custom_feeds.json     # RSS feed configuration
├── requirements.txt      # Python dependencies
├── run_ancap_rss.*      # Platform-specific run scripts
├── README.md            # ANCAP-specific documentation
├── data/                # Application data
│   ├── favorites.json   # Saved favorite articles
│   └── read_articles.json # Read article tracking
└── logs/                # Application logs
    └── ancap_rss.log   # Debug and error logs
```

### 🧪 Testing:
- ✅ Application runs correctly from new location
- ✅ All data files are properly organized
- ✅ Scripts execute without issues
- ✅ Documentation is updated and accurate

### 🎯 Benefits:
- **Better organization** - Clear separation of application files
- **Easier distribution** - Self-contained ANCAP folder
- **Improved development** - Cleaner project structure
- **Enhanced documentation** - Dedicated README for quick start

This reorganization maintains full compatibility while providing a cleaner, more professional project structure.

---

**Ready for review and merge!** 🚀
