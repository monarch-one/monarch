#!/usr/bin/env python3
"""
Development helper script for ANCAP RSS Reader
Provides easy commands for Docker development workflow
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(cmd, capture_output=False):
    """Run a shell command"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout.strip()
        else:
            result = subprocess.run(cmd, shell=True)
            return result.returncode == 0, ""
    except Exception as e:
        print(f"Error running command: {e}")
        return False, ""

def check_docker():
    """Check if Docker is available"""
    success, _ = run_command("docker --version", capture_output=True)
    if not success:
        print("❌ Docker is not installed or not in PATH")
        print("📖 See docs/DOCKER-INSTALL.md for installation instructions")
        return False
    
    success, _ = run_command("docker info", capture_output=True)
    if not success:
        print("❌ Docker is not running")
        print("🐳 Please start Docker Desktop or Docker service")
        return False
    
    return True

def docker_build():
    """Build Docker image"""
    print("🏗️  Building ANCAP RSS Reader Docker image...")
    success, _ = run_command("docker build -t ancap-rss:latest .")
    if success:
        print("✅ Build completed successfully!")
    else:
        print("❌ Build failed!")
    return success

def docker_run():
    """Run Docker container"""
    print("🚀 Starting ANCAP RSS Reader...")
    print("⚠️  Press Ctrl+C to exit")
    success, _ = run_command(
        "docker run -it --rm "
        "--name ancap-rss-dev "
        "-v ancap-rss-data:/app/data "
        "-v ancap-rss-logs:/app/logs "
        "ancap-rss:latest"
    )
    return success

def docker_dev():
    """Run development container with live reload"""
    print("🔧 Starting development mode...")
    success, _ = run_command(
        "docker run -it --rm "
        "--name ancap-rss-dev "
        f"-v {os.getcwd()}/ANCAP:/app "
        "-v ancap-rss-dev-data:/app/data "
        "-v ancap-rss-dev-logs:/app/logs "
        "ancap-rss:latest"
    )
    return success

def docker_shell():
    """Open shell in container"""
    print("🐚 Opening shell in ANCAP RSS Reader container...")
    success, _ = run_command(
        "docker run -it --rm "
        "--name ancap-rss-shell "
        "-v ancap-rss-data:/app/data "
        "-v ancap-rss-logs:/app/logs "
        "--entrypoint /bin/bash "
        "ancap-rss:latest"
    )
    return success

def docker_clean():
    """Clean Docker resources"""
    print("🧹 Cleaning Docker resources...")
    
    # Stop containers
    run_command("docker stop ancap-rss-dev ancap-rss-shell", capture_output=True)
    
    # Remove image
    run_command("docker rmi ancap-rss:latest", capture_output=True)
    
    # Remove volumes
    run_command("docker volume rm ancap-rss-data ancap-rss-logs ancap-rss-dev-data ancap-rss-dev-logs", capture_output=True)
    
    print("✅ Cleanup completed!")

def show_status():
    """Show Docker status"""
    print("📊 ANCAP RSS Reader Docker Status")
    print("=" * 40)
    
    # Check image
    success, output = run_command("docker images ancap-rss:latest --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}\\t{{.CreatedSince}}'", capture_output=True)
    if success and output:
        print("🖼️  Image:")
        print(output)
    else:
        print("🖼️  Image: Not built")
    
    print()
    
    # Check containers
    success, output = run_command("docker ps -a --filter name=ancap-rss --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'", capture_output=True)
    if success and output:
        print("📦 Containers:")
        print(output)
    else:
        print("📦 Containers: None")
    
    print()
    
    # Check volumes
    success, output = run_command("docker volume ls --filter name=ancap-rss --format 'table {{.Name}}\\t{{.Driver}}\\t{{.Scope}}'", capture_output=True)
    if success and output:
        print("💾 Volumes:")
        print(output)
    else:
        print("💾 Volumes: None")

def main():
    parser = argparse.ArgumentParser(
        description="ANCAP RSS Reader Development Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dev.py build     # Build Docker image
  python dev.py run       # Run the application
  python dev.py dev       # Development mode with live reload
  python dev.py shell     # Open shell in container
  python dev.py status    # Show Docker status
  python dev.py clean     # Clean all Docker resources
        """
    )
    
    parser.add_argument(
        'command',
        choices=['build', 'run', 'dev', 'shell', 'clean', 'status', 'check'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    print("🎯 ANCAP RSS Reader Development Helper")
    print("=" * 40)
    
    if args.command == 'check':
        if check_docker():
            print("✅ Docker is ready!")
        sys.exit(0)
    
    # Check Docker for other commands
    if not check_docker():
        sys.exit(1)
    
    # Execute command
    if args.command == 'build':
        success = docker_build()
    elif args.command == 'run':
        success = docker_run()
    elif args.command == 'dev':
        success = docker_dev()
    elif args.command == 'shell':
        success = docker_shell()
    elif args.command == 'clean':
        docker_clean()
        success = True
    elif args.command == 'status':
        show_status()
        success = True
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
