# Use the latest Alpine image as the base
FROM alpine:latest

# Install necessary dependencies
RUN apk update && apk add --no-cache \
    git \
    curl \
    tar \
    bash \
    gcc \
    musl-dev \
    libc-dev \
    make \
    go

# Set Go environment variables
ENV GOPATH="/go"
ENV PATH="${GOPATH}/bin:/usr/local/go/bin:${PATH}"
ENV CGO_ENABLED=1  # Enable CGO

# Clone the whatsmeow repository
RUN git clone https://github.com/tulir/whatsmeow /go/src/whatsmeow

# Set the working directory to mdtest
WORKDIR /go/src/whatsmeow/mdtest

# Build the project
RUN go build -o mdtest

# Run the built binary on container run
CMD ["./mdtest"]
