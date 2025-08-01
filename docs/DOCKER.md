# 🐳 Docker Guide for ANCAP RSS Reader

This guide explains how to run ANCAP RSS Reader using Docker for easy installation and deployment.

## 🚀 Quick Start

### Option 1: One-Click Run (Recommended)

**Windows:**
```cmd
docker-run.bat
```

**Linux/macOS:**
```bash
./docker-run.sh
```

**PowerShell (Cross-platform):**
```powershell
.\docker-run.ps1
```

### Option 2: Manual Docker Commands

```bash
# Build the image
docker build -t ancap-rss:latest .

# Run the application
docker run -it --rm \
  --name ancap-rss \
  -v ancap-rss-data:/app/data \
  -v ancap-rss-logs:/app/logs \
  ancap-rss:latest
```

### Option 3: Docker Compose

```bash
# Production mode
docker-compose up ancap-rss

# Development mode (with live reload)
docker-compose --profile dev up ancap-rss-dev
```

## 📋 Prerequisites

1. **Docker Desktop** (Windows/macOS) or **Docker Engine** (Linux)
   - Download from: https://docker.com/get-started
   - Ensure Docker is running before executing commands

2. **Git** (optional, for cloning the repository)

## 🛠️ Installation Methods

### Method 1: Using Docker Scripts (Easiest)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/monarch-one/monarch.git
   cd monarch
   ```

2. **Run the application:**
   ```bash
   # Linux/macOS
   chmod +x docker-run.sh
   ./docker-run.sh

   # Windows
   docker-run.bat

   # PowerShell
   .\docker-run.ps1
   ```

### Method 2: Direct Docker Commands

1. **Build and run:**
   ```bash
   docker build -t ancap-rss .
   docker run -it --rm ancap-rss
   ```

### Method 3: Docker Compose

1. **Start the application:**
   ```bash
   docker-compose up ancap-rss
   ```

## 📁 Data Persistence

Docker volumes are used to persist your data:

- **`ancap-rss-data`** - Stores favorites and read articles
- **`ancap-rss-logs`** - Application logs and debug information

Your data will persist even when containers are removed!

## 🔧 Configuration

### Custom RSS Feeds

1. **Edit feeds before building:**
   ```bash
   cp custom_feeds.example.json custom_feeds.json
   # Edit custom_feeds.json with your preferred feeds
   docker build -t ancap-rss .
   ```

2. **Mount custom feeds at runtime:**
   ```bash
   docker run -it --rm \
     -v $(pwd)/custom_feeds.json:/app/custom_feeds.json \
     ancap-rss
   ```

## 🎮 Available Commands

### Docker Run Scripts

| Command | Description |
|---------|-------------|
| `run` | Start the RSS reader (default) |
| `build` | Build the Docker image |
| `dev` | Development mode with live reload |
| `compose` | Use Docker Compose |
| `stop` | Stop all running containers |
| `clean` | Remove containers, images, and volumes |
| `logs` | Show application logs |
| `shell` | Open shell in container |
| `help` | Show help message |

### Examples

```bash
# Start the application
./docker-run.sh run

# Build the image
./docker-run.sh build

# Development mode
./docker-run.sh dev

# View logs
./docker-run.sh logs

# Clean everything
./docker-run.sh clean

# Get help
./docker-run.sh help
```

## 🔍 Troubleshooting

### Common Issues

1. **Docker not running:**
   ```
   Error: Docker is not running
   ```
   **Solution:** Start Docker Desktop or Docker service

2. **Permission denied (Linux):**
   ```bash
   chmod +x docker-run.sh
   ```

3. **Image build fails:**
   ```bash
   # Clean Docker cache
   docker system prune -f
   ./docker-run.sh build
   ```

4. **Container won't start:**
   ```bash
   # Check logs
   ./docker-run.sh logs
   
   # Clean and rebuild
   ./docker-run.sh clean
   ./docker-run.sh build
   ```

### Reset Everything

```bash
# Complete reset (removes all data)
./docker-run.sh clean

# Rebuild and start fresh
./docker-run.sh build
./docker-run.sh run
```

## 🏗️ Development

### Development Mode

```bash
# Start with live reload
./docker-run.sh dev

# Or with Docker Compose
docker-compose --profile dev up ancap-rss-dev
```

### Debugging

```bash
# Open shell in container
./docker-run.sh shell

# View real-time logs
docker logs -f ancap-rss-reader
```

## 🌐 Network and Security

- **No exposed ports** - Terminal application only
- **Non-root user** - Runs as `ancap` user for security
- **Network isolation** - Only RSS feed connections
- **Volume security** - Data stored in Docker volumes

## 📊 Resource Usage

- **Image size:** ~150MB (Python slim + dependencies)
- **Memory usage:** ~50-100MB during operation
- **CPU usage:** Minimal (RSS parsing only)
- **Storage:** Volumes for data persistence

## 🚀 Advanced Usage

### Custom Environment Variables

```bash
docker run -it --rm \
  -e TERM=xterm-256color \
  -e PYTHONUNBUFFERED=1 \
  ancap-rss
```

### Volume Mounting

```bash
# Mount local data directory
docker run -it --rm \
  -v $(pwd)/my-data:/app/data \
  ancap-rss
```

### Multi-platform Support

```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 -t ancap-rss .
```

## 📝 License

This Docker configuration is part of the ANCAP RSS Reader project and follows the same MIT License.

---

**Made with 🐳 Docker for the liberty-loving community**
