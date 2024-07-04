#!/bin/sh

echo "Updating the package list..."
apk update

echo "Installing required packages..."
apk add --no-cache curl tar bash

# Define Go version and download URL
GO_VERSION=1.21.1
GO_TARBALL=go${GO_VERSION}.linux-amd64.tar.gz
GO_URL=https://golang.org/dl/${GO_TARBALL}

echo "Downloading Go ${GO_VERSION}..."
curl -O ${GO_URL}

# Verify the download (optional step)
# sha256sum ${GO_TARBALL}

# Check if the download was successful
if [ $? -ne 0 ]; then
    echo "Failed to download ${GO_URL}"
    exit 1
fi

echo "Extracting ${GO_TARBALL} to /usr/local..."
tar -C /usr/local -xzf ${GO_TARBALL}

# Check if tar extraction was successful
if [ $? -ne 0 ]; then
    echo "Failed to extract ${GO_TARBALL}"
    exit 1
fi

# Get the path to the 'go' executable
GO_PATH=$(which go)

# Set up Go environment variables
echo "Setting up Go environment..."
echo "export PATH=\$(dirname ${GO_PATH}):\$PATH" >> ~/.profile
echo "export GOPATH=\$HOME/go" >> ~/.profile
echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.profile

# Source the profile to apply the changes
source ~/.profile

echo "Verifying Go installation..."
${GO_PATH} version

echo "Go ${GO_VERSION} has been successfully installed."
