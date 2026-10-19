# Multi-stage lightweight production container
FROM python:3.11-slim

# Install system dependencies: FFmpeg, fonts, and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-dejavu-core \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy repository source code
COPY . .

# Run automated integrity verification
RUN python -m pipeline.verify_claims

# Expose publishing dashboard port
EXPOSE 8000

# Default command: launch local publishing dashboard
CMD ["python", "run_pipeline.py", "--serve", "--port", "8000"]
