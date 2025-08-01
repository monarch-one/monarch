#!/bin/bash
# ANCAP RSS Reader Launcher Script for Unix/Linux/macOS

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    python3 scripts/setup.py
fi

# Activate virtual environment and run the application
if [ -f "venv/bin/python" ]; then
    ./venv/bin/python ancap_rss.py "$@"
else
    echo "Error: Virtual environment not properly configured"
    echo "Please run: python3 scripts/setup.py"
    exit 1
fi
