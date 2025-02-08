#!/bin/zsh

# Define the directory where your docker-compose.yml is located
COMPOSE_DIR=$(dirname "$0")

# Navigate to the directory
cd $COMPOSE_DIR || {
  echo "Failed to navigate to directory: $COMPOSE_DIR"
  exit 1
}

# Start the test environment
echo "Starting test environment..."
docker-compose --profile test up -d

# Define the name of the virtual environment
VENV_NAME="miniscan_env"

# Set up a local Python environment if needed
if [ ! -d "$VENV_NAME" ]; then
  echo "Creating virtual environment..."
  python3 -m venv $VENV_NAME
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install test dependencies
pip install -r test-requirements.txt

# Run the tests
echo "Running tests..."
pytest test/

# Deactivate the virtual environment
deactivate

# Stop the test environment
echo "Stopping test environment..."
docker-compose --profile test down
