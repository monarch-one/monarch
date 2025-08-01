# 🐳 Docker Installation Guide

This guide will help you install Docker to run ANCAP RSS Reader in a containerized environment.

## 🚀 Why Use Docker?

- ✅ **No Python setup required** - Everything is included
- ✅ **Consistent environment** - Works the same everywhere
- ✅ **Easy installation** - One command to run
- ✅ **Isolated** - Doesn't affect your system
- ✅ **Portable** - Share and deploy easily

## 📥 Installing Docker

### Windows

1. **Download Docker Desktop:**
   - Go to: https://docker.com/products/docker-desktop
   - Download "Docker Desktop for Windows"
   - Requires Windows 10/11 with WSL2

2. **Install:**
   - Run the installer
   - Follow the setup wizard
   - Restart your computer when prompted

3. **Verify installation:**
   ```cmd
   docker --version
   docker run hello-world
   ```

### macOS

1. **Download Docker Desktop:**
   - Go to: https://docker.com/products/docker-desktop
   - Download "Docker Desktop for Mac"
   - Choose Intel or Apple Silicon version

2. **Install:**
   - Open the `.dmg` file
   - Drag Docker to Applications
   - Start Docker from Applications

3. **Verify installation:**
   ```bash
   docker --version
   docker run hello-world
   ```

### Linux (Ubuntu/Debian)

1. **Update packages:**
   ```bash
   sudo apt update
   sudo apt install ca-certificates curl gnupg lsb-release
   ```

2. **Add Docker's official GPG key:**
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

3. **Add repository:**
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

4. **Install Docker:**
   ```bash
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

5. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

6. **Verify installation:**
   ```bash
   docker --version
   docker run hello-world
   ```

### Linux (CentOS/RHEL/Fedora)

1. **Install Docker:**
   ```bash
   # CentOS/RHEL
   sudo yum install -y docker
   
   # Fedora
   sudo dnf install -y docker
   ```

2. **Start Docker service:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

## 🔧 Post-Installation Setup

### Configure Docker Desktop (Windows/macOS)

1. **Open Docker Desktop**
2. **Go to Settings:**
   - **Resources** → Adjust CPU/Memory if needed
   - **General** → Enable "Use Docker Compose V2"

### Test Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose
docker-compose --version

# Test with hello-world
docker run hello-world

# Test system info
docker system info
```

## 🚀 Running ANCAP RSS Reader

Once Docker is installed:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/monarch-one/monarch.git
   cd monarch
   ```

2. **Run with our scripts:**
   ```bash
   # Windows
   docker-run.bat
   
   # Linux/macOS (make executable first)
   chmod +x docker-run.sh
   ./docker-run.sh
   
   # PowerShell (cross-platform)
   .\docker-run.ps1
   ```

3. **Or run manually:**
   ```bash
   docker build -t ancap-rss .
   docker run -it --rm ancap-rss
   ```

## 🔍 Troubleshooting

### Common Issues

#### "Docker is not running" Error

**Windows/macOS:**
- Start Docker Desktop from Start Menu/Applications
- Wait for Docker to fully start (whale icon in system tray)

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl status docker
```

#### Permission Denied (Linux)

```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo (not recommended)
sudo docker run hello-world
```

#### WSL2 Issues (Windows)

1. **Enable WSL2:**
   ```cmd
   wsl --install
   ```

2. **Update WSL2:**
   ```cmd
   wsl --update
   ```

3. **Set WSL2 as default:**
   ```cmd
   wsl --set-default-version 2
   ```

#### Docker Desktop Won't Start

1. **Reset Docker Desktop:**
   - Windows: Docker Desktop → Troubleshoot → Reset to factory defaults
   - macOS: Docker Desktop → Preferences → Reset → Factory defaults

2. **Check system requirements:**
   - Windows: WSL2, Hyper-V enabled
   - macOS: macOS 10.15 or later
   - Linux: 64-bit kernel 3.10+

### Getting Help

1. **Docker Documentation:** https://docs.docker.com/
2. **Docker Desktop Issues:** https://docs.docker.com/desktop/troubleshoot/
3. **Community Support:** https://forums.docker.com/

## 💡 Alternative: No Docker Installation

If you can't install Docker, you can still run ANCAP RSS Reader natively:

1. **Install Python 3.7+**
2. **Follow the native installation guide** in the main README
3. **Use the ANCAP folder** for the application files

## 🎯 Next Steps

After Docker is installed:

1. ✅ **Test Docker:** `docker run hello-world`
2. ✅ **Clone repository:** `git clone https://github.com/monarch-one/monarch.git`
3. ✅ **Run ANCAP RSS Reader:** `./docker-run.sh` or `docker-run.bat`

---

**Happy containerizing! 🐳**
