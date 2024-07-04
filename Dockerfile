# Use Alpine Linux as base image
FROM alpine:latest

# Update package list and install required tools
RUN apk update && \
    apk add --no-cache git curl tar bash

# Define Go version and download URL
ENV GO_VERSION=1.21.1
ENV GO_TARBALL=go${GO_VERSION}.linux-amd64.tar.gz
ENV GO_URL=https://golang.org/dl/${GO_TARBALL}

# Install Go using the script directly in Dockerfile
RUN echo "Updating the package list..." && \
    apk update && \
    echo "Installing required packages..." && \
    apk add --no-cache curl tar bash && \
    echo "Downloading Go ${GO_VERSION}..." && \
    curl -O ${GO_URL} && \
    echo "Extracting ${GO_TARBALL} to /usr/local..." && \
    tar -C /usr/local -xzf ${GO_TARBALL} && \
    echo "Setting up Go environment..." && \
    echo "export PATH=\$(dirname \$(which go)):\$PATH" >> ~/.profile && \
    echo "export GOPATH=\$HOME/go" >> ~/.profile && \
    echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.profile && \
    source ~/.profile && \
    echo "Verifying Go installation..." && \
    go version && \
    echo "Cleaning up..." && \
    rm ${GO_TARBALL} && \
    echo "Go ${GO_VERSION} has been successfully installed."

# Clone the repository
RUN git clone https://github.com/tulir/whatsmeow /root/whatsmeow

# Set working directory
WORKDIR /root/whatsmeow/mdtest

# Build the project using the installed Go
RUN $(which go) build

# Set entry point to run the built executable
ENTRYPOINT ["./mdtest"]
