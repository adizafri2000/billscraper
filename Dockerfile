# Use the latest Alpine image as the base
FROM alpine:latest

# Install necessary dependencies
RUN apk update && apk add --no-cache \
    git \
    curl \
    tar \
    bash

# Install Go
ENV GO_VERSION=1.21.1
RUN curl -LO https://dl.google.com/go/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz && \
    rm go$GO_VERSION.linux-amd64.tar.gz

# Set Go environment variables
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/go"
ENV PATH="${GOPATH}/bin:${PATH}"

# Clone the whatsmeow repository
RUN git clone https://github.com/tulir/whatsmeow /go/src/whatsmeow

# Set the working directory to mdtest
WORKDIR /go/src/whatsmeow/mdtest

# Build the project
RUN /usr/local/go/bin/go build

# Run the built binary on container run
CMD ["./mdtest"]
