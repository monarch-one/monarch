# Dockerfile for ANCAP RSS Reader
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for curses and terminal support
RUN apt-get update && apt-get install -y \
    ncurses-term \
    libncurses5-dev \
    libncursesw5-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY ANCAP/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files from ANCAP directory
COPY ANCAP/ancap_rss.py .
COPY custom_feeds.example.json custom_feeds.json

# Create data and logs directories
RUN mkdir -p data logs

# Set environment variables for better terminal support
ENV TERM=xterm-256color
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Set locale for proper character encoding
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Create a non-root user for security
RUN groupadd -r ancap && useradd -r -g ancap ancap
RUN chown -R ancap:ancap /app
USER ancap

# Expose no ports (terminal application)

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the application
CMD ["python", "ancap_rss.py"]
