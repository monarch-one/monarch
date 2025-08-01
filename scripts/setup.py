#!/usr/bin/env python3
"""
ANCAP RSS Reader Setup Script
Automated installation and configuration helper
"""

import os
import sys
import subprocess
import json
import shutil
import platform
from pathlib import Path

def print_banner():
    """Print the ANCAP RSS banner"""
    print("""
▄▀█ █▄ █ █▀▀ ▄▀█ █▀█
█▀█ █ ▀█ █▄▄ █▀█ █▀▀
» A LIBERTARIAN RSS READER «

Setup Script v1.0
""")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    print("\n📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📚 Installing dependencies...")
    
    # Determine pip executable
    if platform.system() == "Windows":
        pip_cmd = os.path.join("venv", "Scripts", "pip")
    else:
        pip_cmd = os.path.join("venv", "bin", "pip")
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Try running: pip install -r requirements.txt")
        return False

def setup_configuration():
    """Set up initial configuration"""
    print("\n⚙️ Setting up configuration...")
    
    # Copy example config if custom config doesn't exist
    if not os.path.exists("custom_feeds.json"):
        if os.path.exists("custom_feeds.example.json"):
            shutil.copy("custom_feeds.example.json", "custom_feeds.json")
            print("✅ Created custom_feeds.json from example")
        else:
            # Create basic config
            basic_feeds = [
                ["BBC News", "http://feeds.bbci.co.uk/news/rss.xml"],
                ["Reuters", "https://feeds.reuters.com/reuters/topNews"],
                ["Hacker News", "https://hnrss.org/frontpage"]
            ]
            with open("custom_feeds.json", "w") as f:
                json.dump(basic_feeds, f, indent=2)
            print("✅ Created basic custom_feeds.json")
    else:
        print("✅ custom_feeds.json already exists")
    
    # Create data and logs directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    print("✅ Created data and logs directories")

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    # Determine python executable in venv
    if platform.system() == "Windows":
        python_cmd = os.path.join("venv", "Scripts", "python")
    else:
        python_cmd = os.path.join("venv", "bin", "python")
    
    try:
        # Test imports
        test_script = """
import feedparser
import bs4
import requests
import curses
print("All modules imported successfully")
"""
        result = subprocess.run([python_cmd, "-c", test_script], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All dependencies are working")
            return True
        else:
            print("❌ Dependency test failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_launcher_scripts():
    """Create convenient launcher scripts"""
    print("\n🚀 Creating launcher scripts...")
    
    if platform.system() == "Windows":
        # Windows batch file
        batch_content = f"""@echo off
cd /d "{os.getcwd()}"
venv\\Scripts\\python ancap_rss.py %*
pause
"""
        with open("run_ancap_rss.bat", "w") as f:
            f.write(batch_content)
        print("✅ Created run_ancap_rss.bat")
        
        # PowerShell script
        ps_content = f"""Set-Location "{os.getcwd()}"
& ".\\venv\\Scripts\\python" "ancap_rss.py" $args
"""
        with open("run_ancap_rss.ps1", "w") as f:
            f.write(ps_content)
        print("✅ Created run_ancap_rss.ps1")
    
    else:
        # Unix shell script
        shell_content = f"""#!/bin/bash
cd "{os.getcwd()}"
./venv/bin/python ancap_rss.py "$@"
"""
        with open("run_ancap_rss.sh", "w") as f:
            f.write(shell_content)
        os.chmod("run_ancap_rss.sh", 0o755)
        print("✅ Created run_ancap_rss.sh")

def print_next_steps():
    """Print what to do next"""
    print("""
🎉 Installation completed successfully!

Next steps:
1. 📝 Edit custom_feeds.json to add your favorite RSS feeds
2. 🚀 Run the application:""")
    
    if platform.system() == "Windows":
        print("""   • Double-click run_ancap_rss.bat, or
   • Run: .\\venv\\Scripts\\python ancap_rss.py""")
    else:
        print("""   • Run: ./run_ancap_rss.sh, or
   • Run: ./venv/bin/python ancap_rss.py""")
    
    print("""
📚 Documentation:
   • README.md - Overview and features
   • docs/CONFIGURATION.md - Detailed configuration
   • docs/TROUBLESHOOTING.md - Common issues

🆘 Need help?
   • GitHub Issues: https://github.com/monarch-one/monarch/issues
   • Documentation: https://github.com/monarch-one/monarch/wiki

Happy reading! 📰
""")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Virtual Environment", create_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Configuration", setup_configuration),
        ("Testing", test_installation),
        ("Launcher Scripts", create_launcher_scripts)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please check the error messages above and try again.")
            sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main()
