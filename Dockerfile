# FloatChat Dockerfile for Render
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements-production.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 10000

# Command for Render deployment with Streamlit
CMD ["python", "app_streamlit_render.py"]