#!/bin/sh

# Update the package list
apk update

# Install required packages
apk add --no-cache curl tar bash

# Define Go version and download URL
GO_VERSION=1.21.1
GO_TARBALL=go${GO_VERSION}.linux-amd64.tar.gz
GO_URL=https://golang.org/dl/${GO_TARBALL}

# Download the latest Go version
curl -O ${GO_URL}

# Verify the download (optional step)
# sha256sum ${GO_TARBALL}

# Extract the tarball to /usr/local
tar -C /usr/local -xzf ${GO_TARBALL}

# Get the path to the 'go' executable
GO_PATH=$(which go)

# Set up Go environment variables
echo "export PATH=\$(dirname ${GO_PATH}):\$PATH" >> ~/.profile
echo "export GOPATH=\$HOME/go" >> ~/.profile
echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.profile

# Source the profile to apply the changes
source ~/.profile

# Verify the installation
${GO_PATH} version
