# Use the official Python 3.13 image from the Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY src/mini_scan /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the test requirements file into the container
COPY test-requirements.txt .

# Install the test dependencies
RUN pip install --no-cache-dir -r test-requirements.txt

# Default command for running the application
CMD ["python", "main.py"]
