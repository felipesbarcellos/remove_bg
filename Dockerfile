# Use Python official image with minimal footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies (only essential ones)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Create directories for images
RUN mkdir -p imagens/entrada imagens/saida imagens/originais

# Set permissions
RUN chmod -R 755 imagens

# Fix line endings in the startup script
RUN sed -i 's/\r$//' startup.sh && chmod +x startup.sh

# Use non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the startup script
CMD ["/bin/bash", "/app/startup.sh"]
