#!/bin/bash
# Docker run script for ANCAP RSS Reader
# Usage: ./docker-run.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ASCII Art
echo -e "${YELLOW}"
echo "▄▀█ █▄ █ █▀▀ ▄▀█ █▀█"
echo "█▀█ █ ▀█ █▄▄ █▀█ █▀▀"
echo "» Docker Launcher «"
echo -e "${NC}"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Default command
COMMAND=${1:-run}

case $COMMAND in
    "build")
        print_info "Building ANCAP RSS Reader Docker image..."
        docker build -t ancap-rss:latest .
        print_success "Image built successfully!"
        ;;
    "run")
        print_info "Starting ANCAP RSS Reader..."
        print_warning "Press Ctrl+C to exit the application"
        echo ""
        
        # Check if image exists
        if ! docker image inspect ancap-rss:latest &> /dev/null; then
            print_info "Image not found. Building first..."
            docker build -t ancap-rss:latest .
        fi
        
        # Run the container
        docker run -it --rm \
            --name ancap-rss-instance \
            -v ancap-rss-data:/app/data \
            -v ancap-rss-logs:/app/logs \
            ancap-rss:latest
        ;;
    "dev")
        print_info "Starting ANCAP RSS Reader in development mode..."
        docker-compose --profile dev up ancap-rss-dev
        ;;
    "compose")
        print_info "Starting ANCAP RSS Reader with Docker Compose..."
        docker-compose up ancap-rss
        ;;
    "stop")
        print_info "Stopping ANCAP RSS Reader containers..."
        docker-compose down
        docker stop ancap-rss-instance 2>/dev/null || true
        print_success "Containers stopped!"
        ;;
    "clean")
        print_info "Cleaning up Docker resources..."
        docker-compose down -v
        docker rmi ancap-rss:latest 2>/dev/null || true
        docker volume rm ancap-rss-data ancap-rss-logs 2>/dev/null || true
        print_success "Cleanup completed!"
        ;;
    "logs")
        print_info "Showing application logs..."
        docker logs ancap-rss-reader 2>/dev/null || \
        docker logs ancap-rss-instance 2>/dev/null || \
        print_error "No running containers found"
        ;;
    "shell")
        print_info "Opening shell in ANCAP RSS Reader container..."
        docker run -it --rm \
            --name ancap-rss-shell \
            -v ancap-rss-data:/app/data \
            -v ancap-rss-logs:/app/logs \
            --entrypoint /bin/bash \
            ancap-rss:latest
        ;;
    "help"|"-h"|"--help")
        echo "ANCAP RSS Reader Docker Launcher"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  build    Build the Docker image"
        echo "  run      Run the application (default)"
        echo "  dev      Run in development mode with live reload"
        echo "  compose  Use Docker Compose to run"
        echo "  stop     Stop all running containers"
        echo "  clean    Remove containers, images, and volumes"
        echo "  logs     Show application logs"
        echo "  shell    Open a shell in the container"
        echo "  help     Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 run       # Start the RSS reader"
        echo "  $0 build     # Build the image"
        echo "  $0 dev       # Development mode"
        echo "  $0 clean     # Clean everything"
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        print_info "Use '$0 help' to see available commands"
        exit 1
        ;;
esac
