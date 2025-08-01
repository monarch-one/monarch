#!/usr/bin/env pwsh
# Docker run script for ANCAP RSS Reader (PowerShell)
# Usage: .\docker-run.ps1 [command]

param(
    [Parameter(Position=0)]
    [string]$Command = "run"
)

# Colors for output
$RED = "`e[31m"
$GREEN = "`e[32m"
$YELLOW = "`e[33m"
$BLUE = "`e[34m"
$NC = "`e[0m"

# ASCII Art
Write-Host ""
Write-Host "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█" -ForegroundColor Yellow
Write-Host "█▀█ █ ▀█ █▄▄ █▀█ █▀▀" -ForegroundColor Yellow
Write-Host "» Docker Launcher «" -ForegroundColor White
Write-Host ""

function Write-Info {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if Docker is installed
try {
    $null = Get-Command docker -ErrorAction Stop
}
catch {
    Write-Error "Docker is not installed. Please install Docker Desktop first."
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Docker is running
try {
    $null = docker info 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
}
catch {
    Write-Error "Docker is not running. Please start Docker Desktop first."
    Read-Host "Press Enter to exit"
    exit 1
}

switch ($Command.ToLower()) {
    "build" {
        Write-Info "Building ANCAP RSS Reader Docker image..."
        docker build -t ancap-rss:latest .
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Image built successfully!"
        } else {
            Write-Error "Build failed!"
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    "run" {
        Write-Info "Starting ANCAP RSS Reader..."
        Write-Warning "Press Ctrl+C to exit the application"
        Write-Host ""
        
        # Check if image exists
        $imageExists = docker image inspect ancap-rss:latest 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Info "Image not found. Building first..."
            docker build -t ancap-rss:latest .
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Build failed!"
                Read-Host "Press Enter to exit"
                exit 1
            }
        }
        
        # Run the container
        docker run -it --rm `
            --name ancap-rss-instance `
            -v ancap-rss-data:/app/data `
            -v ancap-rss-logs:/app/logs `
            ancap-rss:latest
    }
    
    "dev" {
        Write-Info "Starting ANCAP RSS Reader in development mode..."
        docker-compose --profile dev up ancap-rss-dev
    }
    
    "compose" {
        Write-Info "Starting ANCAP RSS Reader with Docker Compose..."
        docker-compose up ancap-rss
    }
    
    "stop" {
        Write-Info "Stopping ANCAP RSS Reader containers..."
        docker-compose down 2>$null
        docker stop ancap-rss-instance 2>$null
        Write-Success "Containers stopped!"
    }
    
    "clean" {
        Write-Info "Cleaning up Docker resources..."
        docker-compose down -v 2>$null
        docker rmi ancap-rss:latest 2>$null
        docker volume rm ancap-rss-data, ancap-rss-logs 2>$null
        Write-Success "Cleanup completed!"
    }
    
    "logs" {
        Write-Info "Showing application logs..."
        $logShown = $false
        try {
            docker logs ancap-rss-reader 2>$null
            $logShown = $true
        } catch {}
        
        if (-not $logShown) {
            try {
                docker logs ancap-rss-instance 2>$null
                $logShown = $true
            } catch {}
        }
        
        if (-not $logShown) {
            Write-Error "No running containers found"
        }
    }
    
    "shell" {
        Write-Info "Opening shell in ANCAP RSS Reader container..."
        docker run -it --rm `
            --name ancap-rss-shell `
            -v ancap-rss-data:/app/data `
            -v ancap-rss-logs:/app/logs `
            --entrypoint /bin/bash `
            ancap-rss:latest
    }
    
    { $_ -in @("help", "-h", "--help") } {
        Write-Host "ANCAP RSS Reader Docker Launcher" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Usage: .\docker-run.ps1 [command]" -ForegroundColor White
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  build    Build the Docker image"
        Write-Host "  run      Run the application (default)"
        Write-Host "  dev      Run in development mode with live reload"
        Write-Host "  compose  Use Docker Compose to run"
        Write-Host "  stop     Stop all running containers"
        Write-Host "  clean    Remove containers, images, and volumes"
        Write-Host "  logs     Show application logs"
        Write-Host "  shell    Open a shell in the container"
        Write-Host "  help     Show this help message"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Green
        Write-Host "  .\docker-run.ps1 run       # Start the RSS reader"
        Write-Host "  .\docker-run.ps1 build     # Build the image"
        Write-Host "  .\docker-run.ps1 dev       # Development mode"
        Write-Host "  .\docker-run.ps1 clean     # Clean everything"
    }
    
    default {
        Write-Error "Unknown command: $Command"
        Write-Info "Use '.\docker-run.ps1 help' to see available commands"
        exit 1
    }
}

if ($Command -in @("build", "stop", "clean")) {
    Read-Host "Press Enter to exit"
}
