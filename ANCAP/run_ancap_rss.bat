@echo off
cd /d "%~dp0"
venv\Scripts\python ancap_rss.py %*
pause
