#!/bin/zsh

# Define the directory where your docker-compose.yml is located
COMPOSE_DIR=$(dirname "$0")

# Navigate to the directory
cd $COMPOSE_DIR || {
  echo "Failed to navigate to directory: $COMPOSE_DIR"
  exit 1
}

# Run Docker Compose
docker-compose up --build
