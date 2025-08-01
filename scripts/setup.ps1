# PowerShell Setup Script for ANCAP RSS Reader
# Run with: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1

Write-Host @"
▄▀█ █▄ █ █▀▀ ▄▀█ █▀█
█▀█ █ ▀█ █▄▄ █▀█ █▀▀
» A LIBERTARIAN RSS READER «

PowerShell Setup Script v1.0
"@ -ForegroundColor Yellow

# Check if Python is installed
Write-Host "`n🐍 Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $pythonVersion found" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python not found. Please install Python 3.7+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Cyan
try {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "`n📚 Installing dependencies..." -ForegroundColor Cyan
try {
    & ".\venv\Scripts\pip" install -r requirements.txt
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Try running manually: .\venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to continue anyway"
}

# Setup configuration
Write-Host "`n⚙️ Setting up configuration..." -ForegroundColor Cyan
if (-not (Test-Path "custom_feeds.json")) {
    if (Test-Path "custom_feeds.example.json") {
        Copy-Item "custom_feeds.example.json" "custom_feeds.json"
        Write-Host "✅ Created custom_feeds.json from example" -ForegroundColor Green
    } else {
        $basicFeeds = @'
[
  ["BBC News", "http://feeds.bbci.co.uk/news/rss.xml"],
  ["Reuters", "https://feeds.reuters.com/reuters/topNews"],
  ["Hacker News", "https://hnrss.org/frontpage"],
  ["Mises Institute", "https://mises.org/feeds/rss"]
]
'@
        $basicFeeds | Out-File -FilePath "custom_feeds.json" -Encoding UTF8
        Write-Host "✅ Created basic custom_feeds.json" -ForegroundColor Green
    }
} else {
    Write-Host "✅ custom_feeds.json already exists" -ForegroundColor Green
}

# Create directories
New-Item -ItemType Directory -Force -Path "data" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Write-Host "✅ Created data and logs directories" -ForegroundColor Green

# Test installation
Write-Host "`n🧪 Testing installation..." -ForegroundColor Cyan
try {
    $testResult = & ".\venv\Scripts\python" -c "import feedparser, bs4, requests, curses; print('All modules imported successfully')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ All dependencies are working" -ForegroundColor Green
    } else {
        Write-Host "❌ Dependency test failed: $testResult" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Test failed: $_" -ForegroundColor Red
}

# Create launcher scripts
Write-Host "`n🚀 Creating launcher scripts..." -ForegroundColor Cyan

# Batch file
$batchContent = @"
@echo off
cd /d "$PWD"
venv\Scripts\python ancap_rss.py %*
pause
"@
$batchContent | Out-File -FilePath "run_ancap_rss.bat" -Encoding ASCII
Write-Host "✅ Created run_ancap_rss.bat" -ForegroundColor Green

# PowerShell script
$psContent = @"
Set-Location "$PWD"
& ".\venv\Scripts\python" "ancap_rss.py" `$args
"@
$psContent | Out-File -FilePath "run_ancap_rss.ps1" -Encoding UTF8
Write-Host "✅ Created run_ancap_rss.ps1" -ForegroundColor Green

# Success message
Write-Host @"

🎉 Installation completed successfully!

Next steps:
1. 📝 Edit custom_feeds.json to add your favorite RSS feeds
2. 🚀 Run the application:
   • Double-click run_ancap_rss.bat, or
   • Run: .\venv\Scripts\python ancap_rss.py

📚 Documentation:
   • README.md - Overview and features
   • docs\CONFIGURATION.md - Detailed configuration
   • docs\TROUBLESHOOTING.md - Common issues

🆘 Need help?
   • GitHub: https://github.com/monarch-one/monarch

Happy reading! 📰
"@ -ForegroundColor Green

Read-Host "`nPress Enter to exit"
