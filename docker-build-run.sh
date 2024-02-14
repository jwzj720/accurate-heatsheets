#!/bin/bash

# Step 1: Build the Docker Image
docker build -t vuejs-app .

# Step 2: Run the Docker Container
docker run -it -p 8080:8080 vuejs-app

ls