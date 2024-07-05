# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables to avoid user prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    golang-go \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    build-essential

# Clone the repository and build the Go project from master branch
RUN git clone -b master --single-branch https://github.com/adizafri2000/whatsmeow-adjusted && \
    cd whatsmeow-adjusted/mdtest && \
    go build -o go_app

# Set the working directory
WORKDIR /app

# Copy the FastAPI application files
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

# Create a directory for the Go binary and copy it
RUN mkdir -p /app/mdtest && \
    cp /whatsmeow-adjusted/mdtest/go_app /app/mdtest/

# Create a virtual environment and install Python dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Start the FastAPI application with Uvicorn
CMD ["/app/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
