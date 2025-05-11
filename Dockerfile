# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to ensure output is sent straight to terminal (stdout)
ENV PYTHONUNBUFFERED=1

# Install PostgreSQL development package and other dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc netcat && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Specify the entrypoint to execute the start.sh script
ENTRYPOINT ["bash", "/app/entrypoint.sh"]

