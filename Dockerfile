# Use Alpine Linux as base image
FROM alpine:latest

# Update package list and install required tools
RUN apk update && \
    apk add --no-cache git curl tar bash

# Copy install-go.sh script to the container
COPY install-go.sh /root/install-go.sh

# Run the script to install Go
RUN chmod +x /root/install-go.sh && \
    ./root/install-go.sh

# Clone the repository
RUN git clone https://github.com/tulir/whatsmeow /root/whatsmeow

# Set working directory
WORKDIR /root/whatsmeow/mdtest

# Build the project using the installed Go
RUN $(which go) build

# Set entry point to run the built executable
ENTRYPOINT ["./mdtest"]
