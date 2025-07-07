FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates fonts-liberation \
    xvfb libgtk-3-0 libdbus-glib-1-2 libnss3 libxss1 libasound2 \
    chromium chromium-driver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create test working dir
WORKDIR /tests
COPY . .

# Default CMD for local runs
CMD ["pytest", "--html=report.html"]
