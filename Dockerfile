# Dockerfile for ANCAP RSS Reader
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ncurses-term \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ancap_rss.py .
COPY custom_feeds.example.json custom_feeds.json

# Create data and logs directories
RUN mkdir -p data logs

# Set environment variables
ENV TERM=xterm-256color
ENV PYTHONUNBUFFERED=1

# Expose no ports (terminal application)

# Run the application
CMD ["python", "ancap_rss.py"]
