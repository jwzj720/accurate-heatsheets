#!/bin/bash

# Build the Docker image
docker build -t vuejs-app .

# Run the Docker container with volume mapping
docker run -v $(pwd):/app -p 8080:8080 -it --rm --name vuejs-app vuejs-app