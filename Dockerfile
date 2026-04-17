FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Selenium (if using Chrome/Firefox)
# However, user mentioned they might not use Selenium, so keep it lean for now.
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]
