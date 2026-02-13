# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/user/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 user
USER user

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user . /app

# Expose port (7860 for Hugging Face)
EXPOSE 7860

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]
