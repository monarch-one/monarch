@echo off
REM Docker run script for ANCAP RSS Reader (Windows)
REM Usage: docker-run.bat [command]

setlocal EnableDelayedExpansion

REM ASCII Art
echo.
echo ▄▀█ █▄ █ █▀▀ ▄▀█ █▀█
echo █▀█ █ ▀█ █▄▄ █▀█ █▀▀
echo » Docker Launcher «
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Default command
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=run

if "%COMMAND%"=="build" (
    echo [INFO] Building ANCAP RSS Reader Docker image...
    docker build -t ancap-rss:latest .
    if errorlevel 1 (
        echo [ERROR] Build failed!
        pause
        exit /b 1
    )
    echo [SUCCESS] Image built successfully!
    pause
    goto :EOF
)

if "%COMMAND%"=="run" (
    echo [INFO] Starting ANCAP RSS Reader...
    echo [WARNING] Press Ctrl+C to exit the application
    echo.
    
    REM Check if image exists
    docker image inspect ancap-rss:latest >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Image not found. Building first...
        docker build -t ancap-rss:latest .
        if errorlevel 1 (
            echo [ERROR] Build failed!
            pause
            exit /b 1
        )
    )
    
    REM Run the container
    docker run -it --rm --name ancap-rss-instance -v ancap-rss-data:/app/data -v ancap-rss-logs:/app/logs ancap-rss:latest
    goto :EOF
)

if "%COMMAND%"=="dev" (
    echo [INFO] Starting ANCAP RSS Reader in development mode...
    docker-compose --profile dev up ancap-rss-dev
    goto :EOF
)

if "%COMMAND%"=="compose" (
    echo [INFO] Starting ANCAP RSS Reader with Docker Compose...
    docker-compose up ancap-rss
    goto :EOF
)

if "%COMMAND%"=="stop" (
    echo [INFO] Stopping ANCAP RSS Reader containers...
    docker-compose down >nul 2>&1
    docker stop ancap-rss-instance >nul 2>&1
    echo [SUCCESS] Containers stopped!
    pause
    goto :EOF
)

if "%COMMAND%"=="clean" (
    echo [INFO] Cleaning up Docker resources...
    docker-compose down -v >nul 2>&1
    docker rmi ancap-rss:latest >nul 2>&1
    docker volume rm ancap-rss-data ancap-rss-logs >nul 2>&1
    echo [SUCCESS] Cleanup completed!
    pause
    goto :EOF
)

if "%COMMAND%"=="logs" (
    echo [INFO] Showing application logs...
    docker logs ancap-rss-reader 2>nul || docker logs ancap-rss-instance 2>nul || echo [ERROR] No running containers found
    pause
    goto :EOF
)

if "%COMMAND%"=="shell" (
    echo [INFO] Opening shell in ANCAP RSS Reader container...
    docker run -it --rm --name ancap-rss-shell -v ancap-rss-data:/app/data -v ancap-rss-logs:/app/logs --entrypoint /bin/bash ancap-rss:latest
    goto :EOF
)

if "%COMMAND%"=="help" goto :help
if "%COMMAND%"=="-h" goto :help
if "%COMMAND%"=="--help" goto :help

echo [ERROR] Unknown command: %COMMAND%
echo [INFO] Use '%~nx0 help' to see available commands
pause
exit /b 1

:help
echo ANCAP RSS Reader Docker Launcher
echo.
echo Usage: %~nx0 [command]
echo.
echo Commands:
echo   build    Build the Docker image
echo   run      Run the application (default)
echo   dev      Run in development mode with live reload
echo   compose  Use Docker Compose to run
echo   stop     Stop all running containers
echo   clean    Remove containers, images, and volumes
echo   logs     Show application logs
echo   shell    Open a shell in the container
echo   help     Show this help message
echo.
echo Examples:
echo   %~nx0 run       # Start the RSS reader
echo   %~nx0 build     # Build the image
echo   %~nx0 dev       # Development mode
echo   %~nx0 clean     # Clean everything
echo.
pause
